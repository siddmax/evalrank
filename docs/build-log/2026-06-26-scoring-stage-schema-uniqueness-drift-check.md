# Scoring Stage Schema Uniqueness Drift Check

Date: 2026-06-26

## What Changed

- Extended `tests/test_schema_contracts.py` to pin existing scoring-stage catalog uniqueness rules for `stages`, `input_contracts`, and `output_contracts`.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md` so the guard is visible in the public progress and porting map.

## Public Boundary

- This is a drift guard for an already-public schema.
- No new scoring stages, formulas, thresholds, scorer runtime, DB work, private methodology, or held-out evaluation material moved into this repo.

## Verification

- `python3 -m unittest tests.test_schema_contracts`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
