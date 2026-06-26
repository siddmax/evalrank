# EvalRank Status

Last updated: 2026-06-26

## Built

- Public Apache-2.0 repository scaffold.
- Public package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` guidance.
- `CLAUDE.md` shim to `@AGENTS.md`.
- Public boundary checker for private imports, disallowed coupling, excluded method markers, and missing package license/notice files.
- Public boundary checker guards for secret files, high-signal secret values, and held-out/private data paths.
- Public Python package metadata drift guard for package names, versions, licenses, Python floor, dependency edges, and CLI entrypoint.
- Core Python capability fingerprint, raw entry, request, candidate set, stage candidate, evidence item, result row, use-case catalog, scoring stage catalog, ranking group, evidence set, exclusion, `the_call`, abstention, and recommendation contracts in `packages/core`.
- Public core fixture factory for canonical capability fingerprint, raw entry, request, candidate set, stage candidate, evidence item, Problem Details, result row, use-case catalog, scoring stage catalog, ranking group, evidence set, exclusion, and recommendation payloads with public abstention fields, with synthetic request use cases aligned to the public catalog.
- Shared public fixture-kind dispatch in core, reused by CLI and MCP fixture adapters.
- Public JSON Schemas for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, scoring stage catalogs, evidence sets, exclusions, ranked entities, recommendations with closed ranking groups and public abstention objects, evidence items, and retry-aware RFC 9457 Problem Details.
- Public OpenAPI 3.1.1 contract for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, including reusable Problem Details responses for malformed requests, validation errors, rate limits, temporary unavailability, and upstream timeouts.
- Public retry-aware Problem Details extensions: `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url`.
- Pinned public `methodology_version` format: `YYYY-MM-DD.SEQ.slug`.
- Python SDK package metadata, public core contract re-exports, and dependency-free `EvalRankClient` behavior for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`.
- TypeScript SDK package metadata, mirrored public contract types/constants, and dependency-free native `fetch` `EvalRankClient` behavior for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`.
- Python and TypeScript SDK clients strictly parse `Retry-After` as non-negative integer seconds and treat malformed retry headers as absent while preserving Problem Details errors.
- SDK README drift checks for the Python and TypeScript public surfaces.
- CLI package metadata, deterministic public fixture command, explicit public `use-cases` and `scoring-stages` metadata commands, and explicit public `recommend` command for `POST /v1/recommendations`.
- MCP package metadata, deterministic public fixture adapter, explicit public `evalrank.use_cases` and `evalrank.scoring_stages` metadata tools, and explicit public `evalrank.recommend` tool for `POST /v1/recommendations`.
- Public scoring-stage vocabulary and catalog contract, use-case taxonomy method, and method-boundary notes.
- Runnable public fixture bundle example, including the scoring stage catalog.
- Schema drift tests for core payload keys and public enum constants.
- Exact package README metadata drift guard for Python package manifests and the TypeScript SDK manifest.
- Exact CLI and MCP README drift checks for public fixture commands, route commands, fixture kinds, and tool names.
- Exact schema README drift check for public schema and OpenAPI filenames.
- Exact methods README drift check for public method-note filenames.
- Exact repo structure drift check for public top-level directories and package directories.
- Exact `CLAUDE.md` shim drift check for the required `@AGENTS.md` reference.
- Scoped `AGENTS.md` coverage drift check for public work areas.
- Ranked entity `axes.evidence` schema and TypeScript type hardening.
- Scoring-stage catalog schema uniqueness drift guard.
- Scoring-stage catalog ordinal contiguity hardening.
- Recommendation `ranked` schema uniqueness hardening.
- Recommendation `RankingGroup.ranked` schema uniqueness hardening.
- Recommendation exclusion uniqueness hardening.
- Recommendation abstention envelope consistency hardening.
- Recommendation abstention-as-empty-single-scale hardening.
- Recommendation `shortlist_depth` count consistency hardening.
- Recommendation ranked-row rank contiguity/order hardening.
- Ranked entity freshness date format hardening.
- Public temporal field format hardening.
- Result row public source URL hardening.
- TypeScript SDK non-empty array helper type for schema `minItems: 1` public arrays.
- TypeScript SDK `UseCase` discriminated union for public ranked and veto-overlay branches.
- TypeScript SDK `TheCall` discriminated union for public `recommend` and `abstain` branches.
- TypeScript SDK `Recommendation` discriminated union for public `single-scale` and `kind-grouped` branches.
- Python core `CandidateSet` and `EvidenceSet` now reject mutable list-backed sequence inputs before serialization.
- Tests for core contracts, schema-contract drift, repo docs, and public boundary rules.
- Public progress tracker and repo structure map.
- Public route navigation map in `NAVIGATION.md`.
- Public porting map for deciding what moves from Syndai/private workstreams into this repo.
- Earlier public/private porting audit confirming the then-current private Syndai dirty worktree had Memphant spec edits plus two Memphant plan files and no EvalRank public-port candidate.
- Public/private source scan classifying the current Syndai EvalRank spec, build-readiness, migration, and doc-validation surfaces without copying raw private text.
- Public/private source inventory refresh documenting current private EvalRank specs, build plans, proof assets, backend migration assets, GitHub security settings, and next public port slices without copying raw private text.
- GitHub public repo security metadata snapshot confirming public visibility, secret scanning, push protection, and Dependabot security updates are enabled.
- Public-repo safety guidance in `SECURITY.md` for private disclosure, no public secret reports, immediate rotation on exposure, and coordinated remediation if sensitive data reaches Git history.
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
- Capability fingerprint declared-shape schema hardening build log in `docs/build-log/2026-06-26-capability-fingerprint-shape-schema-hardening.md`.
- Recommendation comparability schema hardening build log in `docs/build-log/2026-06-26-recommendation-comparability-schema-hardening.md`.
- `the_call` branch schema hardening build log in `docs/build-log/2026-06-26-the-call-branch-schema-hardening.md`.
- Score-component map hardening build log in `docs/build-log/2026-06-26-score-components-contract-hardening.md`.
- Recommendation envelope validation hardening build log in `docs/build-log/2026-06-26-recommendation-envelope-contract-hardening.md`.
- JSON-object metadata validation hardening build log in `docs/build-log/2026-06-26-json-object-contract-hardening.md`.
- Public doc progress and porting audit in `docs/build-log/2026-06-26-public-doc-progress-porting-audit.md`.
- Primitive and sequence field validation hardening build log in `docs/build-log/2026-06-26-primitive-sequence-contract-hardening.md`.
- Unique request entity-types hardening build log in `docs/build-log/2026-06-26-evaluation-request-entity-type-uniqueness.md`.
- Ranked-entity caveat string hardening build log in `docs/build-log/2026-06-26-ranked-entity-caveat-hardening.md`.
- Public string-field validation hardening build log in `docs/build-log/2026-06-26-public-string-field-contract-hardening.md`.
- Private source port-routing build log in `docs/build-log/2026-06-26-private-source-port-routing.md`.
- Public abstention contract build log in `docs/build-log/2026-06-26-abstention-contract.md`.
- Scoring-stage abstention output alignment build log in `docs/build-log/2026-06-26-scoring-stage-abstention-output.md`.
- Public progress and port-over routing refresh in `docs/build-log/2026-06-26-progress-portover-refresh.md`.
- Port-over inventory refresh build log in `docs/build-log/2026-06-26-port-over-inventory-refresh.md`.
- Public progress and private-side porting recheck build log in `docs/build-log/2026-06-26-public-progress-porting-recheck.md`.
- Public progress, porting, and public-repo safety refresh in `docs/build-log/2026-06-26-public-repo-porting-safety-refresh.md`.
- Current public/private porting workstream refresh in `docs/build-log/2026-06-26-public-porting-workstream-refresh.md`.
- CLI recommendation command build log in `docs/build-log/2026-06-26-cli-recommendation-command.md`.
- TypeScript recommendation client build log in `docs/build-log/2026-06-26-typescript-recommendation-client.md`.
- MCP recommendation tool build log in `docs/build-log/2026-06-26-mcp-recommendation-tool.md`.
- Python package metadata drift guard build log in `docs/build-log/2026-06-26-python-package-metadata-drift-guard.md`.
- Python SDK metadata route build log in `docs/build-log/2026-06-26-python-sdk-metadata-routes.md`.
- TypeScript SDK metadata route build log in `docs/build-log/2026-06-26-typescript-sdk-metadata-routes.md`.
- CLI metadata command build log in `docs/build-log/2026-06-26-cli-metadata-commands.md`.
- MCP metadata tool build log in `docs/build-log/2026-06-26-mcp-metadata-tools.md`.
- Package README metadata drift-guard build log in `docs/build-log/2026-06-26-package-readme-metadata-drift-guard.md`.
- Package README exact metadata drift-check build log in `docs/build-log/2026-06-26-package-readme-exact-metadata-drift-check.md`.
- CLI and MCP README exact drift-check build log in `docs/build-log/2026-06-26-cli-mcp-readme-exact-drift-check.md`.
- Schema README exact drift-check build log in `docs/build-log/2026-06-26-schema-readme-exact-drift-check.md`.
- Methods README exact drift-check build log in `docs/build-log/2026-06-26-methods-readme-exact-drift-check.md`.
- Repo structure exact drift-check build log in `docs/build-log/2026-06-26-repo-structure-drift-check.md`.
- `CLAUDE.md` shim drift-check build log in `docs/build-log/2026-06-26-claude-shim-drift-check.md`.
- Scoped `AGENTS.md` coverage drift-check build log in `docs/build-log/2026-06-26-scoped-agents-drift-check.md`.
- Ranked entity axes shape hardening build log in `docs/build-log/2026-06-26-ranked-entity-axes-contract-hardening.md`.
- TypeScript non-empty array parity build log in `docs/build-log/2026-06-26-typescript-nonempty-array-parity.md`.
- TypeScript use-case branch parity build log in `docs/build-log/2026-06-26-typescript-use-case-branch-parity.md`.
- TypeScript `the_call` branch parity build log in `docs/build-log/2026-06-26-typescript-the-call-branch-parity.md`.
- TypeScript recommendation branch parity build log in `docs/build-log/2026-06-26-typescript-recommendation-branch-parity.md`.
- Public tuple sequence contract hardening build log in `docs/build-log/2026-06-26-tuple-sequence-contract-hardening.md`.
- Scoring-stage schema uniqueness drift-check build log in `docs/build-log/2026-06-26-scoring-stage-schema-uniqueness-drift-check.md`.
- Scoring-stage ordinal contiguity build log in `docs/build-log/2026-06-26-scoring-stage-ordinal-contiguity.md`.
- Recommendation ranked schema uniqueness hardening build log in `docs/build-log/2026-06-26-recommendation-ranked-schema-uniqueness.md`.
- Ranking group schema uniqueness hardening build log in `docs/build-log/2026-06-26-ranking-group-schema-uniqueness.md`.
- Recommendation exclusion uniqueness hardening build log in `docs/build-log/2026-06-26-recommendation-exclusion-uniqueness.md`.
- SDK retry-after parser hardening build log in `docs/build-log/2026-06-26-sdk-retry-after-parser-hardening.md`.
- Recommendation abstention envelope consistency build log in `docs/build-log/2026-06-26-recommendation-abstention-envelope-consistency.md`.
- Recommendation abstention-as-empty-single-scale build log in `docs/build-log/2026-06-26-abstention-no-ranked-answer.md`.
- Recommendation `shortlist_depth` count consistency build log in `docs/build-log/2026-06-26-shortlist-depth-count-consistency.md`.
- Recommendation ranked-row rank contiguity/order build log in `docs/build-log/2026-06-26-recommendation-rank-contiguity.md`.
- Ranked entity freshness date format build log in `docs/build-log/2026-06-26-freshness-date-format-hardening.md`.
- Public temporal field format build log in `docs/build-log/2026-06-26-public-temporal-format-hardening.md`.
- Result row public source URL build log in `docs/build-log/2026-06-26-result-row-source-url-hardening.md`.
- Public progress and private-side port-routing refresh build log in `docs/build-log/2026-06-26-public-progress-private-routing-refresh.md`.

## Current Public Surface

| Surface | Built | Not built yet |
| --- | --- | --- |
| Core contracts | `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `EvidenceSet`, `Exclusion`, `TheCall`, `Abstention`, `ProblemDetails`, `RankedEntity`, `Recommendation`, public recommendation ID aliases, `EntityRef`, public constants, shared fixture-kind dispatch, strict public score-component maps, strict public calendar-valid freshness/result-run dates, strict public UTC timestamp format, strict public HTTP(S) result source URLs, strict scoring-stage ordinal contiguity, strict recommendation envelope validation, strict recommendation rank contiguity/order, strict recommendation exclusion uniqueness, strict abstention/the-call consistency, strict abstention-as-empty-single-scale behavior, strict recommendation `shortlist_depth` count consistency, and synthetic fixture factories. | Source adapters, storage models, graph persistence, scorer engine, benchmark weights, IRT clusters, Stage-2+ scorer rows, trust/security policy runtime. |
| Schemas | JSON Schemas for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, result rows, use-case catalogs, scoring stage catalogs, evidence sets, exclusions, ranked entities with strict public score-component maps and `YYYY-MM-DD` freshness dates, public UTC timestamp fields, recommendations with closed ranking groups, public abstention objects, and empty single-scale abstention branches, evidence items, and retry-aware RFC 9457 Problem Details, plus OpenAPI 3.1.1 for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, with drift tests against public contracts and pinned public patterns. | Persistence schemas, scorer-runtime schemas, benchmark-weight schemas, and additional route-specific problem types beyond the current public error vocabulary. |
| Python SDK | Package metadata, public re-exports from `evalrank_core`, including `ProblemDetails`, public vocabulary constants, public fixture dispatch helpers, and dependency-free HTTP(S)-only `EvalRankClient` behavior for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` success plus Problem Details errors, with strict numeric `Retry-After` parsing. | Installed package release flow and additional non-fixture client behavior beyond the current public metadata and recommendation routes. |
| TypeScript SDK | Package metadata, public constants, interfaces for current payload contracts, including abstention/the-call state typing and empty single-scale abstention typing, and dependency-free native `fetch` `EvalRankClient` behavior for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` success plus Problem Details errors, with strict numeric `Retry-After` parsing. | Built JS distribution, published package release flow, and additional non-fixture client behavior beyond the current public metadata and recommendation routes. |
| CLI | Deterministic `fixture fingerprint`, `fixture raw-entry`, `fixture request`, `fixture candidate-set`, `fixture stage-candidate`, `fixture evidence`, `fixture problem`, `fixture result-row`, `fixture use-cases`, `fixture scoring-stages`, `fixture ranking-group`, `fixture evidence-set`, `fixture exclusion`, `fixture recommendation`, explicit HTTP(S)-only `use-cases --base-url ...`, `scoring-stages --base-url ...`, and `recommend --base-url ... --request ...` commands. | Auth, retries, service discovery, workspace/project operations, private DTOs, hosted receipts, or persistence. |
| MCP | Deterministic `evalrank.fixture` adapter, public `evalrank.use_cases` and `evalrank.scoring_stages` tools for explicit HTTP(S)-only metadata success and Problem Details errors, and public `evalrank.recommend` tool for explicit HTTP(S)-only `POST /v1/recommendations` success and Problem Details errors. | Live MCP server runtime, evidence lookup, scorer tools, auth, retries, service discovery, hosted receipts, persistence, or private data access. |
| Methods | Public scoring-stage vocabulary and storage-free `ScoringStageCatalog`, including `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, and `Abstention`; public use-case taxonomy method; and private-boundary notes. | Proprietary weights, thresholds, graders, held-out tasks, and benchmark outputs. |
| Examples | `examples/public_fixture.py` prints the current synthetic public fixture bundle: raw entry, request, candidate set, stage candidate, evidence item, Problem Details, evidence set, result row, use-case catalog, scoring stage catalog, exclusion, and recommendation JSON; its README is drift-checked against the emitted JSON keys plus nested recommendation and scoring-stage contract refs. | Non-fixture demos, live API examples, and private-data examples. |
| Docs | Status tracker, repo structure map with exact drift tests, porting map, route navigation map, package READMEs, build logs, and public/private workstream router. | UI navigation docs; add only when UI routes or deeplinks exist. |

## Progress Snapshot

| Area | State | Next owner |
| --- | --- | --- |
| Repo foundation | Built: public scaffold, package boundaries, license/notice hygiene, root/scoped agent docs, CI, `make check`, deterministic public-boundary scanner, package metadata checks, and package README metadata drift guards. | Open-Core Boundary / CI keeps leak and drift checks current. |
| Public contracts | Built through the current storage-free payload set: fingerprints, raw entries, requests, candidate sets, stage candidates, result rows, use-case catalogs, scoring stage catalogs, ranking groups, evidence sets, exclusions, `the_call`, abstentions, recommendations, public aliases, entity refs, and evidence items. | Public Contracts pins the next standalone payload before SDK/CLI/MCP behavior grows. |
| Schemas and methods | Built: JSON Schemas, OpenAPI route contracts for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`, retry-aware Problem Details, public scoring-stage vocabulary/catalog, and sanitized use-case taxonomy method note. | Methods / Schemas and Public Surface Contracts add only public, product-neutral semantics. |
| Interfaces | Built: Python SDK re-exports plus stdlib metadata/recommendation client behavior, TypeScript public types/constants plus native `fetch` metadata/recommendation client behavior, CLI fixture and recommendation commands, MCP fixture and recommendation tools, runnable public example, and README drift guards. | SDK / CLI / MCP promotes more behavior only after public route/client contracts are pinned. |
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
| Capability fingerprint schemas now reject empty `declared_capability_shape` objects, matching core behavior. | Built here as schema/core parity hardening for the existing public fingerprint payload; no source adapter, live fetch behavior, private runtime, or DB work moved. | Public Contracts, Methods / Schemas |
| Recommendation schemas now pin `single-scale` versus `kind-grouped` branch shapes, matching core behavior. | Built here as schema/core parity hardening for existing public recommendation envelopes; no scorer normalization, private score semantics, hosted receipt behavior, private runtime, or DB work moved. | Public Contracts, Methods / Schemas |
| Recommendation schemas now pin `the_call` `recommend` versus `abstain` branch shapes, matching core behavior. | Built here as schema/core parity hardening for the existing public decision envelope; no confidence policy, private abstention taxonomy, scorer/runtime behavior, hosted receipt behavior, or DB work moved. | Public Contracts, Methods / Schemas |
| Ranked entity `score_components` now reject non-object maps, blank/non-string names, booleans, and out-of-range values before serialization. | Built here as public contract hardening; no private scorer formula was added. | Public Contracts, Methods / Schemas |
| Recommendation envelopes now reject schema-incompatible metadata and duplicate ranked entities before serialization. | Built here as public contract hardening; no scorer/runtime, route implementation, hosted receipt, or private evidence behavior was added. | Public Contracts, Methods / Schemas |
| Evidence item `metadata` and evaluation request `constraints` now reject non-object, non-string-key, and non-JSON values before serialization. | Built here as public contract hardening; no private evidence lookup, source adapter, or policy behavior was added. | Public Contracts, Methods / Schemas |
| Entity references, freshness dates, request entity-type arrays, ranked-entity integer fields, and caveats now reject schema-incompatible Python values before serialization. | Built here as public contract hardening; no schema expansion, scorer behavior, or private runtime behavior was added. | Public Contracts, Methods / Schemas |
| Evaluation requests now reject duplicate `entity_types`, and the schema pins `uniqueItems`. | Built here as public request-shape hardening; no candidate resolver, scorer behavior, route implementation, DB work, or private source adapter moved. | Public Contracts, Methods / Schemas |
| Ranked entity caveats now reject empty strings before serialization, and the schema pins the same non-empty item rule. | Built here as schema/core parity hardening for the existing public `caveats` array; no scorer behavior, private runtime, or DB work moved. | Public Contracts, Methods / Schemas |
| Capability fingerprint, raw entry, evidence item, evidence set, candidate set, `the_call`, and abstention public string fields now reject truthy non-strings before serialization. | Built here as public contract hardening against existing schemas; no source adapter, scorer/runtime behavior, private evidence lookup, DB work, or hosted operation moved. | Public Contracts, Methods / Schemas |
| Recommendation abstention responses now include a public `Abstention` reason/detail object and ordinary recommendations include `abstention: null`. | Built here as a storage-free response contract; evidence-floor thresholds, confidence policy, private reason taxonomy, scorer/runtime behavior, DB work, and hosted operations were not moved. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| The public scoring-stage catalog now names `Abstention` as an output of `ranking-or-abstention`. | Built here as catalog alignment after the public `Abstention` contract; no scorer thresholds, private policy, runtime, or DB behavior moved. | Methods / Schemas, Public Contracts |
| Earlier private-side dirty worktree check found Memphant spec edits and two Memphant plan files, not EvalRank public-port candidates. | Documented here as a routing decision; no private Memphant planning text was copied into the public repo. | Memphant / memory-system workstream, Docs / Public Planning, Open-Core Boundary / CI |
| Earlier private-side dirty worktree recheck found only Memphant planning changes and no uncommitted EvalRank-specific public-port candidate at that time. | Documented here as a public-safe category/path review only; no private file contents were copied. | Memphant / memory-system workstream, Docs / Public Planning, Public Contracts |
| Current private-side dirty worktree refresh found preflight/repo-guidance edits, backend runtime reliability edits, private EvalRank doc-validation edits, and Memphant memory-system planning edits. | Documented as categories only. None should be copied into this public repo now; extract only a future storage-free EvalRank contract or public doc check if one is deliberately identified. | Syndai runtime workstream, Memphant / memory-system workstream, Docs / Public Planning, Open-Core Boundary / CI |
| Current private-side EvalRank source scan classified private specs, build-readiness plans, migration bootstrap, migration guards, doc validators, and UI proof assets. | Documented here as a public-safe routing decision; raw private docs, proof assets, operations scripts, and private migrations were not copied. | Docs / Public Planning, Public Surface Contracts, DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Current private-source inventory counted private EvalRank specs, build plans, proof assets, and backend migration assets, then routed the next port slices. | Documented as categories and owners only. Public work stays on storage-free contracts, deterministic fixtures/checks, route contracts, and sanitized method notes; DB, runtime, UI proofs, hosted ops, and eval-integrity material stay private. | Docs / Public Planning, Public Contracts, Public Surface Contracts, Open-Core Boundary / CI, DB Bootstrap / Syndai Ops, Scoring / Materializer Runtime, Evaluation Integrity |
| GitHub repo security metadata was checked for the public repo. | Public visibility, secret scanning, push protection, and Dependabot security updates are enabled; the local boundary scanner remains the required gate because platform scanning is only a backstop. | Open-Core Boundary / CI, Secrets / Deploy Ops |
| Public security reporting and porting safety docs were refreshed after rechecking the public repo metadata and private-side dirty worktree. | Built here as docs-only guidance: public reports must not include secrets/private fixtures/customer data, exposed secrets must be treated as compromised, and next ports stay on public contracts/checks rather than private Memphant planning. | Docs / Public Planning, Open-Core Boundary / CI, Secrets / Deploy Ops |
| Python SDK added a dependency-free recommendation client for the existing public `POST /v1/recommendations` route contract. | Built here as HTTP(S)-only stdlib HTTP/JSON behavior; no auth, retries, hosted receipts, tenant context, private DTOs, service discovery, local file URLs, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| CLI added an explicit recommendation command for the existing public `POST /v1/recommendations` route contract. | Built here as HTTP(S)-only file/stdin JSON plumbing around the public Python SDK client; no hidden network calls, auth, retries, environment-variable defaults, hosted receipts, private DTOs, database work, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| TypeScript SDK added a dependency-free recommendation client for the existing public `POST /v1/recommendations` route contract. | Built here as HTTP(S)-only native `fetch` behavior with local package runtime tests; no auth, retries, hosted receipts, tenant context, private DTOs, service discovery, environment-variable defaults, local file URLs, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| MCP added an explicit recommendation tool for the existing public `POST /v1/recommendations` route contract. | Built here as HTTP(S)-only JSON plumbing around the public Python SDK client; no hidden network calls, auth, retries, environment-variable defaults, hosted receipts, private DTOs, database work, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| Python package metadata drift guard now pins public package dependency edges and package hygiene metadata. | Built here as stdlib `tomllib` tests over existing `pyproject.toml` files; no packaging release or publishing workflow was added. | Open-Core Boundary / CI |
| Package READMEs now carry manifest metadata and a deterministic drift guard. | Built here as local stdlib tests that bind public Python package READMEs and the TypeScript SDK README to current package names, imports, dependencies, entrypoints, license, module type, and private publish status; no publish workflow, private package index, credentials, or hosted deployment behavior was added. | Open-Core Boundary / CI, Docs / Public Planning |
| Package README metadata drift checks now reject stale extra package metadata lines. | Built here as a stdlib exact-set check over each public README metadata block and current package manifests; no runtime behavior, packaging release flow, private package index, credentials, or hosted deployment behavior moved. | Open-Core Boundary / CI, Docs / Public Planning |
| CLI and MCP README drift checks now reject stale extra public commands, fixture kinds, and tool names. | Built here as stdlib regex checks over public docs and existing public fixture/tool constants; no runtime behavior, private services, or new package surface moved. | Open-Core Boundary / CI, SDK / CLI / MCP, Docs / Public Planning |
| Schema README drift checks now reject stale extra schema/OpenAPI filenames. | Built here as a stdlib regex check over public schema docs and current public schema files; no schema shape, runtime behavior, or private material moved. | Open-Core Boundary / CI, Methods / Schemas, Docs / Public Planning |
| Methods README drift checks now reject stale extra method-note filenames. | Built here as a stdlib exact-set check over public method note files and `methods/README.md`; no private methodology, scorer weights, thresholds, benchmark data, runtime behavior, or new method content moved. | Open-Core Boundary / CI, Methods / Schemas, Docs / Public Planning |
| Ranked entity `axes.evidence` is now closed in JSON Schema and mirrored in the TypeScript SDK type. | Built here as schema/type parity with the existing Python `RankedEntity.to_dict()` output; no private evidence scoring, weights, formulas, scorer runtime, or persistence behavior moved. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| TypeScript SDK now exposes `NonEmptyArray<T>` for already-public schema `minItems: 1` arrays. | Built here as compile-time parity for existing Python and JSON Schema contracts; no runtime validation, new route behavior, private data, scorer logic, or persistence behavior moved. | SDK / CLI / MCP, Public Contracts |
| TypeScript SDK now models `UseCase` as a ranked/veto-overlay discriminated union. | Built here as compile-time parity for existing Python and JSON Schema use-case branch rules; no private rank-policy tuning, scorer runtime, hosted behavior, or persistence moved. | SDK / CLI / MCP, Public Contracts |
| TypeScript SDK now models `TheCall` as a `recommend`/`abstain` discriminated union. | Built here as compile-time parity for existing Python and JSON Schema branch rules; no private confidence policy, thresholds, scorer runtime, hosted behavior, or persistence moved. | SDK / CLI / MCP, Public Contracts |
| TypeScript SDK now models `Recommendation` as a `single-scale`/`kind-grouped` discriminated union. | Built here as compile-time parity for existing Python and JSON Schema comparability branch rules; no scorer normalization, private score semantics, hosted receipt behavior, runtime, or DB work moved. | SDK / CLI / MCP, Public Contracts |
| Python SDK added metadata route helpers for the existing public `GET /v1/use-cases` and `GET /v1/scoring-stages` route contracts. | Built here as explicit HTTP(S)-only stdlib GET behavior sharing public JSON and Problem Details handling; no auth, retries, service discovery, environment-variable defaults, hosted receipts, private DTOs, database work, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| TypeScript SDK added metadata route helpers for the existing public `GET /v1/use-cases` and `GET /v1/scoring-stages` route contracts. | Built here as explicit HTTP(S)-only native `fetch` GET behavior sharing public JSON and Problem Details handling; no auth, retries, service discovery, environment-variable defaults, hosted receipts, private DTOs, database work, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| CLI added explicit metadata commands for the existing public `GET /v1/use-cases` and `GET /v1/scoring-stages` route contracts. | Built here as explicit HTTP(S)-only Python SDK plumbing with JSON stdout and Problem Details stderr; no hidden network calls, auth, retries, environment-variable defaults, hosted receipts, private DTOs, database work, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| MCP added explicit metadata tools for the existing public `GET /v1/use-cases` and `GET /v1/scoring-stages` route contracts. | Built here as explicit HTTP(S)-only Python SDK plumbing with MCP text JSON results and Problem Details tool errors; no hidden network calls, auth, retries, environment-variable defaults, hosted receipts, private DTOs, database work, or production evidence lookup moved. | SDK / CLI / MCP, Public Surface Contracts |
| `CandidateSet` and `EvidenceSet` now reject mutable list-backed sequence inputs in the Python core. | Built here as public contract immutability hardening for existing storage-free payloads; JSON serialization still emits public arrays, empty evidence sets remain valid, and no graph lookup, evidence lookup, scorer runtime, DB work, or private source adapter moved. | Public Contracts |
| Scoring-stage catalog schema tests now pin uniqueness on stages and stage contract refs. | Built here as a drift guard for the existing public schema; no new scorer stages, scoring formulas, runtime, DB work, or private methodology moved. | Methods / Schemas, Open-Core Boundary / CI |
| Scoring-stage catalogs now reject non-contiguous ordinals in the Python core. | Built here as public method-stage order hardening; JSON Schema remains structural, and no scorer formulas, runtime, DB work, telemetry, or private methodology moved. | Public Contracts, Methods / Schemas |
| Recommendation `ranked` now pins `uniqueItems` in JSON Schema. | Built here as schema/core parity for the existing single-scale recommendation contract; no scorer normalization, private score semantics, hosted receipt behavior, runtime, or DB work moved. | Public Contracts, Methods / Schemas |
| Recommendation `RankingGroup.ranked` now pins `uniqueItems` in JSON Schema. | Built here as schema/core parity for the existing grouped recommendation contract; no cross-kind normalization, scorer runtime, private score semantics, DB work, or hosted receipt behavior moved. | Public Contracts, Methods / Schemas |
| Recommendation `exclusions` now pin `uniqueItems` in JSON Schema and reject duplicate exclusion rows in the Python core. | Built here as public response-shape hardening for existing storage-free exclusions; no gate policy, private safety taxonomy, scorer runtime, DB work, hosted operation, or telemetry moved. | Public Contracts, Methods / Schemas |
| Python and TypeScript SDKs now parse `Retry-After` strictly as integer seconds. | Built here as public client error-header hardening for existing Problem Details behavior; malformed headers become absent retry hints, and no retry loop, auth, hosted receipt, service discovery, telemetry, or private route behavior moved. | SDK / CLI / MCP, Public Surface Contracts |
| Recommendation abstention state now requires `the_call` and `abstention` to agree. | Built here as public envelope consistency in core, JSON Schema, and TypeScript types; no evidence-floor threshold, private abstention taxonomy, scorer/runtime behavior, DB work, or hosted operation moved. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Recommendation abstention responses must be empty single-scale responses. | Built here as public response-shape consistency in core, JSON Schema, and TypeScript types; no scorer threshold, evidence-floor policy, private reason taxonomy, runtime behavior, DB work, or hosted operation moved. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Recommendation `shortlist_depth` now must match the returned ranked row count. | Built here as Python core response-shape consistency for single-scale and kind-grouped recommendations; JSON Schema stays structural, and no scorer threshold, private ranking policy, runtime behavior, DB work, hosted operation, or telemetry moved. | Public Contracts |
| Remaining live scorer calls, hosted receipts, auth, persistence, graph lookup, source adapters, and eval-integrity material were not ported. | Keep private or out until each item has a public contract and no secret/private-data dependency. | Public Surface Contracts, Scoring / Materializer Runtime, DB Bootstrap / Syndai Ops, Hosted Ops / GTM, Evaluation Integrity |

