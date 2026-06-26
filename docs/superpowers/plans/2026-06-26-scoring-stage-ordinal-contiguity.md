# Scoring Stage Ordinal Contiguity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reject public scoring-stage catalogs whose ordinals skip stages.

**Architecture:** Keep the invariant in `ScoringStageCatalog.__post_init__`, where duplicate IDs and duplicate ordinals are already checked. Do not add JSON Schema workarounds for semantic sequence arithmetic; schema remains structural and the Python reference contract owns contiguous ordering.

**Tech Stack:** Python stdlib dataclasses and `unittest`.

---

### Task 1: Pin Contiguous Stage Ordinals

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-scoring-stage-ordinal-contiguity.md`

- [x] **Step 1: Write the failing test**

Add `test_scoring_stage_catalog_rejects_gapped_ordinals` to `tests/test_core_contracts.py` with stages numbered `1` and `3`; also pin the missing-initial-ordinal case so catalogs start at `1`.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_rejects_gapped_ordinals
```

Expected: fail because `ScoringStageCatalog` currently accepts unique but non-contiguous ordinals.

- [x] **Step 3: Implement shared validation**

In `ScoringStageCatalog.__post_init__`, after collecting ordinals, reject when `seen_ordinals != set(range(1, len(self.stages) + 1))`.

- [x] **Step 4: Verify green**

Run:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_rejects_gapped_ordinals tests.test_core_contracts.CoreContractTests.test_scoring_stage_catalog_serializes_public_stage_vocabulary
make check
```

Expected: focused tests and full gate pass.

- [x] **Step 5: Update public docs**

Record the public core invariant in `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and the dated build log. Keep private scorer stages, formulas, runtime, persistence, source adapters, and hosted behavior out.

## Self-Review

- Spec coverage: one regression, one constructor validation, docs/build log.
- Placeholder scan: no TBD/TODO placeholders.
- Type consistency: uses existing `ScoringStageCatalog.stages` and `ScoringStage.ordinal`.
