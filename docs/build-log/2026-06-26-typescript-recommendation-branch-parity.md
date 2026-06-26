# TypeScript Recommendation Branch Parity

Date: 2026-06-26

## Changed

- Replaced the loose TypeScript `Recommendation` interface with `SingleScaleRecommendation | KindGroupedRecommendation`.
- Mirrored the existing Python and JSON Schema comparability branch rules for `single-scale` and `kind-grouped`.
- Added focused TypeScript surface checks.
- Updated `TESTS.md`, `packages/sdk-ts/README.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is TypeScript compile-time parity with an existing public contract. It does not add runtime validation, scorer normalization, private score semantics, hosted receipts, runtime behavior, graph lookup, source adapters, or persistence.

## Verification

- `python3 -m unittest tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `npm run test --prefix packages/sdk-ts`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
