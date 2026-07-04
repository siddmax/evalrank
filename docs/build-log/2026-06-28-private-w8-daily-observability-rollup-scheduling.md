# Private W8 Daily Observability Rollup Scheduling

The private Syndai EvalRank worktree scheduled daily recommendation SLI rollups through the existing durable worker path.

Public-safe summary:

- Adds no public route, public storage, public telemetry contract, or provider dependency.
- Reuses the private `pg_cron -> pgmq -> eval_pipeline_worker` pattern.
- Adds message type `evalrank_observability_rollup` on the existing private EvalRank queue.
- Refreshes recent UTC recommendation SLI rollups from private append-only recommendation facts.
- Archives successful jobs, retries failures through queue visibility timeout, and moves unsupported/poison messages to DLQ.

Verification in the private worktree:

- Red tests first failed on missing observability rollup constants/helpers.
- Focused cron/worker/source-of-truth lane passed with `39 passed`.
- Focused `ruff` and `ty` checks passed.
- Migration validation passed.
- Target migration applied.
- Target readback verified the cron job, schedule, pgmq command shape, no HTTP/pg_net command, and existing queue.

Hosted trace export, deployed load proof, and public analytics UI remain future W8 work.
