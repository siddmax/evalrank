# Confidence Interval Schema Drift Guard

Date: 2026-06-26

## What changed

- Schema tests now pin public `ci95` fields for `RankedEntity` and `ResultRow` as exactly two numeric unit-interval values.
- Public docs now mention the fixed `[low, high]` shape.

## Public boundary

This is a storage-free schema drift guard. No scorer calibration, confidence policy, private benchmark data, runtime, persistence, hosted receipt behavior, telemetry, or private thresholds moved.

## Verification

```sh
python3 -m unittest tests.test_schema_contracts.SchemaContractTests.test_confidence_interval_schemas_pin_two_unit_scores
```
