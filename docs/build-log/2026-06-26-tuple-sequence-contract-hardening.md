# Tuple Sequence Contract Hardening

Date: 2026-06-26

## What Changed

- Hardened `CandidateSet.candidates` so the Python core rejects mutable list-backed inputs before serialization.
- Hardened `EvidenceSet.evidence_items` so the Python core rejects mutable list-backed inputs while still allowing empty tuple-backed evidence sets for no-evidence or abstention paths.
- Added focused regressions for both list-input cases in `tests/test_core_contracts.py`.
- Updated the public status, porting, and test docs to route this as public contract hardening.

## Public Boundary

- JSON serialization still emits public arrays.
- No private candidate resolver, graph lookup, evidence lookup, source adapter, scorer runtime, DB migration, telemetry, production row, or held-out evaluation material moved into this repo.

## Verification

- `python3 -m unittest tests.test_core_contracts`
- `python3 scripts/check_public_boundary.py --root .`
- `python3 -m unittest discover tests`
- `make check`
