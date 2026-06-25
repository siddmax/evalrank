# EvalRank Status

Last updated: 2026-06-25

## Built

- Public Apache-2.0 repository scaffold.
- Public package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` guidance.
- `CLAUDE.md` shim to `@AGENTS.md`.
- Public boundary checker for private imports, disallowed coupling, excluded method markers, and missing package license/notice files.
- Public boundary checker guards for secret files, high-signal secret values, and held-out/private data paths.
- Core Python recommendation and evidence contracts in `packages/core`.
- Public core fixture factory for canonical example recommendation and evidence payloads.
- Public JSON Schemas for ranked entities, recommendations, and evidence items.
- Python SDK package metadata and public core contract re-exports.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Public scoring-stage vocabulary and method-boundary note.
- Schema drift tests for core payload keys and public enum constants.
- Tests for core contracts, schema-contract drift, and public boundary rules.
- Public progress tracker and repo structure map.
- Public porting map for deciding what moves from Syndai/private workstreams into this repo.
- Direct `main` push workflow during scratch-build phase; branch protection is currently removed.
- `make check` local gate shared with CI.
- W0 public exit packet in `docs/build-log/2026-06-25-w0-public-exit.md`.
- Public W1 entity/evidence contract plan in `docs/superpowers/plans/2026-06-25-entity-evidence-contracts.md`.
- Public porting workstream sync in `docs/build-log/2026-06-25-porting-workstream-sync.md`.
- W1 entity/evidence contract build log in `docs/build-log/2026-06-25-w1-entity-evidence-contracts.md`.
- Python SDK re-export build log in `docs/build-log/2026-06-25-python-sdk-reexports.md`.
- CLI fixture command build log in `docs/build-log/2026-06-25-cli-fixtures.md`.
- MCP fixture adapter build log in `docs/build-log/2026-06-25-mcp-fixtures.md`.
- Public scoring-stage build log in `docs/build-log/2026-06-25-scoring-stages.md`.

## In Progress

- Public/private porting triage.
- Current source of truth is split between:
  - Python contracts in `packages/core/src/evalrank_core/contracts.py`
  - Public JSON Schemas in `schemas/`
  - Public porting decisions in `docs/PORTING.md`
  - Build-readiness docs in Syndai under `docs/superpowers/plans/evalrank/`

## Porting Queue

| Priority | Workstream | Destination | Public handling |
| --- | --- | --- | --- |
| 1 | Public Contracts | This repo | First entity/evidence slice ported; extend only for new public payload contracts. |
| 2 | Methods / Schemas | This repo | Public scoring-stage vocabulary ported; add details only after private material is removed. |
| 3 | SDK / CLI / MCP | This repo | First public fixture slices ported; extend after concrete non-fixture contracts are pinned. |
| 4 | Docs / Public Planning | This repo | Keep sanitized build logs and status docs current; do not copy private planning text verbatim. |
| 5 | DB Bootstrap / Syndai Ops | Syndai repo | Keep Supabase migrations, live bootstrap, and operational checks private during incubation. |
| 6 | Evaluation Integrity | Private eval systems | Keep held-out tasks, graders, answers, traces, and benchmark results private. |
| 7 | Hosted Ops / GTM | Private hosted systems | Keep billing, admin, telemetry, vendor intent, and account operations out of this repo. |

## Next

- Add an OpenAPI skeleton only when the first REST surface exists or a concrete route contract is ready.
- Add package-level implementation for the next public surface only after its contract is pinned.
- Add `NAVIGATION.md` when EvalRank has UI routes, API routes, deeplinks, or navigation-critical docs.

## Left

- W1+: data-plane tables, entity graph, evidence ledger, trust/security primitives, scorer stages, engine materializer, public surfaces, web, telemetry, governance, and GTM fleet.

## Update Rules

- Update this file when a feature lands, a wave gate changes, or an item moves between `Next`, `In Progress`, and `Built`.
- Keep dated build logs under `docs/build-log/` for immutable-ish snapshots; keep this file current.
