# Retry-Aware Problem Details Contract

Date: 2026-06-26

## Built

- Extended `schemas/problem.schema.json` with optional public Problem Details fields: `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url`.
- Added reusable OpenAPI response components for `400`, `422`, `429`, `503`, and `504`.
- Added reusable OpenAPI header components for `X-Request-Id`, `Retry-After`, `RateLimit`, and `RateLimit-Policy`.
- Mirrored public Problem Details codes and `ProblemDetails` type in the TypeScript SDK.
- Updated status, porting, route, schema, SDK, repo-structure, and test docs.

## Public Boundary

- This is a contract-only port. It does not add a service client, live server, auth flow, tenant logic, rate-limit enforcement, persistence, or deployment wiring.
- Private problem types, hosted error internals, production telemetry, customer examples, held-out eval data, and private Syndai/Finn/Savida code remain excluded.
- Supabase schema bootstrap and migrations remain private in Syndai until EvalRank owns persistence or its own Supabase project.

## Verification

- Red check before implementation: `python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract tests.test_sdk_ts` failed on missing public error extensions, response components, headers, and TypeScript types.
- Focused check after implementation: `python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract tests.test_sdk_ts`.
