# 2026-06-28 Private Worker-Owned Source Refresh Scheduling

## What Changed

- The private Syndai worktree moved EvalRank source refresh scheduling from an eval-worker sleep loop to the existing Syndai `pg_cron -> pgmq -> worker` runtime pattern.
- The private worker now reconciles cron on boot, reads durable `evalrank_source_refresh_jobs` messages, archives only after the pipeline/cache refresh succeeds, and sends exhausted poison messages to the shared DLQ.
- The private cache refresh now projects coding-router lifecycle facts before active evidence materialization.

## Boundary

- EvalRank persistence remains in the private `evalrank` schema.
- The queue, DLQ, cron job, worker process, and customer/control-plane infrastructure remain private Syndai runtime.
- This public repo did not gain a hosted scheduler, private DB client, request-time scorer, source adapter, or private fixture.

## Verification

- Private red regression failed before implementation.
- Focused private worker scheduling lane: `36 passed`.
- Broader private eval-pipeline lane: `90 passed`.
- Private migration/source-of-truth lane: `58 passed`.
- Private materializer/script migration lane: `50 passed`.
- Private migration validation and EvalRank migration-boundary checks passed.
- Focused private ruff and ty checks passed.
- Target DB upgrade reached `2026_06_28_002_eval_pipeline_pgcron_bridge`.
- Target DB verification found queues `evalrank_source_refresh_jobs` / `evalrank_source_refresh_jobs_dlq`.
- Target DB verification found active cron job `evalrank-source-refresh` on `0 5 * * 1`.
- Private repo `make check`: passed.
- Public repo `make check`: passed.
- `git diff --check` in private and public repos: passed.

## Coverage Rationale

This closes a W5 orchestration gap without widening the public repo: cached recommendations keep the best UX path, refresh work becomes durable and retryable, and private runtime state stays private. Remaining work includes terminal dogfood source rows, hosted/staging proof, quota/billing, broader telemetry transport, and Pi promotion readiness.
