# Capability Fingerprint Shape Schema Hardening

Date: 2026-06-26

## What changed

- `capability-fingerprint.schema.json` now requires `declared_capability_shape` to contain at least one property.
- Added focused schema regression coverage for the existing core `CapabilityFingerprintInput` requirement.

## Public boundary

- This is schema/core parity hardening for an already-public payload.
- No source adapter, live fetch behavior, scorer runtime, DB work, hosted operation, private evidence, or private methodology detail moved into this repo.
