# 2026-06-28 Private Coding Validation Outcomes

## What Changed

- Added a private Syndai source adapter for aggregate coding validation outcomes.
- The adapter reads `syndai.coding_validation_runs` joined to `syndai.coding_runs` offline, then writes derived EvalRank rows through the private projection writer.
- Derived EvalRank agent ids are obfuscated with a stable group fingerprint; raw executor/model names, run ids, validator output, and customer identifiers are not copied into EvalRank rows or this public repo.

## Boundary

- The source read stays private in Syndai.
- The benchmark catalog row, source snapshot, entities, evidence, results, and materialized cache stay in the private `evalrank` schema.
- No public API, auth, billing, hosted route, request-time scorer behavior, or public runtime changed.

## Verification

- Focused private adapter/script/migration lane: `5 passed`.
- Expanded private source/materializer/migration lane: `99 passed`.
- Focused ruff, ty, and `scripts/check_evalrank_migration_boundary.py`: passed.
- Target DB migration applied: `2026_06_28_027_evalrank_coding_validation_outcome_benchmark`.
- Target projection wrote 3 stage candidates, 3 evidence rows, and 3 result rows for `coding-validation-outcomes-2026-06-28`.
- Target materialization emitted `rec_aaab288a1d36c339084ab725` with 3 candidates, standardized trust, and no caveats.
- Private repo `make check`: passed.
- Public repo `make check`: passed.
- `git diff --check` in private and public repos: passed.

## Coverage Rationale

This adds a non-empty private live behavior source that projects and materializes through the existing EvalRank cache spine. It does not complete source-worker scheduling, telemetry fact-table ingestion, terminal dogfood production, hosted/staging proof, quota/billing, or Pi promotion.
