# EvalRank Public Porting Map

This repo is public. Port only artifacts that are portable, sanitized, and useful without private Syndai/Finn/Savida context.

Last reviewed: 2026-06-26

## Default Rule

- Public by default: contracts, schemas, SDK boundaries, CLI/MCP interfaces, examples, public method notes, repo hygiene, and deterministic boundary checks.
- Private by default: secrets, live DB operations, customer data, production telemetry, private evidence rows, held-out benchmark tasks or answers, billing/admin internals, vendor intent data, hosted-product-only workflows, and private Syndai/Finn/Savida integration code.
- When unsure, keep the source private and port a short public summary instead.
- Do not copy raw private planning docs into this repo. Rewrite as public-safe summaries with synthetic examples.
- Do not rely on platform secret scanning as the only guard. Run the repo boundary check before every port, and treat anything sensitive that reaches Git history as compromised.
- Public reports, docs, examples, and build logs must not include secrets, exploit details, private benchmark fixtures, customer data, live project refs, or account-operation traces.

## Already Public

- Apache-2.0 repository scaffold and package boundaries.
- Root and scoped `AGENTS.md`, plus `CLAUDE.md` shim.
- Public progress docs: `docs/STATUS.md` and `docs/REPO_STRUCTURE.md`.
- Public boundary checker and default unit tests.
- Public Python package metadata drift guard for package names, versions, licenses, Python floor, dependency edges, and CLI entrypoint.
- Exact package README metadata drift guard for public package names, imports, dependencies, entrypoint, licenses, and TypeScript SDK manifest metadata.
- Exact CLI and MCP README drift guards for public fixture commands, route commands, fixture kinds, and tool names.
- Exact schema README drift guard for public schema and OpenAPI filenames.
- Exact methods README drift guard for public method-note filenames.
- Exact repo structure drift guard for public top-level directories and package directories.
- Exact `CLAUDE.md` shim drift guard for the required `@AGENTS.md` reference.
- Scoped `AGENTS.md` coverage drift guard for public work areas.
- Core Python capability fingerprint, raw entry, evaluation request, candidate set, stage candidate, evidence item, result row, ranking group, evidence set, exclusion, `the_call`, abstention, recommendation, and entity reference contracts.
- Public JSON Schemas for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, evidence sets, exclusions, ranked entities, recommendations with closed ranking groups and public abstention objects, evidence items, and retry-aware RFC 9457 Problem Details.
- Public OpenAPI 3.1.1 contract for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, including reusable Problem Details responses and retry/rate-limit header contracts.
- Python `ProblemDetails` contract and `PROBLEM_CODES` re-exports for the public RFC 9457 error payload shape.
- Deterministic public `ProblemDetails` fixture via `problem` fixture kind and `sample_problem_details()`.
- Pinned public `methodology_version` format: `YYYY-MM-DD.SEQ.slug`.
- Direct `main` push workflow for the scratch-build phase.
- `make check` public local/CI gate.
- W0 public exit packet and W1 entity/evidence contract plan.
- Storage-free capability fingerprints, evaluation requests, candidate sets, stage candidates, result rows, evidence sets, exclusions, entity references, evidence items, public fixtures, and schemas.
- Python SDK package metadata, public core contract re-exports, and dependency-free `EvalRankClient` behavior for the public `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` routes.
- Python SDK re-exports for public vocabulary constants shared with core contracts.
- TypeScript SDK package metadata, mirrored public contract types/constants, and dependency-free native `fetch` `EvalRankClient` behavior for the public `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` routes.
- CLI package metadata, deterministic public fixture command, explicit public `use-cases` and `scoring-stages` metadata commands, and explicit public `recommend` command for `POST /v1/recommendations`.
- MCP package metadata, deterministic public fixture adapter, explicit public `evalrank.use_cases` and `evalrank.scoring_stages` metadata tools, and explicit public `evalrank.recommend` tool for `POST /v1/recommendations`.
- Runnable public fixture example.
- Example README drift guard for the public fixture bundle output keys and nested recommendation/scoring-stage contract refs.
- Core and schema README drift guards for the public contract and schema docs.
- Public scoring-stage vocabulary, storage-free `ScoringStageCatalog`, use-case taxonomy method note, and method-boundary notes.
- Public progress router for deciding which private EvalRank workstream owns each future port.
- Public recommendation join aliases: `recommendation_id`, `recommend_id`, and `search_run_id`.
- Public `RawEntry` contract and deterministic `raw-entry` fixture surfaces.
- Public `CandidateSet` contract and deterministic `candidate-set` fixture surfaces.
- Public `StageCandidate` contract and deterministic `stage-candidate` fixture surfaces.
- Public `ResultRow` contract and deterministic `result-row` fixture surfaces.
- Public `UseCaseCatalog` contract, deterministic `use-cases` fixture surfaces, and `GET /v1/use-cases` route contract.
- Public `ScoringStageCatalog` contract and deterministic `scoring-stages` fixture surfaces.
- Public `RankingGroup` contract and deterministic `ranking-group` fixture surfaces for `kind-grouped` recommendations.
- Public `EvidenceSet` contract and deterministic `evidence-set` fixture surfaces.
- Public `Exclusion` contract and deterministic `exclusion` fixture surfaces.
- Public structured `the_call` and abstention contracts embedded in recommendation fixtures.
- Public `score_components` map shape hardened for ranked entities: non-empty public names and 0-1 numeric values only.
- Public recommendation envelope validation hardened for schema-compatible metadata: non-empty rationale/source fields, boolean degradation state, non-negative snapshot lag, and no duplicate ranked entities.
- Public capability fingerprint declared-shape schema hardened to require at least one property, matching the existing core contract.
- Public recommendation comparability schema hardened to pin `single-scale` and `kind-grouped` envelope branches, matching the existing core contract.
- Public `the_call` schema hardened to pin `recommend` and `abstain` branch shapes, matching the existing core contract.
- Public JSON-object fields hardened for evidence item `metadata` and evaluation request `constraints`: object values only, string keys only, and JSON-serializable values only.
- Public primitive and sequence fields hardened for entity refs, freshness dates, request entity-type arrays, ranked-entity integer fields, and non-empty caveat strings.
- Evaluation request `entity_types` are pinned as unique public request metadata in Python and JSON Schema.
- Public string fields hardened for capability fingerprints, raw entries, evidence items, evidence sets, candidate sets, `the_call`, and abstention: actual non-empty strings only.
- Ranked entity `axes.evidence` is closed to public evidence count and trust-tier coverage in schema and TypeScript types.
- TypeScript SDK `NonEmptyArray<T>` mirrors already-public schema `minItems: 1` arrays for request entity types, candidates, retrieval arms, catalogs, stage contract refs, recommendation groups, and ranking groups.
- TypeScript SDK `UseCase` mirrors already-public ranked and veto-overlay branch shapes as a discriminated union.
- TypeScript SDK `TheCall` mirrors already-public `recommend` and `abstain` branch shapes as a discriminated union.
- TypeScript SDK `Recommendation` mirrors already-public `single-scale` and `kind-grouped` branch shapes as a discriminated union.
- Shared public fixture-kind dispatch reused by CLI, MCP, Python SDK, and TypeScript SDK types.
- Public `NAVIGATION.md` route map for the first API contract.
- Public/private porting audit confirming that the current private Syndai dirty worktree contains Memphant spec edits and two Memphant plan files, with no EvalRank public-port candidate.
- Public/private source routing snapshot for the current Syndai EvalRank specs, build-readiness plans, migration bootstrap, doc validators, and UI proof assets.
- Public/private source inventory refresh covering current private EvalRank specs, build plans, proof assets, backend migration assets, repo security settings, and dirty-worktree routing without copying private source text.
- Public/private dirty-worktree recheck confirming the current uncommitted private-side changes still route to Memphant/memory work, not EvalRank public core.
- GitHub public-repo security metadata snapshot showing secret scanning, push protection, and Dependabot security updates enabled.
- Public `SECURITY.md` guidance for private vulnerability reporting, no public sensitive reports, immediate rotation if secrets are exposed, and coordinated remediation when sensitive data reaches Git history.

