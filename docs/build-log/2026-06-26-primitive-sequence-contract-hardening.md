# Primitive And Sequence Contract Hardening

Date: 2026-06-26

## What Changed

- Hardened existing public Python contracts so schema-constrained primitive and sequence fields reject invalid Python values before `to_dict()`.
- Added focused regressions for `EntityRef`, `Freshness`, `EvaluationRequest.entity_types`, and `RankedEntity` rank/evidence/caveat fields.
- Kept the change storage-free and public-safe: no schemas were expanded, no scorer behavior was added, and no private runtime or data dependency moved here.

## Guarded Fields

| Contract | Field class | Public rule |
| --- | --- | --- |
| `EntityRef` | `entity_type`, `entity_id` | Non-empty strings only. |
| `Freshness` | `last_eval`, `next_refresh` | Non-empty strings only. |
| `EvaluationRequest` | `request_id`, `use_case`, `requested_at`, `entity_types` | Required strings plus a non-empty tuple of non-empty strings. |
| `RankedEntity` | `entity_type`, `entity_id`, `rank`, `evidence_count`, `caveats` | Required strings, real integer counts/ranks, and tuple-backed string caveats. |

## Verification

- Red: `python3 -m unittest tests.test_core_contracts` failed on the new primitive/sequence validation regressions.
- Green: `python3 -m unittest tests.test_core_contracts` passed after the core contract fix.
