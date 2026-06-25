# Public Abstention Contract

Date: 2026-06-26

## What Changed

- Added a storage-free public `Abstention` contract with non-empty `reason` and `detail` fields.
- Added `abstention` to recommendation payloads: ordinary recommendations emit `null`, and `Recommendation.abstain()` emits a public reason/detail object with an optional distinct public detail.
- Mirrored the shape in `recommendation.schema.json`, the Python SDK re-export surface, and the TypeScript SDK `Recommendation` interface.
- Updated public docs, status, test map, and porting map so agents treat abstention as a public contract while keeping private policy details out.

## Public Boundary

- Public: response shape, JSON Schema, SDK types/re-exports, synthetic fixtures, and docs.
- Private: evidence-floor thresholds, confidence policy, private reason taxonomy, scorer/runtime behavior, DB migrations, hosted receipts, telemetry, and held-out evaluation material.

## Verification

- Red: `python3 -m unittest tests.test_core_contracts tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts` failed before implementation on missing `Abstention`, missing `abstention` payload/schema fields, and missing SDK docs/types.
- Green: `python3 -m unittest tests.test_core_contracts tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts`
- Green: `npm run check --prefix packages/sdk-ts`
- Green: `make check`
- Review: gstack checklist found one helper-completeness issue, auto-fixed by adding optional `detail` support to `Recommendation.abstain()`, with focused contract coverage.

## Porting Decision

Port the public abstention object to this repo because it is storage-free and useful for interoperable recommendation responses. Keep the actual abstention policy, thresholds, scorer rows, private evidence lookups, and hosted implementation in the private Scoring / Materializer Runtime and DB Bootstrap / Syndai Ops workstreams until a later public cutover is explicitly designed.
