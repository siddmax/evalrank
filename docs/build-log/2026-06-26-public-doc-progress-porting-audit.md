# Public Doc Progress And Porting Audit

Date: 2026-06-26

## What Changed

- Updated `docs/STATUS.md` with the latest public-safe progress note: the current private Syndai dirty worktree was checked and contains Memphant spec edits only.
- Updated `docs/PORTING.md` with a dated dirty-worktree routing section so agents do not copy adjacent memory-system planning into EvalRank by mistake.
- Updated `docs/REPO_STRUCTURE.md` and root `AGENTS.md` with the same ownership rule: adjacent Memphant, AgentsDB, memory, or general agent-system docs are not EvalRank public-core material unless a concrete storage-free EvalRank contract is extracted.

## What Is Done

- Public repository scaffold, package boundaries, scoped agent docs, package hygiene, CI, and `make check`.
- Public core contracts and schemas through the current storage-free payload set: fingerprints, raw entries, requests, candidate sets, stage candidates, evidence items, result rows, use-case catalogs, ranking groups, evidence sets, exclusions, `the_call`, ranked entities, and recommendations.
- Public fixture surfaces across core, Python SDK, TypeScript SDK types, CLI, MCP adapter, and the runnable example.
- Public OpenAPI contracts for `GET /v1/use-cases` and `POST /v1/recommendations`, including retry-aware RFC 9457 Problem Details.
- Public contract hardening for score components, recommendation envelopes, evidence metadata, and request constraints.

## Porting Decision

| Source area | Decision | Workstream |
| --- | --- | --- |
| Current uncommitted Syndai Memphant spec edits | Do not port to EvalRank. They belong to the memory-system workstream unless a future task extracts a concrete EvalRank public contract. | Memphant / memory-system workstream |
| Existing Syndai EvalRank migrations, bootstrap scripts, grants/RLS, live DB checks, and shared Finn/Supabase operations | Keep private until EvalRank owns persistence or its own Supabase project. | DB Bootstrap / Syndai Ops |
| Public-safe storage-free contracts, schemas, fixtures, method notes, and deterministic drift/leak checks | Keep porting one pinned artifact at a time with tests and synthetic examples. | Public Contracts, Methods / Schemas, SDK / CLI / MCP, Open-Core Boundary / CI |
| Hosted auth, telemetry, billing/admin, deploy config, credentials, live project refs, production rows, and held-out eval material | Keep out of this public repo. | Hosted Ops / GTM, Secrets / Deploy Ops, Evaluation Integrity |

## Public-Repo Guardrail

GitHub public repositories have secret scanning and push-protection support, but EvalRank still treats the local boundary scanner and human/agent port review as required. Platform scanning is a backstop, not the porting policy.

## Verification Intent

- Run the public boundary check and full repo gate before committing this docs-only sync.
