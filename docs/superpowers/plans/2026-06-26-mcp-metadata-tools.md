# MCP Metadata Tools Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add MCP tools for the already-public metadata route contracts.

**Architecture:** Keep the MCP package a thin public adapter. Add `evalrank.use_cases` for `GET /v1/use-cases` and `evalrank.scoring_stages` for `GET /v1/scoring-stages`, routing through `EvalRankClient` with explicit `base_url` and existing Problem Details tool-error behavior.

**Tech Stack:** Python stdlib tests, existing public Python SDK client, existing MCP text-result adapter.

---

### Task 1: MCP Metadata Tools

**Files:**
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `packages/mcp/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-mcp-metadata-tools.md`

- [x] **Step 1: Write failing MCP tests**

Add tests proving:
- README and tool manifest list `evalrank.use_cases` and `evalrank.scoring_stages`.
- `evalrank.use_cases` calls `GET /v1/use-cases`.
- `evalrank.scoring_stages` calls `GET /v1/scoring-stages`.
- Metadata route Problem Details responses return MCP `isError: true` text results.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_mcp_fixture
```

Expected: fail because the metadata tools do not exist yet.

- [x] **Step 3: Implement minimal tools**

Reuse `EvalRankClient`, explicit `base_url` validation, text JSON results, and public Problem Details tool-error handling. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, persistence, or hosted receipt behavior.

- [x] **Step 4: Update docs**

Update package/root READMEs, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and a dated build log.

- [x] **Step 5: Verify green**

Run:

```sh
python3 -m unittest tests.test_mcp_fixture
python3 scripts/check_public_boundary.py --root .
make check
```
