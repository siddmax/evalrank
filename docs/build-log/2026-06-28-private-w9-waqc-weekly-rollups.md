# Private W9 WAQC Weekly Rollups

The private Syndai EvalRank worktree added the first W9 north-star metric rollup over private recommendation facts.

Public-safe summary:

- Adds no public route, public storage, billing contract, telemetry export contract, or provider dependency.
- Derives weekly WAQC from private append-only recommendation events.
- Counts headline WAQC from distinct external keyed consumers with successful recommendation calls.
- Keeps first-party dogfood and anonymous diagnostics separate from the headline adoption metric.
- Uses rebuildable UTC Monday-week windows so the metric can be backfilled from raw facts.
- Schedules weekly refresh through the existing private durable worker queue; no new scheduler or provider account is introduced.

Verification in the private worktree:

- Red migration test first failed on the missing private migration.
- Red helper test first failed on the missing rollup module.
- Focused WAQC helper/migration lane passed with `4 passed`.
- Focused private `ruff`, `ty`, and EvalRank migration-boundary checks passed.
- Target private migration applied.
- Target readback verified the rollup table shape and refreshed week `2026-06-22` from 2 existing recommendation facts. Existing facts were non-keyed, so headline external WAQC correctly read back as `0`.
- Red scheduling tests first failed on missing cron constants and worker dispatch.
- Focused private cron/worker/source-of-truth lane passed with `45 passed`.
- Focused scheduler `ruff`, `ty`, Alembic validation, and EvalRank migration-boundary checks passed.
- Target cron migration applied.
- Target readback verified job `evalrank-waqc-rollup` on `30 5 * * 1`, using `pgmq.send`, no HTTP command, with the queue present.

Hosted dashboards, W1-W4 retention cohorts, governance tripwires, and GTM agents remain future W9 work.
