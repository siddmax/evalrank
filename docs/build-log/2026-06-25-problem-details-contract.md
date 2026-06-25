# Problem Details Contract

Date: 2026-06-25

## Built

- `schemas/problem.schema.json` for RFC 9457 Problem Details.
- `POST /v1/recommendations` `400` response using `application/problem+json`.
- OpenAPI `ProblemDetails` component reference.
- Schema and OpenAPI regression tests.

## Explicitly Not Built

- Live error runtime.
- Hosted auth or tenant error behavior.
- Private problem type URIs.
- Validation-error extension arrays.
- Receipt lookup errors or HMAC-backed identifiers.
- Telemetry, logging, persistence, or deploy wiring.

## Port-Over Assessment

- Public Surface Contracts owns the shared RFC 9457 shape in this repo because it is a portable HTTP API contract.
- Public Contracts and Methods / Schemas own future public problem-type extensions only when their semantics are product-neutral and stable.
- Hosted Ops / Deploy Ops keeps auth, tenant, receipt, telemetry, logging, and deployment error behavior private.
- DB Bootstrap / Syndai Ops keeps Supabase-backed error persistence and live schema checks private until EvalRank owns persistence.
- Evaluation Integrity keeps held-out evaluator failures, private judge traces, and benchmark-specific error details out of this repo.

## Public Boundary Notes

- The schema allows RFC 9457 extension members, but this slice does not publish private extension names or problem type URIs.
- The OpenAPI contract names only the invalid-request response for `POST /v1/recommendations`.
- Synthetic tests cover the public contract shape without private requests, customers, traces, credentials, or production rows.

## Verification

```sh
python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract
make check
npm run check --prefix packages/sdk-ts
```
