# W6 Public Reference Materializer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a public-safe reference materializer that proves the storage-free W6 spine: `EvaluationRequest -> CandidateSet/StageCandidate -> EvidenceSet/ResultRow/Exclusion -> Recommendation or Abstention`.

**Architecture:** Add a dependency-free `evalrank_core.materializer` module that validates the request/candidate/evidence/result boundary, ranks existing `StageCandidate` rows deterministically, emits existing `Recommendation` envelopes with `served_from="materialized-cache"`, and abstains when public evidence is insufficient. The public module exposes only portable contracts and deterministic behavior; runtime persistence and hosted operation are maintained in a separate private system, so DB persistence, source adapters, scorer weights, thresholds, telemetry, and live evidence-graph materialization stay out of this public package.

**Tech Stack:** Python stdlib, frozen dataclass contracts already in `evalrank_core.contracts`, and stdlib `unittest`.

---

### Task 1: Pin Public W6 Behavior With BDD Tests

**Files:**
- Add: `tests/test_core_materializer.py`

- [x] **Step 1: Test deterministic materialized-cache recommendation output**

Build a public fixture with multiple candidates, evidence rows, and result rows. Assert the materializer returns a usable single-scale `Recommendation`, ranks by Stage-1 score with deterministic tie-breaks, stamps the methodology version, exposes `served_from="materialized-cache"`, carries evidence counts/components, and produces the same `recommendation_id` on repeated calls.

- [x] **Step 2: Test public abstention behavior**

Assert the materializer returns an empty single-scale abstention when no public evidence survives for the request.

- [x] **Step 3: Test boundary validation**

Assert mismatched request IDs, use cases, candidate refs, and unsupported result entity kinds fail before serialization.

### Task 2: Implement The Reference Materializer

**Files:**
- Add: `packages/core/src/evalrank_core/materializer.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Add a pure function over public contracts**

Implement `materialize_recommendation(...)` with explicit public contract inputs. Do not add persistence, source lookup, private scorer policy, network calls, or new dependencies.

- [x] **Step 2: Keep scoring public and replaceable**

Use Stage-1 fused score as the ordering source and expose simple public component values for explanation only. Keep private weights, confidence thresholds, calibration, CI tuning, and held-out benchmark assumptions out of the public package.

- [x] **Step 3: Export the materializer API**

Re-export the public function from `evalrank_core.__init__` so SDKs and examples can import it without depending on private modules.

### Task 3: Document The Public Surface

**Files:**
- Modify: `packages/core/README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Add: `docs/build-log/2026-06-26-w6-reference-materializer.md`

- [x] **Step 1: Document the public materializer boundary**

Add a short core README note that the reference materializer emits deterministic public recommendations only from provided inputs, and that runtime persistence and hosted operation are maintained in a separate private system.

- [x] **Step 2: Update test/status docs**

Add the materializer tests to `TESTS.md`, update W6 status honestly, and add a build log entry for the completed public slice.

### Task 4: Verify

- [x] **Step 1: Run red/green focused tests**

Run `python3 -m unittest tests.test_core_materializer` before and after implementation.

- [x] **Step 2: Run docs and full checks**

Run `python3 -m unittest tests.test_repo_docs`, `python3 -m unittest discover tests`, `make check`, and `git diff --check`.
