# EvalRank Status

Last updated: 2026-06-25

## Built

- Public Apache-2.0 repository scaffold.
- Public package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` guidance.
- `CLAUDE.md` shim to `@AGENTS.md`.
- Public boundary checker for private imports, disallowed coupling, excluded method markers, and missing package license/notice files.
- Public boundary checker guards for secret files, high-signal secret values, and held-out/private data paths.
- Core Python capability fingerprint, raw entry, request, `the_call`, recommendation, and evidence contracts in `packages/core`.
- Public core fixture factory for canonical capability fingerprint, raw entry, request, recommendation, and evidence payloads.
- Public JSON Schemas for capability fingerprints, raw entries, evaluation requests, ranked entities, recommendations, and evidence items.
- Public OpenAPI 3.1.1 contract for `POST /v1/recommendations`.
- Pinned public `methodology_version` format: `YYYY-MM-DD.SEQ.slug`.
- Python SDK package metadata and public core contract re-exports.
- TypeScript SDK package metadata and mirrored public contract types/constants.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Public scoring-stage vocabulary and method-boundary note.
- Runnable public fixture example.
- Schema drift tests for core payload keys and public enum constants.
- Tests for core contracts, schema-contract drift, and public boundary rules.
- Public progress tracker and repo structure map.
- Public route navigation map in `NAVIGATION.md`.
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
- Evaluation request contract build log in `docs/build-log/2026-06-25-evaluation-request-contract.md`.
- Methodology version format build log in `docs/build-log/2026-06-25-methodology-version-format.md`.
- Capability fingerprint contract build log in `docs/build-log/2026-06-25-capability-fingerprint-contract.md`.
- Public progress and porting router refresh in `docs/build-log/2026-06-25-progress-and-porting-router.md`.
- Recommendation join aliases build log in `docs/build-log/2026-06-25-recommendation-join-aliases.md`.
- Public port-over status refresh in `docs/build-log/2026-06-25-public-port-over-status.md`.
- Raw entry contract build log in `docs/build-log/2026-06-25-raw-entry-contract.md`.
- Structured `the_call` contract build log in `docs/build-log/2026-06-25-the-call-contract.md`.
- Public OpenAPI contract build log in `docs/build-log/2026-06-25-public-openapi-contract.md`.

## Current Public Surface

| Surface | Built | Not built yet |
| --- | --- | --- |
| Core contracts | `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `TheCall`, `RankedEntity`, `Recommendation`, public recommendation ID aliases, `EntityRef`, `EvidenceItem`, public constants, and synthetic fixture factories. | Source adapters, storage models, graph persistence, scorer engine, trust/security policy runtime. |
| Schemas | JSON Schemas for capability fingerprints, raw entries, evaluation requests, ranked entities, recommendations, and evidence items, plus OpenAPI 3.1.1 for `POST /v1/recommendations`, with drift tests against public contracts and pinned public patterns. | Persistence schemas and additional route/error contracts. |
| Python SDK | Package metadata and public re-exports from `evalrank_core`. | Installed package release flow and non-fixture client behavior. |
| TypeScript SDK | Package metadata, public constants, and interfaces for current payload contracts, including `RawEntry` and `TheCall`. | Built JS distribution, published package release flow, and non-fixture client behavior. |
| CLI | Deterministic `fixture fingerprint`, `fixture raw-entry`, `fixture request`, `fixture evidence`, and `fixture recommendation` commands. | Real evaluation commands, API clients, auth, or workspace/project operations. |
| MCP | Deterministic `evalrank.fixture` adapter and public tool manifest, including `raw-entry`. | Live MCP server runtime, evidence lookup, scorer tools, or private data access. |
| Methods | Public scoring-stage vocabulary and private-boundary note. | Proprietary weights, thresholds, graders, held-out tasks, and benchmark outputs. |
| Examples | `examples/public_fixture.py` prints synthetic public recommendation and evidence JSON. | Non-fixture demos, live API examples, and private-data examples. |
| Docs | Status tracker, repo structure map, porting map, route navigation map, package READMEs, build logs, and public/private workstream router. | UI navigation docs; add only when UI routes or deeplinks exist. |

## In Progress

- Public/private porting triage and workstream routing.
- Current source of truth is split between:
  - Python contracts in `packages/core/src/evalrank_core/contracts.py`
  - Public JSON Schemas in `schemas/`
  - Public porting decisions in `docs/PORTING.md`
- Private Syndai build-readiness docs and operational plans, summarized here only when public-safe.
- Latest port review: storage-free contracts, schemas, synthetic fixtures, public SDK/CLI/MCP boundaries, public route contracts, and sanitized method notes can move here. Public recommendation identifier aliases, storage-free `RawEntry`, structured public `the_call`, and the first storage-free OpenAPI route contract have moved. DB bootstrap, Supabase migrations, live deploy wiring, telemetry, billing/admin/GTM, private integrations, credentials, production data, HMAC/secret-backed hosted IDs, source adapters, live fetch behavior, scorer thresholds, and held-out evaluation material stay private.

