# Result Row Source URL Hardening

Date: 2026-06-26

## What changed

- Python core `ResultRow.source_url` now rejects non-HTTP(S) URL values.
- `result-row.schema.json` mirrors the same public HTTP(S) source URL shape.
- Core and schema tests cover local paths, private URI schemes, missing URL schemes, and schema/core scheme-case parity.

## Public boundary

This is storage-free provenance validation. No source adapter, live fetch behavior, production evidence row, DB work, hosted operation, telemetry, or private benchmark material moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_result_row_rejects_invalid_public_shape tests.test_schema_contracts.SchemaContractTests.test_result_row_schema_pins_public_provenance_envelope
```
