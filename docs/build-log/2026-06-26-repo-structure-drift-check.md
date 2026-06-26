# Repo Structure Drift Check

Date: 2026-06-26

## Changed

- Added a stdlib repo-doc test so `docs/REPO_STRUCTURE.md` must track public top-level directories and package directories.
- Updated `docs/REPO_STRUCTURE.md`, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.
- Rechecked private-side routing: current dirty private work remains outside the EvalRank public core, so no raw private content was ported.

## Boundary

This is a deterministic public-doc drift guard. It does not copy private plans, private repo paths, live identifiers, hosted operations, persistence, source adapters, scorer runtime, telemetry, customer data, or held-out eval material.

## Verification

- `python3 -m unittest tests.test_repo_docs`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
