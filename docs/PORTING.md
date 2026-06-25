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
- Core Python recommendation contracts.
- Public JSON Schemas for ranked entities and recommendations.
- Direct `main` push workflow for the scratch-build phase.
- `make check` public local/CI gate.
- W0 public exit packet and W1 entity/evidence contract plan.
- Storage-free entity references, evidence items, public fixtures, and evidence-item schema.
- Python SDK package metadata and public core contract re-exports.

## Porting Decisions

| Artifact or workstream | Destination | Owner workstream | Status |
| --- | --- | --- | --- |
| Public contract dataclasses and JSON Schemas | This repo | Public Contracts | Partly ported |
| Entity references, evidence items, and evidence-item schema | This repo | Public Contracts | Ported |
| Repo boundary checks, license hygiene, and CI gates | This repo | Open-Core Boundary / CI | Partly ported |
| Sanitized build-readiness summaries from Syndai planning docs | This repo | Docs / Public Planning | In progress |
| Public build-order and wave status | This repo | Docs / Public Planning | In progress |
| Public scoring-stage vocabulary and method boundaries | This repo | Methods / Schemas | Port sanitized public boundaries only |
| REST/OpenAPI contracts | This repo | Public Surface Contracts | Wait until the first concrete route contract exists |
| SDK, CLI, and MCP implementations | This repo | SDK / CLI / MCP | Python SDK re-export ported; CLI/MCP wait for concrete commands/tools |
| Public methodology notes | This repo | Methods / Schemas | Port only after removing held-out and proprietary details |
| Finn/Supabase `evalrank` schema bootstrap and migration runner | Syndai repo | DB Bootstrap / Syndai Ops | Keep private during incubation |
| Secrets, Doppler config, live project refs, and deployment credentials | Private ops only | Secrets / Deploy Ops | Never port |
| Production evidence graph rows, telemetry, and customer traces | Private hosted systems | Hosted Ops | Never port |
| Held-out fixtures, graders, answers, traces, and benchmark results | Private eval systems | Evaluation Integrity | Never port |
| Billing, admin, GTM, vendor intent, and account-operation flows | Private hosted systems | Hosted Ops / GTM | Keep private unless sanitized as public docs |

## Port Now

- Additional storage-free Python contracts and JSON Schemas when a new public payload is pinned.
- Synthetic public fixtures that prove contract shape without using production data.
- Deterministic checks that prevent private imports, secrets, private data paths, and missing package hygiene.
- Public build logs that summarize decisions without exposing private projects, credentials, customers, held-out tasks, or live telemetry.
- Package README and agent guidance needed for contributors to work inside the public repo.

## Port Later

- REST/OpenAPI surfaces after a concrete route contract exists.
- CLI and MCP behavior after a concrete public command or tool contract is pinned.
- Public scoring method notes after proprietary thresholds, held-out eval details, and private ranking experiments are removed.
- Persistence migrations only after EvalRank owns its own deploy/release path or has its own Supabase project.

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

- GitHub push protection can block supported secrets before they enter a repository.
- GitHub secret scanning can detect hardcoded credentials in repository history, but prevention is cheaper than cleanup.
- If sensitive data reaches Git history, treat it as compromised, rotate credentials, and follow a coordinated removal process.
- Supabase custom schemas must be deliberately exposed and granted for API access; EvalRank incubation uses private schema bootstrap outside this public repo.
