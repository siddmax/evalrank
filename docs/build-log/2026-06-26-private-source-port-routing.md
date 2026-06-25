# Private Source Port Routing

Date: 2026-06-26

## What Changed

- Reviewed the public EvalRank repo status and the current private Syndai EvalRank source areas.
- Updated `docs/STATUS.md` with the latest public-safe progress snapshot.
- Updated `docs/PORTING.md` with the current routing for private specs, build-readiness plans, migration bootstrap, doc validators, UI proof assets, and GitHub public-repo security metadata.

## Current Public State

- Public repo: `siddmax/evalrank`.
- Visibility: public.
- Public core already includes storage-free contracts, JSON Schemas, OpenAPI contracts for `GET /v1/use-cases` and `POST /v1/recommendations`, synthetic fixtures, SDK/CLI/MCP fixture surfaces, public method notes, `STATUS.md`, `PORTING.md`, `REPO_STRUCTURE.md`, `TESTS.md`, and `NAVIGATION.md`.
- Current public boundary remains contract-first and fixture-only. There is no live scorer, graph lookup, source adapter, hosted auth, billing/admin, persistence, or private eval material in this repo.

## Private-Side Scan

| Private-side area | Port decision | Workstream |
| --- | --- | --- |
| Current uncommitted Syndai worktree | Do not port. The dirty files are Memphant docs/plans, not EvalRank public-core artifacts. | Memphant / memory-system workstream |
| `docs/superpowers/specs/evidence-ranked-platform/` | Use as private input only. Port storage-free API or method shapes only after rewriting them as public contracts with synthetic fixtures. | Public Contracts, Public Surface Contracts, Methods / Schemas |
| `docs/superpowers/plans/evalrank/` | Keep raw build-readiness plans private. Port only public-safe build-order summaries, status notes, and dated build logs. | Docs / Public Planning |
| `backend/evalrank_migrations/` and migration runner scripts | Keep private while EvalRank incubates inside the shared Finn/Supabase deploy path. | DB Bootstrap / Syndai Ops |
| EvalRank migration guard tests | Keep with private DB bootstrap for now; later extract public migration-policy checks only if EvalRank owns persistence. | DB Bootstrap / Syndai Ops, Open-Core Boundary / CI |
| EvalRank doc-validation rules in Syndai | Do not copy private spec validators. Distill only public-facing invariants into this repo when public docs carry the matching claims. | Docs / Public Planning, Open-Core Boundary / CI |
| UI proof images and hosted-product design assets | Keep private until a public UI route or public product doc intentionally exists. | Public Surface Contracts, Hosted Ops / GTM |
| Held-out suites, graders, answers, traces, benchmark outputs, and judge calibration | Never port. | Evaluation Integrity |

## GitHub Public-Repo Security Snapshot

Checked with the GitHub CLI on 2026-06-26:

- `visibility`: public.
- `secret_scanning`: enabled.
- `secret_scanning_push_protection`: enabled.
- `dependabot_security_updates`: enabled.
- `secret_scanning_non_provider_patterns`: disabled.
- `secret_scanning_validity_checks`: disabled.

This does not replace the local boundary scanner. Anything sensitive that enters Git history must still be treated as compromised.

## Next Routing

- Public Contracts: continue with storage-free payload hardening and new contracts only when schemas, fixtures, SDK/CLI/MCP surfaces, and tests can move together.
- Public Surface Contracts: extend OpenAPI only for concrete public route contracts; keep hosted auth, tenant logic, private receipt IDs, and live throttling private.
- Open-Core Boundary / CI: consider distilled public doc-drift checks from Syndai only when they guard public docs in this repo.
- DB Bootstrap / Syndai Ops: keep migrations, grants/RLS, live DB checks, and shared Finn/Supabase operations private until an explicit persistence cutover exists.
- Evaluation Integrity: keep held-out and private benchmark material out permanently.

## Verification Intent

- Run the public boundary check and full `make check` before committing this docs-only update.
