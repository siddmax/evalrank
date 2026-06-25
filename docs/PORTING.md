# EvalRank Public Porting Map

This repo is public. Port only artifacts that are portable, sanitized, and useful without private Syndai/Finn/Savida context.

Last reviewed: 2026-06-26

## Default Rule

- Public by default: contracts, schemas, SDK boundaries, CLI/MCP interfaces, examples, public method notes, repo hygiene, and deterministic boundary checks.
- Private by default: secrets, live DB operations, customer data, production telemetry, private evidence rows, held-out benchmark tasks or answers, billing/admin internals, vendor intent data, hosted-product-only workflows, and private Syndai/Finn/Savida integration code.
- When unsure, keep the source private and port a short public summary instead.
- Do not copy raw private planning docs into this repo. Rewrite as public-safe summaries with synthetic examples.

## Already Public

- Apache-2.0 repository scaffold and package boundaries.
- Root and scoped `AGENTS.md`, plus `CLAUDE.md` shim.
- Public progress docs: `docs/STATUS.md` and `docs/REPO_STRUCTURE.md`.
- Public boundary checker and default unit tests.
- Core Python capability fingerprint, raw entry, evaluation request, candidate set, stage candidate, evidence item, result row, ranking group, evidence set, exclusion, `the_call`, recommendation, and entity reference contracts.
- Public JSON Schemas for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, evidence sets, exclusions, ranked entities, recommendations with closed ranking groups, evidence items, and retry-aware RFC 9457 Problem Details.
- Public OpenAPI 3.1.1 contract for `GET /v1/use-cases` and `POST /v1/recommendations`, including reusable Problem Details responses and retry/rate-limit header contracts.
- Pinned public `methodology_version` format: `YYYY-MM-DD.SEQ.slug`.
- Direct `main` push workflow for the scratch-build phase.
- `make check` public local/CI gate.
- W0 public exit packet and W1 entity/evidence contract plan.
- Storage-free capability fingerprints, evaluation requests, candidate sets, stage candidates, result rows, evidence sets, exclusions, entity references, evidence items, public fixtures, and schemas.
- Python SDK package metadata and public core contract re-exports.
- TypeScript SDK package metadata and mirrored public contract types/constants, including public Problem Details codes and shape.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Runnable public fixture example.
- Public scoring-stage vocabulary, use-case taxonomy method note, and method-boundary notes.
- Public progress router for deciding which private EvalRank workstream owns each future port.
- Public recommendation join aliases: `recommendation_id`, `recommend_id`, and `search_run_id`.
- Public `RawEntry` contract and deterministic `raw-entry` fixture surfaces.
- Public `CandidateSet` contract and deterministic `candidate-set` fixture surfaces.
- Public `StageCandidate` contract and deterministic `stage-candidate` fixture surfaces.
- Public `ResultRow` contract and deterministic `result-row` fixture surfaces.
- Public `UseCaseCatalog` contract, deterministic `use-cases` fixture surfaces, and `GET /v1/use-cases` route contract.
- Public `RankingGroup` contract and deterministic `ranking-group` fixture surfaces for `kind-grouped` recommendations.
- Public `EvidenceSet` contract and deterministic `evidence-set` fixture surfaces.
- Public `Exclusion` contract and deterministic `exclusion` fixture surfaces.
- Public structured `the_call` contract embedded in recommendation fixtures.
- Public `NAVIGATION.md` route map for the first API contract.

## Ported To Date

