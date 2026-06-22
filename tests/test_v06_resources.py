"""Tests for subscriptions, payouts and locations resources."""

from __future__ import annotations

import httpx
import respx

BASE = "https://sandbox-merchant.revolut.com"


# --- subscriptions ----------------------------------------------------------
@respx.mock
def test_subscriptions_crud(client):
    respx.post(f"{BASE}/api/subscriptions").mock(
        return_value=httpx.Response(201, json={"id": "sub_1", "state": "active"})
    )
    respx.get(f"{BASE}/api/subscriptions/sub_1").mock(
        return_value=httpx.Response(200, json={"id": "sub_1"})
    )
    respx.get(f"{BASE}/api/subscriptions").mock(
        return_value=httpx.Response(200, json={"subscriptions": [{"id": "sub_1"}]})
    )
    cancel = respx.post(f"{BASE}/api/subscriptions/sub_1/cancel").mock(
        return_value=httpx.Response(200, json={"id": "sub_1", "state": "cancelled"})
    )
    assert client.subscriptions.create(amount=999, currency="EUR").state == "active"
    assert client.subscriptions.retrieve("sub_1").id == "sub_1"
    assert [s.id for s in client.subscriptions.list()] == ["sub_1"]
    assert client.subscriptions.cancel("sub_1").state == "cancelled"
    assert cancel.called


@respx.mock
async def test_async_subscriptions(async_client):
    respx.get(f"{BASE}/api/subscriptions").mock(
        return_value=httpx.Response(200, json=[{"id": "sub_1"}])
    )
    assert [s.id for s in await async_client.subscriptions.list()] == ["sub_1"]


# --- payouts ----------------------------------------------------------------
@respx.mock
def test_payouts(client):
    respx.get(f"{BASE}/api/payouts/po_1").mock(
        return_value=httpx.Response(200, json={"id": "po_1", "state": "completed"})
    )
    respx.get(f"{BASE}/api/payouts").mock(
        return_value=httpx.Response(200, json={"payouts": [{"id": "po_1"}]})
    )
    assert client.payouts.retrieve("po_1").state == "completed"
    assert [p.id for p in client.payouts.list()] == ["po_1"]


# --- locations --------------------------------------------------------------
@respx.mock
def test_locations_crud(client):
    respx.post(f"{BASE}/api/locations").mock(
        return_value=httpx.Response(201, json={"id": "loc_1", "name": "Web"})
    )
    respx.get(f"{BASE}/api/locations/loc_1").mock(
        return_value=httpx.Response(200, json={"id": "loc_1"})
    )
    respx.get(f"{BASE}/api/locations").mock(
        return_value=httpx.Response(200, json={"locations": [{"id": "loc_1"}]})
    )
    respx.patch(f"{BASE}/api/locations/loc_1").mock(
        return_value=httpx.Response(200, json={"id": "loc_1", "name": "Shop"})
    )
    respx.delete(f"{BASE}/api/locations/loc_1").mock(return_value=httpx.Response(204))
    assert client.locations.create(name="Web", type="online").name == "Web"
    assert client.locations.retrieve("loc_1").id == "loc_1"
    assert [loc.id for loc in client.locations.list()] == ["loc_1"]
    assert client.locations.update("loc_1", name="Shop").name == "Shop"
    assert client.locations.delete("loc_1") is None


@respx.mock
async def test_async_locations(async_client):
    respx.get(f"{BASE}/api/locations").mock(
        return_value=httpx.Response(200, json={"locations": [{"id": "loc_1"}]})
    )
    assert [loc.id for loc in await async_client.locations.list()] == ["loc_1"]
