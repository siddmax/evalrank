# Private W9 Affiliation-Gated Draft PR

Private Syndai work on 2026-06-28 tightened the WAQC regression draft-PR artifact path so it fails closed on the private operator-affiliation completeness gate.

Public-safe summary:

- Private draft-PR payload generation now requires the operator-affiliation registry check to pass before emitting JSON for a future provider dispatcher.
- Generated draft bodies include private affiliation/COI gate text, and the existing publication-governance tripwire treats operator-COI disclosure as required.
- The command requires `DATABASE_URL` or `--database-url` so the gate is DB-backed instead of trusting metadata.
- No GitHub API call, branch push, remote PR, Slack alert, GTM posting, public route, public SDK/CLI/MCP behavior, billing, telemetry, or public persistence changed.

Verification:

- Private red focused tests failed first because the builder and command lacked the affiliation gate.
- Private focused helper/command tests passed with `9 passed`.
- Private focused ruff and ty checks passed for the touched helper/script/tests.
- Private root `make check` passed.
- Public docs test, public boundary check, public `make check`, and public/private `git diff --check` passed.