| Workstream | Public artifact now in this repo | Private material intentionally excluded |
| --- | --- | --- |
| Public Contracts | `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `RankingGroup`, `EvidenceSet`, `Exclusion`, `TheCall`, `RankedEntity`, `Recommendation`, public recommendation ID aliases, `EntityRef`, constants, and synthetic fixture factories. | Source adapters, graph lookup, storage tables, production entity rows, production result rows, customer context, private score semantics, cross-kind score normalization, benchmark weights, IRT clusters, scorer thresholds, Stage-2+ scorer rows, gate policy, private reason taxonomy, hosted HMAC derivation. |
| Methods / Schemas | JSON Schemas for public payloads, the pinned public `methodology_version` format, the public scoring-stage vocabulary including `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, and `Exclusion`, and the public use-case taxonomy method note. | Proprietary weights, thresholds, held-out eval definitions, benchmark answers, confidence policy, synthesis rules, private exclusion policy, private ranking experiments, and private scorer-stage internals. |
| SDK / CLI / MCP | Python SDK re-exports, TypeScript public types/constants, deterministic CLI fixture command, and deterministic MCP fixture adapter, including `raw-entry`, `candidate-set`, `stage-candidate`, `result-row`, `use-cases`, `ranking-group`, `evidence-set`, and `exclusion`. | Live service clients, auth, tenant/project operations, production evidence lookup, source adapters, gate policy, and hosted-only workflows. |
| Public Surface Contracts | OpenAPI 3.1.1 contract for `GET /v1/use-cases` and `POST /v1/recommendations` over existing public schemas and reusable RFC 9457 Problem Details responses for malformed requests, validation errors, rate limits, temporary unavailability, and upstream timeouts. | Hosted auth, tenant logic, receipt storage, HMAC-backed IDs, private DTOs, private problem types, live rate-limit enforcement, live routing, and deployment wiring. |
| Examples | `examples/public_fixture.py` runnable synthetic fixture output. | Customer demos, production evidence rows, private traces, and held-out eval examples. |
| Open-Core Boundary / CI | Boundary scanner, unit tests, package license/notice checks, and default `make check`. | Private repo checks, Doppler config, live project refs, and deployment credentials. |
| Docs / Public Planning | `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, this porting map, package READMEs, and dated build logs. | Raw private planning docs, private customer examples, operational runbooks, and held-out eval detail. |

## Workstream Router

Use this table before copying anything from private EvalRank planning into this public repo.

| Private-side artifact or change | Public destination | Workstream owner | Public handling |
| --- | --- | --- | --- |
| Storage-free payload contracts, candidate sets, stage candidates, result rows, evidence sets, exclusions, identifier aliases, and JSON-compatible request/response shapes | `packages/core`, `schemas`, SDK types | Public Contracts | Port when the shape stands alone with synthetic fixtures and schema drift tests. |
| Recommendation ID aliases (`recommendation_id`, `recommend_id`, `search_run_id`) | `packages/core`, `schemas`, SDK types | Public Contracts | Public alias contract can move here; hosted HMAC derivation, route receipts, and secret keys stay private until a public route contract exists. |
| OpenAPI, route schemas, REST/MCP parity contracts | `schemas`, route docs, `NAVIGATION.md` | Public Surface Contracts | Initial public route contracts and shared retry-aware Problem Details contract are ported; add more only after a concrete public route exists, and do not copy private DTOs, auth flows, tenant logic, private problem types, hosted-only response fields, or live throttling behavior. |
| CLI/MCP/SDK behavior beyond fixtures | `packages/cli`, `packages/mcp`, `packages/sdk-*` | SDK / CLI / MCP | Implement one pinned public contract at a time, with deterministic tests and no live private service dependency. |
| Public method vocabulary and non-proprietary scoring explanations | `methods`, `schemas`, `docs` | Methods / Schemas | Rewrite as sanitized public notes; omit proprietary weights, thresholds, held-out tasks, answers, traces, and private benchmark outputs. |
| Live candidate resolution, source adapters, and graph lookup | Private incubation first | Scoring / Materializer Runtime | Keep private until it can run on public inputs without private evidence rows, production metadata, hosted workers, or proprietary tuning. |
| Stage-2+ scorer rows, IRT/theta/trust features, LLM tie-break fields, and conformal shortlist metadata | Private incubation first | Scoring / Materializer Runtime | Keep private until each field is storage-free, public-input-only, and stripped of proprietary tuning, thresholds, and held-out eval signal. |
| Deterministic scoring or materializer code | Future core/runtime package only after split | Scoring / Materializer Runtime | Keep private during incubation unless it can run on synthetic/public inputs without private evidence rows, secrets, or proprietary tuning. |
| Public-boundary, license, CI, fixture, and schema drift checks | `scripts`, `tests`, `.github/workflows` | Open-Core Boundary / CI | Port aggressively when checks prevent private leaks or public contract drift. |
| Repo progress, build order, and sanitized decision summaries | `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, `docs/build-log` | Docs / Public Planning | Summarize decisions; never paste raw private docs, live IDs, customers, or runbooks. |
| Supabase schema bootstrap, migrations, roles, grants, RLS, pg_cron/pgmq, live DB checks | Syndai repo until cutover | DB Bootstrap / Syndai Ops | Keep private while EvalRank incubates in shared Finn/Supabase infrastructure. A future public cutover needs explicit migration ownership and API exposure docs. |
| Hosted deploy, Fly/Doppler/Modal/R2/OpenObserve wiring, production schedulers | Private hosted systems | Hosted Ops / Deploy Ops | Keep out of this repo; only public setup docs may move after secrets and live IDs are removed. |
| Auth, billing, admin, onboarding, tiering, account ops, GTM/vendor intent | Private hosted systems | Hosted Ops / GTM | Keep private unless converted into product-neutral public docs with no customer or operational data. |
| Held-out suites, graders, answer keys, model traces, judge calibration, private benchmark results | Private eval systems | Evaluation Integrity | Never port; publish only synthetic or public reproducible fixtures. |

