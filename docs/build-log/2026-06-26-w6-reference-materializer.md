# W6 Public Reference Materializer

Date: 2026-06-26

Scope: public-safe core runtime only.

## Built

- Added `evalrank_core.materializer.materialize_recommendation(...)`.
- Reused existing public contracts instead of adding a parallel response shape: `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceSet`, `ResultRow`, `Exclusion`, `RankedEntity`, `TheCall`, `Abstention`, and `Recommendation`.
- Added deterministic Stage-1 ordering: descending `fused_score`, then stable `candidate_id` tie-breaks.
- Added public `materialized-cache` output behavior through the existing `Recommendation.served_from` field.
- Added public abstention behavior when no non-excluded candidate has public evidence or result rows.
- Added boundary validation for request IDs, use cases, candidate references, evidence subjects, result-row subjects, exclusions, and duplicate Stage-1 rows.
- Documented the public materializer boundary in `packages/core/README.md`.
- Added the materializer test map entry in `TESTS.md`.

## Boundary

- This is a storage-free reference materializer over caller-supplied public inputs.
- It does not add DB persistence, source adapters, network calls, private scorer weights, confidence thresholds, calibration, telemetry, hosted route execution, private evidence-graph lookup, or held-out benchmark material.
- Real W6 proof-of-spine still belongs in Syndai: one cached ranking emitted from the private evidence graph/cache path.

## Verification

- Red test: `python3 -m unittest tests.test_core_materializer` failed before implementation because `evalrank_core.materializer` did not exist.
- Green focused test: `python3 -m unittest tests.test_core_materializer` passed with 3 tests after implementation.
- Focused core contract drift check: `python3 -m unittest tests.test_core_contracts` passed with 52 tests.
- Focused repo-doc drift check: `python3 -m unittest tests.test_repo_docs` passed with 9 tests.
- Full Python suite: `python3 -m unittest discover tests` passed with 223 tests.
- Whitespace check: `git diff --check` passed.
- Default local gate: `make check` passed: public boundary scanner, 223 Python tests, TypeScript syntax check, and 7 TypeScript runtime tests.
