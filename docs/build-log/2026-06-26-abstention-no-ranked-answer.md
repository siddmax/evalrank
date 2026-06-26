# Abstention No Ranked Answer

Date: 2026-06-26

## What changed

- Added core `Recommendation` validation that rejects abstentions with ranked rows, grouped rows, or `kind-grouped` comparability.
- Added a JSON Schema branch requiring public abstentions to be empty `single-scale` responses with `shortlist_depth: 0`, `ranked: []`, and `groups: null`.
- Updated TypeScript SDK recommendation types so abstaining responses are represented only by an empty single-scale branch.
- Updated public package/schema docs, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is public response-shape consistency for an existing storage-free abstention contract. It does not add scorer thresholds, evidence-floor policy, private reason taxonomy, runtime behavior, persistence, source adapters, hosted receipts, telemetry, or DB work.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_abstention_with_ranked_answer tests.test_schema_contracts.SchemaContractTests.test_recommendation_schema_pins_abstention_as_empty_single_scale tests.test_sdk_ts.TypeScriptSdkTests.test_public_interfaces_cover_schema_payloads
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
```
