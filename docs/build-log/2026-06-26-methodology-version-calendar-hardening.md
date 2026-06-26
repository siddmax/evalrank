# Methodology Version Calendar Hardening

Date: 2026-06-26

## What changed

- Python core `methodology_version` validation now rejects impossible dates in the `YYYY-MM-DD.SEQ.slug` prefix.
- Existing structural JSON Schema patterns remain unchanged because calendar validation belongs in the reference core contract.
- Core tests cover invalid methodology-version formats and calendar-invalid dates through ranked rows and recommendation envelopes.

## Public boundary

This is storage-free contract validation. No methodology weights, thresholds, scorer formulas, private benchmark material, runtime behavior, DB work, hosted operation, telemetry, or held-out evaluation material moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_methodology_version_rejects_unpinned_format
```
