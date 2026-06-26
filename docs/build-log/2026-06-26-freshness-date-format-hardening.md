# Freshness Date Format Hardening

Date: 2026-06-26

## What changed

- Python core `Freshness` now rejects `last_eval` and `next_refresh` values outside public calendar-valid `YYYY-MM-DD` date strings.
- `ranked-entity.schema.json` mirrors the same structural pattern for freshness dates.
- Core and schema tests cover invalid timestamp, compact, slash-separated, and impossible calendar date forms.

## Public boundary

This is storage-free payload validation. No private scheduler cadence, runtime refresh policy, telemetry, DB work, source adapter, or hosted operation moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_freshness_requires_public_date_format tests.test_schema_contracts.SchemaContractTests.test_ranked_entity_schema_pins_freshness_date_format
```
