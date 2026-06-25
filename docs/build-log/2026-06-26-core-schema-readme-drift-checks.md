# Core And Schema README Drift Checks

Date: 2026-06-26

## What Changed

- Added deterministic README drift checks for the public core package and schema docs.
- Updated `packages/core/README.md` to name the current public contract surface.
- Updated `packages/core/README.md` and `schemas/README.md` to document that public string fields must be actual non-empty strings before serialization.
- Kept this public-safe: no new contract, schema, runtime, source adapter, DB, hosted operation, or private evidence behavior moved here.

## Verification

- Red: focused README drift tests failed on missing core contract names and missing public string-field documentation.
- Green: focused README drift tests passed after the README updates.
- Full local gate: `make check` passed with the public boundary scan and 133 unit tests.
- Review: gstack checklist review found no issues; Greptile triage was skipped because this direct-main workflow has no PR.