## Latest Port Review

Reviewed the private-side EvalRank planning and migration surface by category on 2026-06-26. The public repo should keep accepting only artifacts that stand alone without private infrastructure or data.

| Decision | Workstream |
| --- | --- |
| Port storage-free payload contracts, JSON Schemas, synthetic fixtures, package boundaries, public examples, and deterministic boundary checks here. | Public Contracts, Methods / Schemas, SDK / CLI / MCP, Open-Core Boundary / CI, Docs / Public Planning |
| Port REST/OpenAPI contracts here only after a concrete public route contract exists; keep shared retry/error vocabulary public and hosted enforcement private. | Public Surface Contracts |
| Port deterministic runtime code only after it is separable from private data, live workers, proprietary tuning, and hosted-only controls. | Scoring / Materializer Runtime |
| Keep Supabase schema bootstrap, migration runners, roles, workload isolation, live deployment wiring, and operational checks private during incubation. | DB Bootstrap / Syndai Ops |
| Keep held-out tasks, graders, answers, traces, private benchmark results, and judge-calibration material private. | Evaluation Integrity |
| Keep telemetry operations, billing/admin, vendor intent, account operations, private integrations, credentials, and live project refs out of this repo. | Hosted Ops / GTM, Secrets / Deploy Ops |

Public docs may summarize private planning decisions, but must not copy raw private plans, live identifiers, customer examples, runbooks, production rows, or held-out evaluation details.

## Current Private-Side Scan

The latest private-side scan found EvalRank planning material in private spec, API, data/methodology, relation-graph, and build-readiness docs. Treat those docs as inputs for sanitized public summaries only; do not copy them into this repo.

| Private-side source area | Public action | Owning workstream |
| --- | --- | --- |
| Storage-free contract vocabulary from API and build-readiness planning | Port one pinned payload at a time with core dataclasses, JSON Schemas, fixtures, SDK types, CLI output, MCP output, and drift tests. `StageCandidate` is now ported as the Stage-1 retrieval row; `ResultRow` is now ported as the public ingested-result provenance envelope. | Public Contracts, SDK / CLI / MCP |
| Public API route shapes and Problem Details error semantics | Shared retry-aware Problem Details semantics are ported; port only concrete public route contracts after that, and keep hosted auth, tenant logic, receipt storage, private DTOs, live throttling, and private problem types out. | Public Surface Contracts |
| Public use-case taxonomy names, definitions, entity-kind spans, safety-overlay policy, and sanitized method explanation | Ported as a storage-free `UseCaseCatalog` contract, synthetic fixture, schema, SDK/CLI/MCP parity surface, `GET /v1/use-cases` OpenAPI route contract, and public method note. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Methods / Schemas |
| Public recommendation comparability discriminator and ranking-group row shape | Ported as closed `RankingGroup` rows for `kind-grouped` responses; this only says groups are ranked within one entity type. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Use-case benchmark weights, IRT fit clusters, benchmark crosswalk, confidence policies, and thin-coverage/synthesis details | Keep private during incubation; later publish only sanitized method explanations that omit weights, held-out tasks, private corpora, proprietary thresholds, and benchmark outputs. | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |
| Public scoring-stage names, use-case taxonomy, trust/freshness vocabulary, and method-boundary explanations | Scoring-stage and use-case taxonomy notes are ported; future notes must omit formulas, thresholds, held-out eval details, private benchmark outputs, and production traces. | Methods / Schemas |
| Boundary checks, license/notice hygiene, schema drift tests, and secret/private-data guards | Port aggressively when they reduce public leak risk or contract drift. | Open-Core Boundary / CI |
| Supabase schema, migrations, grants/RLS, workload isolation, live DB checks, and shared Finn deployment details | Keep private until EvalRank owns persistence or its own Supabase project; then design a public migration ownership plan. | DB Bootstrap / Syndai Ops |
| Deterministic scorer/materializer runtime and entity/evidence graph behavior | Incubate privately until public-input-only pieces are separable from proprietary tuning, production rows, live workers, and source adapters. | Scoring / Materializer Runtime |
| Held-out suites, synthetic internal corpora, graders, answers, calibration traces, and private benchmark outputs | Never port; publish only synthetic or public reproducible fixtures. | Evaluation Integrity |
| Hosted deploy, telemetry, billing/admin, vendor intent, account operations, credentials, and live project refs | Keep private unless later rewritten into product-neutral public docs with all operational detail removed. | Hosted Ops / GTM, Secrets / Deploy Ops |

