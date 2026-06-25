# SDK README Drift Checks

Date: 2026-06-26

## Built

- Added README drift checks for Python and TypeScript SDK public surfaces.
- Updated the Python SDK README to list the current public re-export surface.
- Updated `docs/STATUS.md`.

## Kept Out

- No service client, auth flow, hosted route behavior, private data access, package publish flow, or generated build output.

## Verification

- Red first: `python3 -m unittest tests.test_sdk_python.PythonSdkTests.test_sdk_readme_lists_public_reexport_surface` failed while the Python README omitted newer public contracts.
- Green: `python3 -m unittest tests.test_sdk_python tests.test_sdk_ts`.
