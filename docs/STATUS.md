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
- TypeScript SDK package metadata and mirrored public contract types/constants.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Public scoring-stage vocabulary and method-boundary note.
- Runnable public fixture example.
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
- Public progress and porting audit in `docs/build-log/2026-06-25-public-progress-and-porting-audit.md`.
- TypeScript SDK public type surface build log in `docs/build-log/2026-06-25-typescript-sdk-types.md`.
- Runnable public fixture example build log in `docs/build-log/2026-06-25-public-fixture-example.md`.

## Current Public Surface

| Surface | Built | Not built yet |
| --- | --- | --- |
| Core contracts | `RankedEntity`, `Recommendation`, `EntityRef`, `EvidenceItem`, public constants, and synthetic fixture factories. | Storage models, graph persistence, scorer engine, trust/security policy runtime. |
| Schemas | JSON Schemas for ranked entities, recommendations, and evidence items, with drift tests against Python contracts. | OpenAPI route schemas and persistence schemas. |
| Python SDK | Package metadata and public re-exports from `evalrank_core`. | Installed package release flow and non-fixture client behavior. |
| TypeScript SDK | Package metadata, public constants, and interfaces for current payload contracts. | Built JS distribution, published package release flow, and non-fixture client behavior. |
| CLI | Deterministic `fixture evidence` and `fixture recommendation` commands. | Real evaluation commands, API clients, auth, or workspace/project operations. |
| MCP | Deterministic `evalrank.fixture` adapter and public tool manifest. | Live MCP server runtime, evidence lookup, scorer tools, or private data access. |
| Methods | Public scoring-stage vocabulary and private-boundary note. | Proprietary weights, thresholds, graders, held-out tasks, and benchmark outputs. |
| Examples | `examples/public_fixture.py` prints synthetic public recommendation and evidence JSON. | Non-fixture demos, live API examples, and private-data examples. |
| Docs | Status tracker, repo structure map, porting map, package READMEs, and build logs. | `NAVIGATION.md`; add it only when UI/API routes or deeplinks exist. |

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
| 1 | Public Contracts | This repo | First recommendation and entity/evidence slices ported; extend only for new public payload contracts. |
| 2 | Methods / Schemas | This repo | Public scoring-stage vocabulary ported; add details only after private material is removed. |
| 3 | SDK / CLI / MCP | This repo | Python SDK, TypeScript SDK types, CLI fixture, and MCP fixture slices ported; extend after concrete non-fixture contracts are pinned. |
| 4 | Docs / Public Planning | This repo | Current status, repo structure, porting docs, and first runnable example are public-safe; keep updating them with each port. |
| 5 | DB Bootstrap / Syndai Ops | Syndai repo | Keep Supabase migrations, live bootstrap, and operational checks private during incubation. |
| 6 | Evaluation Integrity | Private eval systems | Keep held-out tasks, graders, answers, traces, and benchmark results private. |
| 7 | Hosted Ops / GTM | Private hosted systems | Keep billing, admin, telemetry, vendor intent, and account operations out of this repo. |

## Next

- Public Contracts workstream: pin the next storage-free payload contract before adding more SDK/CLI/MCP behavior.
- SDK / CLI / MCP workstream: promote fixture-only adapters to real commands/tools only after the target public contract exists.
- Public Surface Contracts workstream: add an OpenAPI skeleton only when the first REST route exists or a concrete route contract is ready.
- Docs / Public Planning workstream: keep `docs/STATUS.md`, `docs/PORTING.md`, `docs/REPO_STRUCTURE.md`, package READMEs, and build logs aligned in the same change.
- Add `NAVIGATION.md` only when EvalRank has UI routes, API routes, deeplinks, or navigation-critical docs.

## Left

- Public repo: additional contracts, schemas, SDK/CLI/MCP behavior, public examples, route contracts, UI/navigation docs, and reproducible public evaluation fixtures.
- Private/Syndai or hosted systems: data-plane tables, Supabase migrations, entity graph persistence, evidence ledger, private trust/security policy runtime, engine materializer, production telemetry, governance operations, billing/admin, and GTM fleet.
- Private evaluation systems: held-out tasks, graders, answers, traces, benchmark outputs, and proprietary ranking experiments.

## Update Rules

- Update this file when a feature lands, a wave gate changes, or an item moves between `Next`, `In Progress`, and `Built`.
- Keep dated build logs under `docs/build-log/` for immutable-ish snapshots; keep this file current.
