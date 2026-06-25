# Methodology Version Format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce the pinned public `methodology_version` format `YYYY-MM-DD.SEQ.slug` everywhere current public fixtures emit it.

**Architecture:** Validate the format once in `evalrank_core.contracts`, because every public surface routes through core fixtures/contracts. Mirror the same anchored pattern in JSON Schemas and update public fixture values plus docs.

**Tech Stack:** Python stdlib `re`, dataclasses, JSON Schema draft 2020-12, stdlib `unittest`.

---

### Task 1: Pin Methodology Version Format

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `schemas/ranked-entity.schema.json`
- Modify: `schemas/recommendation.schema.json`
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `tests/test_schema_contracts.py`
- Modify: docs/status/build-log files as needed

- [x] **Step 1: Write failing contract tests**

Add tests that assert `RankedEntity` and `Recommendation.single_scale()` accept `2026-06-25.1.public-fixture-v1` and reject the old `2026.06.1` format.

- [x] **Step 2: Run focused tests to verify red**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts
```

Expected: fail because the old fixture still emits `2026.06.1` and core does not enforce the pinned format.

- [x] **Step 3: Add minimal core validation**

Use one compiled stdlib regex and one helper in `contracts.py`; call it from `RankedEntity.__post_init__` and `Recommendation.__post_init__`.

- [x] **Step 4: Update fixture and schema patterns**

Change `PUBLIC_METHODOLOGY_VERSION` to `2026-06-25.1.public-fixture-v1`. Add the same anchored pattern to public schemas that expose `methodology_version`.

- [x] **Step 5: Verify**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts
make check
```

Expected: all pass.

---

## Self-Review

- Spec coverage: Covers the W0-pinned public `methodology_version` shape without adding storage, migrations, APIs, or private data.
- Placeholder scan: No placeholders.
- Type consistency: Uses the existing `methodology_version` field name across core and schemas.
