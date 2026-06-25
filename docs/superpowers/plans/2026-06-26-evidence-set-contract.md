# Evidence Set Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin a storage-free public `EvidenceSet` payload that groups evidence attached to an evaluation request.

**Architecture:** Add one frozen core dataclass beside `CandidateSet` and serialize existing `EvidenceItem.to_dict()` rows. Mirror it in JSON Schema using a relative `$ref` to `evidence-item.schema.json`, and expose only deterministic fixture surfaces. Do not add evidence lookup, scorer runtime, persistence, telemetry, source adapters, or private evidence rows.

**Tech Stack:** Python stdlib dataclasses, JSON Schema draft 2020-12, TypeScript source types, stdlib `unittest`.

---

### Task 1: Core Evidence Set Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Write failing core and fixture tests**

Add tests that construct `EvidenceSet(request_id="req_public_fixture_01", use_case="web-browsing", evidence_items=(EvidenceItem(...),), generated_at="2026-06-25T00:00:00Z")`, assert `to_dict()` emits `object`, `request_id`, `use_case`, `generated_at`, and `evidence_items`, and assert blank request/use case, non-`EvidenceItem` rows, duplicate `evidence_id`, and blank generated time are rejected. Also assert an empty evidence set is allowed to represent abstention/no-evidence paths.

- [x] **Step 2: Run red core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: fail because `EvidenceSet` and `sample_evidence_set()` do not exist.

- [x] **Step 3: Implement minimal core contract**

Add frozen `EvidenceSet` with fields `request_id`, `use_case`, `evidence_items`, and `generated_at`. Validate required strings, require each row to be an `EvidenceItem`, reject duplicate evidence IDs, and serialize rows with `EvidenceItem.to_dict()`.

- [x] **Step 4: Run focused core tests**

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: pass.

### Task 2: Schema And SDK Mirrors

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Create: `schemas/evidence-set.schema.json`
- Modify: `schemas/README.md`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing schema and SDK tests**

Require `evidence-set.schema.json` to mirror `EvidenceSet.to_dict()`, use draft 2020-12, be a closed object, expose `evidence_items` as an array of `evidence-item.schema.json` references, and expose `EvidenceSet` through Python and TypeScript SDK surfaces.

- [x] **Step 2: Run red schema and SDK tests**

```sh
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
```

Expected: fail because the schema and SDK exports do not exist.

- [x] **Step 3: Add minimal schema and SDK exports**

Create a closed evidence-set schema with `object`, `request_id`, `use_case`, `generated_at`, and `evidence_items`. Add Python SDK re-export and TypeScript `EvidenceSet` interface only.

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
- Create: `docs/build-log/2026-06-26-evidence-set-contract.md`

- [x] **Step 1: Write failing CLI and MCP tests**

Require `evalrank fixture evidence-set` and `evalrank.fixture` with `kind="evidence-set"` to return the deterministic public evidence set fixture.

- [x] **Step 2: Run red CLI and MCP tests**

```sh
python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture
```

Expected: fail because `evidence-set` is not an allowed fixture kind.

- [x] **Step 3: Add minimal fixture adapter support and docs**

Wire `sample_evidence_set().to_dict()` into the existing CLI/MCP fixture switch and update public docs/status/porting/build-log. Keep live evidence lookup and evidence-ledger persistence out of scope.

- [x] **Step 4: Run full checks, review, commit, push**

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: pass. Then run public boundary/secret scan, gstack review, Ponytail review, commit, push directly to `main`, and verify the matching CI run.

## Self-Review

- Spec coverage: Covers the public evidence-attachment payload without adding retrieval, scoring, storage, or private data.
- Placeholder scan: No placeholders.
- Type consistency: `EvidenceSet`, `evidence-set.schema.json`, `sample_evidence_set`, and fixture kind `evidence-set` are consistent.

## GSTACK REVIEW REPORT

Plan review: PASS. The smallest useful evidence-attachment contract is a request-scoped list of existing `EvidenceItem` rows. Live lookup, evidence ledgers, scoring, and storage remain private/deferred.

NO UNRESOLVED DECISIONS
