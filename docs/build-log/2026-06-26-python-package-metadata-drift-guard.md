# Python Package Metadata Drift Guard

Date: 2026-06-26

## What changed

- Added `tests/test_package_metadata.py`.
- Pinned public Python package names, versions, descriptions, licenses, Python floor, dependency edges, and the CLI script entrypoint.
- Added `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md` coverage for the guard.

## Boundary

This is a deterministic public package-hygiene check. It does not add release automation, publishing credentials, private package indexes, deployment wiring, or hosted operations.