## In Progress

- Public/private porting triage and workstream routing.
- Current source of truth is split between:
  - Python contracts in `packages/core/src/evalrank_core/contracts.py`
  - Public JSON Schemas in `schemas/`
  - Public porting decisions in `docs/PORTING.md`
- Private Syndai build-readiness docs and operational plans, summarized here only when public-safe.
- Latest private-side dirty check: Syndai currently has uncommitted preflight/repo-guidance edits, backend runtime reliability edits, a private EvalRank doc-validator test/check path, and Memphant memory-system spec/plan edits. Treat preflight and runtime work as Syndai-owned, Memphant work as memory-system-owned, and EvalRank-named doc-validator material as private input only unless a later task extracts an explicit EvalRank storage-free contract or public doc check.
- Latest private-source inventory: the Syndai checkout contains 25 private EvalRank spec docs, 6 private EvalRank build-plan docs, 18 private UI/proof assets, and 5 backend migration/guard/test assets. These are routing inputs only. Public ports should continue as explicit storage-free contracts, schemas, synthetic fixtures, deterministic checks, public route contracts, or sanitized method notes.
- Latest public-repo safety review: `siddmax/evalrank` is public with GitHub secret scanning, push protection, and Dependabot security updates enabled; local public-boundary checks remain mandatory because platform scanning is only a backstop.
- Latest port review: storage-free contracts, schemas, synthetic fixtures, public SDK/CLI/MCP boundaries, public route contracts, deterministic public-boundary checks, and sanitized method notes can move here. Public recommendation identifier aliases, storage-free `RawEntry`, public `CandidateSet`, public `StageCandidate`, public `EvidenceItem`, public `ResultRow`, public `UseCaseCatalog`, public `ScoringStageCatalog`, public `RankingGroup`, public `EvidenceSet`, public `Exclusion`, structured public `the_call`, public `Abstention`, the first storage-free OpenAPI route contracts, retry-aware public Problem Details error shape, Python/TypeScript SDK metadata route helpers, CLI metadata commands, and MCP metadata tools have moved. The private-side planning scan is summarized in `docs/PORTING.md` by workstream, not copied. Private EvalRank specs, build-readiness plans, UI proof assets, doc validators, DB bootstrap, Supabase migrations, live deploy wiring, telemetry, billing/admin/GTM, private integrations, credentials, production data, HMAC/secret-backed hosted IDs, source adapters, live fetch behavior, graph lookup, live evidence lookup, evidence ledger runtime, cross-kind score normalization, benchmark weights, IRT fit clusters, thin-coverage/synthesis policy details, Stage-2+ scorer rows, gate policy, private reason taxonomy, scorer thresholds, private problem types, and held-out evaluation material stay private unless a later task extracts a concrete public contract.

