# Package README Metadata Drift Guard

Date: 2026-06-26

## Changed

- Added package metadata blocks to public package READMEs.
- Extended `tests/test_package_metadata.py` so Python package READMEs must match `pyproject.toml` names, imports, dependencies, entrypoints, and licenses.
- Extended the same test to bind the TypeScript SDK README to `package.json` package name, module type, types entry, license, and private publish status.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is an Open-Core Boundary / CI slice. It does not add publishing, release automation, credentials, private package indexes, hosted deployment behavior, service discovery, auth, retries, or private route semantics.

## Verification

- `python3 -m unittest tests.test_package_metadata`
- `python3 scripts/check_public_boundary.py --root .`
- `git diff --check`
- `make check` (191 Python tests, TypeScript check, and 6 TypeScript runtime tests)
