# Private Cached Recommend API And Telemetry Read Surface

Date: 2026-06-27

Scope: private Syndai EvalRank worktree only. This public log records the public-safe status update; no private schema data, private fixtures, customer data, hosted runtime code, secrets, or Syndai implementation files were copied into the public EvalRank repo.

## What Changed Privately

- Added a private cache reader for the active `evalrank.recommendation_cache` base row.
- Added a private `GET /api/v1/recommend?use_case=...` route that returns the materialized recommendation payload unchanged.
- Added `recommend.called` event construction from that same payload, including top-k entity ids, status, latency, `served_from`, methodology version, and trace id.
- Added active-span EvalRank attributes for the recommendation id, domain, status, served-from value, latency, and top-k entity ids when an OpenTelemetry span is present.
- Registered the private controller in the Syndai Litestar app and documented the focused route/test lane.

## Evidence

- Focused private route/cache/telemetry/app-DI lane: `27 passed`.
- Focused private lint lane for the changed route/cache/telemetry/test files: passed.
- Private `make check`: passed.
- Private `make eval-coding-deterministic`: `240 passed, 3 skipped`.
- Public `make check`: passed with 223 Python tests and 7 TypeScript SDK tests.
- Public and private `git diff --check`: passed.

## Product Decision

The hosted EvalRank read path should serve active materialized recommendations from the verified cache. It should not run live evals, IRT fitting, Stage-2 scoring, Stage-3 adjudication, or Stage-4 shortlist work during the user request.

That is the best long-term UX and cost posture: expensive accuracy work happens offline in the private worker/promotion path, while users receive a fast deterministic response with the same recommendation id, evidence caveats, methodology version, and telemetry join key that the worker produced.

## Public Boundary

The public EvalRank repo still owns product-neutral contracts, schemas, SDKs, CLI, MCP boundary, examples, and method notes. Private route execution, Postgres reads, telemetry emission, source adapters, workers, and caches remain in Syndai's private worktree and dedicated private `evalrank` schema until EvalRank has its own deploy/release path or dedicated Supabase project.
