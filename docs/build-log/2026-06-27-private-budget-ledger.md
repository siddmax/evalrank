# Private Budget Ledger

Date: 2026-06-27

Private Syndai work added the first EvalRank hard budget reservation gate for async expensive scoring work. The implementation lives in the private `evalrank` schema and is intentionally not a public-core runtime feature.

What changed privately:

- Added `evalrank.budget_ledger` with scoped period caps, reserved/spent counters, RLS, and `evalrank_cron` write access.
- Added a small reservation helper that uses one conditional `UPDATE ... RETURNING` to prevent read-then-act overspend under concurrent dispatchers.
- The helper returns `budget.reserved` on success and `budget.ceiling_reached` when the cap would be exceeded or no configured budget row exists.

Validation:

- Red/green unit and migration-contract tests.
- Focused private EvalRank lane passed with `50 passed`.
- Focused ruff, ty, and EvalRank migration-boundary checks passed.
- Target DB proof applied migration `2026_06_27_024_evalrank_budget_ledger`, verified `evalrank.budget_ledger`, verified `evalrank_cron` update access, reserved `0.250000` against a scoped proof row, and returned `budget.ceiling_reached` for a later over-cap reservation while keeping counters bounded.

Decision:

The budget gate belongs before queue enqueue in async eval/synthesis/model-swap/GTM workers. It is not on the live `recommend()` request path, which should keep serving cached rankings quickly.
