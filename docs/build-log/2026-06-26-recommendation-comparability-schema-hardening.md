# Recommendation Comparability Schema Hardening

Date: 2026-06-26

## What changed

- `recommendation.schema.json` now pins comparability-specific response shapes:
  - `single-scale` recommendations must have `groups: null`.
  - `kind-grouped` recommendations must have no top-level ranked rows and at least one group.
- Added focused schema regression coverage for the existing core `Recommendation` branch rules.

## Public boundary

- This is schema/core parity hardening for an already-public recommendation envelope.
- No scorer normalization, private score semantics, source adapter, DB work, hosted receipt behavior, private evidence, or held-out evaluation material moved into this repo.
