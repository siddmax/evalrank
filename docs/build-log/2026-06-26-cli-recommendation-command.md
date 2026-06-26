# CLI Recommendation Command

Date: 2026-06-26

## What changed

- Added `evalrank recommend --base-url URL --request PATH`.
- Added stdin support with `--request -`.
- Reused the public Python SDK `EvalRankClient` instead of duplicating HTTP code.
- Added tests for request file JSON, stdin JSON, route path, public recommendation output, public Problem Details stderr output, malformed/non-object request JSON rejection, and non-HTTP(S) base URL rejection.
- Closed the SDK HTTP error body handle after reading Problem Details to avoid leaking the response resource.

## Boundary

This is explicit HTTP(S)-only public API plumbing. It does not add hidden network calls, auth, retries, service discovery, environment-variable defaults, tenant context, hosted receipt IDs, private DTOs, database work, production evidence lookup, scorer runtime, persistence, or source adapters.
