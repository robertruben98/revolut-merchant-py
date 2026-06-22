"""Resource classes for each Merchant API object group."""

from .customers import AsyncCustomersResource, CustomersResource
from .locations import AsyncLocationsResource, LocationsResource
from .orders import AsyncOrdersResource, OrdersResource
from .payment_methods import AsyncPaymentMethodsResource, PaymentMethodsResource
from .payments import AsyncPaymentsResource, PaymentsResource
from .payouts import AsyncPayoutsResource, PayoutsResource
from .refunds import AsyncRefundsResource, RefundsResource
from .subscriptions import AsyncSubscriptionsResource, SubscriptionsResource
from .webhooks import AsyncWebhooksResource, WebhooksResource

__all__ = [
    "AsyncCustomersResource",
    "AsyncLocationsResource",
    "AsyncOrdersResource",
    "AsyncPaymentMethodsResource",
    "AsyncPaymentsResource",
    "AsyncPayoutsResource",
    "AsyncRefundsResource",
    "AsyncSubscriptionsResource",
    "AsyncWebhooksResource",
    "CustomersResource",
    "LocationsResource",
    "OrdersResource",
    "PaymentMethodsResource",
    "PaymentsResource",
    "PayoutsResource",
    "RefundsResource",
    "SubscriptionsResource",
    "WebhooksResource",
]
