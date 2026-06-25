# Recommendation Envelope Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Python `Recommendation` contract reject payloads that violate the already-public recommendation JSON Schema.

**Architecture:** Keep validation in `Recommendation.__post_init__`, matching the existing core-contract pattern. Do not add scorer logic, storage behavior, route behavior, private IDs, or new dependencies.

**Tech Stack:** Python dataclasses, `unittest`, local JSON Schema docs, existing `make check`.

---

### Task 1: Recommendation Envelope Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: `TESTS.md`
- Create: `docs/build-log/2026-06-26-recommendation-envelope-contract-hardening.md`

- [x] **Step 1: Write failing tests**

Add regression coverage proving that `Recommendation` rejects schema-incompatible envelope values before serialization:

```python
with self.assertRaisesRegex(ValueError, "degraded"):
    Recommendation(..., degraded="false")
```

Also reject duplicate ranked entities in a single-scale recommendation:

```python
with self.assertRaisesRegex(ValueError, "duplicate ranked entity"):
    Recommendation.single_scale(..., ranked=[row, row], ...)
```

- [x] **Step 2: Verify tests fail**

Run:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_schema_incompatible_envelope_fields tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_duplicate_ranked_entities
```

Expected before implementation: failures because `ValueError` is not raised.

- [x] **Step 3: Implement minimal validation**

In `Recommendation.__post_init__`, validate:

```python
shortlist_depth: int >= 0 and not bool
depth_rationale: non-empty string
degraded: bool
served_from: non-empty string
base_snapshot_lag_ms: int >= 0 and not bool
ranked rows: RankedEntity instances, envelope methodology, no duplicate (entity_type, entity_id)
```

- [x] **Step 4: Verify focused green**

Run the same focused `unittest` command and expect `OK`.

- [x] **Step 5: Update docs and full checks**

Update status/porting/test docs and add a dated build log. Then run:

```sh
python3 -m unittest tests.test_core_contracts
python3 scripts/check_public_boundary.py --root .
make check
git diff --check
```
