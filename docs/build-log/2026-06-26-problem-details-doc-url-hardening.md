# Problem Details Doc URL Hardening

Date: 2026-06-26

## What changed

- Python core `ProblemDetails.doc_url` now rejects non-HTTP(S) URL values.
- `problem.schema.json` mirrors the same public HTTP(S) documentation URL shape.
- Core and schema tests cover local paths, private URI schemes, missing URL schemes, and schema/core scheme-case parity.

## Public boundary

This is storage-free error-contract validation. No private problem type, hosted error runtime, auth context, tenant context, telemetry, live route enforcement, DB work, or operational runbook moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_problem_details_rejects_schema_incompatible_values tests.test_schema_contracts.SchemaContractTests.test_problem_schema_pins_evalrank_error_extensions
```
