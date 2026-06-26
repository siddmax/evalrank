# MCP Base URL Schema Hardening

Date: 2026-06-26

## Built

- Updated public MCP route tool input schemas so `evalrank.recommend`, `evalrank.use_cases`, and `evalrank.scoring_stages` advertise non-empty HTTP(S) `base_url` values.
- Added a focused MCP manifest test for the public `base_url` schema shape.
- Updated MCP README, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md` with the shipped public boundary.

## Boundary

- This is manifest/runtime boundary parity for already-public route tools.
- No service discovery, auth, retries, hosted receipts, private service calls, database work, scorer runtime, or private Syndai data moved into this repo.

## Verification

- `python3 -m unittest tests.test_mcp_fixture`
- `python3 -m unittest tests.test_repo_docs`
- `python3 scripts/check_public_boundary.py --root .`
- `git diff --check`
- `make check`
