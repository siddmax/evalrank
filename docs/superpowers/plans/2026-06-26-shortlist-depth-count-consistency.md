# Shortlist Depth Count Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reject direct `Recommendation(...)` payloads whose `shortlist_depth` disagrees with the public ranked rows.

**Architecture:** Keep the fix in the shared Python `Recommendation` constructor because all public fixture factories and SDK-facing payloads route through that contract. Do not add JSON Schema tricks for array-length arithmetic; schema stays a structural contract and Python owns the derived count invariant.

**Tech Stack:** Python stdlib dataclasses and `unittest`.

---

### Task 1: Pin Core Count Consistency

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-shortlist-depth-count-consistency.md`

- [x] **Step 1: Write the failing test**

Add `test_recommendation_rejects_shortlist_depth_count_drift` to `tests/test_core_contracts.py` with one bad single-scale payload and one bad kind-grouped payload.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_shortlist_depth_count_drift
```

Expected: fail because the constructor currently accepts mismatched `shortlist_depth`.

- [x] **Step 3: Implement the shared validation**

In `Recommendation.__post_init__`, reject `shortlist_depth != len(ranked)` for `single-scale` non-abstentions and `shortlist_depth != sum(len(group.ranked) for group in groups)` for `kind-grouped` responses.

- [x] **Step 4: Verify green**

Run:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_shortlist_depth_count_drift
make check
```

Expected: focused test and full gate pass.

- [x] **Step 5: Update public docs**

Record the public core invariant in `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and the dated build log. Keep private scorer thresholds, runtime, persistence, source adapters, and hosted behavior out.

## Self-Review

- Spec coverage: one regression, one constructor validation, docs/build log.
- Placeholder scan: no TBD/TODO placeholders.
- Type consistency: uses existing `Recommendation.shortlist_depth`, `ranked`, and `groups` fields.
