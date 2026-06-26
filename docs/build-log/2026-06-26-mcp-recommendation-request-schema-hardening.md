# MCP Recommendation Request Schema Hardening

Date: 2026-06-26

## Built

- Updated the public `evalrank.recommend` MCP tool manifest so its `request` input advertises the public `EvaluationRequest` payload shape.
- Added focused MCP manifest tests for required request fields, non-empty string fields, unique non-empty `entity_types`, timestamp pattern, and open JSON `constraints`.
- Updated MCP README, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md` with the shipped public boundary.

## Boundary

- This is manifest/OpenAPI parity for the existing public recommendation route.
- Server-side API validation remains authoritative.
- No auth, private DTOs, hosted receipts, service discovery, database work, scorer runtime, private source adapters, or private Syndai data moved into this repo.

## Verification

- `python3 -m unittest tests.test_mcp_fixture`
- `python3 -m unittest tests.test_repo_docs`
- `python3 scripts/check_public_boundary.py --root .`
- `git diff --check`
- `make check`
