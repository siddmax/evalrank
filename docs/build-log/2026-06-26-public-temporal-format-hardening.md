# Public Temporal Format Hardening

Date: 2026-06-26

## What changed

- Python core public event timestamp fields now reject values outside calendar-valid UTC `YYYY-MM-DDTHH:MM:SSZ`.
- `ResultRow.date_run` now reuses the public calendar-valid `YYYY-MM-DD` date validator.
- JSON Schemas mirror the structural timestamp/date patterns for raw entries, catalogs, evidence items/sets, evaluation requests, candidate sets, recommendations, and result rows.

## Public boundary

This is storage-free payload validation. No private scheduler cadence, runtime refresh policy, telemetry, DB work, source adapter, live route, hosted operation, or deployment detail moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_public_temporal_fields_require_pinned_formats tests.test_schema_contracts.SchemaContractTests.test_temporal_schema_fields_pin_public_formats
```
