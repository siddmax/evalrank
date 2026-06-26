# Package README Exact Metadata Drift Check

Date: 2026-06-26

## Changed

- Tightened package README metadata tests so documented distribution/package names, imports, dependencies, entrypoints, license, module type, type entrypoint, and publish status must match package manifests exactly.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is a deterministic public-doc drift guard. It does not change runtime behavior, package publishing, private package indexes, credentials, hosted behavior, persistence, source adapters, or dependencies.

## Verification

- `python3 -m unittest tests.test_package_metadata`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
