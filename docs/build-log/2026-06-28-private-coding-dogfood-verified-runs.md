# 2026-06-28 Private Coding Dogfood Verified Runs

## What Changed

- Added a private Syndai source adapter for aggregate terminal coding dogfood outcomes.
- The adapter reads `sentry_auto` terminal dogfood outcomes and execution-attempt cost aggregates offline, then writes derived EvalRank rows through the private projection writer.
- Derived EvalRank agent ids are obfuscated with a stable group fingerprint; raw executor/model names are not copied into the public repo or served-cache identifiers.

## Boundary

- The source read stays private in Syndai.
- The benchmark catalog row and future derived entities/evidence/results stay in the private `evalrank` schema.
- No public API, auth, billing, hosted route, or request-time scorer behavior changed.

## Verification

- Focused private adapter/script/migration lane: `5 passed`.
- Expanded private source/materializer/migration lane: `95 passed`.
- Focused ruff, ty, and `scripts/check_evalrank_migration_boundary.py`: passed.
- Target DB migration applied: `2026_06_28_026_evalrank_coding_dogfood_outcome_benchmark`.
- Target projection failed closed because there are currently no terminal `sentry_auto` dogfood outcome rows.
- Private repo `make check`: passed.
- Public repo `make check`: passed.
- `git diff --check` in private and public repos: passed.

## Coverage Rationale

This adds the correct private adapter path for stronger behavioral evidence, but it does not yet count as live source coverage or cache proof until terminal dogfood rows exist.