## Current Port-Over Snapshot

| Change or source area | Public status | Owning workstream |
| --- | --- | --- |
| Public repository scaffold, package boundaries, CI, license/notice hygiene, and boundary scanner | Ported here | Open-Core Boundary / CI |
| Storage-free core payloads: capability fingerprint, methodology version, raw entry, evaluation request, candidate set, stage candidate, evidence item, result row, use-case catalog, ranking group, evidence set, exclusion, `the_call`, abstention, ranked entity, recommendation, recommendation aliases, strict public calendar-valid freshness/result-run dates, strict public UTC timestamp format, strict public HTTP(S) result source URLs, strict recommendation envelope validation, strict recommendation rank contiguity/order, strict recommendation exclusion uniqueness, strict abstention-as-empty-single-scale behavior, strict recommendation `shortlist_depth` count consistency, tuple-backed candidate/evidence set validation, and entity reference | Ported here | Public Contracts |
| Public JSON Schemas and schema drift tests for current payloads | Ported here, including retry-aware Problem Details extensions | Methods / Schemas, Public Contracts, Public Surface Contracts |
| Synthetic fixtures, runnable public example, CLI fixture/metadata/recommend commands, MCP fixture/metadata/recommend tools, Python SDK re-exports/client, and TypeScript public types/client | Ported here, including raw-entry, candidate-set, stage-candidate, result-row, problem, use-cases, scoring-stages, ranking-group, evidence-set, exclusion fixture surfaces, first recommendation clients/tools, Python/TypeScript SDK metadata route helpers, CLI metadata commands, MCP metadata tools, and README drift guards | SDK / CLI / MCP, Examples, Open-Core Boundary / CI |
| Public package README metadata | Ported here as concise package metadata blocks plus deterministic manifest drift tests for public distribution names, imports, dependencies, entrypoint, license, TypeScript module/type metadata, and private publish status. | Open-Core Boundary / CI, Docs / Public Planning |
| Public scoring-stage vocabulary, catalog, and private-boundary notes | Ported here, including contiguous public stage ordinals, `ScoringStageCatalog`, `CandidateSet`, `StageCandidate`, `ResultRow`, `EvidenceSet`, `Exclusion`, `Abstention`, and the use-case taxonomy method | Methods / Schemas |
| `RawEntry` ingestion-normalization contract | Ported here as a storage-free synthetic fixture contract | Public Contracts |
| `CandidateSet` candidate-resolution contract | Ported here as a storage-free list of public `EntityRef` candidates; Python core inputs must be tuple-backed before serialization to public arrays | Public Contracts, Methods / Schemas |
| `StageCandidate` Stage-1 retrieval row | Ported here as a storage-free candidate fingerprint plus public entity, fused score, RRF ranks, and retrieval provenance | Public Contracts, Methods / Schemas |
| `ResultRow` ingested result provenance envelope | Ported here as a storage-free benchmark/result row with public flags and verification state | Public Contracts, Methods / Schemas |
| `EvidenceSet` evidence-attachment contract | Ported here as a storage-free list of public `EvidenceItem` rows; empty tuple-backed inputs are allowed for no-evidence or abstention paths before serialization to public arrays | Public Contracts, Methods / Schemas |
| `Exclusion` exclusions-with-reasons contract | Ported here as a storage-free subject plus public reason/detail row | Public Contracts, Methods / Schemas |
| Structured public `the_call` / decision-confidence shape and public `Abstention` reason/detail object | Ported here as storage-free nested recommendation contracts | Public Contracts, Methods / Schemas |
| REST/OpenAPI source of truth | Route contracts ported for `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations`; public errors use reusable RFC 9457 Problem Details responses plus retry and rate-limit headers | Public Surface Contracts |
| Use-case taxonomy and `/v1/use-cases` route shape | Ported here as storage-free public taxonomy only: id/slug, name, one-line definition, entity-kind spans, ranked-vs-overlay policy, fixture, schema, SDK/CLI/MCP parity, OpenAPI route contract, and sanitized method note | Public Contracts, Public Surface Contracts, SDK / CLI / MCP, Methods / Schemas |
| Recommendation comparability and ranking groups | Ported here as storage-free response shapes only: single-scale recommendations now require unique ranked rows, and `kind-grouped` recommendations contain closed `RankingGroup` rows with within-kind ranked entities, unique grouped ranked rows, and rationale | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Use-case benchmark weights, IRT cluster crosswalk, confidence policies, and synthesis/coverage rules | Keep private for now; later publish only sanitized method notes that omit weights, held-out tasks, proprietary tuning, and private benchmark outputs | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |
| Supabase schema bootstrap, migrations, grants/RLS, live DB checks, and shared Finn/Supabase operations | Keep private | DB Bootstrap / Syndai Ops |
| Syndai EvalRank migration guard and runner tests | Keep private with the current DB bootstrap; port only a public migration-policy checklist if EvalRank later owns persistence. | DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| Syndai EvalRank doc-validation rules for private specs and build plans | Do not copy private spec checks. Distill only public-facing invariants into this repo when the matching public docs or plans exist. | Docs / Public Planning, Open-Core Boundary / CI |
| Current Syndai dirty worktree categories | Preflight/repo-guidance and backend runtime reliability edits stay in Syndai; Memphant spec/plan edits stay in the memory-system workstream; EvalRank-named doc-validator material remains private input only. Port only an explicit public contract or public doc check extracted from those areas. | Syndai runtime workstream, Memphant / memory-system workstream, Docs / Public Planning, Public Contracts only after explicit extraction |
| Private EvalRank UI proof assets and hosted-product design docs | Keep private until UI routes or public product docs are intentionally added; then port only synthetic screenshots or public-safe docs. | Public Surface Contracts, Hosted Ops / GTM |
| Deterministic scorer, materializer, entity graph persistence, and evidence-ledger runtime | Incubate private until separable from production data and proprietary tuning | Scoring / Materializer Runtime |
| Hosted receipts, HMAC-backed IDs, auth, billing/admin/GTM, telemetry, deploy config, and credentials | Keep private | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out tasks, graders, answers, traces, benchmark outputs, and judge-calibration material | Never port | Evaluation Integrity |

