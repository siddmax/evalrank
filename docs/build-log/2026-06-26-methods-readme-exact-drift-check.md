# Methods README Exact Drift Check

Date: 2026-06-26

## Changed

- Tightened method docs tests so `methods/README.md` must list the public method-note filenames exactly.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is a deterministic public-doc drift guard. It does not add private methodology, scorer weights, thresholds, benchmark data, runtime behavior, hosted behavior, persistence, source adapters, or dependencies.

## Verification

- `python3 -m unittest tests.test_methods_docs`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
