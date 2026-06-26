# Tuple Sequence Contract Hardening Plan

Date: 2026-06-26

## Goal

Make the Python core reject mutable list-backed sequence inputs for existing public `CandidateSet` and `EvidenceSet` contracts.

## Steps

1. Require tuple-backed inputs for `CandidateSet.candidates`.
2. Require tuple-backed inputs for `EvidenceSet.evidence_items` while preserving valid empty evidence sets.
3. Add focused core regressions for list inputs.
4. Update public status, porting, and test docs.
5. Run local checks and pre-landing review before direct `main` push.

## Public Boundary

- Safe: immutability hardening for already-public storage-free contracts.
- Excluded: live candidate resolution, graph lookup, evidence lookup, source adapters, scorer runtime, persistence, telemetry, private rows, and held-out eval material.
