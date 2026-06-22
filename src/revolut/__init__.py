"""revolut-python — a typed client for the Revolut Merchant API (sync + async)."""

from __future__ import annotations

from ._http.base import RetryConfig
from ._version import __version__
from .client import AsyncRevolutMerchantClient, RevolutMerchantClient
from .config import DEFAULT_API_VERSION, Environment
from .exceptions import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    InvalidRequestError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    RevolutError,
    ServerError,
    SignatureVerificationError,
)
from .models import (
    CaptureMode,
    Customer,
    Location,
    Money,
    Order,
    OrderList,
    OrderState,
    OrderType,
    Payment,
    PaymentMethod,
    PaymentState,
    Payout,
    Refund,
    Subscription,
    Webhook,
    WebhookEvent,
    WebhookEventPayload,
)
from .webhooks_verify import compute_signature, verify_signature

__all__ = [
    "DEFAULT_API_VERSION",
    "APIConnectionError",
    "APIStatusError",
    "AsyncRevolutMerchantClient",
    "AuthenticationError",
    "BadRequestError",
    "CaptureMode",
    "Customer",
    "Environment",
    "InvalidRequestError",
    "Location",
    "Money",
    "NotFoundError",
    "Order",
    "OrderList",
    "OrderState",
    "OrderType",
    "Payment",
    "PaymentMethod",
    "PaymentState",
    "Payout",
    "PermissionDeniedError",
    "RateLimitError",
    "Refund",
    "RetryConfig",
    "RevolutError",
    "RevolutMerchantClient",
    "ServerError",
    "SignatureVerificationError",
    "Subscription",
    "Webhook",
    "WebhookEvent",
    "WebhookEventPayload",
    "__version__",
    "compute_signature",
    "verify_signature",
]
