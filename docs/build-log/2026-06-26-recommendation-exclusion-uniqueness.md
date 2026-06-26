# Recommendation Exclusion Uniqueness

Date: 2026-06-26

## What changed

- Added a core regression test rejecting duplicate `Recommendation.exclusions` rows.
- Added a schema drift assertion that `recommendation.schema.json` pins `exclusions.uniqueItems`.
- Hardened `Recommendation.__post_init__` to reject duplicate public exclusion rows before serialization.
- Updated public core, schema, status, porting, and test docs.

## Boundary

This is public response-shape hardening for existing storage-free exclusions. It does not add gate policy, private safety taxonomy, scorer runtime, persistence, source adapters, hosted behavior, DB work, telemetry, or held-out evaluation material.

## Verification

Red:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_duplicate_exclusions
python3 -m unittest tests.test_schema_contracts.SchemaContractTests.test_recommendation_schema_reuses_exclusion_schema
```

Green:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_duplicate_exclusions tests.test_core_contracts.CoreContractTests.test_recommendation_serializes_public_exclusions tests.test_schema_contracts.SchemaContractTests.test_recommendation_schema_reuses_exclusion_schema
python3 scripts/check_public_boundary.py --root .
make check
```
