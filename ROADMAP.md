# Roadmap — revolut-merchant-py

A typed Python client for the **Revolut Merchant API** with both synchronous and
asynchronous clients. Versioning follows [SemVer](https://semver.org/).

> Current version: **1.0.0** on
> [PyPI](https://pypi.org/project/revolut-merchant-py/). Auto-publish via PyPI
> Trusted Publishing on `v*` tags.

## v0.1.0 — Foundations ✅ (shipped)

- [x] Project scaffolding: `src` layout, `hatchling` packaging, MIT license
- [x] Tooling: `ruff` (lint + format), `mypy --strict`, `pytest` + `respx`
- [x] CI matrix (Python 3.10–3.13) via GitHub Actions
- [x] Config + constants (base URLs, API version header)
- [x] Exception hierarchy mapped from HTTP status codes
- [x] Core HTTP layer (sync `httpx.Client` + async `httpx.AsyncClient`)
- [x] Auth via secret API key (Bearer) + idempotency keys

## v0.2.0 — Orders & Payments ✅ (shipped)

- [x] Pydantic models: `Money`, enums, `Order`, `Payment`, `Refund`, `Customer`
- [x] `orders` resource: create, retrieve, list, update, capture, cancel
- [x] `payments` resource: retrieve, list, pay (saved method)
- [x] `refunds` resource: create refund
- [ ] Pagination helpers (auto-iterating list endpoints) — moved to v0.5.0

## v0.3.0 — Customers & Webhooks ✅ (shipped)

- [x] `customers` resource: create, retrieve, list, update, delete
- [x] `webhooks` resource: create, list, retrieve, update, rotate secret, delete
- [x] Webhook signature verification (HMAC-SHA256, timestamp tolerance)
- [x] Typed webhook event payloads

## v0.4.0 — Polish & Docs ✅ (shipped)

- [x] Full README usage guide (sync + async, webhooks)
- [x] Auto-retry with backoff for 429 / 5xx
- [x] 100% of public API type-annotated; `mypy --strict` clean
- [x] Test coverage ≥ 90% (currently 98%)
- [x] Packaging + PyPI release pipeline (Trusted Publishing, OIDC)

## v0.5.0 — Pagination, saved methods & live verification

- [x] Auto-pagination helpers: `iter()` over list endpoints (cursor / `page_token`)
- [x] Saved payment methods / tokenization CRUD (list / retrieve / update / delete)
- [x] Live sandbox integration tests (harness under `tests/integration`, gated by `REVOLUT_SECRET_KEY`)
- [x] Verify endpoint path strings against a real sandbox (#23 — done in 1.0.1; disputes/report-runs found not to exist and were removed)

## v0.6.0 — Remaining resources & docs site ✅ (shipped)

- [x] `subscriptions` resource
- [x] `payouts` resource
- [x] `locations` resource
- [x] Documentation site (mkdocs-material) published from CI
- [~] `disputes` / `report runs` — not part of the Merchant API (404 in sandbox); removed in 1.0.1

## v1.0.0 — Stable API ✅ (shipped)

- [x] Public API frozen (guarded by a test); no breaking changes expected
- [x] Documented deprecation policy and SemVer commitment (README)
- [x] All in-scope Merchant API resources covered (verified against sandbox)
- [x] Hardening: debug logging, per-request timeout override, backoff jitter
- [x] Live-sandbox suite run with real credentials (1.0.1)

## Future / maybe

- [ ] Optional: Business API module
- [ ] Optional: Open Banking module
