# Ranking Group Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin the public storage-free ranking-group row for `kind-grouped` recommendations.

**Architecture:** Reuse existing `RankedEntity` rows and `Recommendation.groups`; replace loose dict groups with one closed `RankingGroup` contract. Keep the shape public-only: group key, entity type, within-group ranked rows, and rationale. Do not add scorer behavior, cross-kind score semantics, DB tables, source adapters, hosted receipts, or private thresholds.

**Tech Stack:** Python dataclasses, stdlib `unittest`, JSON Schema 2020-12, TypeScript type declarations.

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

- [x] Add failing tests for `RankingGroup.to_dict()`, validation, `Recommendation.kind_grouped()`, schema shape, Python SDK export, TypeScript interface, CLI `fixture ranking-group`, and MCP `ranking-group`.
- [x] Run `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts` and confirm failures are for missing ranking-group surfaces.

### Task 2: Minimal Contract Surface

**Files:**
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `packages/core/src/evalrank_core/fixtures.py`
- Modify: `packages/core/src/evalrank_core/__init__.py`
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `packages/sdk-ts/src/index.ts`
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/mcp/src/evalrank_mcp/__init__.py`

- [x] Add `RankingGroup` with `group_key`, `entity_type`, `ranked`, and `group_rationale`.
- [x] Add `Recommendation.kind_grouped()` that serializes `groups` as `RankingGroup.to_dict()` rows and keeps `ranked` empty.
- [x] Add deterministic `sample_ranking_group()` and expose fixture kind `ranking-group`.

### Task 3: Schema And Docs

**Files:**
- Modify: `schemas/recommendation.schema.json`
- Modify: `schemas/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-ranking-group-contract.md`

- [x] Replace loose group objects with a closed `RankingGroup` schema under `recommendation.schema.json`.
- [x] Update docs to mark ranking groups as ported while keeping scorer/runtime/private benchmark semantics out.

### Task 4: Verify And Ship

- [x] Run the focused unittest command from Task 1.
- [x] Run `npm run check --prefix packages/sdk-ts`.
- [x] Run `make check`.
- [x] Run gstack pre-landing review plus Ponytail scope pass.
- [ ] Commit and push directly to `main`; verify the matching GitHub Actions run.

## GSTACK REVIEW REPORT

Scope Check: CLEAN

Intent: Pin the public storage-free ranking-group row for `kind-grouped` recommendations.
Delivered: Added `RankingGroup` across core, schema, SDK, CLI, MCP, tests, README docs, status docs, and porting docs.

Plan completion: Tasks 1-3 complete. Task 4 local verification and pre-landing review complete. Final commit/push/CI verification is still the remaining ship step.

Pre-Landing Review: No issues found.

Evidence:
- Focused regression suite passed 104 tests.
- `npm run check --prefix packages/sdk-ts` passed.
- `make check` passed public boundary scan and 117 tests.
- `git diff --check` passed.
- gstack review log status: clean, 0 issues, no unresolved findings.
- Ponytail scope pass: kept the slice to contract/schema/fixture/SDK/CLI/MCP/docs only; no DB, scorer, source adapter, hosted receipt, or private benchmark behavior added.
