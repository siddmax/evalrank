# 2026-06-29 Private W7 Stripe EvalRank Meter Setup Profile

Private Syndai worktree update only. The existing Stripe meter setup helper now has an explicit EvalRank recommendation profile.

The profile can create or reuse the private hosted billing resources needed for future live settlement proof:

- Billing Meter event name: `evalrank_recommendation`
- Product: `EvalRank Recommendations - Metered`
- Monthly metered price attached to the meter

The existing no-arg Syndai outcome setup remains the default. EvalRank setup requires an explicit `--unit-amount-cents`, so live pricing stays an operator/finance decision rather than a hidden default.

Public boundary: no public route, SDK, CLI, MCP, schema, receipt contract, or public billing surface changed here.

Verification summary:

- Red test run failed first because the setup script did not accept args or profiles.
- Focused private setup tests passed with `3 passed`.
- Focused private ruff and ty checks passed.

Remaining: live Stripe proof still requires dashboard/API access, a chosen cents-per-recommendation price, `STRIPE_SECRET_KEY` in Doppler, real keyed external recommendation facts, and settlement/readback verification after dispatch. No browser/account setup or Stripe network call was performed.
