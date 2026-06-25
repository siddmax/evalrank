# Entity Evidence Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add public, storage-free entity and evidence contracts that can anchor later evidence graph work.

**Architecture:** Keep the contract in `evalrank_core.contracts` beside the existing recommendation contracts. Mirror the payload in JSON Schema and public fixtures. Do not add database migrations, private fixtures, or scoring engine behavior.

**Tech Stack:** Python dataclasses, stdlib `unittest`, JSON Schema draft 2020-12.

---

### Task 1: Core Entity And Evidence Contracts

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Test: `tests/test_core_contracts.py`
- Test: `tests/test_core_fixtures.py`

- [x] **Step 1: Add failing tests for entity/evidence payloads**

```python
def test_evidence_item_serializes_public_subject_and_score():
    item = EvidenceItem(...)
    assert item.to_dict()["subject"]["id"] == "tool:public-search-demo"
```

Run: `python3 -m unittest tests.test_core_contracts`
Expected: FAIL because `EvidenceItem` and `EntityRef` are not defined.

- [x] **Step 2: Implement minimal dataclasses**

Add `EntityRef` and `EvidenceItem` to `contracts.py`. Validate required IDs, allowed evidence kinds, non-empty source/timestamps, and optional `score` in `[0, 1]`.

- [x] **Step 3: Export and fixture the contracts**

Export both classes from `evalrank_core.__init__`. Add `sample_entity_ref()` and `sample_evidence_item()` to `fixtures.py`.

- [x] **Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures`
Expected: PASS.

### Task 2: Public Evidence Schema

**Files:**
- Create: `schemas/evidence-item.schema.json`
- Modify: `schemas/README.md`
- Modify: `tests/test_schema_contracts.py`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`

- [x] **Step 1: Add failing schema drift tests**

Assert `sample_evidence_item().to_dict()` keys match `evidence-item.schema.json`, and schema enums match core constants.

Run: `python3 -m unittest tests.test_schema_contracts`
Expected: FAIL because the schema file does not exist.

- [x] **Step 2: Add schema and docs**

Create `schemas/evidence-item.schema.json` with strict top-level properties for `evidence_id`, `subject`, `kind`, `source`, `observed_at`, `summary`, `score`, and `metadata`.

- [x] **Step 3: Run full check**

Run: `make check`
Expected: PASS.

### Self-Review

- Spec coverage: Covers public data-plane contracts and entity/evidence graph entry point without storage or private data.
- Placeholder scan: No placeholders remain.
- Type consistency: `EntityRef`, `EvidenceItem`, and schema property names match across tests, fixtures, and docs.
