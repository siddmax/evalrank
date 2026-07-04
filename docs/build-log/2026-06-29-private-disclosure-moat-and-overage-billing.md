# 2026-06-29 — Private disclosure moat + Model A overage billing

Public-safe summary of private-worktree work in `codex-evalrank-w6-spine`. No
secrets, Stripe object ids, or private benchmark text are recorded here.

## Disclosure access-tier gate (the moat)

Added a per-use-case disclosure tier so the public/SEO surface shows only a
small curated set of generic "marquee" categories while the long tail of
specific use cases requires a key.

- New EvalRank migration adds a curated `evalrank.use_case_access` table
  (`access_tier` default `api`, RLS + grants), seeded with the known generic
  use cases as `public`. `access_tier` is orthogonal to the existing
  `publishable` evidence-depth filter: it gates *which categories* are visible
  without a key, not field depth within a row.
- The active-cache reader LEFT JOINs the table (one query, coalesce missing to
  `api`).
- The recommend route returns `404` for anonymous callers on `api`-tier use
  cases — indistinguishable from an unknown use case — so the gated catalog
  cannot be enumerated by probing. Keyed callers get the full catalog.
- Anonymous reads were already per-IP rate limited by the existing route limit;
  no new limiter was added (edge bot/DDoS is handled at the CDN).

## Pricing + disclosure decisions (pinned, private)

- Billing shape: **no seats**. Flat tier + included recommendation quota +
  hard-cap-by-default + opt-in, self-capped overage at **1¢/recommendation**
  (benchmarked against a comparable per-call developer API). Billing never
  affects rank.
- Disclosure tiers split by **category granularity** (marquee public vs
  API-only), not by evidence depth.
- A cached-read financial model backs the rate: the billed unit is a cached
  read (near-zero marginal cost), so contribution margin is ~96% and profit is
  gated by the periodic eval-pipeline recompute (a fixed cost), not the per-rec
  rate. These are private business decisions; only product-neutral notes belong
  in the public repo.

## Model A overage billing

Within the included quota, keyed reads are free and never settled. Past it, the
route hard-stops by default; opted-in callers under their monthly USD cap are
served and metered.

- EvalRank billing resolves a test/live Stripe key (`STRIPE_TEST_KEY` else
  `STRIPE_SECRET_KEY`), so it bills test-mode during incubation and live
  otherwise. The shared Stripe REST helpers gained a backward-compatible
  `api_key` parameter (default keeps the existing live key), so Syndai outcome
  billing is unchanged.
- New EvalRank migration adds `overage_enabled` + `overage_monthly_cap_usd` to
  `evalrank.recommendation_quota_limits` and a `billable` flag (+ partial
  index) on `evalrank.recommend_events`.
- Overage requires both opt-in AND an explicit USD cap (fail closed = no
  surprise bills); the cap is enforced at quota-check granularity (a self-set
  soft cap may overshoot by a request under concurrency).
- Settlement enqueues only `billable` facts (previously every keyed read), and
  a stateless, idempotent subscription guard ensures the customer carries the
  metered price before meter events post.

## Preflight migration coverage

The preflight migration safety net (schema-touch detector + live-DB migration
check) previously watched only the Alembic `backend/migrations/` path. It now
also covers `backend/evalrank_migrations/` raw-SQL migrations and reminds
operators that EvalRank migrations are applied via
`apply_evalrank_migrations.py` and are not auto-applied on deploy.

## Verification

Unit-level only (mocked Stripe/DB): focused EvalRank lanes plus the coding
Stripe billing lanes passed (220 passed at the final sweep), with focused ruff,
ty, and the EvalRank migration-boundary check green. End-to-end test-mode
Stripe and hosted smoke proof remain open until deploy.
