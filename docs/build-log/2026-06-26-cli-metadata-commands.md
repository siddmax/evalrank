# CLI Metadata Commands

Date: 2026-06-26

## Built

- Added explicit `evalrank use-cases --base-url ...` for `GET /v1/use-cases`.
- Added explicit `evalrank scoring-stages --base-url ...` for `GET /v1/scoring-stages`.
- Routed both commands through the public Python SDK `EvalRankClient`.
- Added focused CLI tests for README coverage, GET route paths, no request body, JSON stdout, Problem Details stderr, and non-HTTP base URL rejection.
- Updated public package docs, root docs, test map, status tracker, and porting map.

## Public Boundary

This is public CLI plumbing for route contracts that already exist in `schemas/openapi.json`.

No auth, retries, service discovery, environment-variable defaults, hosted receipt IDs, tenant context, private DTOs, database work, source adapters, production evidence lookup, scorer runtime, private methodology, or held-out evaluation material moved into this repo.

## Port Decision

Port the CLI metadata commands here because they expose only storage-free public catalog routes and synthetic-testable HTTP behavior.

Keep MCP metadata tools as a separate SDK / CLI / MCP follow-up slice. Keep live hosted implementations, DB bootstrap, Supabase migrations, runtime scorer/materializer behavior, graph/evidence lookup, and eval-integrity material in their private owning workstreams until each has a separable public contract.

## Verification

```sh
python3 -m unittest tests.test_cli_fixture
python3 scripts/check_public_boundary.py --root .
make check
```
