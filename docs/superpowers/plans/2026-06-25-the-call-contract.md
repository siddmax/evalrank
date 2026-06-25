# The Call Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin the public `the_call` decision-confidence shape embedded in recommendation payloads.

**Architecture:** Add a small `TheCall` dataclass in `evalrank_core.contracts` and serialize it through the existing `Recommendation.the_call` field. Keep it storage-free and public-safe: decision, confidence, reason, and abstention reason only. Mirror the nested shape in the recommendation JSON Schema and SDK types; do not add scorer behavior, private thresholds, routes, adapters, or persistence.

**Tech Stack:** Python dataclasses and stdlib `unittest`; JSON Schema draft 2020-12; TypeScript interfaces.

---

### Task 1: Pin Core TheCall Shape

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Write failing core tests**

Add tests that `TheCall.recommend(confidence=0.86, reason="clear top set").to_dict()` emits:

```python
{
    "decision": "recommend",
    "confidence": 0.86,
    "reason": "clear top set",
    "abstention_reason": None,
}
```

Also assert `TheCall.abstain(reason="insufficient_evidence")` emits `decision: "abstain"`, `confidence: None`, and `abstention_reason: "insufficient_evidence"`. Assert invalid decision, missing recommend confidence, invalid confidence, and blank reason raise `ValueError`.

- [x] **Step 2: Run tests to verify they fail**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: import/name failures for missing `TheCall` and missing fixture behavior.

- [x] **Step 3: Implement minimal core contract**

Add `THE_CALL_DECISIONS = {"recommend", "abstain"}` and frozen `TheCall` with `recommend()`, `abstain()`, validation, and `to_dict()`. Change `Recommendation.the_call` to `TheCall | None`, serialize with `to_dict()`, and make `Recommendation.abstain()` use `TheCall.abstain(reason)`.

- [x] **Step 4: Run focused core checks**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: pass.

### Task 2: Mirror Schema And SDK Surfaces

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `schemas/recommendation.schema.json`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing surface tests**

Add assertions that:

- Recommendation schema `the_call` is either `null` or a closed object with `decision`, `confidence`, `reason`, and `abstention_reason`.
- Schema decision enum matches `THE_CALL_DECISIONS`.
- Python SDK re-exports `TheCall`.
- TypeScript SDK exports `THE_CALL_DECISIONS`, `TheCall`, and `Recommendation.the_call: TheCall | null`.

- [x] **Step 2: Run tests to verify they fail**

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```

Expected: failures for missing schema enum, SDK exports, and TypeScript type.

- [x] **Step 3: Implement minimal public surfaces**

Update the nested recommendation schema, Python SDK re-export, and TypeScript constants/interfaces. Do not add new CLI/MCP fixture kinds.

- [x] **Step 4: Run focused surface checks**

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```

Expected: pass.

### Task 3: Document And Ship

**Files:**
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `packages/core/README.md`
- Modify: `packages/sdk-python/README.md`
- Modify: `packages/sdk-ts/README.md`
- Modify: `schemas/README.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-25-the-call-contract.md`

- [x] **Step 1: Update public docs**

Move structured public `the_call` from next candidate to built public contract. State that scorer thresholds, private confidence tuning, held-out evidence floors, routes, and persistence stay private.

- [x] **Step 2: Run full checks**

Run:

```sh
make check
npm run check --prefix packages/sdk-ts
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture recommendation
```

Expected: pass and recommendation fixture JSON includes structured `the_call`.

- [x] **Step 3: Review, commit, push**

Run the pre-push review gate, commit the scoped files, push directly to `main`, then verify GitHub `public-boundary` succeeds.

## Self-Review

- Spec coverage: Covers the public nested decision-confidence shape without adding scorer behavior, thresholds, routes, adapters, or persistence.
- Placeholder scan: No placeholders.
- Type consistency: Uses `TheCall`, `the_call`, `decision`, `confidence`, `reason`, and `abstention_reason` consistently across core, schema, SDK, tests, and docs.

## GSTACK REVIEW REPORT

Plan review: PASS. The existing recommendation fixture and payload slot are enough public surface for `the_call`; adding a new CLI/MCP fixture kind, route, scorer, threshold config, or persistence layer would be speculative.

NO UNRESOLVED DECISIONS
