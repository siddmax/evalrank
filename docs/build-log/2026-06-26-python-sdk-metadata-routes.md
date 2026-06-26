# Python SDK Metadata Routes

Date: 2026-06-26

## Built

- Added dependency-free `EvalRankClient.use_cases()` for `GET /v1/use-cases`.
- Added dependency-free `EvalRankClient.scoring_stages()` for `GET /v1/scoring-stages`.
- Reused the existing HTTP(S)-only base URL validation, JSON response parsing, and public Problem Details error handling.
- Added focused SDK tests for route paths, `Accept: application/json`, no request body, and metadata-route Problem Details errors.
- Updated public package docs, root docs, test map, status tracker, and porting map.

## Public Boundary

This is public SDK plumbing for route contracts that already exist in `schemas/openapi.json`.

No auth, retries, service discovery, environment-variable defaults, hosted receipt IDs, tenant context, private DTOs, database work, source adapters, production evidence lookup, scorer runtime, private methodology, or held-out evaluation material moved into this repo.

## Port Decision

Port the Python SDK metadata-route helpers here because they expose only storage-free public catalog routes and synthetic-testable HTTP behavior.

Keep TypeScript metadata helpers, CLI metadata commands, and MCP metadata tools as separate SDK / CLI / MCP follow-up slices. Keep live hosted implementations, DB bootstrap, Supabase migrations, runtime scorer/materializer behavior, graph/evidence lookup, and eval-integrity material in their private owning workstreams until each has a separable public contract.

## Verification

```sh
python3 -m unittest tests.test_sdk_python
python3 scripts/check_public_boundary.py --root .
make check
```
