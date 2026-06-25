# Python Problem Details Contract

Date: 2026-06-26

## What Changed

- Added a storage-free Python `ProblemDetails` contract for the public RFC 9457 error payload shape and retry-safe EvalRank extensions.
- Added `PROBLEM_CODES` as the core source of truth for public problem code values.
- Re-exported `ProblemDetails` and `PROBLEM_CODES` through `evalrank_core` and `evalrank_sdk`.
- Added contract, schema-enum parity, Python SDK re-export, and README drift coverage.

## Public Boundary

- Public: RFC 9457 fields, public retry/error extensions, and JSON-safe extension members.
- Private: hosted auth context, tenant context, private problem types, production telemetry, scorer runtime details, and customer examples.

## Verification Intent

- `python3 -m unittest tests.test_core_contracts tests.test_schema_contracts tests.test_sdk_python`
- `make check`