## Ported To Date

| Workstream | Public artifact now in this repo | Private material intentionally excluded |
| --- | --- | --- |
| Public Contracts | `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `EvidenceSet`, `Exclusion`, `TheCall`, `Abstention`, `ProblemDetails`, `RankedEntity`, `Recommendation`, public recommendation ID aliases, strict public string fields, strict public `score_components`, strict recommendation envelope validation, `EntityRef`, constants, and synthetic fixture factories. | Source adapters, graph lookup, storage tables, production entity rows, production result rows, customer context, private score semantics, cross-kind score normalization, benchmark weights, IRT clusters, scorer thresholds, Stage-2+ scorer rows, gate policy, private reason taxonomy, hosted HMAC derivation, private problem types. |
| Methods / Schemas | JSON Schemas for public payloads, the pinned public `methodology_version` format, strict public score-component map shape, the public scoring-stage vocabulary and storage-free `ScoringStageCatalog` including `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, and `Abstention`, and the public use-case taxonomy method note. | Proprietary weights, thresholds, held-out eval definitions, benchmark answers, confidence policy, synthesis rules, private exclusion policy, private ranking experiments, and private scorer-stage internals. |
| SDK / CLI / MCP | Python SDK re-exports plus dependency-free `EvalRankClient` behavior for the public metadata and recommendation routes; TypeScript native `fetch` `EvalRankClient` behavior for the public metadata and recommendation routes; explicit CLI metadata and recommendation commands; explicit MCP metadata and recommendation tools; TypeScript public types/constants including fixture kinds and abstention; shared public fixture-kind dispatch; deterministic CLI fixture command; and deterministic MCP fixture adapter, including `raw-entry`, `candidate-set`, `stage-candidate`, `result-row`, `problem`, `use-cases`, `ranking-group`, `evidence-set`, and `exclusion`. | Auth, tenant/project operations, production evidence lookup, source adapters, gate policy, hosted-only workflows, service discovery, retries, environment-variable defaults, and hosted receipt behavior. |
| Public Surface Contracts | OpenAPI 3.1.1 contract for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` over existing public schemas and reusable RFC 9457 Problem Details responses for malformed requests, validation errors, rate limits, temporary unavailability, and upstream timeouts. | Hosted auth, tenant logic, receipt storage, HMAC-backed IDs, private DTOs, private problem types, live rate-limit enforcement, live routing, and deployment wiring. |
| Examples | `examples/public_fixture.py` runnable synthetic fixture output plus README coverage for each emitted JSON key. | Customer demos, production evidence rows, private traces, and held-out eval examples. |
| Open-Core Boundary / CI | Boundary scanner, unit tests, package license/notice checks, and default `make check`. | Private repo checks, Doppler config, live project refs, and deployment credentials. |
| Package Metadata | Stdlib checks for Python package names, versions, licenses, Python floor, dependency edges, CLI entrypoint, and package README metadata drift. | Publish credentials, release automation, private package indexes, and hosted deployment wiring. |
| Docs / Public Planning | `docs/STATUS.md`, `docs/REPO_STRUCTURE.md` with exact public directory drift tests, this porting map, package READMEs, and dated build logs. | Raw private planning docs, private customer examples, operational runbooks, and held-out eval detail. |

## Workstream Router

Use this table before copying anything from private EvalRank planning into this public repo.

| Private-side artifact or change | Public destination | Workstream owner | Public handling |
| --- | --- | --- | --- |
| Storage-free payload contracts, candidate sets, stage candidates, result rows, evidence sets, exclusions, abstentions, identifier aliases, and JSON-compatible request/response shapes | `packages/core`, `schemas`, SDK types | Public Contracts | Port when the shape stands alone with synthetic fixtures and schema drift tests. |
| Recommendation ID aliases (`recommendation_id`, `recommend_id`, `search_run_id`) | `packages/core`, `schemas`, SDK types | Public Contracts | Public alias contract can move here; hosted HMAC derivation, route receipts, and secret keys stay private until a public route contract exists. |
| OpenAPI, route schemas, REST/MCP parity contracts | `schemas`, route docs, `NAVIGATION.md` | Public Surface Contracts | Initial public route contracts and shared retry-aware Problem Details contract are ported, including the scoring-stages metadata route; add more only after a concrete public route exists, and do not copy private DTOs, auth flows, tenant logic, private problem types, hosted-only response fields, or live throttling behavior. |
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
| Adjacent Memphant, AgentsDB, memory, or general agent-system planning docs | Their owning private/public workstream, not EvalRank by default | Docs / Public Planning routes only when an EvalRank contract is explicitly extracted | Do not port into this repo unless the extracted artifact is storage-free, product-neutral, synthetic-testable, and public-safe. |

## Immediate Port Routing

Use this queue for the next public-repo decisions. Each row is intentionally phrased as a public artifact or private workstream, not as a raw copy instruction from private docs.

| Candidate change | Destination | Workstream | Handling |
| --- | --- | --- | --- |
| README and repo-structure drift guards for CLI, MCP, core, schemas, examples, docs, packages, and future SDK surfaces | This repo | Open-Core Boundary / CI, Docs / Public Planning | Package manifest, package README, command/tool, schema, method, and repo-structure guards are ported; keep extending when public docs can drift from a current contract or directory. |
| Additional schema or fixture drift checks for already-public payloads | This repo | Open-Core Boundary / CI, Public Contracts | Port now when the check prevents public contract skew or private leakage. |
| Next storage-free payload contract | This repo | Public Contracts, Methods / Schemas | Port only after the shape stands alone with synthetic fixtures, JSON Schema, SDK type/re-export coverage, and no private source adapter dependency. |
| Non-fixture SDK/CLI/MCP behavior for currently public routes | This repo after client semantics are pinned | SDK / CLI / MCP, Public Surface Contracts | Python SDK stdlib metadata/recommendation client, TypeScript native `fetch` metadata/recommendation client, CLI explicit metadata/recommendation commands, and MCP explicit metadata/recommendation tools are now ported; retries, auth, tenant context, live hosted receipts, private DTOs, environment-variable defaults, and production service dependencies stay out until separately pinned. |
| Additional public API routes or route-specific Problem Details | This repo | Public Surface Contracts | Port later only for concrete public routes; shared retry/rate-limit vocabulary is already public. |
| Sanitized scoring and use-case method notes | This repo | Methods / Schemas | Port selectively after removing weights, thresholds, held-out task references, private benchmark outputs, private corpora, and production traces. |
| Public-facing doc-drift checks distilled from Syndai EvalRank validators | This repo only after matching public claims exist | Open-Core Boundary / CI, Docs / Public Planning | Port later as deterministic tests over public docs. Do not copy private spec names, private plan paths, or private-only assertions. |
| Deterministic scorer/materializer components | Private incubation first | Scoring / Materializer Runtime | Split only public-input-only components later; keep proprietary tuning, live workers, private evidence rows, source adapters, and graph persistence out. |
| Supabase schema bootstrap, migrations, grants/RLS, live DB checks, and shared Finn/Supabase operations | Syndai/private systems until an explicit EvalRank persistence cutover exists | DB Bootstrap / Syndai Ops | Keep private. If EvalRank later owns persistence, design the migration ownership and public exposure model before adding migrations here. |
| Hosted auth, telemetry, billing/admin, GTM, vendor intent, deploy config, credentials, and live project refs | Private hosted systems | Hosted Ops / GTM, Secrets / Deploy Ops | Keep private unless rewritten later as product-neutral public docs with all operational identifiers removed. |
| Held-out tasks, graders, answer keys, traces, judge calibration, private benchmark results, and proprietary ranking experiments | Private eval systems only | Evaluation Integrity | Never port. Publish only synthetic or public reproducible fixtures. |

## Recent Public Delta Routing

| Recent change | Port decision | Workstream |
| --- | --- | --- |
| Public fixture bundle now includes raw entry, request, candidate set, stage candidate, evidence item, evidence set, result row, use-case catalog, exclusion, and recommendation outputs with public abstention fields. | Already ported as synthetic public examples only; no customer, production, or held-out rows moved. | Public Contracts, Examples |
| Shared public fixture-kind dispatch now drives CLI, MCP, Python SDK, and TypeScript SDK fixture lists. | Already ported because it reduces public contract drift without adding live service behavior. | SDK / CLI / MCP, Open-Core Boundary / CI |
| `GET /v1/scoring-stages` route contract. | Already ported because `ScoringStageCatalog` is a concrete public metadata contract; live routing, auth, storage, and scorer runtime stay private. | Public Surface Contracts, Methods / Schemas |
| README drift checks for SDK, example, core, and schema surfaces. | Already ported because they are deterministic public-boundary checks. | Open-Core Boundary / CI, Docs / Public Planning |
| Package README metadata drift guard. | Already ported because it binds public package docs to manifest metadata without adding private package indexes, publish credentials, or hosted deploy behavior. | Open-Core Boundary / CI, Docs / Public Planning |
| Package README exact metadata drift guard. | Already ported because it rejects stale extra package metadata docs using only current public manifests and README metadata blocks without adding runtime behavior, publish credentials, private package indexes, or hosted deployment behavior. | Open-Core Boundary / CI, Docs / Public Planning |
| CLI and MCP README exact drift guards. | Already ported because they reject stale extra public command/tool docs using only public constants and README text without adding runtime behavior, private services, or dependencies. | Open-Core Boundary / CI, SDK / CLI / MCP, Docs / Public Planning |
| Schema README exact drift guard. | Already ported because it rejects stale public schema/OpenAPI filename references using only current public files and README text without adding runtime behavior or private material. | Open-Core Boundary / CI, Methods / Schemas, Docs / Public Planning |
| Methods README exact drift guard. | Already ported because it rejects stale public method-note filenames using only current public method docs and README text without adding private methodology, scorer behavior, or dependencies. | Open-Core Boundary / CI, Methods / Schemas, Docs / Public Planning |
| Repo structure exact drift guard. | Already ported because it rejects stale public directory/package ownership docs using only the current public repo tree and `docs/REPO_STRUCTURE.md`, without copying private plans or adding runtime behavior. | Open-Core Boundary / CI, Docs / Public Planning |
| `CLAUDE.md` shim exact drift guard. | Already ported because it rejects agent-entrypoint drift using only the public root shim and `AGENTS.md` convention, without adding runtime behavior or private material. | Open-Core Boundary / CI, Docs / Public Planning |
| Scoped `AGENTS.md` coverage drift guard. | Already ported because it rejects missing local agent guidance for public work areas using only current public directories, without adding private instructions or runtime behavior. | Open-Core Boundary / CI, Docs / Public Planning |
| Nested public fixture README drift checks for recommendation abstention, `the_call`, and scoring-stage output contracts. | Already ported because they keep public examples aligned with existing public contracts without adding private data or runtime behavior. | Open-Core Boundary / CI, Examples |
| Python SDK public vocabulary constant re-exports. | Already ported because they mirror existing public schema/core/TypeScript vocabulary without exposing scorer thresholds, private trust policy, or runtime behavior. | SDK / CLI / MCP, Public Contracts |
| Python `ProblemDetails` contract and public problem-code enum. | Already ported because it mirrors existing OpenAPI/schema/TypeScript public error contracts without exposing hosted auth, tenant context, private problem types, telemetry, or runtime behavior. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP |
| Public Problem Details fixture. | Already ported as a synthetic `problem` fixture so examples, CLI, MCP, Python SDK, and TypeScript fixture kinds can demonstrate the public RFC 9457 shape without hosted error telemetry, tenant context, or private problem types. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Examples |
| Capability fingerprint declared-shape schema hardening. | Already ported because it aligns the public schema with the existing core requirement without adding source adapters, live fetch behavior, private runtime, or DB work. | Public Contracts, Methods / Schemas |
| Recommendation comparability schema hardening. | Already ported because it aligns the public schema with the existing core branch rules without exposing cross-kind normalization, scorer internals, hosted receipts, private runtime, or DB work. | Public Contracts, Methods / Schemas |
| `the_call` branch schema hardening. | Already ported because it aligns the public schema with the existing `recommend`/`abstain` core rules without exposing confidence policy, private abstention taxonomy, scorer internals, hosted receipts, private runtime, or DB work. | Public Contracts, Methods / Schemas |
| Ranked entity score-component map hardening. | Already ported because it closes an existing public payload shape without exposing formulas, weights, or scorer calibration. | Public Contracts, Methods / Schemas |
| Recommendation envelope validation hardening. | Already ported because it aligns the public Python contract with the public schema and blocks duplicate ranked rows without exposing scorer/runtime behavior. | Public Contracts, Methods / Schemas |
| Ranked entity axes shape hardening. | Already ported because it aligns the public schema and TypeScript type with the existing Python `RankedEntity.to_dict()` output without exposing private evidence scoring, weights, formulas, scorer runtime, or persistence. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| TypeScript non-empty array parity. | Already ported because it mirrors existing Python and JSON Schema `minItems: 1` public contracts at compile time without adding runtime validation, service behavior, private data, scorer logic, or persistence. | SDK / CLI / MCP, Public Contracts |
| TypeScript use-case branch parity. | Already ported because it mirrors existing Python and JSON Schema ranked/veto-overlay public branch rules at compile time without exposing private rank-policy tuning, scorer runtime, hosted behavior, or persistence. | SDK / CLI / MCP, Public Contracts |
| TypeScript `the_call` branch parity. | Already ported because it mirrors existing Python and JSON Schema `recommend`/`abstain` public branch rules at compile time without exposing confidence policy, thresholds, scorer internals, hosted receipts, runtime, or DB work. | SDK / CLI / MCP, Public Contracts |
| TypeScript recommendation branch parity. | Already ported because it mirrors existing Python and JSON Schema `single-scale`/`kind-grouped` public branch rules at compile time without exposing cross-kind normalization, scorer internals, hosted receipts, runtime, or DB work. | SDK / CLI / MCP, Public Contracts |
| Evidence metadata and request constraint JSON-object hardening. | Already ported because it prevents invalid public JSON without adding private evidence lookup, source adapters, or policy semantics. | Public Contracts, Methods / Schemas |
| Primitive and sequence field hardening for existing public payloads. | Already ported because it aligns Python contracts with public schemas without adding private runtime behavior; ranked-entity caveats now reject empty strings in both core and schema. | Public Contracts, Methods / Schemas |
| Evaluation request entity-type uniqueness. | Already ported as public request-shape hardening; duplicate target types are rejected without adding candidate resolution, scorer behavior, route implementation, DB work, or private source adapters. | Public Contracts, Methods / Schemas |
| Public string-field hardening for existing public payloads. | Already ported because it aligns the Python contracts with existing string schemas and blocks truthy non-string DTO values without adding source adapters, scorer/runtime behavior, private evidence lookup, DB work, or hosted operations. | Public Contracts, Methods / Schemas |
| Public `Abstention` reason/detail object in recommendation responses. | Already ported because it is a storage-free response shape; evidence-floor thresholds, private confidence policy, private reason taxonomy, scorer/runtime behavior, DB work, and hosted operations stay private. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| `Abstention` output in the public scoring-stage catalog. | Already ported as a storage-free contract reference for `ranking-or-abstention`; thresholds, policy, runtime, and DB behavior stay private. | Methods / Schemas, Public Contracts |
| Private Syndai dirty worktree contained Memphant spec edits plus two Memphant validation/lifecycle plan files during the latest check. | Do not port into EvalRank. Keep out of this public repo unless a future task extracts a concrete EvalRank storage-free contract and strips private context. | Memphant / memory-system workstream, Docs / Public Planning |
| Private Syndai dirty worktree recheck still showed only the Memphant dirty set and no uncommitted EvalRank-specific public-port candidate. | No public port now. Keep the category/path summary only and continue public work on schema/core parity, fixtures, route contracts, and sanitized method notes. | Memphant / memory-system workstream, Public Contracts, Docs / Public Planning |
| Private EvalRank source scan found spec docs, build-readiness plans, migration bootstrap, migration guards, doc validators, and UI proof assets. | Document as routing input only; do not copy raw private docs, proof assets, migration scripts, or private plan text into the public repo. | Docs / Public Planning, Public Surface Contracts, DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Public security-reporting and porting-safety docs were refreshed. | Already ported as docs-only guidance; public reports must not include secrets/private fixtures/customer data, exposed secrets are treated as compromised, and the local boundary scanner remains the required gate. | Docs / Public Planning, Open-Core Boundary / CI, Secrets / Deploy Ops |
| GitHub repository security metadata check. | Public visibility, secret scanning, push protection, and Dependabot security updates are enabled; local public-boundary checks remain required before porting or pushing. | Open-Core Boundary / CI, Secrets / Deploy Ops |
| Python SDK recommendation client behavior. | Already ported as dependency-free HTTP(S)-only `POST /v1/recommendations` request/response JSON handling and Problem Details error surfacing; auth, tenant context, hosted receipts, private DTOs, service discovery, retries, and service dependencies stay private/out. | SDK / CLI / MCP, Public Surface Contracts |
| Python SDK metadata route client behavior. | Already ported as dependency-free HTTP(S)-only `GET /v1/use-cases` and `GET /v1/scoring-stages` JSON handling with shared Problem Details error surfacing; auth, tenant context, hosted receipts, private DTOs, service discovery, retries, environment-variable defaults, database work, and production evidence lookup stay private/out. | SDK / CLI / MCP, Public Surface Contracts |
| CLI recommendation command behavior. | Already ported as explicit HTTP(S)-only `--base-url` plus file/stdin public request JSON handling around the Python SDK client; hidden network calls, auth, retries, environment-variable defaults, private DTOs, database work, and production evidence lookup stay out. | SDK / CLI / MCP, Public Surface Contracts |
| TypeScript SDK recommendation client behavior. | Already ported as dependency-free native `fetch` `POST /v1/recommendations` request/response JSON handling and Problem Details error surfacing; auth, tenant context, hosted receipts, private DTOs, service discovery, retries, environment-variable defaults, and service dependencies stay private/out. | SDK / CLI / MCP, Public Surface Contracts |
| TypeScript SDK metadata route client behavior. | Already ported as dependency-free native `fetch` `GET /v1/use-cases` and `GET /v1/scoring-stages` JSON handling with shared Problem Details error surfacing; auth, tenant context, hosted receipts, private DTOs, service discovery, retries, environment-variable defaults, database work, and production evidence lookup stay private/out. | SDK / CLI / MCP, Public Surface Contracts |
| CLI metadata command behavior. | Already ported as explicit HTTP(S)-only `use-cases --base-url` and `scoring-stages --base-url` JSON handling around the Python SDK client; hidden network calls, auth, retries, environment-variable defaults, private DTOs, database work, and production evidence lookup stay out. | SDK / CLI / MCP, Public Surface Contracts |
| MCP recommendation tool behavior. | Already ported as explicit HTTP(S)-only `evalrank.recommend` JSON handling around the Python SDK client; hidden network calls, auth, retries, environment-variable defaults, hosted receipts, private DTOs, database work, and production evidence lookup stay out. | SDK / CLI / MCP, Public Surface Contracts |
| MCP metadata tool behavior. | Already ported as explicit HTTP(S)-only `evalrank.use_cases` and `evalrank.scoring_stages` JSON handling around the Python SDK client; hidden network calls, auth, retries, environment-variable defaults, hosted receipts, private DTOs, database work, and production evidence lookup stay out. | SDK / CLI / MCP, Public Surface Contracts |
| Runtime scorer/materializer and graph/evidence lookup. | Keep private during incubation; split only public-input-only code later. | Scoring / Materializer Runtime |
| DB migrations, Supabase bootstrap, grants/RLS, live checks, and deploy wiring. | Keep in Syndai/private systems until an explicit EvalRank persistence cutover exists. | DB Bootstrap / Syndai Ops, Hosted Ops / Deploy Ops |
| Held-out tasks, graders, answer keys, traces, judge calibration, and benchmark outputs. | Never port. | Evaluation Integrity |

## Latest Port Review

Reviewed the private-side EvalRank planning and migration surface by category on 2026-06-26. The public repo should keep accepting only artifacts that stand alone without private infrastructure or data.

| Decision | Workstream |
| --- | --- |
| Port storage-free payload contracts, JSON Schemas, synthetic fixtures, package boundaries, public examples, and deterministic boundary checks here. | Public Contracts, Methods / Schemas, SDK / CLI / MCP, Open-Core Boundary / CI, Docs / Public Planning |
| Port REST/OpenAPI contracts here only after a concrete public route contract exists; keep shared retry/error vocabulary public and hosted enforcement private. | Public Surface Contracts |
| Port deterministic runtime code only after it is separable from private data, live workers, proprietary tuning, and hosted-only controls. | Scoring / Materializer Runtime |
| Keep Supabase schema bootstrap, migration runners, roles, workload isolation, live deployment wiring, and operational checks private during incubation. | DB Bootstrap / Syndai Ops |
| Keep private EvalRank spec docs, build-readiness plans, UI proof assets, and doc validators out of this repo unless a public-safe contract or deterministic public doc check is deliberately extracted. | Docs / Public Planning, Open-Core Boundary / CI, Public Surface Contracts |
| Keep held-out tasks, graders, answers, traces, private benchmark results, and judge-calibration material private. | Evaluation Integrity |
| Keep telemetry operations, billing/admin, vendor intent, account operations, private integrations, credentials, and live project refs out of this repo. | Hosted Ops / GTM, Secrets / Deploy Ops |

Public docs may summarize private planning decisions, but must not copy raw private plans, live identifiers, customer examples, runbooks, production rows, or held-out evaluation details.

## Latest Private Source Inventory

Reviewed on 2026-06-26 from the private Syndai checkout. This is an inventory and router only; none of the private source text, proof assets, migrations, or operational details should be copied into this public repo.

| Private-side source | Observed shape | Public handling | Workstream owner |
| --- | --- | --- | --- |
| Private EvalRank spec corpus | 25 private Markdown spec docs covering product, architecture, data/methodology, API, trust, UI, legal, telemetry, governance, and related planning. | Treat as input only. Extract one storage-free contract, public route shape, or sanitized method note at a time with synthetic fixtures and tests. | Public Contracts, Public Surface Contracts, Methods / Schemas, Docs / Public Planning |
| Private EvalRank build-plan corpus | 6 private build-readiness docs: relations graph, master plan, foundation/services, pinned decisions, validation playbook, and README. | Port only public-safe build-order/status summaries and workstream routing. Do not copy account/service assumptions, live operations, or private runbooks. | Docs / Public Planning, Open-Core Boundary / CI |
| Private UI/proof asset corpus | 18 private UI/proof assets and generated HTML/CSS proof files. | Keep private until public UI routes or public product docs intentionally exist; later use generated or synthetic public assets only. | Public Surface Contracts, Hosted Ops / GTM |
| Private backend migration and guard assets | 5 private migration, guard, runner, and test assets tied to shared Finn/Supabase operations. | Keep private. If EvalRank later owns persistence, design a new public migration subsystem instead of copying live scripts. | DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Current Syndai dirty worktree | Uncommitted and untracked private edits remain in Memphant specs and Memphant validation/lifecycle plans. | Do not port to EvalRank. Route to Memphant / memory-system workstream unless a future task extracts a concrete EvalRank contract. | Memphant / memory-system workstream |
| GitHub repo security metadata for `siddmax/evalrank` | Public visibility, secret scanning, push protection, and Dependabot security updates are enabled. | Keep local boundary checks mandatory; platform scanning is a backstop, not the public/private decision engine. | Open-Core Boundary / CI, Secrets / Deploy Ops |

## Next Port Slices

| Order | Slice | Destination | Guardrail |
| --- | --- | --- | --- |
| 1 | More schema/core parity hardening for already-public contracts. | This repo. | Must be storage-free, covered by focused tests, and aligned with JSON Schema. |
| 2 | Additional deterministic fixture and README drift checks for public packages/examples. | This repo. | Package manifest README drift guard is ported; continue only with synthetic fixtures, public docs, and local checks. |
| 3 | Additional non-fixture client semantics for currently public routes. | This repo after each client contract is pinned. | Python SDK HTTP(S)-only metadata and recommendation success/error JSON handling, TypeScript native `fetch` metadata and recommendation success/error JSON handling, CLI explicit HTTP(S)-only metadata commands, CLI explicit HTTP(S)-only file/stdin recommendation command, and MCP explicit metadata/recommendation tools are ported. Exclude auth, tenants, hosted receipts, live service dependencies, private DTOs, retries, service discovery, environment-variable defaults, local file URLs, and production evidence lookup. |
| 4 | Additional route-specific public Problem Details or OpenAPI surfaces. | This repo after concrete public routes exist. | Keep hosted enforcement, live throttling, private problem types, and deployment wiring private. |
| 5 | Sanitized method notes distilled from private methodology docs. | This repo only after private material is removed. | Omit weights, thresholds, held-out tasks, benchmark outputs, private corpora, traces, and proprietary tuning. |
| 6 | Public-facing doc-drift checks distilled from private validators. | This repo only when public docs carry the matching claim. | Do not copy private spec names, private plan paths, or private-only assertions. |

Do not start public DB migrations, source adapters, graph/evidence lookup, runtime scorer/materializer, UI proof asset ports, hosted ops, GTM, telemetry, or eval-integrity material until the owning private workstream produces a separable public contract.

## Current Port Decision

Rechecked on 2026-06-26 after the latest public SDK metadata-route slice and private-side worktree scan.

| Decision | Workstream | Public handling |
| --- | --- | --- |
| Continue porting schema/core parity hardening for already-public payloads. | Public Contracts, Methods / Schemas | Safe for this repo when covered by focused tests and no private source adapter or scorer policy is added. |
| Continue adding deterministic docs, README, schema, fixture, and public-boundary drift checks. | Open-Core Boundary / CI, Docs / Public Planning | Safe for this repo when checks run locally and use only public docs/contracts. |
| Extend non-fixture public-route client behavior only after each request/response/client error semantic is pinned. | SDK / CLI / MCP, Public Surface Contracts | Python SDK HTTP(S)-only metadata and recommendation success/error JSON handling, TypeScript native `fetch` metadata and recommendation handling, CLI explicit HTTP(S)-only metadata and recommendation commands, and MCP explicit metadata/recommendation tools are public now; retries, auth, tenant context, hosted receipts, private DTOs, service URLs, environment-variable defaults, and production evidence lookup stay out until separately pinned. |
| Keep the current Syndai dirty worktree out of EvalRank. | Memphant / memory-system | Dirty files are Memphant specs/plans, not EvalRank public core. Port only a future explicit storage-free EvalRank contract extracted from that work. |
| Keep persistence, source adapters, scorer runtime, UI proof assets, hosted ops, GTM, telemetry, and eval-integrity material private. | DB Bootstrap / Syndai Ops, Scoring / Materializer Runtime, Hosted Ops / GTM, Evaluation Integrity, Secrets / Deploy Ops | Do not port until a public contract is separable from private data, secrets, live infrastructure, and proprietary tuning. |

## Latest Dirty-Worktree Check

Checked and rechecked the private Syndai worktree on 2026-06-26 before this public doc sync.

| Private-side state | Port decision | Workstream |
| --- | --- | --- |
| Uncommitted and untracked files were limited to `docs/superpowers/specs/memphant/` spec edits plus `docs/superpowers/plans/2026-06-26-memphant-gapcheck-validation.md` and `docs/superpowers/plans/2026-06-26-memphant-lifecycle-validation.md`. | Do not port to EvalRank. They are adjacent memory/eval planning, not the EvalRank public core. | Memphant / memory-system workstream, outside this repo |
| EvalRank private source areas still exist in Syndai docs, plans, backend migration scripts, and `backend/evalrank_migrations/`. | Keep using them only as inputs for sanitized summaries and explicit storage-free public contracts. | Public Contracts, Public Surface Contracts, DB Bootstrap / Syndai Ops |
| No current uncommitted EvalRank-specific private artifact was found that should move now. | Next public work remains contract hardening and pinned storage-free payloads, not raw private-doc copying. | Docs / Public Planning, Public Contracts |

## Current Private-Side Scan

The latest private-side scan found EvalRank planning material in private spec, API, data/methodology, relation-graph, and build-readiness docs. Treat those docs as inputs for sanitized public summaries only; do not copy them into this repo.

| Private-side source area | Public action | Owning workstream |
| --- | --- | --- |
| Storage-free contract vocabulary from API and build-readiness planning | Port one pinned payload at a time with core dataclasses, JSON Schemas, fixtures, SDK types, CLI output, MCP output, and drift tests. `StageCandidate` is now ported as the Stage-1 retrieval row; `ResultRow` is now ported as the public ingested-result provenance envelope; `Abstention` is now ported as the public no-ranked-answer reason/detail object. | Public Contracts, SDK / CLI / MCP |
| Public API route shapes and Problem Details error semantics | Shared retry-aware Problem Details semantics are ported, along with concrete public metadata route contracts for use cases and scoring stages; keep hosted auth, tenant logic, receipt storage, private DTOs, live throttling, and private problem types out. | Public Surface Contracts |
| Public use-case taxonomy names, definitions, entity-kind spans, safety-overlay policy, and sanitized method explanation | Ported as a storage-free `UseCaseCatalog` contract, synthetic fixture, schema, SDK/CLI/MCP parity surface, `GET /v1/use-cases` OpenAPI route contract, and public method note. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Methods / Schemas |
| Public scoring-stage names, order, contract refs, and boundary notes | Ported as a storage-free `ScoringStageCatalog` contract, synthetic fixture, schema, SDK/CLI/MCP parity surface, runnable example output, and public method note; formulas, thresholds, graders, telemetry, and runtime scorer behavior stay private. | Public Contracts, SDK / CLI / MCP, Methods / Schemas |
| Public recommendation comparability discriminator and ranking-group row shape | Ported as closed `RankingGroup` rows for `kind-grouped` responses; this only says groups are ranked within one entity type. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Private build-readiness plans under `docs/superpowers/plans/evalrank/` | Keep raw plans private; port only public-safe status/build-order summaries and dated build logs. | Docs / Public Planning |
| Private EvalRank spec docs under `docs/superpowers/specs/evidence-ranked-platform/` | Use as inputs only. Extract one storage-free API, method, or payload contract at a time, rewrite with synthetic examples, and test before porting. | Public Contracts, Public Surface Contracts, Methods / Schemas |
| Current Memphant dirty specs and validation/lifecycle plans | Keep in the Memphant / memory-system workstream. They should not be copied into EvalRank; only a future explicit EvalRank contract extracted from them belongs here. | Memphant / memory-system workstream first; Public Contracts only after extraction |
| Syndai EvalRank doc validators and tests | Keep private validators with private specs. Distill public-facing invariants into this repo only when public docs carry the matching claim. | Docs / Public Planning, Open-Core Boundary / CI |
| UI proof assets and hosted-product design docs | Keep private until a public UI route or public product doc intentionally exists; then port only public-safe assets or generated/synthetic screenshots. | Public Surface Contracts, Hosted Ops / GTM |
| Use-case benchmark weights, IRT fit clusters, benchmark crosswalk, confidence policies, and thin-coverage/synthesis details | Keep private during incubation; later publish only sanitized method explanations that omit weights, held-out tasks, private corpora, proprietary thresholds, and benchmark outputs. | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |
| Public scoring-stage names, order, contract refs, use-case taxonomy, trust/freshness vocabulary, and method-boundary explanations | Scoring-stage catalog and use-case taxonomy notes are ported; future notes must omit formulas, thresholds, held-out eval details, private benchmark outputs, and production traces. | Methods / Schemas |
| Boundary checks, license/notice hygiene, schema drift tests, and secret/private-data guards | Port aggressively when they reduce public leak risk or contract drift. | Open-Core Boundary / CI |
| Python package metadata and dependency-edge guards | Ported as deterministic `tomllib` tests over public `pyproject.toml` files, with package README metadata drift checks for Python packages and the TypeScript SDK. | Open-Core Boundary / CI |
| Supabase schema, migrations, grants/RLS, workload isolation, live DB checks, and shared Finn deployment details | Keep private until EvalRank owns persistence or its own Supabase project; then design a public migration ownership plan. | DB Bootstrap / Syndai Ops |
| Deterministic scorer/materializer runtime and entity/evidence graph behavior | Incubate privately until public-input-only pieces are separable from proprietary tuning, production rows, live workers, and source adapters. | Scoring / Materializer Runtime |
| Held-out suites, synthetic internal corpora, graders, answers, calibration traces, and private benchmark outputs | Never port; publish only synthetic or public reproducible fixtures. | Evaluation Integrity |
| Hosted deploy, telemetry, billing/admin, vendor intent, account operations, credentials, and live project refs | Keep private unless later rewritten into product-neutral public docs with all operational detail removed. | Hosted Ops / GTM, Secrets / Deploy Ops |

## Current Port-Over Assessment

Use this table for the next port decision. The destination is this public repo only when the artifact is portable without private data, secrets, live infrastructure, or proprietary hosted behavior.

| Candidate change | Port decision | Workstream |
| --- | --- | --- |
| Public repo scaffold, package boundaries, license/notice files, CI, and deterministic public-boundary checks | Already ported; keep strengthening leak classes as they are discovered. | Open-Core Boundary / CI |
| Storage-free public payloads and aliases currently represented by core dataclasses and JSON Schemas | Already ported for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, ranking groups, evidence sets, exclusions, `the_call`, abstentions, ranked entities, recommendations, recommendation aliases, strict public string fields, strict recommendation envelope validation, entity refs, and evidence items. | Public Contracts |
| Public fixture surfaces across core, SDKs, CLI, MCP, and examples | Already ported for deterministic synthetic fixtures only, including candidate-set, stage-candidate, result-row, problem, use-cases, scoring-stages, ranking-group, evidence-set, exclusion, and recommendation abstention-field fixtures. | SDK / CLI / MCP, Examples |
| Public scoring-stage vocabulary and use-case taxonomy method | Already ported as a method-boundary note plus storage-free `ScoringStageCatalog`, including `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, ranked use-case policy, safety overlay policy, and cross-kind grouping guidance, without formulas, thresholds, private eval data, or benchmarks. | Methods / Schemas |
| `RawEntry` ingestion-normalization shape | Ported as a storage-free contract with synthetic fixtures and deterministic content hash; source adapters, production metadata, and live fetch behavior stay private. | Public Contracts |
| `CandidateSet` candidate-resolution shape | Ported as a storage-free list of public `EntityRef` candidates; live candidate resolution, source adapters, graph lookup, and production entity rows stay private. | Public Contracts, Methods / Schemas |
| `StageCandidate` Stage-1 retrieval row | Ported as a storage-free candidate fingerprint plus public `EntityRef`, fused score, RRF ranks, and retrieval provenance; Stage-2+ scorer fields, graph lookup, source adapters, storage, telemetry, and private tuning stay private. | Public Contracts, Methods / Schemas |
| `ResultRow` ingested result provenance envelope | Ported as a storage-free row with benchmark, harness, raw-score unit, provenance, public flags, and verification state; source adapters, production rows, private benchmark material, scorer fitting, and storage tables stay private. | Public Contracts, Methods / Schemas |
| `EvidenceSet` evidence-attachment shape | Ported as a storage-free list of public `EvidenceItem` rows; empty evidence lists support abstention or no-evidence paths. Live evidence lookup, evidence-ledger persistence, source adapters, production traces, and private rows stay private. | Public Contracts, Methods / Schemas |
| `Exclusion` exclusions-with-reasons shape | Ported as a storage-free subject plus public reason/detail row; Stage-0 gate policy, private safety taxonomy, constraint evaluation, and production traces stay private. | Public Contracts, Methods / Schemas |
| Public `the_call` / decision-confidence response shape and `Abstention` reason/detail object | Ported as nested recommendation contracts with no proprietary thresholds, held-out evidence floors, private reason taxonomy, or private confidence tuning. | Public Contracts, Methods / Schemas |
| REST/OpenAPI contract | Concrete route contracts ported for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`; public errors use reusable Problem Details responses plus retry/rate-limit headers; keep private auth, tenant logic, hosted receipt internals, private problem types, live throttling, and app DTOs out. | Public Surface Contracts |
| Use-case taxonomy and `/v1/use-cases` route contract | Ported as a finite public catalog with slugs, display names, one-line definitions, entity-kind spans, ranked-vs-overlay policy, safety overlay, and sanitized method note; benchmark weights, IRT clusters, confidence policy, synthesis/coverage rules, and live table/storage semantics stay private. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Methods / Schemas |
| Recommendation comparability and ranking groups | Ported as storage-free `RankingGroup` rows for within-kind rankings only; cross-kind normalization, scorer internals, and private score semantics stay private. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Recommendation receipt route and HMAC-backed hosted ID derivation | Do not port yet. Public aliases are enough for open-core interoperability; secret-backed derivation belongs with hosted route design. | Public Surface Contracts, Hosted Ops / Deploy Ops |
| Entity graph tables, evidence ledger storage, methodology table, migrations, grants, RLS, and live DB checks | Keep in Syndai/private systems until EvalRank owns persistence or its own Supabase project. | DB Bootstrap / Syndai Ops |
| EvalRank migration guard and runner scripts in Syndai | Keep private with the shared Finn/Supabase bootstrap. If persistence moves here, port the policy as a new public migration subsystem, not by copying live operational scripts. | DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Public-facing doc-drift checks distilled from Syndai EvalRank validators | Port later only after matching public claims exist; do not copy private spec names, private plan paths, or private-only assertions. | Open-Core Boundary / CI, Docs / Public Planning |
| Deterministic scorer and materializer runtime | Incubate privately first, then split only public-input-only pieces that do not depend on production rows, private workers, or proprietary tuning. | Scoring / Materializer Runtime |
| SDK/CLI/MCP behavior beyond fixtures | Port one public contract at a time after the corresponding contract and schema are pinned. | SDK / CLI / MCP |
| UI routes, API-route navigation docs, deeplinks, and `NAVIGATION.md` | API route navigation is ported for the first public route; UI/deeplink docs wait until those surfaces exist. | Public Surface Contracts, Docs / Public Planning |
| Hosted ops, telemetry, billing/admin/GTM, vendor intent, credentials, deploy files, live project refs, private integrations, and account operations | Keep private unless later rewritten as product-neutral public docs with all operational detail removed. | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out suites, graders, answer keys, traces, judge calibration, private benchmark results, and proprietary ranking experiments | Never port. Publish only synthetic or public reproducible fixtures. | Evaluation Integrity |
| Adjacent Memphant, AgentsDB, memory, or general agent-system specs | Do not port into EvalRank by default. Route to their owning workstream unless a concrete EvalRank contract is extracted, sanitized, and tested. | Docs / Public Planning, Public Contracts when explicitly extracted |

## Porting Decisions

| Artifact or workstream | Destination | Owner workstream | Status |
| --- | --- | --- | --- |
| Public contract dataclasses and JSON Schemas | This repo | Public Contracts | Capability fingerprint, raw entry, request, candidate set, stage candidate, result row, use-case catalog, ranking group, evidence set, exclusion, `the_call`, abstention, recommendation, entity, and evidence slices ported |
| Use-case taxonomy catalog | This repo | Public Contracts, Public Surface Contracts | Ported; only taxonomy contract, fixture, schema, SDK/CLI/MCP surfaces, and `GET /v1/use-cases` route contract moved |
| Recommendation join aliases | This repo | Public Contracts | Ported; hosted HMAC derivation stays private |
| Entity references, evidence items, and evidence-item schema | This repo | Public Contracts | Ported |
| Repo boundary checks, license hygiene, and CI gates | This repo | Open-Core Boundary / CI | Partly ported |
| Sanitized build-readiness summaries from Syndai planning docs | This repo | Docs / Public Planning | In progress |
| Public build-order and wave status | This repo | Docs / Public Planning | In progress |
| Public scoring-stage vocabulary, scoring stage catalog, use-case taxonomy method, and method boundaries | This repo | Methods / Schemas | Public boundary notes and storage-free catalog ported |
| REST/OpenAPI contracts | This repo | Public Surface Contracts | `GET /v1/use-cases`, `GET /v1/scoring-stages`, `POST /v1/recommendations`, and retry-aware Problem Details contracts ported |
| SDK, CLI, and MCP implementations | This repo | SDK / CLI / MCP | Python SDK re-export/client with metadata and recommendation route helpers, TypeScript public types/client with metadata and recommendation route helpers, CLI fixture/metadata/recommend commands, and MCP fixture/metadata/recommend tools ported, including candidate-set, stage-candidate, result-row, problem, use-cases, scoring-stages, ranking-group, evidence-set, exclusion, and recommendation abstention-field fixture surfaces |
| Public methodology notes | This repo | Methods / Schemas | Scoring-stage and use-case taxonomy notes ported; future notes only after removing held-out and proprietary details |
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
- Additional TypeScript SDK behavior only when the package-level check/runtime test and repo tests prove the public contract shape.

## Port Later

- Additional REST/OpenAPI surfaces after concrete route contracts exist.
- Route-specific public problem types after their public semantics are stable and separable from hosted internals.
- Recommendation receipt routes and HMAC-backed hosted identifiers after public route semantics and secret handling are designed.
- Full REST/OpenAPI, CLI, SDK, and MCP behavior beyond public fixtures after concrete public contracts are pinned.
- Source adapters, live fetch behavior, and candidate-resolution graph lookup after they can run without private service dependencies or production metadata.
- Public scoring method details after proprietary thresholds, held-out eval details, and private ranking experiments are removed.
- Deterministic scorer/materializer runtime after it is split from private evidence rows, hosted workers, and proprietary tuning.
- Persistence migrations only after EvalRank owns its own deploy/release path or has its own Supabase project.
- Public migration-policy checks only after EvalRank owns persistence; do not copy Syndai live migration scripts or deployment assumptions.
- Public doc-drift checks distilled from private validators only after the corresponding public docs exist.
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
- GitHub secret scanning runs automatically for public repositories and can detect hardcoded credentials in repository history, but prevention is cheaper than cleanup: https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
- If sensitive data reaches Git history, treat it as compromised, rotate credentials, and follow a coordinated removal process: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- Supabase custom schemas must be deliberately exposed and granted for API access; EvalRank incubation uses private schema bootstrap outside this public repo: https://supabase.com/docs/guides/api/using-custom-schemas
- For public API design, prefer a dedicated exposed API schema and keep internal tables/helpers in non-exposed schemas; grants and RLS together decide what API roles can touch: https://supabase.com/docs/guides/api/securing-your-api

## Current GitHub Public-Repo Check

Checked on 2026-06-26 with `gh api repos/siddmax/evalrank`.

| Setting | Status | Porting implication |
| --- | --- | --- |
| Repository visibility | Public | Treat every committed byte and all future history as public. |
| Secret scanning | Enabled | Backstop only; still run the local boundary check before every push. |
| Secret scanning push protection | Enabled | Helps block supported secrets before push, but does not replace review. |
| Dependabot security updates | Enabled | Dependency security backstop for future package work. |
| Secret scanning non-provider patterns | Disabled | Revisit under Secrets / Deploy Ops if EvalRank later defines organization-specific secret formats. |
| Secret scanning validity checks | Disabled | Revisit under Secrets / Deploy Ops if managed secrets ever become part of a public workflow. |
