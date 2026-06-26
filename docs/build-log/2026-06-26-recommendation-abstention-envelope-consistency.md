# Recommendation Abstention Envelope Consistency

Date: 2026-06-26

## What changed

- Added core `Recommendation` validation that rejects dangling or contradictory `the_call` / `abstention` combinations.
- Added JSON Schema branch rules requiring abstaining calls to carry an `abstention` object and recommending calls to carry `abstention: null`.
- Mirrored the same public state in the TypeScript SDK `Recommendation` types.
- Updated public package/schema docs, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is public envelope consistency for an existing storage-free response contract. It does not add evidence-floor thresholds, private abstention taxonomy, scorer runtime, persistence, source adapters, hosted receipts, telemetry, or DB work.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_inconsistent_abstention_envelope tests.test_schema_contracts.SchemaContractTests.test_recommendation_schema_pins_abstention_envelope_consistency tests.test_sdk_ts.TypeScriptSdkTests.test_public_interfaces_cover_schema_payloads
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
```
