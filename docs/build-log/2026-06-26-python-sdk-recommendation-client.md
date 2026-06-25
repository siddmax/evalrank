# Python SDK Recommendation Client

Date: 2026-06-26

## What changed

- Added `EvalRankClient` to the Python SDK for dependency-free `POST /v1/recommendations` calls.
- Added `EvalRankApiError` for non-2xx public Problem Details responses.
- Added stdlib `HTTPServer` tests for request JSON, response JSON, `Retry-After` Problem Details behavior, and HTTP(S)-only base URL validation.
- Updated SDK README, root README, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is public request/response plumbing only. It does not add auth, tenant context, retries, hosted receipt IDs, service discovery, local file URL handling, private DTOs, production evidence lookup, scorer runtime, persistence, or source adapters.
