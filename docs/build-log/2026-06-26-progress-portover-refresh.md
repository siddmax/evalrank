# Progress Port-Over Refresh

Date: 2026-06-26

## What Changed

- Refreshed `docs/STATUS.md` with the latest public build state and current private-side dirty-worktree routing.
- Refreshed `docs/PORTING.md` so agents route the current Memphant spec and plan edits to the Memphant / memory-system workstream instead of copying them into EvalRank.
- Rechecked the private Syndai file inventory by path only and avoided copying raw private planning text into this public repo.

## What Is Done

- Public EvalRank has storage-free core contracts through recommendation abstention and scoring-stage abstention output alignment.
- Public schemas, OpenAPI route contracts, SDK type/re-export surfaces, fixture-only CLI/MCP adapters, runnable public examples, status docs, porting docs, repo structure docs, route navigation, and boundary tests are in place.
- The public repo remains contract-first and fixture-only: no live scorer, source adapter, graph lookup, persistence, auth, billing/admin, telemetry, hosted receipts, deploy config, production rows, or held-out evaluation material has been ported.

## Current Port Decision

| Source area | Decision | Workstream |
| --- | --- | --- |
| Current Syndai dirty worktree: Memphant spec edits and two Memphant validation/lifecycle plan files | Do not port to EvalRank. Keep in the Memphant / memory-system workstream unless a future task extracts a concrete storage-free EvalRank contract. | Memphant / memory-system workstream |
| Private EvalRank planning docs, build-readiness plans, UI proof assets, doc validators, and migration bootstrap in Syndai | Use as private inputs only. Summarize decisions publicly; do not copy raw docs, proof assets, live operational scripts, or private migrations. | Docs / Public Planning, Public Contracts, Public Surface Contracts, DB Bootstrap / Syndai Ops |
| Additional storage-free payloads, JSON Schemas, synthetic fixtures, public method notes, and deterministic boundary/drift checks | Port here one pinned artifact at a time with tests and public examples. | Public Contracts, Methods / Schemas, SDK / CLI / MCP, Open-Core Boundary / CI |
| Supabase schema bootstrap, grants/RLS, live DB checks, hosted deploy wiring, telemetry, billing/admin, credentials, production evidence rows, and held-out benchmark material | Keep private. | DB Bootstrap / Syndai Ops, Hosted Ops / GTM, Secrets / Deploy Ops, Evaluation Integrity |

## Public Safety Note

GitHub secret scanning and push protection are useful backstops for a public repository, but they are not the policy. Run the local public-boundary check before every port, and treat any real secret that reaches Git history as compromised and requiring revocation or rotation.

## Verification Intent

- `python3 scripts/check_public_boundary.py --root .`
- `make check`
