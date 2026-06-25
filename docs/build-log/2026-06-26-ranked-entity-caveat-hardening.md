# Ranked Entity Caveat Hardening

Date: 2026-06-26

## What changed

- `RankedEntity` now rejects empty strings in `caveats`.
- `ranked-entity.schema.json` now pins caveat items as non-empty strings.
- Added focused regression coverage for the core and schema caveat constraints.

## Public boundary

- This is schema/core parity hardening for an already-public payload.
- No scorer behavior, private runtime, source adapter, DB work, hosted operation, or private methodology detail moved into this repo.
