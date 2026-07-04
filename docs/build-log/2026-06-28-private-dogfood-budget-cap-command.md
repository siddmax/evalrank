# Private Dogfood Budget Cap Command

## What Changed

- The private Syndai worktree added `set-budget` to the existing Sentry dogfood provisioner.
- The command upserts the existing `syndai.coding_dogfood_budgets` row for a repository.
- The private target repository `siddmax/Syndai` now has `monthly_usd_cap=50.00`.
- The dogfood bootstrap audit now prints the cap value when present.

## Boundary

- This public repo did not gain private dogfood, Sentry, database, billing, or hosted runtime code.
- The budget cap is private Syndai dispatcher config, not EvalRank evidence.
- EvalRank dogfood evidence remains blocked until real terminal `sentry_auto` outcomes exist and are projected into the private `evalrank` schema.

## Verification

- Focused private provisioner lane: `10 passed`.
- Focused private ruff and ty checks passed.
- Target dry-run and target upsert succeeded for repository `f568bbbb-fcb4-46c3-8fc2-04e530eeb805`.
- Target audit now reports `budget: monthly_usd_cap=50.00`; remaining blockers are missing token, missing Sentry binding, and 0 terminal outcomes.
- Private `make check` passed.
- Public `make check` passed with 223 Python tests and 7 TypeScript SDK tests.
- `git diff --check` passed in both repos.

## Coverage Rationale

This finishes the cheap cost-control prerequisite for live dogfood dispatch. It does not create fake dogfood evidence or bypass Sentry provisioning.
