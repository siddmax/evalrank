# Schema README Exact Drift Check

Date: 2026-06-26

## Changed

- Tightened schema README tests so documented public schema and OpenAPI filenames must match the actual files exactly.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is a deterministic public-doc drift guard. It does not change schema shape, runtime behavior, private services, hosted behavior, persistence, source adapters, or dependencies.

## Verification

- `python3 -m unittest tests.test_schema_contracts`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
