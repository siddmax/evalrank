# SDK Retry-After Parser Hardening

Date: 2026-06-26

## What changed

- Hardened Python SDK `EvalRankClient` Problem Details handling so malformed `Retry-After` headers are treated as absent retry hints instead of escaping as raw parser errors.
- Hardened TypeScript SDK `EvalRankClient` Problem Details handling so `Retry-After` is accepted only when it is non-negative integer seconds.
- Added focused Python and TypeScript regressions that prove malformed retry hints still preserve public Problem Details errors.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is public client error-header parsing for already-public route contracts. It does not add retry loops, auth, tenant context, service discovery, environment-variable defaults, hosted receipts, private DTOs, telemetry, database work, production evidence lookup, scorer runtime, or source adapters.

## Verification

```sh
python3 -m unittest tests.test_sdk_python.PythonSdkTests.test_recommend_treats_malformed_retry_after_as_absent tests.test_sdk_python.PythonSdkTests.test_recommend_raises_public_problem_details_error tests.test_sdk_python.PythonSdkTests.test_metadata_route_raises_public_problem_details_error
npm run test --prefix packages/sdk-ts
```
