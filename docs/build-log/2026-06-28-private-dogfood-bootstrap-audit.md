# Private Dogfood Bootstrap Audit

## What Changed

- The private Syndai worktree added a read-only Sentry dogfood bootstrap audit to the existing provisioning CLI.
- The audit names real operator blockers before EvalRank can project terminal `sentry_auto` dogfood evidence.
- Missing dogfood budgets are reported as warnings because the current dispatcher treats no budget row as unbounded; this is a cost-control gap, not the current evidence blocker.
- The audit points operators back to the existing Sentry provision command instead of adding a second provisioning path.

## Boundary

- This public repo did not gain private Sentry, database, dogfood, or hosted-product code.
- Dogfood source rows remain private-side work and should be projected into the dedicated private `evalrank` schema only after real terminal outcomes exist.
- Syndai-owned auth/control-plane and dogfood bootstrap objects remain in Syndai-owned schemas during incubation.

## Verification

- Focused private audit unit lane: `7 passed`.
- Focused private ruff and ty checks passed.
- Target read-only audit found repository `f568bbbb-fcb4-46c3-8fc2-04e530eeb805`, no Sentry binding, no triggers, 0 terminal `sentry_auto` outcomes, missing `SENTRY_PROVISION_TOKEN`, and a missing-budget warning.
- Private `make check` passed.
- Public `make check` passed with 223 Python tests and 7 TypeScript SDK tests.
- `git diff --check` passed in both repos.

## Coverage Rationale

This improves W5 operator UX and accuracy without over-hardening. It does not claim live dogfood evidence; the next gate is real Sentry provisioning plus terminal dogfood outcomes from the existing dispatcher path.
