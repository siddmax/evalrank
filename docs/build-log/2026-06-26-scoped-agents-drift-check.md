# Scoped Agents Drift Check

Date: 2026-06-26

## Changed

- Added a repo-doc test so public work areas must keep scoped `AGENTS.md` guidance.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is a deterministic public-doc drift guard. It does not add private agent instructions, private repo paths, hosted operations, runtime behavior, source adapters, persistence, telemetry, customer data, or held-out eval material.

## Verification

- `python3 -m unittest tests.test_repo_docs`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
