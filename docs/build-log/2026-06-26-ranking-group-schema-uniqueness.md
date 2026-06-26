# Ranking Group Schema Uniqueness

Date: 2026-06-26

## What Changed

- Added `uniqueItems: true` to grouped recommendation `RankingGroup.ranked` JSON Schema rows.
- Extended the ranking-group schema-contract test to pin the uniqueness rule.
- Updated status, porting, and test docs so the change is routed as public schema/core parity.

## Public Boundary

- This is storage-free schema hardening for an existing public recommendation payload.
- No cross-kind score normalization, scorer runtime, private score semantics, hosted receipt behavior, DB work, telemetry, production row, or held-out evaluation material moved into this repo.

## Verification

- `python3 -m unittest tests.test_schema_contracts`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
