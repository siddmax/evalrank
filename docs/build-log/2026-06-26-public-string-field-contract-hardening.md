# Public String-Field Contract Hardening

Date: 2026-06-26

## What Changed

- Hardened existing public Python contracts so schema-constrained string fields reject truthy non-string values before `to_dict()`.
- Added focused regressions for `CapabilityFingerprintInput`, `RawEntry`, `EvidenceItem`, `EvidenceSet`, `CandidateSet`, and `TheCall`.
- Kept the change storage-free and public-safe: no schemas were expanded, no source adapter or scorer behavior was added, and no private runtime, database, hosted operation, or evidence lookup moved here.

## Guarded Fields

| Contract | Fields | Public rule |
| --- | --- | --- |
| `CapabilityFingerprintInput` | `id_scheme`, `canonical_id`, `entity_kind` | Non-empty strings only. |
| `RawEntry` | `source`, `source_id`, `entity_kind`, `canonical_id`, `fetched_at` | Non-empty strings only. |
| `EvidenceItem` | `evidence_id`, `source`, `observed_at`, `summary` | Non-empty strings only. |
| `EvidenceSet` | `request_id`, `use_case`, `generated_at` | Non-empty strings only. |
| `CandidateSet` | `request_id`, `use_case`, `generated_at` | Non-empty strings only. |
| `TheCall` | `reason`, `abstention_reason` | Non-empty strings only when required by the public decision shape. |

## Verification

- Red: targeted `tests.test_core_contracts` methods failed on the new truthy non-string regressions.
- Green: targeted `tests.test_core_contracts` methods passed after replacing local truthiness checks with `_require_nonempty_string`.
- Full local gate: `make check` passed with the public boundary scan and 131 unit tests.
