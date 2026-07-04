# 2026-06-29 Private W7 Billing Readback Route

Private Syndai worktree update only. The private API now has authenticated `GET /api/v1/evalrank/billing/readbacks` over existing EvalRank settlement readback rows.

Boundary:

- Requires the existing `evalrank:recommendations:read` customer API-key scope.
- Returns only the authenticated customer's private settlement readback rows.
- Does not add a public receipt contract, public SDK/CLI/MCP route, public schema, or request-path Stripe call.

Verification summary:

- Red private route test failed first with `404`.
- Focused private controller/readback tests passed with `15 passed`.
- Full private W7 billing lane passed with `24 passed`.
- Focused private ruff/ty checks passed.
- Private `make check` passed.
- Public `python3 -m unittest tests.test_repo_docs`, public boundary check, public `make check`, and `git diff --check` in both repos passed.

Remaining: hosted readback proof still needs deployed staging, a customer API key, real billable keyed recommendation facts, Stripe meter dispatch, and provider readback rows. Account/dashboard setup remains deferred to the final account checklist.
