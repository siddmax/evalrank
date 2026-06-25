# Port-Over Inventory Refresh

Date: 2026-06-26

## What changed

- Refreshed `docs/PORTING.md` with the current private-source inventory and next public port slices.
- Kept the update public-safe: only source categories, counts, workstream owners, and routing decisions are recorded.
- Did not copy private Syndai spec text, proof assets, migrations, operational assumptions, live identifiers, customer data, held-out evaluation material, or credentials.

## Current routing

| Source area | Decision |
| --- | --- |
| Storage-free contracts, schemas, fixtures, public route shapes, package docs, and deterministic checks | Port here one slice at a time with tests. |
| Private EvalRank specs and build plans | Use only as inputs for sanitized public summaries or explicit contracts. |
| UI proof assets and hosted-product docs | Keep private until a public UI route or product doc exists. |
| Supabase migrations, migration runner, live DB checks, grants/RLS, and shared Finn operations | Keep in Syndai/private systems until an explicit persistence cutover exists. |
| Scorer/materializer runtime, graph/evidence lookup, source adapters, proprietary tuning, and private methodology details | Incubate privately until public-input-only pieces can be separated. |
| Held-out tasks, graders, answers, traces, judge calibration, and private benchmark outputs | Never port. |
| Current Memphant dirty worktree | Route to Memphant / memory-system workstream, not EvalRank. |

## Verification inputs

- Scanned private Syndai EvalRank paths by file path and headings only.
- Rechecked the public GitHub repo metadata: public visibility, secret scanning, push protection, and Dependabot security updates are enabled.
- External guardrail reviewed: GitHub documents secret scanning for public repositories as automatic, but this repo still relies on local boundary checks for public/private decisions.