## Porting Queue

| Priority | Workstream | Destination | Public handling |
| --- | --- | --- | --- |
| 1 | Public Contracts | This repo | First raw entry, request, candidate set, stage candidate, result row, use-case catalog, ranking group, evidence set, exclusion, `the_call`, abstention, recommendation, recommendation alias, and entity/evidence slices ported; extend only for new public payload contracts. |
| 2 | Methods / Schemas | This repo | Public scoring-stage vocabulary/catalog, contiguous stage-order invariant, and use-case taxonomy method note ported; add details only after private material is removed. |
| 3 | SDK / CLI / MCP | This repo | Python and TypeScript SDK metadata route helpers, CLI metadata commands, MCP metadata tools, Python SDK/TypeScript SDK/CLI/MCP first recommendation clients/tools, and fixture surfaces are ported; richer behavior waits for pinned public contracts. |
| 4 | Docs / Public Planning | This repo | Current status, repo structure, porting docs, and first runnable example are public-safe; keep updating them with each port. |
| 5 | Public Surface Contracts | This repo | First OpenAPI route contracts and retry-aware public error responses are ported; add more routes only when concrete public contracts exist, and keep private DTOs and hosted auth outside. |
| 6 | DB Bootstrap / Syndai Ops | Syndai repo | Keep Supabase migrations, live bootstrap, grants/RLS, and operational checks private during incubation. |
| 7 | Scoring / Materializer Runtime | Private incubation first | Split reusable deterministic core before porting; private data, proprietary weights, and live workers stay out. |
| 8 | Evaluation Integrity | Private eval systems | Keep held-out tasks, graders, answers, traces, and benchmark results private. |
| 9 | Hosted Ops / GTM | Private hosted systems | Keep billing, admin, telemetry, vendor intent, and account operations out of this repo. |
| 10 | Secrets / Deploy Ops | Private ops only | Keep credentials, Doppler config, live project refs, and deploy environment files out of Git history. |

