# EvalRank Status

Last updated: 2026-06-26

## Built

- Public Apache-2.0 repository scaffold.
- Public package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` guidance.
- `CLAUDE.md` shim to `@AGENTS.md`.
- Public boundary checker for private imports, disallowed coupling, excluded method markers, and missing package license/notice files.
- Public boundary checker guards for secret files, high-signal secret values, and held-out/private data paths.
- Core Python capability fingerprint, raw entry, request, candidate set, stage candidate, evidence item, result row, use-case catalog, scoring stage catalog, ranking group, evidence set, exclusion, `the_call`, abstention, and recommendation contracts in `packages/core`.
- Public core fixture factory for canonical capability fingerprint, raw entry, request, candidate set, stage candidate, evidence item, Problem Details, result row, use-case catalog, scoring stage catalog, ranking group, evidence set, exclusion, and recommendation payloads with public abstention fields, with synthetic request use cases aligned to the public catalog.
- Shared public fixture-kind dispatch in core, reused by CLI and MCP fixture adapters.
- Public JSON Schemas for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, scoring stage catalogs, evidence sets, exclusions, ranked entities, recommendations with closed ranking groups and public abstention objects, evidence items, and retry-aware RFC 9457 Problem Details.
- Public OpenAPI 3.1.1 contract for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, including reusable Problem Details responses for malformed requests, validation errors, rate limits, temporary unavailability, and upstream timeouts.
- Public retry-aware Problem Details extensions: `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url`.
- Pinned public `methodology_version` format: `YYYY-MM-DD.SEQ.slug`.
- Python SDK package metadata and public core contract re-exports.
- TypeScript SDK package metadata and mirrored public contract types/constants, including public fixture kinds, scoring stage catalog types, Problem Details codes, and type shape.
- SDK README drift checks for the Python and TypeScript public surfaces.
- CLI package metadata and deterministic public fixture command, including `result-row`, `use-cases`, `scoring-stages`, and `ranking-group`.
- MCP package metadata and deterministic public fixture adapter, including `result-row`, `use-cases`, `scoring-stages`, and `ranking-group`.
- Public scoring-stage vocabulary and catalog contract, use-case taxonomy method, and method-boundary notes.
- Runnable public fixture bundle example, including the scoring stage catalog.
- Schema drift tests for core payload keys and public enum constants.
- Tests for core contracts, schema-contract drift, and public boundary rules.
- Public progress tracker and repo structure map.
- Public route navigation map in `NAVIGATION.md`.
- Public porting map for deciding what moves from Syndai/private workstreams into this repo.
- Public/private porting audit confirming the current private Syndai dirty worktree has Memphant spec edits plus two Memphant plan files and no EvalRank public-port candidate.
- Public/private source scan classifying the current Syndai EvalRank spec, build-readiness, migration, and doc-validation surfaces without copying raw private text.
- Public/private source inventory refresh documenting current private EvalRank specs, build plans, proof assets, backend migration assets, GitHub security settings, and next public port slices without copying raw private text.
- GitHub public repo security metadata snapshot confirming public visibility, secret scanning, push protection, and Dependabot security updates are enabled.
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
- Public Problem Details contract build log in `docs/build-log/2026-06-25-problem-details-contract.md`.
- Candidate set contract build log in `docs/build-log/2026-06-25-candidate-set-contract.md`.
- Evidence set contract build log in `docs/build-log/2026-06-26-evidence-set-contract.md`.
- Exclusion contract build log in `docs/build-log/2026-06-26-exclusion-contract.md`.
- Stage candidate contract build log in `docs/build-log/2026-06-26-stage-candidate-contract.md`.
- Retry-aware Problem Details contract build log in `docs/build-log/2026-06-26-problem-details-retry-contract.md`.
- Result row contract build log in `docs/build-log/2026-06-26-result-row-contract.md`.
- Public porting assessment refresh in `docs/build-log/2026-06-26-public-porting-assessment.md`.
- Use-case catalog contract build log in `docs/build-log/2026-06-26-use-case-catalog-contract.md`.
- Ranking group contract build log in `docs/build-log/2026-06-26-ranking-group-contract.md`.
- Use-case taxonomy method build log in `docs/build-log/2026-06-26-use-case-taxonomy-method.md`.
- Fixture use-case alignment build log in `docs/build-log/2026-06-26-fixture-use-case-alignment.md`.
- Public fixture bundle example build log in `docs/build-log/2026-06-26-public-fixture-bundle-example.md`.
- SDK README drift-check build log in `docs/build-log/2026-06-26-sdk-readme-drift-checks.md`.
- Core and schema README drift-check build log in `docs/build-log/2026-06-26-core-schema-readme-drift-checks.md`.
- Scoring stage catalog contract build log in `docs/build-log/2026-06-26-scoring-stage-catalog-contract.md`.
- Scoring stages route contract build log in `docs/build-log/2026-06-26-scoring-stages-route-contract.md`.
- Progress and porting routing refresh in `docs/build-log/2026-06-26-progress-porting-routing.md`.
- Public fixture dispatch build log in `docs/build-log/2026-06-26-public-fixture-dispatch.md`.
- TypeScript fixture-kind parity build log in `docs/build-log/2026-06-26-typescript-fixture-kind-parity.md`.
- Public fixture example README drift-check build log in `docs/build-log/2026-06-26-example-readme-drift-check.md`.
- Public fixture example nested contract README drift-check build log in `docs/build-log/2026-06-26-example-nested-contract-drift-check.md`.
- Python SDK vocabulary export build log in `docs/build-log/2026-06-26-python-sdk-vocabulary-exports.md`.
- Python Problem Details contract build log in `docs/build-log/2026-06-26-python-problem-details-contract.md`.
- Public Problem Details fixture build log in `docs/build-log/2026-06-26-problem-details-fixture.md`.
- Score-component map hardening build log in `docs/build-log/2026-06-26-score-components-contract-hardening.md`.
- Recommendation envelope validation hardening build log in `docs/build-log/2026-06-26-recommendation-envelope-contract-hardening.md`.
- JSON-object metadata validation hardening build log in `docs/build-log/2026-06-26-json-object-contract-hardening.md`.
- Public doc progress and porting audit in `docs/build-log/2026-06-26-public-doc-progress-porting-audit.md`.
- Primitive and sequence field validation hardening build log in `docs/build-log/2026-06-26-primitive-sequence-contract-hardening.md`.
- Unique request entity-types hardening build log in `docs/build-log/2026-06-26-evaluation-request-entity-type-uniqueness.md`.
- Public string-field validation hardening build log in `docs/build-log/2026-06-26-public-string-field-contract-hardening.md`.
- Private source port-routing build log in `docs/build-log/2026-06-26-private-source-port-routing.md`.
- Public abstention contract build log in `docs/build-log/2026-06-26-abstention-contract.md`.
- Scoring-stage abstention output alignment build log in `docs/build-log/2026-06-26-scoring-stage-abstention-output.md`.
- Public progress and port-over routing refresh in `docs/build-log/2026-06-26-progress-portover-refresh.md`.
- Port-over inventory refresh build log in `docs/build-log/2026-06-26-port-over-inventory-refresh.md`.

## Current Public Surface

| Surface | Built | Not built yet |
| --- | --- | --- |
| Core contracts | `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `EvidenceSet`, `Exclusion`, `TheCall`, `Abstention`, `ProblemDetails`, `RankedEntity`, `Recommendation`, public recommendation ID aliases, `EntityRef`, public constants, shared fixture-kind dispatch, strict public score-component maps, strict recommendation envelope validation, and synthetic fixture factories. | Source adapters, storage models, graph persistence, scorer engine, benchmark weights, IRT clusters, Stage-2+ scorer rows, trust/security policy runtime. |
| Schemas | JSON Schemas for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, scoring stage catalogs, evidence sets, exclusions, ranked entities with strict public score-component maps, recommendations with closed ranking groups and public abstention objects, evidence items, and retry-aware RFC 9457 Problem Details, plus OpenAPI 3.1.1 for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, with drift tests against public contracts and pinned public patterns. | Persistence schemas, scorer-runtime schemas, benchmark-weight schemas, and additional route-specific problem types beyond the current public error vocabulary. |
| Python SDK | Package metadata and public re-exports from `evalrank_core`, including `ProblemDetails`, public vocabulary constants, and public fixture dispatch helpers. | Installed package release flow and non-fixture client behavior. |
| TypeScript SDK | Package metadata, public constants, and interfaces for current payload contracts, including `RawEntry`, `CandidateSet`, `StageCandidate`, `ResultRow`, `UseCaseCatalog`, `ScoringStageCatalog`, `RankingGroup`, `EvidenceSet`, `Exclusion`, `TheCall`, `Abstention`, `ProblemDetails`, and public fixture kinds. | Built JS distribution, published package release flow, and non-fixture client behavior. |
| CLI | Deterministic `fixture fingerprint`, `fixture raw-entry`, `fixture request`, `fixture candidate-set`, `fixture stage-candidate`, `fixture evidence`, `fixture problem`, `fixture result-row`, `fixture use-cases`, `fixture scoring-stages`, `fixture ranking-group`, `fixture evidence-set`, `fixture exclusion`, and `fixture recommendation` commands. | Real evaluation commands, API clients, auth, or workspace/project operations. |
| MCP | Deterministic `evalrank.fixture` adapter and public tool manifest, including `raw-entry`, `candidate-set`, `stage-candidate`, `evidence`, `problem`, `result-row`, `use-cases`, `scoring-stages`, `ranking-group`, `evidence-set`, and `exclusion`. | Live MCP server runtime, evidence lookup, scorer tools, or private data access. |
| Methods | Public scoring-stage vocabulary and storage-free `ScoringStageCatalog`, including `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, and `Abstention`; public use-case taxonomy method; and private-boundary notes. | Proprietary weights, thresholds, graders, held-out tasks, and benchmark outputs. |
| Examples | `examples/public_fixture.py` prints the current synthetic public fixture bundle: raw entry, request, candidate set, stage candidate, evidence item, Problem Details, evidence set, result row, use-case catalog, scoring stage catalog, exclusion, and recommendation JSON; its README is drift-checked against the emitted JSON keys plus nested recommendation and scoring-stage contract refs. | Non-fixture demos, live API examples, and private-data examples. |
| Docs | Status tracker, repo structure map, porting map, route navigation map, package READMEs, build logs, and public/private workstream router. | UI navigation docs; add only when UI routes or deeplinks exist. |

## Progress Snapshot

| Area | State | Next owner |
| --- | --- | --- |
| Repo foundation | Built: public scaffold, package boundaries, license/notice hygiene, root/scoped agent docs, CI, `make check`, and deterministic public-boundary scanner. | Open-Core Boundary / CI keeps leak and drift checks current. |
| Public contracts | Built through the current storage-free payload set: fingerprints, raw entries, requests, candidate sets, stage candidates, result rows, use-case catalogs, scoring stage catalogs, ranking groups, evidence sets, exclusions, `the_call`, abstentions, recommendations, public aliases, entity refs, and evidence items. | Public Contracts pins the next standalone payload before SDK/CLI/MCP behavior grows. |
| Schemas and methods | Built: JSON Schemas, OpenAPI route contracts for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, retry-aware Problem Details, public scoring-stage vocabulary/catalog, and sanitized use-case taxonomy method note. | Methods / Schemas and Public Surface Contracts add only public, product-neutral semantics. |
| Interfaces | Built as fixture-only surfaces: Python SDK re-exports, TypeScript public types/constants, deterministic CLI fixture commands, MCP fixture adapter, runnable public example, and README drift guards. | SDK / CLI / MCP promotes non-fixture behavior only after a public route/client contract is pinned. |
| Persistence and hosted ops | Not public: DB bootstrap, Supabase migrations, grants/RLS, live workers, telemetry, auth, billing/admin, deploy config, and credentials. | DB Bootstrap / Syndai Ops, Hosted Ops / GTM, and Secrets / Deploy Ops keep this private until an explicit public cutover exists. |
| Scoring runtime and eval integrity | Not public: deterministic scorer/materializer runtime, graph persistence, source adapters, private weights, IRT clusters, held-out tasks, graders, traces, answers, and benchmark outputs. | Scoring / Materializer Runtime incubates separable public-input-only code privately; Evaluation Integrity keeps held-out material private. |

## Recent Public Delta

| Change | Status | Workstream |
| --- | --- | --- |
| Public fixture outputs were aligned to the public use-case catalog and expanded to include raw entry, candidate set, stage candidate, result row, use-case catalog, scoring stage catalog, ranking group, evidence set, exclusion, and recommendation payloads. | Built here with synthetic fixtures only. | Public Contracts, Examples |
| CLI, MCP, Python SDK, and TypeScript SDK fixture-kind surfaces now share the core public fixture-kind dispatch. | Built here as local deterministic fixture behavior. | SDK / CLI / MCP, Open-Core Boundary / CI |
| `GET /v1/scoring-stages` now exposes the public scoring-stage catalog route contract. | Built here as OpenAPI contract only; no live server, auth, storage, scorer runtime, or hosted deployment behavior was added. | Public Surface Contracts, Methods / Schemas |
| Package and example README drift checks now guard public fixture, SDK, core, and schema surfaces. | Built here with stdlib tests. | Open-Core Boundary / CI, Docs / Public Planning |
| Example README drift checks now include nested public fixture contract refs for recommendation abstention, `the_call`, and scoring-stage output contracts. | Built here as a deterministic docs/example guard; no runtime behavior or private fixture moved. | Open-Core Boundary / CI, Examples |
| Python SDK now re-exports public vocabulary constants from the core source of truth. | Built here as SDK parity with existing schema/core/TypeScript vocabulary; no scorer policy or private runtime behavior moved. | SDK / CLI / MCP, Public Contracts |
| Python core and SDK now expose the public `ProblemDetails` error contract and `PROBLEM_CODES`. | Built here as storage-free public error payload parity with OpenAPI/schema/TypeScript; no hosted auth, tenant context, telemetry, private problem types, or runtime behavior moved. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP |
| Shared public fixtures now include a deterministic `problem` / `sample_problem_details()` payload. | Built here as synthetic RFC 9457 Problem Details fixture parity for core, Python SDK, TypeScript fixture kinds, CLI, MCP, and the runnable example; no hosted error telemetry, tenant context, private problem types, or live service behavior moved. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Examples |
| Ranked entity `score_components` now reject non-object maps, blank/non-string names, booleans, and out-of-range values before serialization. | Built here as public contract hardening; no private scorer formula was added. | Public Contracts, Methods / Schemas |
| Recommendation envelopes now reject schema-incompatible metadata and duplicate ranked entities before serialization. | Built here as public contract hardening; no scorer/runtime, route implementation, hosted receipt, or private evidence behavior was added. | Public Contracts, Methods / Schemas |
| Evidence item `metadata` and evaluation request `constraints` now reject non-object, non-string-key, and non-JSON values before serialization. | Built here as public contract hardening; no private evidence lookup, source adapter, or policy behavior was added. | Public Contracts, Methods / Schemas |
| Entity references, freshness dates, request entity-type arrays, ranked-entity integer fields, and caveats now reject schema-incompatible Python values before serialization. | Built here as public contract hardening; no schema expansion, scorer behavior, or private runtime behavior was added. | Public Contracts, Methods / Schemas |
| Evaluation requests now reject duplicate `entity_types`, and the schema pins `uniqueItems`. | Built here as public request-shape hardening; no candidate resolver, scorer behavior, route implementation, DB work, or private source adapter moved. | Public Contracts, Methods / Schemas |
| Capability fingerprint, raw entry, evidence item, evidence set, candidate set, `the_call`, and abstention public string fields now reject truthy non-strings before serialization. | Built here as public contract hardening against existing schemas; no source adapter, scorer/runtime behavior, private evidence lookup, DB work, or hosted operation moved. | Public Contracts, Methods / Schemas |
| Recommendation abstention responses now include a public `Abstention` reason/detail object and ordinary recommendations include `abstention: null`. | Built here as a storage-free response contract; evidence-floor thresholds, confidence policy, private reason taxonomy, scorer/runtime behavior, DB work, and hosted operations were not moved. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| The public scoring-stage catalog now names `Abstention` as an output of `ranking-or-abstention`. | Built here as catalog alignment after the public `Abstention` contract; no scorer thresholds, private policy, runtime, or DB behavior moved. | Methods / Schemas, Public Contracts |
| Private-side dirty worktree check found Memphant spec edits and two Memphant plan files, not EvalRank public-port candidates. | Documented here as a routing decision; no private Memphant planning text was copied into the public repo. | Memphant / memory-system workstream, Docs / Public Planning, Open-Core Boundary / CI |
| Current private-side EvalRank source scan classified private specs, build-readiness plans, migration bootstrap, migration guards, doc validators, and UI proof assets. | Documented here as a public-safe routing decision; raw private docs, proof assets, operations scripts, and private migrations were not copied. | Docs / Public Planning, Public Surface Contracts, DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Current private-source inventory counted private EvalRank specs, build plans, proof assets, and backend migration assets, then routed the next port slices. | Documented as categories and owners only. Public work stays on storage-free contracts, deterministic fixtures/checks, route contracts, and sanitized method notes; DB, runtime, UI proofs, hosted ops, and eval-integrity material stay private. | Docs / Public Planning, Public Contracts, Public Surface Contracts, Open-Core Boundary / CI, DB Bootstrap / Syndai Ops, Scoring / Materializer Runtime, Evaluation Integrity |
| GitHub repo security metadata was checked for the public repo. | Public visibility, secret scanning, push protection, and Dependabot security updates are enabled; the local boundary scanner remains the required gate because platform scanning is only a backstop. | Open-Core Boundary / CI, Secrets / Deploy Ops |
| Non-fixture clients, live scorer calls, hosted receipts, auth, persistence, graph lookup, source adapters, and eval-integrity material were not ported. | Keep private until each item has a public contract and no secret/private-data dependency. | Public Surface Contracts, Scoring / Materializer Runtime, DB Bootstrap / Syndai Ops, Hosted Ops / GTM, Evaluation Integrity |

## In Progress

- Public/private porting triage and workstream routing.
- Current source of truth is split between:
  - Python contracts in `packages/core/src/evalrank_core/contracts.py`
  - Public JSON Schemas in `schemas/`
  - Public porting decisions in `docs/PORTING.md`
- Private Syndai build-readiness docs and operational plans, summarized here only when public-safe.
- Latest private-side dirty check: Syndai had uncommitted `docs/superpowers/specs/memphant/` edits plus untracked `docs/superpowers/plans/2026-06-26-memphant-gapcheck-validation.md` and `docs/superpowers/plans/2026-06-26-memphant-lifecycle-validation.md`. Treat those as adjacent memory-system planning, not EvalRank public-port material, unless a later task extracts an explicit EvalRank storage-free contract from them.
- Latest private-source inventory: the Syndai checkout contains 25 private EvalRank spec docs, 6 private EvalRank build-plan docs, 18 private UI/proof assets, and 5 backend migration/guard/test assets. These are routing inputs only. Public ports should continue as explicit storage-free contracts, schemas, synthetic fixtures, deterministic checks, public route contracts, or sanitized method notes.
- Latest port review: storage-free contracts, schemas, synthetic fixtures, public SDK/CLI/MCP boundaries, public route contracts, deterministic public-boundary checks, and sanitized method notes can move here. Public recommendation identifier aliases, storage-free `RawEntry`, public `CandidateSet`, public `StageCandidate`, public `EvidenceItem`, public `ResultRow`, public `UseCaseCatalog`, public `ScoringStageCatalog`, public `RankingGroup`, public `EvidenceSet`, public `Exclusion`, structured public `the_call`, public `Abstention`, the first storage-free OpenAPI route contracts, and retry-aware public Problem Details error shape have moved. The private-side planning scan is summarized in `docs/PORTING.md` by workstream, not copied. Private EvalRank specs, build-readiness plans, UI proof assets, doc validators, DB bootstrap, Supabase migrations, live deploy wiring, telemetry, billing/admin/GTM, private integrations, credentials, production data, HMAC/secret-backed hosted IDs, source adapters, live fetch behavior, graph lookup, live evidence lookup, evidence ledger runtime, cross-kind score normalization, benchmark weights, IRT fit clusters, thin-coverage/synthesis policy details, Stage-2+ scorer rows, gate policy, private reason taxonomy, scorer thresholds, private problem types, and held-out evaluation material stay private unless a later task extracts a concrete public contract.

## Current Port-Over Snapshot

| Change or source area | Public status | Owning workstream |
| --- | --- | --- |
| Public repository scaffold, package boundaries, CI, license/notice hygiene, and boundary scanner | Ported here | Open-Core Boundary / CI |
| Storage-free core payloads: capability fingerprint, methodology version, raw entry, evaluation request, candidate set, stage candidate, evidence item, result row, use-case catalog, ranking group, evidence set, exclusion, `the_call`, abstention, ranked entity, recommendation, recommendation aliases, strict recommendation envelope validation, and entity reference | Ported here | Public Contracts |
| Public JSON Schemas and schema drift tests for current payloads | Ported here, including retry-aware Problem Details extensions | Methods / Schemas, Public Contracts, Public Surface Contracts |
| Synthetic fixtures, runnable public example, CLI fixture command, MCP fixture adapter, Python SDK re-exports, and TypeScript public types | Ported here, including raw-entry, candidate-set, stage-candidate, result-row, problem, use-cases, scoring-stages, ranking-group, evidence-set, and exclusion fixture surfaces plus README drift guards | SDK / CLI / MCP, Examples, Open-Core Boundary / CI |
| Public scoring-stage vocabulary, catalog, and private-boundary notes | Ported here, including `ScoringStageCatalog`, `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, `Abstention`, and the use-case taxonomy method | Methods / Schemas |
| `RawEntry` ingestion-normalization contract | Ported here as a storage-free synthetic fixture contract | Public Contracts |
| `CandidateSet` candidate-resolution contract | Ported here as a storage-free list of public `EntityRef` candidates | Public Contracts, Methods / Schemas |
| `StageCandidate` Stage-1 retrieval row | Ported here as a storage-free candidate fingerprint plus public entity, fused score, RRF ranks, and retrieval provenance | Public Contracts, Methods / Schemas |
| `ResultRow` ingested result provenance envelope | Ported here as a storage-free benchmark/result row with public flags and verification state | Public Contracts, Methods / Schemas |
| `EvidenceSet` evidence-attachment contract | Ported here as a storage-free list of public `EvidenceItem` rows; empty lists are allowed for no-evidence or abstention paths | Public Contracts, Methods / Schemas |
| `Exclusion` exclusions-with-reasons contract | Ported here as a storage-free subject plus public reason/detail row | Public Contracts, Methods / Schemas |
| Structured public `the_call` / decision-confidence shape and public `Abstention` reason/detail object | Ported here as storage-free nested recommendation contracts | Public Contracts, Methods / Schemas |
| REST/OpenAPI source of truth | Route contracts ported for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`; public errors use reusable RFC 9457 Problem Details responses plus retry and rate-limit headers | Public Surface Contracts |
| Use-case taxonomy and `/v1/use-cases` route shape | Ported here as storage-free public taxonomy only: id/slug, name, one-line definition, entity-kind spans, ranked-vs-overlay policy, fixture, schema, SDK/CLI/MCP parity, OpenAPI route contract, and sanitized method note | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Methods / Schemas |
| Recommendation comparability and ranking groups | Ported here as storage-free grouped response shape only: `kind-grouped` recommendations now contain closed `RankingGroup` rows with within-kind ranked entities and rationale | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Use-case benchmark weights, IRT cluster crosswalk, confidence policies, and synthesis/coverage rules | Keep private for now; later publish only sanitized method notes that omit weights, held-out tasks, proprietary tuning, and private benchmark outputs | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |
| Supabase schema bootstrap, migrations, grants/RLS, live DB checks, and shared Finn/Supabase operations | Keep private | DB Bootstrap / Syndai Ops |
| Syndai EvalRank migration guard and runner tests | Keep private with the current DB bootstrap; port only a public migration-policy checklist if EvalRank later owns persistence. | DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Syndai EvalRank doc-validation rules for private specs and build plans | Do not copy private spec checks. Distill only public-facing invariants into this repo when the matching public docs or plans exist. | Docs / Public Planning, Open-Core Boundary / CI |
| Current Memphant dirty specs and validation/lifecycle plans in Syndai | Keep out of EvalRank. If they later reveal a reusable evaluation payload or route shape, extract only that public contract into EvalRank with synthetic fixtures and tests. | Memphant / memory-system workstream first; Public Contracts only after explicit extraction |
| Private EvalRank UI proof assets and hosted-product design docs | Keep private until UI routes or public product docs are intentionally added; then port only synthetic screenshots or public-safe docs. | Public Surface Contracts, Hosted Ops / GTM |
| Deterministic scorer, materializer, entity graph persistence, and evidence-ledger runtime | Incubate private until separable from production data and proprietary tuning | Scoring / Materializer Runtime |
| Hosted receipts, HMAC-backed IDs, auth, billing/admin/GTM, telemetry, deploy config, and credentials | Keep private | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out tasks, graders, answers, traces, benchmark outputs, and judge-calibration material | Never port | Evaluation Integrity |

## Porting Queue

| Priority | Workstream | Destination | Public handling |
| --- | --- | --- | --- |
| 1 | Public Contracts | This repo | First raw entry, request, candidate set, stage candidate, result row, use-case catalog, ranking group, evidence set, exclusion, `the_call`, abstention, recommendation, recommendation alias, and entity/evidence slices ported; extend only for new public payload contracts. |
| 2 | Methods / Schemas | This repo | Public scoring-stage vocabulary/catalog and use-case taxonomy method note ported; add details only after private material is removed. |
| 3 | SDK / CLI / MCP | This repo | Python SDK, TypeScript SDK types, CLI fixture, and MCP fixture slices ported; extend after concrete non-fixture contracts are pinned. |
| 4 | Docs / Public Planning | This repo | Current status, repo structure, porting docs, and first runnable example are public-safe; keep updating them with each port. |
| 5 | Public Surface Contracts | This repo | First OpenAPI route contracts and retry-aware public error responses are ported; add more routes only when concrete public contracts exist, and keep private DTOs and hosted auth outside. |
| 6 | DB Bootstrap / Syndai Ops | Syndai repo | Keep Supabase migrations, live bootstrap, grants/RLS, and operational checks private during incubation. |
| 7 | Scoring / Materializer Runtime | Private incubation first | Split reusable deterministic core before porting; private data, proprietary weights, and live workers stay out. |
| 8 | Evaluation Integrity | Private eval systems | Keep held-out tasks, graders, answers, traces, and benchmark results private. |
| 9 | Hosted Ops / GTM | Private hosted systems | Keep billing, admin, telemetry, vendor intent, and account operations out of this repo. |
| 10 | Secrets / Deploy Ops | Private ops only | Keep credentials, Doppler config, live project refs, and deploy environment files out of Git history. |

## Next

- Public Contracts workstream: pin the next storage-free payload contract before adding more SDK/CLI/MCP behavior; keep hardening existing public envelopes when schema/core drift is found.
- SDK / CLI / MCP workstream: promote fixture-only adapters toward `POST /v1/recommendations` only after the non-fixture client contract is pinned.
- Public Surface Contracts workstream: extend OpenAPI only for concrete public routes or route-specific problem types beyond the current shared retry vocabulary.
- Scoring / Materializer Runtime workstream: keep runtime and private evidence material in incubation until the deterministic, storage-free public core is separable.
- Docs / Public Planning workstream: keep `docs/STATUS.md`, `docs/PORTING.md`, `docs/REPO_STRUCTURE.md`, package READMEs, and build logs aligned in the same change.
- Update `NAVIGATION.md` when EvalRank adds or changes public API routes, UI routes, deeplinks, or navigation-critical docs.

## Left

- Public repo: additional storage-free contracts, schemas, SDK/CLI/MCP behavior, public examples, additional routes/problem types, UI navigation docs, and reproducible public evaluation fixtures.
- Private/Syndai or hosted systems: data-plane tables, Supabase migrations, entity graph persistence, evidence ledger, Stage-2+ scorer/materializer rows, private trust/security policy runtime, engine materializer, production telemetry, governance operations, billing/admin, and GTM fleet.
- Private evaluation systems: held-out tasks, graders, answers, traces, benchmark outputs, and proprietary ranking experiments.

## Update Rules

- Update this file when a feature lands, a wave gate changes, or an item moves between `Next`, `In Progress`, and `Built`.
- Keep dated build logs under `docs/build-log/` for immutable-ish snapshots; keep this file current.
