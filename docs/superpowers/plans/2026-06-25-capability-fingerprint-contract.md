# Capability Fingerprint Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the public, storage-free `capability_fingerprint` input contract and deterministic SHA256 digest helper.

**Architecture:** Keep the hash input in `evalrank_core.contracts` beside other public contracts. Canonicalize with stdlib JSON sorting and compact separators, then hash UTF-8 bytes with SHA256. Mirror the payload in JSON Schema and expose a synthetic fixture through existing public package boundaries.

**Tech Stack:** Python stdlib `json`/`hashlib`, dataclasses, JSON Schema draft 2020-12, stdlib `unittest`.

---

### Task 1: Add Capability Fingerprint

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`
- Create: `schemas/capability-fingerprint.schema.json`
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_core_fixtures.py`
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_cli_fixture.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: docs/status/build-log files as needed

- [x] **Step 1: Write failing tests**

Assert a sample fingerprint input serializes `object`, `id_scheme`, `canonical_id`, `entity_kind`, `declared_capability_shape`, and `capability_fingerprint`; assert key order in nested shape does not change the digest; assert missing required fields and non-string declared-shape keys are rejected.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts
```

Expected: fail because the contract, fixture, schema, and exports do not exist.

- [x] **Step 3: Implement minimal contract**

Add `CapabilityFingerprintInput` with `fingerprint()` and `to_dict()`. Use `json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)` and `hashlib.sha256`.

- [x] **Step 4: Mirror public surfaces**

Add `sample_capability_fingerprint_input()`, expose it through CLI/MCP fixture adapters and Python SDK, add TypeScript interface, and add `schemas/capability-fingerprint.schema.json`.

- [x] **Step 5: Verify**

Run:

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts
make check
npm run check --prefix packages/sdk-ts
```

Expected: all pass.

---

## Self-Review

- Spec coverage: Covers the pinned SHA256 hash-input contract without adding storage, migrations, entity graph persistence, or private data.
- Placeholder scan: No placeholders.
- Type consistency: Uses `capability_fingerprint`, `declared_capability_shape`, and existing public package export patterns.
