# Private W9 DB-Backed Regression Draft PR

Private Syndai work on 2026-06-28 let the local WAQC draft-PR artifact command read open private regression facts directly from `evalrank.regression_events`.

Public-safe summary:

- Private draft-PR payload generation can now use a regression id instead of hand-copied regression metadata JSON.
- DB-backed payloads still require a real evidence URL or configured evidence URL base.
- The existing operator-affiliation completeness and publication-governance gates still run before any JSON is emitted.
- No GitHub API call, branch push, remote PR, Slack alert, GTM posting, public route, public SDK/CLI/MCP behavior, billing, telemetry, or public persistence changed.

Verification:

- Private red focused tests failed first on the missing DB-backed command path.
- Private focused helper/command tests passed with `12 passed`.
- Private focused ruff and ty checks passed for the touched helper/script/tests.
- Private root `make check` passed.
- Public docs test, public boundary check, public `make check`, and public/private `git diff --check` passed.
