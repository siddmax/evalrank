# Public Progress And Private Routing Refresh

Date: 2026-06-26

## What changed

- `docs/STATUS.md` records the latest public `ResultRow.source_url` contract hardening and the current private-side routing snapshot.
- `docs/PORTING.md` now separates current private Syndai dirty work into preflight/repo guidance, backend runtime reliability, private EvalRank doc-validation, and Memphant planning categories.
- The next public port remains storage-free contract hardening, public route contracts, public doc checks, and synthetic fixtures only.

## Public boundary

This was an inventory refresh by category and path class only. No private spec text, migration script, hosted runbook, customer data, production evidence, credentials, telemetry, Memphant plan text, or held-out evaluation material moved into this repo.

## Verification

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest tests.test_repo_docs tests.test_methods_docs
```
