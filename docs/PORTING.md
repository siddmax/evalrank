# EvalRank Public Porting Map

This repo is public. Port only artifacts that are portable, sanitized, and useful without private Syndai/Finn/Savida context.

Last reviewed: 2026-06-25

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
- Core Python capability fingerprint, raw entry, evaluation request, recommendation, entity reference, and evidence item contracts.
- Public JSON Schemas for capability fingerprints, raw entries, evaluation requests, ranked entities, recommendations, and evidence items.
- Pinned public `methodology_version` format: `YYYY-MM-DD.SEQ.slug`.
- Direct `main` push workflow for the scratch-build phase.
- `make check` public local/CI gate.
- W0 public exit packet and W1 entity/evidence contract plan.
- Storage-free capability fingerprints, evaluation requests, entity references, evidence items, public fixtures, and schemas.
- Python SDK package metadata and public core contract re-exports.
- TypeScript SDK package metadata and mirrored public contract types/constants.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Runnable public fixture example.
- Public scoring-stage vocabulary and method-boundary note.
- Public progress router for deciding which private EvalRank workstream owns each future port.
- Public recommendation join aliases: `recommendation_id`, `recommend_id`, and `search_run_id`.
- Public `RawEntry` contract and deterministic `raw-entry` fixture surfaces.

## Ported To Date

| Workstream | Public artifact now in this repo | Private material intentionally excluded |
| --- | --- | --- |
| Public Contracts | `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `RankedEntity`, `Recommendation`, public recommendation ID aliases, `EntityRef`, `EvidenceItem`, constants, and synthetic fixture factories. | Source adapters, storage tables, production entity rows, customer context, private score semantics, hosted HMAC derivation. |
| Methods / Schemas | JSON Schemas for public payloads, the pinned public `methodology_version` format, and the public scoring-stage vocabulary. | Proprietary weights, thresholds, held-out eval definitions, benchmark answers, and private ranking experiments. |
| SDK / CLI / MCP | Python SDK re-exports, TypeScript public types/constants, deterministic CLI fixture command, and deterministic MCP fixture adapter, including `raw-entry`. | Live service clients, auth, tenant/project operations, production evidence lookup, source adapters, and hosted-only workflows. |
| Examples | `examples/public_fixture.py` runnable synthetic fixture output. | Customer demos, production evidence rows, private traces, and held-out eval examples. |
| Open-Core Boundary / CI | Boundary scanner, unit tests, package license/notice checks, and default `make check`. | Private repo checks, Doppler config, live project refs, and deployment credentials. |
| Docs / Public Planning | `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, this porting map, package READMEs, and dated build logs. | Raw private planning docs, private customer examples, operational runbooks, and held-out eval detail. |

## Workstream Router

Use this table before copying anything from private EvalRank planning into this public repo.

