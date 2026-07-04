# 2026-06-28 Private Served Cache Source Boundary

## What Changed

- Added a private materializer guard so `autonomous-swe-agent` served caches must come from `coding-router-active-*` snapshots by default.
- Auxiliary validation/dogfood/source-adapter proof caches now require an explicit private override.
- Restored the target active `autonomous-swe-agent` cache from the coding-router refresh chain.

## Boundary

- This remains private Syndai runtime behavior over the private `evalrank` schema.
- No public persistence, public runtime, request-time scorer, hosted route, UI, or billing behavior changed in this Apache-2.0 repo.

## Verification

- Red regression failed before implementation.
- Focused private materializer-script lane: `7 passed`.
- Broader private EvalRank source/materializer lane: `101 passed`.
- Focused ruff and ty checks: passed.
- Target guard proof rejected the validation snapshot by default.
- Target restore emitted `rec_230030790dc52449ed7625be` from `coding-router-active-9d629dd4`.
- Target active-cache check verified the active `autonomous-swe-agent` cache is back on `coding-router-active-9d629dd4`.
- Private repo `make check`: passed.
- Public repo `make check`: passed.
- `git diff --check` in private and public repos: passed.

## Coverage Rationale

This fixes served-cache source ownership for the best UX: public-style recommendation reads stay on the intended risk-adjusted coding-router cache, while auxiliary source evidence can still be projected and inspected privately. It does not complete worker-owned source scheduling, terminal dogfood production, hosted/staging proof, quota/billing, or Pi promotion.
