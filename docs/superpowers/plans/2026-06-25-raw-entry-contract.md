# Raw Entry Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the public storage-free `RawEntry` ingestion-normalization contract.

**Architecture:** Keep `RawEntry` in `evalrank_core.contracts` beside the other public dataclasses. Generate `content_hash` with stdlib SHA256 over normalized content identity fields, excluding `content_hash` and fetch-time metadata. Mirror the payload in JSON Schema and expose only synthetic fixture surfaces through SDK, CLI, and MCP.

**Tech Stack:** Python dataclasses and stdlib `unittest`; JSON Schema draft 2020-12; TypeScript interfaces.

---

### Task 1: Pin RawEntry Core Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`

- [x] **Step 1: Write failing tests**

Add tests that `RawEntry.to_dict()` emits:

```python
{
    "object": "raw_entry",
    "source": "public-fixture",
    "source_id": "public-fixture:search-demo:2026-06-25",
    "entity_kind": "mcp_server",
    "canonical_id": "io.evalrank.public-search-demo",
    "raw_metadata": {"homepage": "https://example.com/evalrank/public-search-demo"},
    "declared_capability_shape": {"tool_names": ["search"]},
    "fetched_at": "2026-06-25T00:00:00Z",
    "content_hash": "<64 hex chars>",
}
```

Assert that hash output is stable when `raw_metadata` and `declared_capability_shape` key order or `fetched_at` changes, and that non-string keys, non-JSON values, or missing capability shape raise `ValueError`.

- [x] **Step 2: Run tests to verify they fail**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: import/name failures for missing `RawEntry` and `sample_raw_entry`.

- [x] **Step 3: Implement minimal core contract**

Add `RawEntry` with required string fields, JSON object validation via the existing `_normalize_json_object()` helper, a `content_hash` property, and sorted `to_dict()` nested objects. Add `sample_raw_entry()` and export both names.

- [x] **Step 4: Run focused core checks**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
```

Expected: pass.

### Task 2: Mirror Public Surfaces

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_cli_fixture.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Create: `schemas/raw-entry.schema.json`
- Modify: `schemas/README.md`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing surface tests**

Add assertions that:

- `raw-entry.schema.json` covers the same keys as `sample_raw_entry().to_dict()`.
- CLI supports `fixture raw-entry`.
- MCP `kind` enum includes `raw-entry` and returns the fixture.
- Python SDK re-exports `RawEntry` and `sample_raw_entry`.
- TypeScript SDK contains `export interface RawEntry` and every payload field.

- [x] **Step 2: Run tests to verify they fail**

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts
```

Expected: failures for missing schema, fixture kind, SDK exports, and TS interface.

- [x] **Step 3: Implement minimal public surfaces**

Add `raw-entry.schema.json` as a closed draft 2020-12 object. Add `raw-entry` fixture handling to CLI/MCP. Re-export the Python names and add the TypeScript interface.

- [x] **Step 4: Run focused surface checks**

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```

Expected: pass.

### Task 3: Document And Ship

**Files:**
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `packages/core/README.md`
- Modify: `packages/cli/README.md`
- Modify: `packages/mcp/README.md`
- Modify: `packages/sdk-python/README.md`
- Modify: `packages/sdk-ts/README.md`
- Modify: `schemas/README.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-25-raw-entry-contract.md`

- [x] **Step 1: Update public docs**

Move `RawEntry` from next candidate to built public contract. State that source adapters, production metadata, live fetch behavior, DB persistence, and private evidence rows stay private.

- [x] **Step 2: Run full checks**

Run:

```sh
make check
npm run check --prefix packages/sdk-ts
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture raw-entry
```

Expected: pass and fixture JSON includes `object: "raw_entry"` plus a 64-character `content_hash`.

- [x] **Step 3: Review, commit, push**

Run the pre-push review gate, commit the scoped files, push directly to `main`, then verify GitHub `public-boundary` succeeds.

## GSTACK REVIEW REPORT

Plan review: PASS. Existing contract helpers cover the needed JSON normalization and hashing shape. The plan intentionally skips adapters, persistence, OpenAPI, source-specific metadata, and runtime ingestion because the current public repo only needs a storage-free payload contract.

NO UNRESOLVED DECISIONS
