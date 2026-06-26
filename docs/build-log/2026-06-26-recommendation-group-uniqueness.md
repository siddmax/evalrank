# Recommendation Group Uniqueness

Date: 2026-06-26

## What changed

- Python core `Recommendation` now rejects duplicate `kind-grouped` groups by `group_key` or `entity_type`.
- `recommendation.schema.json` now marks grouped recommendation rows as `uniqueItems`.
- Core and schema tests pin the new public grouped-response shape.

## Public boundary

This is storage-free response-shape validation. No cross-kind score normalization, scorer runtime, private score semantics, DB work, hosted receipt behavior, telemetry, or private benchmark material moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_kind_grouped_recommendation_rejects_duplicate_groups tests.test_schema_contracts.SchemaContractTests.test_recommendation_schema_pins_group_uniqueness
```