## Current Port-Over Assessment

Use this table for the next port decision. The destination is this public repo only when the artifact is portable without private data, secrets, live infrastructure, or proprietary hosted behavior.

| Candidate change | Port decision | Workstream |
| --- | --- | --- |
| Public repo scaffold, package boundaries, license/notice files, CI, and deterministic public-boundary checks | Already ported; keep strengthening leak classes as they are discovered. | Open-Core Boundary / CI |
| Storage-free public payloads and aliases currently represented by core dataclasses and JSON Schemas | Already ported for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, ranking groups, evidence sets, exclusions, `the_call`, ranked entities, recommendations, recommendation aliases, entity refs, and evidence items. | Public Contracts |
| Public fixture surfaces across core, SDKs, CLI, MCP, and examples | Already ported for deterministic synthetic fixtures only, including candidate-set, stage-candidate, result-row, use-cases, ranking-group, evidence-set, and exclusion fixtures. | SDK / CLI / MCP, Examples |
| Public scoring-stage vocabulary and use-case taxonomy method | Already ported as method-boundary notes, including `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, ranked use-case policy, safety overlay policy, and cross-kind grouping guidance, without formulas, thresholds, private eval data, or benchmarks. | Methods / Schemas |
| `RawEntry` ingestion-normalization shape | Ported as a storage-free contract with synthetic fixtures and deterministic content hash; source adapters, production metadata, and live fetch behavior stay private. | Public Contracts |
| `CandidateSet` candidate-resolution shape | Ported as a storage-free list of public `EntityRef` candidates; live candidate resolution, source adapters, graph lookup, and production entity rows stay private. | Public Contracts, Methods / Schemas |
| `StageCandidate` Stage-1 retrieval row | Ported as a storage-free candidate fingerprint plus public `EntityRef`, fused score, RRF ranks, and retrieval provenance; Stage-2+ scorer fields, graph lookup, source adapters, storage, telemetry, and private tuning stay private. | Public Contracts, Methods / Schemas |
| `ResultRow` ingested result provenance envelope | Ported as a storage-free row with benchmark, harness, raw-score unit, provenance, public flags, and verification state; source adapters, production rows, private benchmark material, scorer fitting, and storage tables stay private. | Public Contracts, Methods / Schemas |
| `EvidenceSet` evidence-attachment shape | Ported as a storage-free list of public `EvidenceItem` rows; empty evidence lists support abstention or no-evidence paths. Live evidence lookup, evidence-ledger persistence, source adapters, production traces, and private rows stay private. | Public Contracts, Methods / Schemas |
| `Exclusion` exclusions-with-reasons shape | Ported as a storage-free subject plus public reason/detail row; Stage-0 gate policy, private safety taxonomy, constraint evaluation, and production traces stay private. | Public Contracts, Methods / Schemas |
| Public `the_call` / decision-confidence response shape | Ported as a nested recommendation contract with no proprietary thresholds, held-out evidence floors, or private confidence tuning. | Public Contracts, Methods / Schemas |
| REST/OpenAPI contract | Concrete route contracts ported for `GET /v1/use-cases` and `POST /v1/recommendations`; public errors use reusable Problem Details responses plus retry/rate-limit headers; keep private auth, tenant logic, hosted receipt internals, private problem types, live throttling, and app DTOs out. | Public Surface Contracts |
| Use-case taxonomy and `/v1/use-cases` route contract | Ported as a finite public catalog with slugs, display names, one-line definitions, entity-kind spans, ranked-vs-overlay policy, safety overlay, and sanitized method note; benchmark weights, IRT clusters, confidence policy, synthesis/coverage rules, and live table/storage semantics stay private. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Methods / Schemas |
| Recommendation comparability and ranking groups | Ported as storage-free `RankingGroup` rows for within-kind rankings only; cross-kind normalization, scorer internals, and private score semantics stay private. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Recommendation receipt route and HMAC-backed hosted ID derivation | Do not port yet. Public aliases are enough for open-core interoperability; secret-backed derivation belongs with hosted route design. | Public Surface Contracts, Hosted Ops / Deploy Ops |
| Entity graph tables, evidence ledger storage, methodology table, migrations, grants, RLS, and live DB checks | Keep in Syndai/private systems until EvalRank owns persistence or its own Supabase project. | DB Bootstrap / Syndai Ops |
| Deterministic scorer and materializer runtime | Incubate privately first, then split only public-input-only pieces that do not depend on production rows, private workers, or proprietary tuning. | Scoring / Materializer Runtime |
| SDK/CLI/MCP behavior beyond fixtures | Port one public contract at a time after the corresponding contract and schema are pinned. | SDK / CLI / MCP |
| UI routes, API-route navigation docs, deeplinks, and `NAVIGATION.md` | API route navigation is ported for the first public route; UI/deeplink docs wait until those surfaces exist. | Public Surface Contracts, Docs / Public Planning |
| Hosted ops, telemetry, billing/admin/GTM, vendor intent, credentials, deploy files, live project refs, private integrations, and account operations | Keep private unless later rewritten as product-neutral public docs with all operational detail removed. | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out suites, graders, answer keys, traces, judge calibration, private benchmark results, and proprietary ranking experiments | Never port. Publish only synthetic or public reproducible fixtures. | Evaluation Integrity |

## Porting Decisions

| Artifact or workstream | Destination | Owner workstream | Status |
| --- | --- | --- | --- |
| Public contract dataclasses and JSON Schemas | This repo | Public Contracts | Capability fingerprint, raw entry, request, candidate set, stage candidate, result row, use-case catalog, ranking group, evidence set, exclusion, `the_call`, recommendation, entity, and evidence slices ported |
| Use-case taxonomy catalog | This repo | Public Contracts, Public Surface Contracts | Ported; only taxonomy contract, fixture, schema, SDK/CLI/MCP surfaces, and `GET /v1/use-cases` route contract moved |
| Recommendation join aliases | This repo | Public Contracts | Ported; hosted HMAC derivation stays private |
| Entity references, evidence items, and evidence-item schema | This repo | Public Contracts | Ported |
| Repo boundary checks, license hygiene, and CI gates | This repo | Open-Core Boundary / CI | Partly ported |
| Sanitized build-readiness summaries from Syndai planning docs | This repo | Docs / Public Planning | In progress |
| Public build-order and wave status | This repo | Docs / Public Planning | In progress |
| Public scoring-stage vocabulary, use-case taxonomy method, and method boundaries | This repo | Methods / Schemas | Public boundary notes ported |
| REST/OpenAPI contracts | This repo | Public Surface Contracts | `GET /v1/use-cases`, `POST /v1/recommendations`, and retry-aware Problem Details contracts ported |
| SDK, CLI, and MCP implementations | This repo | SDK / CLI / MCP | Python SDK re-export, TypeScript public types, CLI fixture command, and MCP fixture adapter ported, including candidate-set, stage-candidate, result-row, use-cases, ranking-group, evidence-set, and exclusion fixture surfaces |
| Public methodology notes | This repo | Methods / Schemas | Scoring-stage and use-case taxonomy notes ported; future notes only after removing held-out and proprietary details |
| Deterministic scorer/materializer runtime | Private incubation first | Scoring / Materializer Runtime | Port later only if storage-free and public-input-only |
| Finn/Supabase `evalrank` schema bootstrap and migration runner | Syndai repo | DB Bootstrap / Syndai Ops | Keep private during incubation |
| Secrets, Doppler config, live project refs, and deployment credentials | Private ops only | Secrets / Deploy Ops | Never port |
| Production evidence graph rows, telemetry, and customer traces | Private hosted systems | Hosted Ops | Never port |
| Held-out fixtures, graders, answers, traces, and benchmark results | Private eval systems | Evaluation Integrity | Never port |
| Billing, admin, GTM, vendor intent, and account-operation flows | Private hosted systems | Hosted Ops / GTM | Keep private unless sanitized as public docs |

## Port Now

- Additional storage-free Python contracts and JSON Schemas when a new public payload is pinned.
- Additional OpenAPI routes only when a concrete public route contract exists.
- Public Problem Details extensions only when they are product-neutral and do not expose hosted internals. Shared `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url` are now ported.
- Public identifier aliases that are deterministic, non-secret, and useful for interoperability.
- Synthetic public fixtures that prove contract shape without using production data and use only public catalog slugs.
- Public runnable examples that consume only synthetic fixtures.
- Deterministic checks that prevent private imports, secrets, private data paths, and missing package hygiene.
- Public build logs that summarize decisions without exposing private projects, credentials, customers, held-out tasks, or live telemetry.
- Package README and agent guidance needed for contributors to work inside the public repo.
- Additional TypeScript SDK source only when the package-level check and repo tests prove the public contract shape.

## Port Later

- Additional REST/OpenAPI surfaces after concrete route contracts exist.
- Route-specific public problem types after their public semantics are stable and separable from hosted internals.
- Recommendation receipt routes and HMAC-backed hosted identifiers after public route semantics and secret handling are designed.
- Full REST/OpenAPI, CLI, SDK, and MCP behavior beyond public fixtures after concrete public contracts are pinned.
- Source adapters, live fetch behavior, and candidate-resolution graph lookup after they can run without private service dependencies or production metadata.
- Public scoring method details after proprietary thresholds, held-out eval details, and private ranking experiments are removed.
- Deterministic scorer/materializer runtime after it is split from private evidence rows, hosted workers, and proprietary tuning.
- Persistence migrations only after EvalRank owns its own deploy/release path or has its own Supabase project.
- UI route docs after routes, deeplinks, or navigation-critical UI docs exist.

## Never Port

- Secrets, tokens, Doppler config, environment files, live project refs, and deployment credentials.
- Customer data, production evidence rows, production telemetry, or account-operation traces.
- Held-out benchmark tasks, answers, graders, traces, and private result tables.
- Private Syndai/Finn/Savida integration code, internal billing/admin flows, and hosted-only vendor intent operations.

## Porting Checklist

Before moving anything into this repo, verify:

- It contains no secrets, tokens, environment files, or live credential material.
- It contains no customer data, production telemetry, private evidence rows, or account-operation traces.
- It contains no held-out benchmark tasks, answers, graders, model traces, or private result tables.
- It does not import or depend on private Syndai/Finn/Savida packages.
- It does not require live database access or private Supabase privileges to understand or test.
- It does not expose proprietary hosted-product workflows that are not part of the open core.
- It does not expose private HMAC keys, hosted receipt derivation, live route IDs, or production project references.
- Its license is compatible with Apache-2.0 public distribution.
- It can pass review as if the full Git history were public forever.
- `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, `TESTS.md`, and the nearest `AGENTS.md` stay current when the port changes scope or checks.
- `python3 scripts/check_public_boundary.py --root .` and `python3 -m unittest discover tests` pass.

