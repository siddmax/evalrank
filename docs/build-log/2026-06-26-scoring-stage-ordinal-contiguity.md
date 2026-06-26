# Scoring Stage Ordinal Contiguity

Date: 2026-06-26

## What changed

- Added core regression tests for `ScoringStageCatalog` payloads with ordinal gaps or missing initial ordinal `1`.
- Hardened `ScoringStageCatalog.__post_init__` so stage ordinals must be contiguous from `1..N`.
- Updated the one-stage catalog test fixture to start at ordinal `1`.
- Updated public core, test, status, and porting docs.

## Boundary

This is public method-stage order consistency for an existing storage-free scoring-stage catalog. JSON Schema stays structural; no scorer formulas, thresholds, private methodology, runtime behavior, source adapters, persistence, telemetry, DB work, or held-out evaluation material moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_rejects_gapped_ordinals tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_rejects_missing_initial_ordinal tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_serializes_public_stage_vocabulary tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_rejects_invalid_public_shape
python3 scripts/check_public_boundary.py --root .
make check
```
