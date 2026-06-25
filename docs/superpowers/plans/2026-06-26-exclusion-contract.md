# Exclusion Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin a storage-free public `Exclusion` row for candidates that are intentionally left out of ranked results.

**Architecture:** Add one frozen core dataclass beside `EntityRef`/`EvidenceItem`, then make `Recommendation.exclusions` serialize only `Exclusion.to_dict()` rows. Mirror the row in JSON Schema and deterministic fixture surfaces. Do not add gate policy, scorer behavior, source adapters, storage, telemetry, hosted auth, or private reason taxonomy.

**Tech Stack:** Python stdlib dataclasses, JSON Schema draft 2020-12, TypeScript source types, stdlib `unittest`.

---

### Task 1: Core Exclusion Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Write failing core and fixture tests**

Add tests that construct:

```python
Exclusion(
    subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
    reason="unknown_cost",
    detail="cost is unknown for this public fixture",
)
```

Assert `to_dict()` emits `subject`, `reason`, and `detail`. Assert blank `reason`, blank `detail`, and non-`EntityRef` subjects are rejected. Add a recommendation test that passes `exclusions=[exclusion]` and asserts serialized exclusions are a list of exclusion dicts.

- [x] **Step 2: Run red core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: fail because `Exclusion` and `sample_exclusion()` do not exist.

- [x] **Step 3: Implement minimal core contract**

Add frozen `Exclusion` with fields `subject`, `reason`, and `detail`. Validate subject type and required strings. Change `Recommendation.exclusions` and `single_scale(..., exclusions=...)` to accept `list[Exclusion]` and serialize with `to_dict()`.

- [x] **Step 4: Run focused core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: pass.

### Task 2: Schema And SDK Mirrors

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Create: `schemas/exclusion.schema.json`
- Modify: `schemas/recommendation.schema.json`
- Modify: `schemas/README.md`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing schema and SDK tests**

Require `exclusion.schema.json` to mirror `Exclusion.to_dict()`, use draft 2020-12, be a closed object, and be referenced by `recommendation.schema.json` for `exclusions.items`. Require Python and TypeScript SDK surfaces to expose `Exclusion`.

- [x] **Step 2: Run red schema and SDK tests**

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
```

Expected: fail because the schema, recommendation ref, and SDK exports do not exist.

- [x] **Step 3: Add minimal schema and SDK exports**

Create a closed exclusion schema with `subject`, `reason`, and `detail`; point `Recommendation.exclusions.items` at it; add Python SDK re-export and TypeScript `Exclusion` interface.

- [x] **Step 4: Run focused schema and SDK tests**

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```

Expected: pass.

### Task 3: Fixture Adapters And Docs

**Files:**
- Modify: `tests/test_cli_fixture.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: package READMEs as needed
- Create: `docs/build-log/2026-06-26-exclusion-contract.md`

- [x] **Step 1: Write failing CLI and MCP tests**

Require `evalrank fixture exclusion` and `evalrank.fixture` with `kind="exclusion"` to return the deterministic public exclusion fixture.

- [x] **Step 2: Run red CLI and MCP tests**

```sh
python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture
```

Expected: fail because `exclusion` is not an allowed fixture kind.

- [x] **Step 3: Add minimal fixture adapter support and docs**

Wire `sample_exclusion().to_dict()` into the existing CLI/MCP fixture switches and update public docs/status/porting/build-log. Keep live gates, policy rules, reason taxonomy, and storage out of scope.

- [x] **Step 4: Run full checks, review, commit, push**

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: pass. Then run public boundary/secret scan, gstack review, Ponytail review, commit, push directly to `main`, and verify the matching CI run.

## Self-Review

- Spec coverage: Covers public exclusions-with-reasons without adding Stage-0 gate policy, scorer runtime, private safety taxonomy, or persistence.
- Placeholder scan: No placeholders.
- Type consistency: `Exclusion`, `exclusion.schema.json`, `sample_exclusion`, fixture kind `exclusion`, and `Recommendation.exclusions` are consistent.

## GSTACK REVIEW REPORT

Plan review: PASS. This is the smallest durable public shape for exclusions-with-reasons: a subject plus public reason/detail, reused inside recommendations.

NO UNRESOLVED DECISIONS