## Current Workstreams

- Public Contracts: pin core payloads and schema compatibility.
- Open-Core Boundary / CI: keep deterministic public-boundary guards current before larger ports.
- DB Bootstrap / Syndai Ops: keep shared Finn/Supabase migrations private until EvalRank owns persistence.
- Methods / Schemas: publish only reusable method notes and schemas.
- SDK / CLI / MCP: implement public clients once contracts stabilize.
- Public Surface Contracts: own OpenAPI, REST, route, and navigation docs when concrete public routes exist.
- Scoring / Materializer Runtime: incubate private runtime until reusable deterministic pieces can be separated safely.
- Hosted Ops / GTM: keep private operational workflows outside this repo.
- Evaluation Integrity: keep held-out materials private and publish only reproducible public fixtures.
- Secrets / Deploy Ops: keep credentials, live project refs, deployment environment files, and private service config out of Git history.
- Docs / Public Planning: keep this file, `docs/STATUS.md`, and `docs/REPO_STRUCTURE.md` aligned.

## External Guardrails

- GitHub push protection can block supported secrets before they enter a repository: https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- GitHub secret scanning can detect hardcoded credentials in repository history, but prevention is cheaper than cleanup: https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns
- If sensitive data reaches Git history, treat it as compromised, rotate credentials, and follow a coordinated removal process.
- Supabase custom schemas must be deliberately exposed and granted for API access; EvalRank incubation uses private schema bootstrap outside this public repo: https://supabase.com/docs/guides/api/using-custom-schemas
- For public API design, prefer a dedicated exposed API schema and keep internal tables/helpers in non-exposed schemas; grants and RLS together decide what API roles can touch: https://supabase.com/docs/guides/api/securing-your-api