## Next

- Public Contracts workstream: pin the next storage-free payload contract before adding more SDK/CLI/MCP behavior; keep hardening existing public envelopes when schema/core drift is found. Do not treat private runtime worker changes as public payload contracts.
- SDK / CLI / MCP workstream: Python SDK, TypeScript SDK, CLI, and MCP now cover the public metadata routes; Python/TypeScript SDKs, CLI, and MCP cover the first `POST /v1/recommendations` behavior. Promote richer behavior only after each public client contract is pinned.
- Public Surface Contracts workstream: extend OpenAPI only for concrete public routes or route-specific problem types beyond the current shared retry vocabulary.
- Scoring / Materializer Runtime workstream: keep runtime and private evidence material in incubation until the deterministic, storage-free public core is separable.
- Docs / Public Planning workstream: keep `docs/STATUS.md`, `docs/PORTING.md`, `docs/REPO_STRUCTURE.md`, package READMEs, and build logs aligned in the same change.
- Secrets / Deploy Ops workstream: keep relying on GitHub push protection and secret scanning as backstops, but block leaks earlier with local boundary checks and private review before every public port.
- Update `NAVIGATION.md` when EvalRank adds or changes public API routes, UI routes, deeplinks, or navigation-critical docs.

## Left

- Public repo: additional storage-free contracts, schemas, SDK/CLI/MCP behavior, public examples, additional routes/problem types, UI navigation docs, and reproducible public evaluation fixtures.
- Private/Syndai or hosted systems: data-plane tables, Supabase migrations, entity graph persistence, evidence ledger, Stage-2+ scorer/materializer rows, private trust/security policy runtime, engine materializer, production telemetry, governance operations, billing/admin, and GTM fleet.
- Private evaluation systems: held-out tasks, graders, answers, traces, benchmark outputs, and proprietary ranking experiments.

## Update Rules

- Update this file when a feature lands, a wave gate changes, or an item moves between `Next`, `In Progress`, and `Built`.
- Keep dated build logs under `docs/build-log/` for immutable-ish snapshots; keep this file current.
