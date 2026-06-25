# EvalRank Public Porting Map

This repo is public. Port only artifacts that are portable, sanitized, and useful without private Syndai/Finn/Savida context.

## Default Rule

- Public by default: contracts, schemas, SDK boundaries, CLI/MCP interfaces, examples, public method notes, repo hygiene, and deterministic boundary checks.
- Private by default: secrets, live DB operations, customer data, production telemetry, private evidence rows, held-out benchmark tasks or answers, billing/admin internals, vendor intent data, hosted-product-only workflows, and private Syndai/Finn/Savida integration code.
- When unsure, keep the source private and port a short public summary instead.

## Already Public

- Apache-2.0 repository scaffold and package boundaries.
- Root and scoped `AGENTS.md`, plus `CLAUDE.md` shim.
- Public progress docs: `docs/STATUS.md` and `docs/REPO_STRUCTURE.md`.
- Public boundary checker and default unit tests.
- Core Python recommendation contracts.
- Public JSON Schemas for ranked entities and recommendations.
- Direct `main` push workflow for the scratch-build phase.

## Porting Decisions

| Artifact or workstream | Destination | Owner workstream | Status |
| --- | --- | --- | --- |
| Public contract dataclasses and JSON Schemas | This repo | Public Contracts | Partly ported |
| Repo boundary checks, license hygiene, and CI gates | This repo | Open-Core Boundary / CI | Partly ported |
| Sanitized build-readiness summaries from Syndai planning docs | This repo | Docs / Public Planning | In progress |
| REST/OpenAPI contracts | This repo | Public Surface Contracts | Wait until the first concrete route contract exists |
| SDK, CLI, and MCP implementations | This repo | SDK / CLI / MCP | Wait until contracts are pinned |
| Public methodology notes | This repo | Methods / Schemas | Port only after removing held-out and proprietary details |
| Finn/Supabase `evalrank` schema bootstrap and migration runner | Syndai repo | DB Bootstrap / Syndai Ops | Keep private during incubation |
| Secrets, Doppler config, live project refs, and deployment credentials | Private ops only | Secrets / Deploy Ops | Never port |
| Production evidence graph rows, telemetry, and customer traces | Private hosted systems | Hosted Ops | Never port |
| Held-out fixtures, graders, answers, traces, and benchmark results | Private eval systems | Evaluation Integrity | Never port |
| Billing, admin, GTM, vendor intent, and account-operation flows | Private hosted systems | Hosted Ops / GTM | Keep private unless sanitized as public docs |

## Porting Checklist

Before moving anything into this repo, verify:

- It contains no secrets, tokens, environment files, or live credential material.
- It contains no customer data, production telemetry, private evidence rows, or account-operation traces.
- It contains no held-out benchmark tasks, answers, graders, model traces, or private result tables.
- It does not import or depend on private Syndai/Finn/Savida packages.
- It does not require live database access or private Supabase privileges to understand or test.
- It does not expose proprietary hosted-product workflows that are not part of the open core.
- Its license is compatible with Apache-2.0 public distribution.
- `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, `TESTS.md`, and the nearest `AGENTS.md` stay current when the port changes scope or checks.
- `python3 scripts/check_public_boundary.py --root .` and `python3 -m unittest discover tests` pass.

## Current Workstreams

- Public Contracts: pin core payloads and schema compatibility.
- Open-Core Boundary / CI: expand deterministic guards before larger ports.
- DB Bootstrap / Syndai Ops: keep shared Finn/Supabase migrations private until EvalRank owns persistence.
- Methods / Schemas: publish only reusable method notes and schemas.
- SDK / CLI / MCP: implement public clients once contracts stabilize.
- Hosted Ops / GTM: keep private operational workflows outside this repo.
- Evaluation Integrity: keep held-out materials private and publish only reproducible public fixtures.
- Docs / Public Planning: keep this file, `docs/STATUS.md`, and `docs/REPO_STRUCTURE.md` aligned.

## External Guardrails

- GitHub push protection can block supported secrets before they enter a repository.
- If sensitive data reaches Git history, treat it as compromised, rotate credentials, and follow a coordinated removal process.
- Supabase custom schemas must be deliberately exposed and granted for API access; EvalRank incubation uses private schema bootstrap outside this public repo.