## Current Port-Over Snapshot

| Change or source area | Public status | Owning workstream |
| --- | --- | --- |
| Public repository scaffold, package boundaries, CI, license/notice hygiene, and boundary scanner | Ported here | Open-Core Boundary / CI |
| Storage-free core payloads: capability fingerprint, methodology version, raw entry, evaluation request, `the_call`, ranked entity, recommendation, recommendation aliases, entity reference, and evidence item | Ported here | Public Contracts |
| Public JSON Schemas and schema drift tests for current payloads | Ported here | Methods / Schemas, Public Contracts |
| Synthetic fixtures, runnable public example, CLI fixture command, MCP fixture adapter, Python SDK re-exports, and TypeScript public types | Ported here | SDK / CLI / MCP, Examples |
| Public scoring-stage vocabulary and private-boundary note | Ported here | Methods / Schemas |
| `RawEntry` ingestion-normalization contract | Ported here as a storage-free synthetic fixture contract | Public Contracts |
| Structured public `the_call` / decision-confidence shape | Ported here as a storage-free nested recommendation contract | Public Contracts, Methods / Schemas |
| REST/OpenAPI source of truth | First route contract ported for `POST /v1/recommendations` | Public Surface Contracts |
| Supabase schema bootstrap, migrations, grants/RLS, live DB checks, and shared Finn/Supabase operations | Keep private | DB Bootstrap / Syndai Ops |
| Deterministic scorer, materializer, entity graph persistence, and evidence-ledger runtime | Incubate private until separable from production data and proprietary tuning | Scoring / Materializer Runtime |
| Hosted receipts, HMAC-backed IDs, auth, billing/admin/GTM, telemetry, deploy config, and credentials | Keep private | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out tasks, graders, answers, traces, benchmark outputs, and judge-calibration material | Never port | Evaluation Integrity |

## Porting Queue

| Priority | Workstream | Destination | Public handling |
| --- | --- | --- | --- |
| 1 | Public Contracts | This repo | First raw entry, request, `the_call`, recommendation, recommendation alias, and entity/evidence slices ported; extend only for new public payload contracts. |
| 2 | Methods / Schemas | This repo | Public scoring-stage vocabulary ported; add details only after private material is removed. |
| 3 | SDK / CLI / MCP | This repo | Python SDK, TypeScript SDK types, CLI fixture, and MCP fixture slices ported; extend after concrete non-fixture contracts are pinned. |
| 4 | Docs / Public Planning | This repo | Current status, repo structure, porting docs, and first runnable example are public-safe; keep updating them with each port. |
| 5 | Public Surface Contracts | This repo | First OpenAPI route contract is ported; add more routes only when concrete public contracts exist, and keep private DTOs and hosted auth outside. |
| 6 | DB Bootstrap / Syndai Ops | Syndai repo | Keep Supabase migrations, live bootstrap, grants/RLS, and operational checks private during incubation. |
| 7 | Scoring / Materializer Runtime | Private incubation first | Split reusable deterministic core before porting; private data, proprietary weights, and live workers stay out. |
| 8 | Evaluation Integrity | Private eval systems | Keep held-out tasks, graders, answers, traces, and benchmark results private. |
| 9 | Hosted Ops / GTM | Private hosted systems | Keep billing, admin, telemetry, vendor intent, and account operations out of this repo. |
| 10 | Secrets / Deploy Ops | Private ops only | Keep credentials, Doppler config, live project refs, and deploy environment files out of Git history. |

## Next

- Public Contracts workstream: pin the next storage-free payload contract before adding more SDK/CLI/MCP behavior.
- SDK / CLI / MCP workstream: promote fixture-only adapters toward `POST /v1/recommendations` only after the non-fixture client contract is pinned.
- Public Surface Contracts workstream: extend OpenAPI only for concrete public routes or shared error contracts.
- Scoring / Materializer Runtime workstream: keep runtime and private evidence material in incubation until the deterministic, storage-free public core is separable.
- Docs / Public Planning workstream: keep `docs/STATUS.md`, `docs/PORTING.md`, `docs/REPO_STRUCTURE.md`, package READMEs, and build logs aligned in the same change.
- Update `NAVIGATION.md` when EvalRank adds or changes public API routes, UI routes, deeplinks, or navigation-critical docs.

## Left

- Public repo: additional contracts, schemas, SDK/CLI/MCP behavior, public examples, additional route/error contracts, UI navigation docs, and reproducible public evaluation fixtures.
- Private/Syndai or hosted systems: data-plane tables, Supabase migrations, entity graph persistence, evidence ledger, private trust/security policy runtime, engine materializer, production telemetry, governance operations, billing/admin, and GTM fleet.
- Private evaluation systems: held-out tasks, graders, answers, traces, benchmark outputs, and proprietary ranking experiments.

## Update Rules

- Update this file when a feature lands, a wave gate changes, or an item moves between `Next`, `In Progress`, and `Built`.
- Keep dated build logs under `docs/build-log/` for immutable-ish snapshots; keep this file current.
