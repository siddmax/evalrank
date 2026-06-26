# Shortlist Depth Count Consistency

Date: 2026-06-26

## What changed

- Added a core regression test for direct `Recommendation(...)` payloads whose `shortlist_depth` disagrees with returned ranked rows.
- Hardened `Recommendation.__post_init__` so single-scale responses require `shortlist_depth == len(ranked)`.
- Hardened grouped responses so `shortlist_depth` must equal the sum of ranked rows across all `RankingGroup` entries.
- Updated public core, test, status, and porting docs.

## Boundary

This is public response-shape consistency for an existing storage-free recommendation contract. JSON Schema stays structural because array-count arithmetic belongs in the Python reference contract. This does not add scorer thresholds, private ranking policy, source adapters, graph lookup, persistence, hosted receipts, telemetry, DB work, or held-out evaluation material.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_shortlist_depth_count_drift
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_shortlist_depth_count_drift tests.test_core_contracts.CoreContractTests.test_core_readme_lists_public_contract_surface
python3 scripts/check_public_boundary.py --root .
make check
```
