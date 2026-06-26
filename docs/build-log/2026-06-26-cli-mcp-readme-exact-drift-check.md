# CLI and MCP README Exact Drift Check

Date: 2026-06-26

## Changed

- Tightened CLI README tests so documented fixture commands and public route commands must match the actual public surface exactly.
- Tightened MCP README tests so documented fixture kinds and tool names must match the actual public surface exactly.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is a deterministic public-doc drift guard. It does not add runtime behavior, private services, live API assumptions, hosted receipts, persistence, source adapters, or dependencies.

## Verification

- `python3 -m unittest tests.test_cli_fixture`
- `python3 -m unittest tests.test_mcp_fixture`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
