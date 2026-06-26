# Recommendation Alias Pattern Drift Guard

Date: 2026-06-26

## What changed

- Schema tests now pin recommendation aliases to the exact public `rec_` plus 24 lowercase hex pattern.
- `recommendation_id`, `recommend_id`, and `search_run_id` still share one schema pattern.

## Public boundary

This is a storage-free schema drift guard. Hosted receipt derivation, HMAC behavior, secret-backed IDs, route persistence, telemetry, and private receipt internals stay out.

## Verification

```sh
python3 -m unittest tests.test_schema_contracts.SchemaContractTests.test_recommendation_join_aliases_share_id_pattern
```
