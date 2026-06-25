# Use Case Catalog Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the public storage-free use-case taxonomy contract and fixture surfaces.

**Architecture:** Keep this as metadata, not runtime. The public repo gets only a finite catalog contract, schema, fixture, SDK/CLI/MCP parity, and a contract-only OpenAPI route for `GET /v1/use-cases`. Benchmark weights, IRT clusters, thin-coverage policy, synthesis rules, DB tables, and hosted behavior stay private.

**Tech Stack:** Python dataclasses, stdlib `unittest`, JSON Schema 2020-12, OpenAPI 3.1.1, TypeScript type declarations.

---

### Task 1: Tests First

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_cli_fixture.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `tests/test_openapi_contract.py`

- [x] Add failing tests for `UseCase`, `UseCaseCatalog`, constants, sample catalog count, schema shape, fixture kind `use-cases`, SDK re-exports/types, and `GET /v1/use-cases`.
- [x] Run `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts tests.test_openapi_contract` and confirm failures are for missing public catalog surfaces.

### Task 2: Minimal Contract Surface

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`

- [x] Add `USE_CASE_ENTITY_KINDS`, `USE_CASE_RANK_POLICIES`, `UseCase`, and `UseCaseCatalog`.
- [x] Add `sample_use_case_catalog()` with 21 ranked use cases plus the safety overlay.
- [x] Add fixture kind `use-cases` to CLI and MCP.
- [x] Mirror the public types and constants in the TypeScript SDK.

### Task 3: Schema, Route, And Docs

**Files:**
- Create: `schemas/use-case-catalog.schema.json`
- Modify: `schemas/openapi.json`
- Modify: `schemas/README.md`
- Modify: `README.md`
- Modify: `NAVIGATION.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-use-case-catalog-contract.md`

- [x] Add a closed JSON Schema for the catalog and nested use-case rows.
- [x] Add `GET /v1/use-cases` as a contract-only OpenAPI path with no live server/auth/persistence claims.
- [x] Update docs to mark the catalog contract as built and keep weights/runtime/private eval material out.

### Task 4: Verify And Ship

- [x] Run the focused unittest command from Task 1.
- [x] Run `npm run check --prefix packages/sdk-ts`.
- [x] Run `make check`.
- [x] Run gstack pre-landing review.
- [x] Commit and push directly to `main`; verify the GitHub Actions run for the pushed SHA.

## GSTACK REVIEW REPORT

PASS. The plan keeps the public slice storage-free and avoids DB, runtime scorer, benchmark weights, IRT crosswalk, and held-out material. Main risk is enum drift across Python, JSON Schema, TypeScript, CLI, MCP, and OpenAPI; Task 1 pins that with focused tests before implementation.

Pre-landing review found and fixed one schema parity gap: the JSON Schema now encodes the same overlay/rank-policy constraint that the Python `UseCase` validator enforces.
