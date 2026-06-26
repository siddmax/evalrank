# Ranked Entity Axes Contract Hardening

Date: 2026-06-26

## Changed

- Tightened `schemas/ranked-entity.schema.json` so `axes.evidence` is a closed public object with `n_items` and trust-tier `coverage`.
- Mirrored the same shape in the TypeScript SDK `RankedEntity` interface.
- Added focused schema and TypeScript surface checks.
- Updated `TESTS.md`, `schemas/README.md`, `packages/sdk-ts/README.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Boundary

This is schema/type parity with the existing Python `RankedEntity.to_dict()` output. It does not add private evidence scoring, weights, formulas, calibration, scorer runtime, graph lookup, source adapters, or persistence.

## Verification

- `python3 -m unittest tests.test_schema_contracts tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `npm run test --prefix packages/sdk-ts`
- `python3 scripts/check_public_boundary.py --root .`
- `make check`
