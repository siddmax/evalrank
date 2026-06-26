# MCP Recommendation Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add public MCP `POST /v1/recommendations` behavior without private service wiring.

**Architecture:** Keep the existing `packages/mcp` shim. Add `evalrank.recommend` to `list_tools()` and route `call_tool()` through the public Python SDK `EvalRankClient`, returning JSON text in MCP tool results.

**Tech Stack:** Python stdlib tests, existing `evalrank-sdk`, existing `evalrank-core`, MCP tool shape.

---

### Task 1: MCP Recommendation Tool

**Files:**
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`
- Modify: `packages/mcp/pyproject.toml`
- Modify: `tests/test_mcp_fixture.py`
- Modify: `packages/mcp/README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-mcp-recommendation-tool.md`

- [x] **Step 1: Write failing tests**

Add tests that prove:
- `list_tools()` exposes `evalrank.fixture` and `evalrank.recommend`.
- `call_tool("evalrank.recommend", {"base_url": "...", "request": {...}})` posts to `/v1/recommendations` and returns recommendation JSON text.
- Problem Details errors return an MCP tool result with `isError: true`.
- Non-object or missing arguments raise `ValueError`.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_mcp_fixture
```

Expected: fail because `evalrank.recommend` is not listed or callable.

- [x] **Step 3: Implement minimal adapter**

Reuse `evalrank_sdk.EvalRankClient` and `EvalRankApiError`. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, persistence, or hosted receipt behavior.

- [x] **Step 4: Verify green**

Run:

```sh
python3 -m unittest tests.test_mcp_fixture
python3 scripts/check_public_boundary.py --root .
make check
```

- [x] **Step 5: Update docs**

Update package README, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and the dated build log with the public/private boundary.
