# Recommendation Join Aliases

Date: 2026-06-25

## Built

- Added `recommend_id` and `search_run_id` to public recommendation payloads.
- Kept both fields as exact aliases of the existing content-addressed `recommendation_id`.
- Mirrored the aliases in the recommendation JSON Schema and TypeScript SDK interface.
- Added focused contract, schema, and SDK tests.

## Boundary

- No hosted receipt route, HMAC key handling, secret-backed ID derivation, storage table, or migration was added.
- Private hosted systems still own any future receipt/HMAC behavior until a public route contract exists.

## Checks

```sh
python3 -m unittest tests.test_core_contracts tests.test_schema_contracts tests.test_sdk_ts
make check
npm run check --prefix packages/sdk-ts
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture recommendation
```
