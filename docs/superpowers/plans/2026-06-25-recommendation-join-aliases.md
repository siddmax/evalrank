# Recommendation Join Aliases Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expose `recommend_id` and `search_run_id` as public recommendation payload aliases for `recommendation_id`.

**Architecture:** Keep `Recommendation.recommendation_id` as the only generated value. Serialize `recommend_id` and `search_run_id` as exact aliases in `to_dict()` so fixtures, CLI, MCP, SDK, and schemas share one ID without introducing hosted HMAC or receipt behavior.

**Tech Stack:** Python dataclasses and stdlib `unittest`; JSON Schema draft 2020-12; TypeScript interfaces.

---

### Task 1: Pin Alias Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `schemas/recommendation.schema.json`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing tests**

Add assertions that a recommendation payload includes `recommend_id` and `search_run_id`, and both equal `recommendation_id`.

Add schema assertions that both alias fields use the same `^rec_[0-9a-f]{24}$` pattern.

Add TypeScript SDK source assertions that both fields exist on `Recommendation`.

- [x] **Step 2: Run tests to verify they fail**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_schema_contracts tests.test_sdk_ts
```

Expected: failures for missing alias fields.

- [x] **Step 3: Implement minimal aliases**

In `Recommendation.to_dict()`, compute `recommendation_id` once and assign:

```python
payload["recommendation_id"] = recommendation_id
payload["recommend_id"] = recommendation_id
payload["search_run_id"] = recommendation_id
```

Add the two schema properties and required fields with the same pattern as `recommendation_id`.

Add the two fields to the TypeScript `Recommendation` interface.

- [x] **Step 4: Run focused checks**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_schema_contracts tests.test_sdk_ts
```

Expected: pass.

### Task 2: Document And Ship

**Files:**
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: `TESTS.md`
- Create: `docs/build-log/2026-06-25-recommendation-join-aliases.md`

- [x] **Step 1: Update public docs**

Move recommendation join aliases from `Next` to `Built`, keep hosted HMAC/receipt work private/deferred, and add a dated build log.

- [x] **Step 2: Run full checks**

Run:

```sh
make check
npm run check --prefix packages/sdk-ts
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture recommendation
```

Expected: pass and fixture JSON includes all three IDs with the same value.

- [x] **Step 3: Review, commit, push**

Run the gstack pre-push review gate, commit the scoped files, push directly to `main`, then verify GitHub `public-boundary` succeeds.

## GSTACK REVIEW REPORT

Plan review: PASS. The smallest durable implementation is alias serialization on the existing recommendation payload. New hosted receipt/HMAC behavior is explicitly out of scope for this public repo slice.
