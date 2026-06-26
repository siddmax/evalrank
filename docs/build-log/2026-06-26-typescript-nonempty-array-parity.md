# TypeScript Non-Empty Array Parity

Date: 2026-06-26

## Changed

- Added `NonEmptyArray<T>` to the public TypeScript SDK.
- Applied it to existing public arrays with Python and JSON Schema `minItems: 1` requirements: request entity types, candidates, retrieval arms, use-case and scoring-stage catalogs, stage contract refs, recommendation groups, and ranking-group rows.
- Added focused TypeScript surface checks.
- Updated `TESTS.md`, `packages/sdk-ts/README.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is TypeScript compile-time parity with existing public contracts. It does not add runtime validation, retries, hosted service behavior, private data, scorer logic, graph lookup, source adapters, or persistence.

## Verification

- `python3 -m unittest tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `npm run test --prefix packages/sdk-ts`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
