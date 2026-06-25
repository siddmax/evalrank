# Evaluation Request Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a public, storage-free `EvaluationRequest` payload that can anchor future request normalization and non-fixture API/CLI/MCP behavior.

**Architecture:** Keep the request contract beside the existing core dataclasses. Mirror it in JSON Schema, public fixtures, SDK exports, CLI/MCP fixture adapters, and TypeScript public types. Do not add REST routes, database migrations, auth, live scoring, or private data access.

**Tech Stack:** Python dataclasses, stdlib `unittest`, JSON Schema draft 2020-12, checked TypeScript source.

---

### Task 1: Core Request Contract And Schema

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Create: `schemas/evaluation-request.schema.json`
- Modify: `schemas/README.md`
- Test: `tests/test_core_contracts.py`
- Test: `tests/test_core_fixtures.py`
- Test: `tests/test_schema_contracts.py`

- [x] **Step 1: Write failing core and schema tests**

Add tests that construct `EvaluationRequest(request_id="req_public_fixture_01", use_case="web-browsing", entity_types=("mcp_server",), requested_at="2026-06-25T00:00:00Z", constraints={"region": "public"})`, assert `to_dict()` emits `object`, `request_id`, `use_case`, `entity_types`, `requested_at`, and sorted `constraints`, and assert blank `request_id`, blank `use_case`, empty `entity_types`, or non-string constraint keys are rejected.

Add schema drift checks for `evaluation-request.schema.json` and enum/key parity.

- [x] **Step 2: Run failing tests**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts
```

Expected: FAIL because `EvaluationRequest`, `sample_evaluation_request`, and `schemas/evaluation-request.schema.json` do not exist.

- [x] **Step 3: Implement minimal contract and schema**

Add frozen `EvaluationRequest` with fields `request_id`, `use_case`, `entity_types`, `requested_at`, and `constraints`. Export it and add `sample_evaluation_request()`. Add the matching strict JSON Schema.

- [x] **Step 4: Run focused tests**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts
```

Expected: PASS.

### Task 2: Existing Public Surfaces

**Files:**
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`
- Test: `tests/test_sdk_python.py`
- Test: `tests/test_cli_fixture.py`
- Test: `tests/test_mcp_fixture.py`
- Test: `tests/test_sdk_ts.py`

- [x] **Step 1: Write failing surface tests**

Assert Python SDK re-exports `EvaluationRequest` and `sample_evaluation_request`, CLI supports `fixture request`, MCP `evalrank.fixture` supports `{"kind": "request"}`, and TypeScript exports `EvaluationRequest`.

- [x] **Step 2: Run failing surface tests**

Run:

```sh
python3 -m unittest tests.test_sdk_python tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_ts
```

Expected: FAIL because the surfaces do not expose the request fixture.

- [x] **Step 3: Expose the request fixture**

Wire the new fixture into the Python SDK, CLI fixture map, MCP fixture map, and TypeScript interface.

- [x] **Step 4: Run focused surface tests**

Run:

```sh
python3 -m unittest tests.test_sdk_python tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```

Expected: PASS.

### Task 3: Docs And Verification

**Files:**
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: `packages/core/README.md`
- Modify: `schemas/README.md`
- Create: `docs/build-log/2026-06-25-evaluation-request-contract.md`

- [x] **Step 1: Update docs**

Document the request fixture and public boundary. Keep private DB/API/hosted work explicitly out of scope.

- [x] **Step 2: Run full checks**

Run:

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: PASS.

### Self-Review

- Spec coverage: Covers a public input-side contract without adding route, storage, auth, or scorer behavior.
- Placeholder scan: No placeholders remain.
- Type consistency: `EvaluationRequest`, `evaluation-request.schema.json`, `sample_evaluation_request`, CLI/MCP `request`, and TypeScript `EvaluationRequest` names match.
