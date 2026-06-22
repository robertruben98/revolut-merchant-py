"""Live sandbox integration tests.

These hit the real Revolut **sandbox** API and are skipped unless a sandbox
secret key is provided:

    REVOLUT_SECRET_KEY=sk_... pytest tests/integration -v

They are excluded from normal/CI runs (which stay hermetic) because no key is
set there. They confirm endpoint paths and field names against a live sandbox
(roadmap issue #23) and act as the release gate.
"""

from __future__ import annotations

import os

import pytest

from revolut import RevolutMerchantClient

SECRET_KEY = os.getenv("REVOLUT_SECRET_KEY")

pytestmark = pytest.mark.skipif(
    not SECRET_KEY, reason="set REVOLUT_SECRET_KEY to run live sandbox tests"
)


@pytest.fixture
def client():
    c = RevolutMerchantClient(secret_key=SECRET_KEY or "", environment="sandbox")
    yield c
    c.close()


def test_create_and_retrieve_order(client):
    order = client.orders.create(amount=1000, currency="GBP")
    assert order.id
    assert order.public_token
    assert order.checkout_url  # returned by the live API
    fetched = client.orders.retrieve(order.id)
    assert fetched.id == order.id


def test_list_orders(client):
    assert isinstance(client.orders.list(limit=5), list)


def test_order_payments_endpoint(client):
    order = client.orders.create(amount=500, currency="GBP")
    assert isinstance(client.payments.list_for_order(order.id), list)


def test_customer_lifecycle_and_payment_methods(client):
    customer = client.customers.create(full_name="Test User", email="t@example.com")
    assert customer.id
    assert isinstance(client.payment_methods.list(customer.id), list)


def test_list_endpoints_respond(client):
    assert isinstance(client.payouts.list(), list)
    assert isinstance(client.subscriptions.list(), list)
    assert isinstance(client.locations.list(), list)
    assert isinstance(client.webhooks.list(), list)


def test_manual_capture_order_created(client):
    order = client.orders.create(amount=500, currency="GBP", capture_mode="manual")
    assert order.state in {"pending", "processing", "authorised"}
