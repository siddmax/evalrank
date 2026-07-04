# 2026-06-27 Private Source Lifecycle Events

Private Syndai added an append-only EvalRank source lifecycle event ledger in the dedicated private `evalrank` schema.

Public boundary: no private rows, prompts, traces, customer data, or hosted runtime code were copied into this repo.

Evidence summary:

- Red/green private tests covered the source-event builder/writer, migration contract, and projection-script contract.
- Private focused checks passed with `52 passed`, plus focused ruff, ty, and EvalRank migration-boundary checks.
- Target DB applied `2026_06_27_025_evalrank_source_evidence_events`.
- Target DB proof projected 25 active coding-router lifecycle events: 12 `observed`, 12 `promoted`, and 1 `snapshot_active`.
- Target DB proof verified `evalrank_cron` can insert but not update event rows, and the append-only trigger is enabled.

Long-term decision: lifecycle events are source facts, not request-path ranking work. They should feed future staleness, tombstone, dispute, and retention flows offline while public recommendation reads continue serving the active materialized cache.
