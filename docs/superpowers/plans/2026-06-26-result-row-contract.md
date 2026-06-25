# Result Row Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin the public storage-free ingested result-row envelope.

**Architecture:** Add one `ResultRow` contract that captures source provenance, score units, confidence interval, public flags, and verification state. Mirror it through schema, synthetic fixtures, CLI/MCP fixture output, TypeScript types, and docs. Do not add persistence, scorer math, source adapters, or production result data.

**Tech Stack:** Python dataclasses, JSON Schema 2020-12, stdlib `unittest`, TypeScript type declarations.

---

### Task 1: Pin Contract Tests

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_cli_fixture.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`

- [x] Add failing tests for `ResultRow.to_dict()`, validation, fixture output, schema shape, Python SDK export, TypeScript interface/constants, CLI `fixture result-row`, and MCP `result-row`.
- [x] Run `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts`.
- [x] Confirm failures are missing `ResultRow`, `result-row.schema.json`, fixture kind, and SDK type exports.

### Task 2: Implement Minimal Contract

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Create: `schemas/result-row.schema.json`

- [x] Add `RESULT_ENTITY_KINDS`, `RESULT_VERIFICATION_STATES`, `RESULT_FLAG_KEYS`, and `ResultRow`.
- [x] Add `sample_result_row()` and expose it through Python SDK, CLI, MCP, and TypeScript.
- [x] Add `result-row.schema.json` with exact public fields and no additional properties.
- [x] Run the focused test command from Task 1 and keep it green.

### Task 3: Update Public Docs

**Files:**
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: `schemas/README.md`
- Modify: package READMEs as needed
- Create: `docs/build-log/2026-06-26-result-row-contract.md`

- [x] Mark `ResultRow` as public and storage-free.
- [x] State that source adapters, live result data, evidence ledger persistence, private benchmark rows, and scorer runtime stay private.
- [x] Run `make check`, TypeScript syntax check, public-boundary check, and review before pushing.

## GSTACK REVIEW REPORT

Plan review: PASS. The slice reuses the repo's existing contract propagation pattern and adds no new dependency, runtime, database object, source adapter, or private data. The only public addition is the storage-free result-row envelope required by the methodology docs.
