# The Call Branch Schema Hardening

Date: 2026-06-26

## What changed

- `recommendation.schema.json` now pins branch-specific `the_call` response shapes:
  - `recommend` requires numeric `confidence` and `abstention_reason: null`.
  - `abstain` requires `confidence: null` and a non-empty `abstention_reason`.
- Added focused schema regression coverage for the existing core `TheCall` branch rules.

## Public boundary

- This is schema/core parity hardening for an already-public decision envelope.
- No confidence policy, private abstention taxonomy, scorer/runtime behavior, hosted receipt behavior, DB work, private evidence, or held-out evaluation material moved into this repo.
