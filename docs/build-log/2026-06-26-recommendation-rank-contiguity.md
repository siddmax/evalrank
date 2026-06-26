# Recommendation Rank Contiguity

Date: 2026-06-26

## What changed

- Python core recommendation contracts now reject duplicate, gapped, or out-of-order rank positions.
- The invariant applies to single-scale `Recommendation.ranked` rows and within-kind `RankingGroup.ranked` rows.
- `tests/test_core_contracts.py` covers duplicate rank `1,1`, gapped rank `1,3`, and unordered rank `2,1` cases.

## Public boundary

This is storage-free response-shape hardening. JSON Schema remains structural; the reference Python core owns the rank arithmetic. No scorer normalization, private score semantics, runtime, DB work, hosted receipts, telemetry, or held-out eval material moved.

## Verification

```sh
python3 -m unittest tests.test_core_contracts
```