| Private-side artifact or change | Public destination | Workstream owner | Public handling |
| --- | --- | --- | --- |
| Storage-free payload contracts, identifier aliases, and JSON-compatible request/response shapes | `packages/core`, `schemas`, SDK types | Public Contracts | Port when the shape stands alone with synthetic fixtures and schema drift tests. |
| Recommendation ID aliases (`recommendation_id`, `recommend_id`, `search_run_id`) | `packages/core`, `schemas`, SDK types | Public Contracts | Public alias contract can move here; hosted HMAC derivation, route receipts, and secret keys stay private until a public route contract exists. |
| OpenAPI, route schemas, REST/MCP parity contracts | `schemas`, future route docs, future `NAVIGATION.md` | Public Surface Contracts | Port only after a concrete public route exists; do not copy private DTOs, auth flows, tenant logic, or hosted-only response fields. |
| CLI/MCP/SDK behavior beyond fixtures | `packages/cli`, `packages/mcp`, `packages/sdk-*` | SDK / CLI / MCP | Implement one pinned public contract at a time, with deterministic tests and no live private service dependency. |
| Public method vocabulary and non-proprietary scoring explanations | `methods`, `schemas`, `docs` | Methods / Schemas | Rewrite as sanitized public notes; omit proprietary weights, thresholds, held-out tasks, answers, traces, and private benchmark outputs. |
| Deterministic scoring or materializer code | Future core/runtime package only after split | Scoring / Materializer Runtime | Keep private during incubation unless it can run on synthetic/public inputs without private evidence rows, secrets, or proprietary tuning. |
| Public-boundary, license, CI, fixture, and schema drift checks | `scripts`, `tests`, `.github/workflows` | Open-Core Boundary / CI | Port aggressively when checks prevent private leaks or public contract drift. |
| Repo progress, build order, and sanitized decision summaries | `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, `docs/build-log` | Docs / Public Planning | Summarize decisions; never paste raw private docs, live IDs, customers, or runbooks. |
| Supabase schema bootstrap, migrations, roles, grants, RLS, pg_cron/pgmq, live DB checks | Syndai repo until cutover | DB Bootstrap / Syndai Ops | Keep private while EvalRank incubates in shared Finn/Supabase infrastructure. A future public cutover needs explicit migration ownership and API exposure docs. |
| Hosted deploy, Fly/Doppler/Modal/R2/OpenObserve wiring, production schedulers | Private hosted systems | Hosted Ops / Deploy Ops | Keep out of this repo; only public setup docs may move after secrets and live IDs are removed. |
| Auth, billing, admin, onboarding, tiering, account ops, GTM/vendor intent | Private hosted systems | Hosted Ops / GTM | Keep private unless converted into product-neutral public docs with no customer or operational data. |
| Held-out suites, graders, answer keys, model traces, judge calibration, private benchmark results | Private eval systems | Evaluation Integrity | Never port; publish only synthetic or public reproducible fixtures. |

## Latest Port Review

Reviewed the private-side EvalRank planning and migration surface by category on 2026-06-25. The public repo should keep accepting only artifacts that stand alone without private infrastructure or data.

| Decision | Workstream |
| --- | --- |
| Port storage-free payload contracts, JSON Schemas, synthetic fixtures, package boundaries, public examples, and deterministic boundary checks here. | Public Contracts, Methods / Schemas, SDK / CLI / MCP, Open-Core Boundary / CI, Docs / Public Planning |
| Port REST/OpenAPI contracts here only after a concrete public route contract exists. | Public Surface Contracts |
| Port deterministic runtime code only after it is separable from private data, live workers, proprietary tuning, and hosted-only controls. | Scoring / Materializer Runtime |
| Keep Supabase schema bootstrap, migration runners, roles, workload isolation, live deployment wiring, and operational checks private during incubation. | DB Bootstrap / Syndai Ops |
| Keep held-out tasks, graders, answers, traces, private benchmark results, and judge-calibration material private. | Evaluation Integrity |
| Keep telemetry operations, billing/admin, vendor intent, account operations, private integrations, credentials, and live project refs out of this repo. | Hosted Ops / GTM, Secrets / Deploy Ops |

Public docs may summarize private planning decisions, but must not copy raw private plans, live identifiers, customer examples, runbooks, production rows, or held-out evaluation details.

## Current Port-Over Assessment

Use this table for the next port decision. The destination is this public repo only when the artifact is portable without private data, secrets, live infrastructure, or proprietary hosted behavior.

| Candidate change | Port decision | Workstream |
| --- | --- | --- |
| Public repo scaffold, package boundaries, license/notice files, CI, and deterministic public-boundary checks | Already ported; keep strengthening leak classes as they are discovered. | Open-Core Boundary / CI |
| Storage-free public payloads and aliases currently represented by core dataclasses and JSON Schemas | Already ported for capability fingerprints, raw entries, evaluation requests, ranked entities, recommendations, recommendation aliases, entity refs, and evidence items. | Public Contracts |
| Public fixture surfaces across core, SDKs, CLI, MCP, and examples | Already ported for deterministic synthetic fixtures only. | SDK / CLI / MCP, Examples |
| Public scoring-stage vocabulary | Already ported as a method-boundary note, without formulas, thresholds, private eval data, or benchmarks. | Methods / Schemas |
| `RawEntry` ingestion-normalization shape | Ported as a storage-free contract with synthetic fixtures and deterministic content hash; source adapters, production metadata, and live fetch behavior stay private. | Public Contracts |
| Public `the_call` / decision-confidence response shape | Port after its public semantics can be expressed without proprietary thresholds, held-out evidence floors, or private confidence tuning. | Public Contracts, Methods / Schemas |
| REST/OpenAPI contract | Port only when a concrete public route exists; keep private auth, tenant logic, hosted receipt internals, and app DTOs out. | Public Surface Contracts |
| Recommendation receipt route and HMAC-backed hosted ID derivation | Do not port yet. Public aliases are enough for open-core interoperability; secret-backed derivation belongs with hosted route design. | Public Surface Contracts, Hosted Ops / Deploy Ops |
| Entity graph tables, evidence ledger storage, methodology table, migrations, grants, RLS, and live DB checks | Keep in Syndai/private systems until EvalRank owns persistence or its own Supabase project. | DB Bootstrap / Syndai Ops |
| Deterministic scorer and materializer runtime | Incubate privately first, then split only public-input-only pieces that do not depend on production rows, private workers, or proprietary tuning. | Scoring / Materializer Runtime |
| SDK/CLI/MCP behavior beyond fixtures | Port one public contract at a time after the corresponding contract and schema are pinned. | SDK / CLI / MCP |
| UI routes, API-route navigation docs, deeplinks, and `NAVIGATION.md` | Wait until navigable public surfaces exist. | Public Surface Contracts, Docs / Public Planning |
| Hosted ops, telemetry, billing/admin/GTM, vendor intent, credentials, deploy files, live project refs, private integrations, and account operations | Keep private unless later rewritten as product-neutral public docs with all operational detail removed. | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out suites, graders, answer keys, traces, judge calibration, private benchmark results, and proprietary ranking experiments | Never port. Publish only synthetic or public reproducible fixtures. | Evaluation Integrity |

## Porting Decisions

| Artifact or workstream | Destination | Owner workstream | Status |
| --- | --- | --- | --- |
| Public contract dataclasses and JSON Schemas | This repo | Public Contracts | Capability fingerprint, raw entry, request, recommendation, entity, and evidence slices ported |
| Recommendation join aliases | This repo | Public Contracts | Ported; hosted HMAC derivation stays private |
| Entity references, evidence items, and evidence-item schema | This repo | Public Contracts | Ported |
| Repo boundary checks, license hygiene, and CI gates | This repo | Open-Core Boundary / CI | Partly ported |
| Sanitized build-readiness summaries from Syndai planning docs | This repo | Docs / Public Planning | In progress |
| Public build-order and wave status | This repo | Docs / Public Planning | In progress |
| Public scoring-stage vocabulary and method boundaries | This repo | Methods / Schemas | Public boundary note ported |
| REST/OpenAPI contracts | This repo | Public Surface Contracts | Wait until the first concrete route contract exists |
| SDK, CLI, and MCP implementations | This repo | SDK / CLI / MCP | Python SDK re-export, TypeScript public types, CLI fixture command, and MCP fixture adapter ported |
| Public methodology notes | This repo | Methods / Schemas | Port only after removing held-out and proprietary details |
| Deterministic scorer/materializer runtime | Private incubation first | Scoring / Materializer Runtime | Port later only if storage-free and public-input-only |
| Finn/Supabase `evalrank` schema bootstrap and migration runner | Syndai repo | DB Bootstrap / Syndai Ops | Keep private during incubation |
| Secrets, Doppler config, live project refs, and deployment credentials | Private ops only | Secrets / Deploy Ops | Never port |
| Production evidence graph rows, telemetry, and customer traces | Private hosted systems | Hosted Ops | Never port |
| Held-out fixtures, graders, answers, traces, and benchmark results | Private eval systems | Evaluation Integrity | Never port |
| Billing, admin, GTM, vendor intent, and account-operation flows | Private hosted systems | Hosted Ops / GTM | Keep private unless sanitized as public docs |

## Port Now

- Additional storage-free Python contracts and JSON Schemas when a new public payload is pinned.
- Public identifier aliases that are deterministic, non-secret, and useful for interoperability.
- Synthetic public fixtures that prove contract shape without using production data.
- Public runnable examples that consume only synthetic fixtures.
- Deterministic checks that prevent private imports, secrets, private data paths, and missing package hygiene.
- Public build logs that summarize decisions without exposing private projects, credentials, customers, held-out tasks, or live telemetry.
- Package README and agent guidance needed for contributors to work inside the public repo.
- Additional TypeScript SDK source only when the package-level check and repo tests prove the public contract shape.

## Port Later

- REST/OpenAPI surfaces after a concrete route contract exists.
- Recommendation receipt routes and HMAC-backed hosted identifiers after public route semantics and secret handling are designed.
- Full REST/OpenAPI, CLI, SDK, and MCP behavior beyond public fixtures after concrete public contracts are pinned.
- Source adapters and live fetch behavior after they can run without private service dependencies or production metadata.
- Public scoring method details after proprietary thresholds, held-out eval details, and private ranking experiments are removed.
- Deterministic scorer/materializer runtime after it is split from private evidence rows, hosted workers, and proprietary tuning.
- Persistence migrations only after EvalRank owns its own deploy/release path or has its own Supabase project.
- UI route docs and `NAVIGATION.md` after routes, deeplinks, or navigation-critical API docs exist.

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
