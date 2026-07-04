# Private W9 Operator Affiliations Check Command

Private Syndai work on 2026-06-28 exposed the operator-affiliations completeness check as a runnable private DB gate.

Public-safe summary:

- Added a private command that checks current Syndai-operated EvalRank candidate rows against the private affiliation registry.
- The command exits nonzero and prints missing entity ids when a registry row is missing.
- No public storage, route, SDK, CLI, MCP, or schema contract changed.

Verification:

- Private red test failed first on the missing script.
- Private focused tests passed with `3 passed`.
- Private ruff and ty checks passed for the touched script/test.
- Target private check passed: all current Syndai-operated EvalRank candidates have operator affiliations.

Current blocker:

- Sentry dogfood remains account-gated. Current private audit still reports missing `SENTRY_PROVISION_TOKEN`, missing Sentry binding, and 0 terminal `sentry_auto` outcomes. Chrome is waiting at Sentry login for manual sign-in before token creation/provisioning can continue.
