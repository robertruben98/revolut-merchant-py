"""Exercise the async resource methods and context managers for sync/async parity."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from revolut import (
    AsyncRevolutMerchantClient,
    RevolutMerchantClient,
)
from revolut.exceptions import APIConnectionError

BASE = "https://sandbox-merchant.revolut.com"


# --- context managers -------------------------------------------------------
@respx.mock
def test_sync_context_manager_closes():
    respx.get(f"{BASE}/api/orders/o").mock(return_value=httpx.Response(200, json={"id": "o"}))
    with RevolutMerchantClient(secret_key="sk", environment="sandbox") as client:
        assert client.orders.retrieve("o").id == "o"


@respx.mock
async def test_async_context_manager_closes():
    respx.get(f"{BASE}/api/orders/o").mock(return_value=httpx.Response(200, json={"id": "o"}))
    async with AsyncRevolutMerchantClient(secret_key="sk", environment="sandbox") as client:
        order = await client.orders.retrieve("o")
        assert order.id == "o"


# --- async customers --------------------------------------------------------
@respx.mock
async def test_async_customers_crud(async_client):
    respx.post(f"{BASE}/api/customers").mock(return_value=httpx.Response(201, json={"id": "c1"}))
    respx.get(f"{BASE}/api/customers/c1").mock(
        return_value=httpx.Response(200, json={"id": "c1", "email": "a@b.com"})
    )
    respx.get(f"{BASE}/api/customers").mock(
        return_value=httpx.Response(200, json={"customers": [{"id": "c1"}]})
    )
    patch = respx.patch(f"{BASE}/api/customers/c1").mock(
        return_value=httpx.Response(200, json={"id": "c1", "full_name": "New"})
    )
    respx.delete(f"{BASE}/api/customers/c1").mock(return_value=httpx.Response(204))

    assert (await async_client.customers.create(email="a@b.com")).id == "c1"
    assert (await async_client.customers.retrieve("c1")).email == "a@b.com"
    assert [c.id for c in await async_client.customers.list()] == ["c1"]
    assert (await async_client.customers.update("c1", full_name="New")).full_name == "New"
    assert await async_client.customers.delete("c1") is None
    assert json.loads(patch.calls.last.request.content) == {"full_name": "New"}


# --- async payments ---------------------------------------------------------
@respx.mock
async def test_async_payments(async_client):
    respx.get(f"{BASE}/api/orders/o/payments").mock(
        return_value=httpx.Response(200, json={"data": [{"id": "p1"}]})
    )
    respx.get(f"{BASE}/api/payments/p1").mock(
        return_value=httpx.Response(200, json={"id": "p1", "state": "captured"})
    )
    respx.post(f"{BASE}/api/orders/o/payments").mock(
        return_value=httpx.Response(201, json={"id": "p2"})
    )
    assert [p.id for p in await async_client.payments.list_for_order("o")] == ["p1"]
    assert (await async_client.payments.retrieve("p1")).state == "captured"
    assert (await async_client.payments.pay("o", payment_method_id="pm")).id == "p2"


# --- async webhooks ---------------------------------------------------------
@respx.mock
async def test_async_webhooks_management(async_client):
    respx.get(f"{BASE}/api/1.0/webhooks").mock(
        return_value=httpx.Response(200, json={"webhooks": [{"id": "w1"}]})
    )
    respx.get(f"{BASE}/api/1.0/webhooks/w1").mock(
        return_value=httpx.Response(200, json={"id": "w1", "url": "https://x"})
    )
    respx.patch(f"{BASE}/api/1.0/webhooks/w1").mock(
        return_value=httpx.Response(200, json={"id": "w1"})
    )
    respx.delete(f"{BASE}/api/1.0/webhooks/w1").mock(return_value=httpx.Response(204))
    respx.post(f"{BASE}/api/1.0/webhooks/w1/rotate-signing-secret").mock(
        return_value=httpx.Response(200, json={"id": "w1", "signing_secret": "wsk_z"})
    )
    assert [w.id for w in await async_client.webhooks.list()] == ["w1"]
    assert (await async_client.webhooks.retrieve("w1")).url == "https://x"
    assert (await async_client.webhooks.update("w1", events=["ORDER_FAILED"])).id == "w1"
    assert await async_client.webhooks.delete("w1") is None
    rotated = await async_client.webhooks.rotate_signing_secret("w1")
    assert rotated.signing_secret == "wsk_z"


# --- async orders update/cancel ---------------------------------------------
@respx.mock
async def test_async_orders_update_and_cancel(async_client):
    respx.patch(f"{BASE}/api/orders/o").mock(return_value=httpx.Response(200, json={"id": "o"}))
    respx.post(f"{BASE}/api/orders/o/cancel").mock(
        return_value=httpx.Response(200, json={"id": "o", "state": "cancelled"})
    )
    assert (await async_client.orders.update("o", metadata={"k": "v"})).id == "o"
    assert (await async_client.orders.cancel("o")).state == "cancelled"


# --- sync gaps: customers/webhooks retrieve+update --------------------------
@respx.mock
def test_sync_customers_retrieve_update(client):
    respx.get(f"{BASE}/api/customers/c1").mock(return_value=httpx.Response(200, json={"id": "c1"}))
    respx.patch(f"{BASE}/api/customers/c1").mock(
        return_value=httpx.Response(200, json={"id": "c1", "email": "x@y.z"})
    )
    assert client.customers.retrieve("c1").id == "c1"
    assert client.customers.update("c1", email="x@y.z").email == "x@y.z"


@respx.mock
def test_sync_webhooks_retrieve_update(client):
    respx.get(f"{BASE}/api/1.0/webhooks/w1").mock(
        return_value=httpx.Response(200, json={"id": "w1"})
    )
    respx.patch(f"{BASE}/api/1.0/webhooks/w1").mock(
        return_value=httpx.Response(200, json={"id": "w1"})
    )
    assert client.webhooks.retrieve("w1").id == "w1"
    assert client.webhooks.update("w1", url="https://z").id == "w1"


@respx.mock
def test_sync_payment_retrieve(client):
    respx.get(f"{BASE}/api/payments/p1").mock(return_value=httpx.Response(200, json={"id": "p1"}))
    assert client.payments.retrieve("p1").id == "p1"


# --- async network error wrapping -------------------------------------------
@respx.mock
async def test_async_wraps_network_errors():
    respx.get(f"{BASE}/api/orders/o").mock(side_effect=httpx.ConnectError("boom"))
    from revolut._http.base import RetryConfig

    c = AsyncRevolutMerchantClient(
        secret_key="sk", environment="sandbox", retry=RetryConfig(max_retries=0)
    )
    with pytest.raises(APIConnectionError):
        await c.orders.retrieve("o")
    await c.aclose()
