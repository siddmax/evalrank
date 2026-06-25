# Evaluation Request Entity-Type Uniqueness

Date: 2026-06-26

## Built

- Hardened `EvaluationRequest` so `entity_types` must be unique.
- Pinned `uniqueItems: true` for `entity_types` in `schemas/evaluation-request.schema.json`.
- Added focused core and schema tests for duplicate rejection and schema parity.

## Kept Private

- Candidate resolver behavior.
- Source adapters and graph lookup.
- Scorer/runtime behavior.
- Route implementation, auth, persistence, or hosted request handling.
