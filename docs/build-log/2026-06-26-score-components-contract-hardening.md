# Score Components Contract Hardening

Date: 2026-06-26

## What Changed

- Hardened `RankedEntity.score_components` so it accepts only a JSON-object map from non-empty public component names to 0-1 numeric scores.
- Updated `ranked-entity.schema.json` with matching `propertyNames` and 0-1 numeric value constraints.
- Added focused regression coverage for invalid score-component maps and schema shape drift.

## Public Boundary

- This pins the public explanation-map shape only.
- It does not publish scorer formulas, private weights, cross-kind normalization, IRT clusters, thresholds, held-out eval material, production telemetry, or scorer runtime code.

## Verification Intent

- Run `python3 -m unittest tests.test_core_contracts tests.test_schema_contracts`.
- Run `make check` before pushing.
