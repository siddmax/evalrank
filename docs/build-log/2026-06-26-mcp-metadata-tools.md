# MCP Metadata Tools

Date: 2026-06-26

## Built

- Added explicit `evalrank.use_cases` for `GET /v1/use-cases`.
- Added explicit `evalrank.scoring_stages` for `GET /v1/scoring-stages`.
- Routed both tools through the public Python SDK `EvalRankClient`.
- Added focused MCP tests for README coverage, tool manifest schemas, GET route paths, no request body, JSON text results, Problem Details tool errors, and invalid metadata arguments.
- Updated public package docs, root docs, test map, status tracker, and porting map.

## Public Boundary

This is public MCP plumbing for route contracts that already exist in `schemas/openapi.json`.

No auth, retries, service discovery, environment-variable defaults, hosted receipt IDs, tenant context, private DTOs, database work, source adapters, production evidence lookup, scorer runtime, private methodology, or held-out evaluation material moved into this repo.

## Port Decision

Port the MCP metadata tools here because they expose only storage-free public catalog routes and synthetic-testable HTTP behavior.

Keep live hosted implementations, DB bootstrap, Supabase migrations, runtime scorer/materializer behavior, graph/evidence lookup, and eval-integrity material in their private owning workstreams until each has a separable public contract.

## Verification

```sh
python3 -m unittest tests.test_mcp_fixture
python3 scripts/check_public_boundary.py --root .
make check
```
