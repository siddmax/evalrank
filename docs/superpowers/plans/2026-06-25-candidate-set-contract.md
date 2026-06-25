# Candidate Set Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin a storage-free public `CandidateSet` payload that connects an `EvaluationRequest` to the public `EntityRef` candidates eligible for scoring.

**Architecture:** Add one frozen core dataclass in `evalrank_core.contracts`, serialize it with existing `EntityRef.to_dict()`, and mirror it in JSON Schema plus the existing synthetic fixture surfaces. Do not add source adapters, retrieval, scorer runtime, graph persistence, private entity rows, or hosted receipt behavior.

**Tech Stack:** Python stdlib dataclasses, JSON Schema draft 2020-12, TypeScript source types, stdlib `unittest`.

---

### Task 1: Core Candidate Set Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Write failing core and fixture tests**

Add tests that construct `CandidateSet(request_id="req_public_fixture_01", use_case="web-browsing", candidates=(EntityRef(...),), generated_at="2026-06-25T00:00:00Z")`, assert `to_dict()` emits `object`, `request_id`, `use_case`, `generated_at`, and `candidates`, and assert blank request/use case, empty candidates, non-`EntityRef` candidates, duplicate candidate refs, and blank generated time are rejected.

- [x] **Step 2: Run red core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: fail because `CandidateSet` and `sample_candidate_set()` do not exist.

- [x] **Step 3: Implement minimal core contract**

Add frozen `CandidateSet` with fields `request_id`, `use_case`, `candidates`, and `generated_at`. Validate required strings, require at least one `EntityRef`, reject duplicate `(entity_type, id)` pairs, and serialize candidates as a list of `EntityRef.to_dict()` payloads.

- [x] **Step 4: Run focused core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: pass.

### Task 2: Schema And Public Mirrors

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Create: `schemas/candidate-set.schema.json`
- Modify: `schemas/README.md`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing schema and SDK tests**

Require `candidate-set.schema.json` to mirror `CandidateSet.to_dict()`, use draft 2020-12, be a closed object, require non-empty `candidates`, and expose `CandidateSet` through the Python and TypeScript SDK surfaces.

- [x] **Step 2: Run red schema and SDK tests**

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
```

Expected: fail because the schema and SDK exports do not exist.

- [x] **Step 3: Add minimal schema and SDK exports**

Create a closed candidate-set schema with `object`, `request_id`, `use_case`, `generated_at`, and `candidates`. Add Python SDK re-export and TypeScript `CandidateSet` interface only.

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
- Create: `docs/build-log/2026-06-25-candidate-set-contract.md`

- [x] **Step 1: Write failing CLI and MCP tests**

Require `evalrank fixture candidate-set` and `evalrank.fixture` with `kind="candidate-set"` to return the deterministic public candidate set fixture.

- [x] **Step 2: Run red CLI and MCP tests**

```sh
python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture
```

Expected: fail because `candidate-set` is not an allowed fixture kind.

- [x] **Step 3: Add minimal fixture adapter support and docs**

Wire `sample_candidate_set().to_dict()` into the existing CLI/MCP fixture switch and update public docs/status/porting/build-log. Keep live candidate resolution and source adapters out of scope.

- [x] **Step 4: Run full checks, review, commit, push**

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: pass. Then run public boundary/secret scan, gstack review, Ponytail review, commit, push directly to `main`, and verify the matching CI run.

## Self-Review

- Spec coverage: Covers the public candidate-resolution payload without adding retrieval, scoring, storage, or private data.
- Placeholder scan: No placeholders.
- Type consistency: `CandidateSet`, `candidate-set.schema.json`, `sample_candidate_set`, and fixture kind `candidate-set` are consistent.

## GSTACK REVIEW REPORT

Plan review: PASS. The smallest useful contract is a storage-free candidate list keyed by request; adding live candidate resolution, scorer behavior, or graph persistence would be premature.

NO UNRESOLVED DECISIONS
