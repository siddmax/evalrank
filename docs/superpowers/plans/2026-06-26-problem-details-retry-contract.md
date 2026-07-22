# Retry-Aware Problem Details Contract

Date: 2026-06-26

## Goal

Pin the public, storage-free retry/error contract for EvalRank route surfaces without adding hosted runtime behavior.

## Public Scope

- Extend the existing RFC 9457 Problem Details schema with optional EvalRank fields: `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url`.
- Keep the public code vocabulary product-neutral: `rate_limited`, `upstream_timeout`, `validation`, `not_found`, `methodology_stale`, `internal`, `unauthorized`, and `forbidden`.
- Reuse OpenAPI response and header components for `400`, `422`, `429`, `503`, and `504`.
- Mirror the public error vocabulary in the TypeScript SDK type surface.
- Update status, porting, route, schema, SDK, and test docs.

## Private Boundary

- No auth, tenants, receipt storage, live rate-limit enforcement, service clients, deployment config, or hosted implementation.
- No private problem types, customer examples, production telemetry, held-out eval material, or private runtime code.
- No datastore migrations or DB bootstrap. Runtime persistence and hosted operation are maintained in a separate private system until EvalRank owns its own deploy path or datastore.

## Checks

- `python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract tests.test_sdk_ts`
- `make check`
