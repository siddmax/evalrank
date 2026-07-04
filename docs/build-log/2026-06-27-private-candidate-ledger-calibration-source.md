# Private Candidate-Ledger Calibration Source

Date: 2026-06-27

Scope: private Syndai EvalRank worktree only. This public log records the public-safe status update; no private schema rows, private fixtures, customer data, hosted runtime code, or Syndai implementation files were copied into the public EvalRank repo.

## What Changed Privately

- Added a calibration-only ingestion path for full golden-eval snapshots that rejects dry runs, selected-case runs, and partial banks.
- Added a private `syndai-coding-router-candidate-ledger` EvalRank source projection for candidate rows that are useful for calibration but not active route evidence.
- Made task-level golden item identities source-independent when a `case_id` is present, so comparable full-bank cases line up across active and candidate snapshots.
- Made item-response projection replace one source snapshot at a time, preventing stale duplicate rows from distorting the response matrix.
- Granted the private EvalRank cron role the delete privilege needed for idempotent source-snapshot replacement.

## Evidence

- Existing full-bank Sonnet candidate baseline: `claude_code / claude-sonnet-4-6`, `dry_run=false`, `task_count=20`, `pass_count=12`, `pass_rate=0.6`, with `coding_repair=3/10`, `site_clone=4/5`, and `review_only=5/5`.
- Private candidate rows ingested: 3.
- Private candidate source snapshot: `coding-router-candidate-ledger-2026-06-27T114700Z`.
- Private candidate item responses projected: 26.
- Private active item responses rebuilt with source-independent case ids: 61.
- Private pooled fit snapshot: `autonomous-swe-agent-pooled-current-plus-candidate-2026-06-27T115200Z`.
- Private pooled fit id: `irt_6d3eb1deb9ff796f74461222`.
- Private pooled fit matrix: 3 entities, 9 informative items, 87 total response rows, 27 binary response rows, and 60 excluded aggregate or non-informative rows.
- Private pooled diagnostics: `publishable=true`, `max_r_hat=1.003291`, `min_effective_sample_size=1167.966431`, `divergence_count=0`.
- Private SBC diagnostics: `sbc_publishable=true`, `sbc_rank_count=210`, `sbc_max_mean_rank_z=2.472782`, `sbc_edge_rank_fraction=0.004762`.
- Private calibration ordering from the pooled fit: Claude Opus first, Codex GPT-5.5 second, Claude Sonnet candidate third.

## Product Decision

Candidate full-bank evidence may improve calibration, but it must not silently become active route evidence. The best long-term user experience is to use all comparable measured evidence for statistical calibration while keeping route promotion governed by the stricter active-evidence gate. This balances accuracy and UX first, then cost, then latency: users get better uncertainty-aware rankings without paying for unnecessary repeated live runs or accepting unearned route promotion.

Pi stays wired and quarantined from default promotion. It is not the third calibration entity for this gate.

## Public Boundary

The public EvalRank repo still owns product-neutral contracts, schemas, SDKs, CLI, MCP boundary, examples, and method notes. Private Supabase/Postgres migrations and source projections remain in Syndai's private `evalrank` schema until EvalRank has its own deploy/release path or dedicated Supabase project.
