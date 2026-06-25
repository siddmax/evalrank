# Public Progress And Porting Recheck

Date: 2026-06-26

## What changed

- Updated the living status and porting maps with the latest public recommendation-comparability schema hardening.
- Rechecked the private Syndai dirty worktree by path/category only.
- Confirmed the current uncommitted private-side changes remain Memphant spec and validation/lifecycle planning work, not EvalRank public-core port candidates.

## Port routing

- Current public EvalRank work stays focused on storage-free contracts, JSON Schemas, synthetic fixtures, route contracts, deterministic checks, and sanitized method notes.
- Current Memphant dirty work routes to the Memphant / memory-system workstream unless a later task extracts an explicit EvalRank storage-free contract.
- Supabase migrations, grants/RLS, live DB checks, deploy wiring, hosted auth, telemetry, billing/admin, and credentials stay in private Syndai/hosted workstreams until an explicit public persistence cutover exists.
- Runtime scorer/materializer, source adapters, graph/evidence lookup, held-out tasks, graders, answers, traces, benchmark outputs, and proprietary tuning stay private until a public-input-only slice is deliberately split.

## Public boundary

- No raw private planning text, private proof assets, migration scripts, customer data, production rows, secrets, telemetry, live project refs, or held-out evaluation material was copied into this repo.
