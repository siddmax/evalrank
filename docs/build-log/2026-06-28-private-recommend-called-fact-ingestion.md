# 2026-06-28 Private Recommend Called Fact Ingestion

## What Changed

- Added a private Syndai `evalrank.recommend_events` fact table for cache-backed recommendation reads.
- The private cached recommendation routes now persist the same `recommend.called` payload they already emit, including bounded top-k entity ids, ranked count, cache lineage lag, consumer class, surface, and methodology version.
- The write is same-session and synchronous on successful reads so pre-production telemetry facts fail fast instead of becoming best-effort background delivery.

## Boundary

- The fact table, grants, RLS policies, and route hook stay in the private Syndai worktree and private `evalrank` schema.
- No public runtime, public persistence, public UI, hosted billing, request-time scorer, or customer evidence lookup was added to this Apache-2.0 repo.

## Verification

- Focused private telemetry writer/controller/migration lane: `9 passed`.
- Private cached recommend API and telemetry lane: `35 passed`.
- Private EvalRank read-scope migration lane: `2 passed`.
- Focused ruff, ty, and `scripts/check_evalrank_migration_boundary.py`: passed.
- Target DB migration applied: `2026_06_28_028_evalrank_recommend_events`.
- Target DB writer proof inserted `evt_evalrank_fact_proof_f1ce417f93b74e1b8d19` with `name='recommend.called'`, domain `autonomous-swe-agent`, surface `api`, and one ranked entity.
- Private repo `make check`: passed.
- Public repo `make check`: passed.
- `git diff --check` in private and public repos: passed.

## Coverage Rationale

This adds the first private queryable fact-table transport for recommendation-read telemetry. It moves W8 and metrics/observability specs forward, but does not complete UI verdict rendering, event streams, KPI analytics, hosted/staging proof, quota/billing, or self-improvement automation.
