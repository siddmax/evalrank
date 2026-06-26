# TypeScript Recommendation Client

Date: 2026-06-26

## What changed

- Added `EvalRankClient` and `EvalRankApiError` to the TypeScript SDK.
- Added a native `fetch` implementation for public `POST /v1/recommendations`.
- Added package runtime tests for success, Problem Details errors, retry-after parsing, route path, headers, and non-HTTP(S) base URL rejection.
- Added `npm run test --prefix packages/sdk-ts`.
- Added TypeScript package check/test commands to `make check` and pinned Node setup in CI.

## Boundary

This is explicit HTTP(S)-only public API plumbing. It does not add auth, retries, service discovery, environment-variable defaults, tenant context, hosted receipt IDs, private DTOs, database work, production evidence lookup, scorer runtime, persistence, or source adapters.
