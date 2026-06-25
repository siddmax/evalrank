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
- Core Python recommendation, entity reference, and evidence item contracts.
- Public JSON Schemas for ranked entities, recommendations, and evidence items.
- Direct `main` push workflow for the scratch-build phase.
- `make check` public local/CI gate.
- W0 public exit packet and W1 entity/evidence contract plan.
- Storage-free entity references, evidence items, public fixtures, and evidence-item schema.
- Python SDK package metadata and public core contract re-exports.
- TypeScript SDK package metadata and mirrored public contract types/constants.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Runnable public fixture example.
- Public scoring-stage vocabulary and method-boundary note.

## Ported To Date

| Workstream | Public artifact now in this repo | Private material intentionally excluded |
| --- | --- | --- |
| Public Contracts | `RankedEntity`, `Recommendation`, `EntityRef`, `EvidenceItem`, constants, and synthetic fixture factories. | Storage tables, production entity rows, customer context, private score semantics. |
| Methods / Schemas | JSON Schemas for public payloads and the public scoring-stage vocabulary. | Proprietary weights, thresholds, held-out eval definitions, benchmark answers, and private ranking experiments. |
| SDK / CLI / MCP | Python SDK re-exports, TypeScript public types/constants, deterministic CLI fixture command, and deterministic MCP fixture adapter. | Live service clients, auth, tenant/project operations, production evidence lookup, and hosted-only workflows. |
| Examples | `examples/public_fixture.py` runnable synthetic fixture output. | Customer demos, production evidence rows, private traces, and held-out eval examples. |
| Open-Core Boundary / CI | Boundary scanner, unit tests, package license/notice checks, and default `make check`. | Private repo checks, Doppler config, live project refs, and deployment credentials. |
| Docs / Public Planning | `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, this porting map, package READMEs, and dated build logs. | Raw private planning docs, private customer examples, operational runbooks, and held-out eval detail. |

## Porting Decisions

| Artifact or workstream | Destination | Owner workstream | Status |
| --- | --- | --- | --- |
| Public contract dataclasses and JSON Schemas | This repo | Public Contracts | Partly ported |
| Entity references, evidence items, and evidence-item schema | This repo | Public Contracts | Ported |
| Repo boundary checks, license hygiene, and CI gates | This repo | Open-Core Boundary / CI | Partly ported |
| Sanitized build-readiness summaries from Syndai planning docs | This repo | Docs / Public Planning | In progress |
| Public build-order and wave status | This repo | Docs / Public Planning | In progress |
| Public scoring-stage vocabulary and method boundaries | This repo | Methods / Schemas | Public boundary note ported |
| REST/OpenAPI contracts | This repo | Public Surface Contracts | Wait until the first concrete route contract exists |
| SDK, CLI, and MCP implementations | This repo | SDK / CLI / MCP | Python SDK re-export, TypeScript public types, CLI fixture command, and MCP fixture adapter ported |
| Public methodology notes | This repo | Methods / Schemas | Port only after removing held-out and proprietary details |
| Finn/Supabase `evalrank` schema bootstrap and migration runner | Syndai repo | DB Bootstrap / Syndai Ops | Keep private during incubation |
| Secrets, Doppler config, live project refs, and deployment credentials | Private ops only | Secrets / Deploy Ops | Never port |
| Production evidence graph rows, telemetry, and customer traces | Private hosted systems | Hosted Ops | Never port |
| Held-out fixtures, graders, answers, traces, and benchmark results | Private eval systems | Evaluation Integrity | Never port |
| Billing, admin, GTM, vendor intent, and account-operation flows | Private hosted systems | Hosted Ops / GTM | Keep private unless sanitized as public docs |

## Port Now

- Additional storage-free Python contracts and JSON Schemas when a new public payload is pinned.
- Synthetic public fixtures that prove contract shape without using production data.
- Public runnable examples that consume only synthetic fixtures.
- Deterministic checks that prevent private imports, secrets, private data paths, and missing package hygiene.
- Public build logs that summarize decisions without exposing private projects, credentials, customers, held-out tasks, or live telemetry.
- Package README and agent guidance needed for contributors to work inside the public repo.
- Additional TypeScript SDK source only when the package-level check and repo tests prove the public contract shape.

## Port Later

- REST/OpenAPI surfaces after a concrete route contract exists.
- Full REST/OpenAPI, CLI, SDK, and MCP behavior beyond public fixtures after concrete public contracts are pinned.
- Public scoring method details after proprietary thresholds, held-out eval details, and private ranking experiments are removed.
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
- Hosted Ops / GTM: keep private operational workflows outside this repo.
- Evaluation Integrity: keep held-out materials private and publish only reproducible public fixtures.
- Docs / Public Planning: keep this file, `docs/STATUS.md`, and `docs/REPO_STRUCTURE.md` aligned.

## External Guardrails

- GitHub push protection can block supported secrets before they enter a repository: https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- GitHub secret scanning can detect hardcoded credentials in repository history, but prevention is cheaper than cleanup: https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns
- If sensitive data reaches Git history, treat it as compromised, rotate credentials, and follow a coordinated removal process.
- Supabase custom schemas must be deliberately exposed and granted for API access; EvalRank incubation uses private schema bootstrap outside this public repo: https://supabase.com/docs/guides/api/using-custom-schemas
- For public API design, prefer a dedicated exposed API schema and keep internal tables/helpers in non-exposed schemas: https://supabase.com/docs/guides/api/securing-your-api
