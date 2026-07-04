# Private W9 GitHub Draft PR Dispatch

Private Syndai work on 2026-06-28 added an account-gated GitHub draft-PR dispatch wrapper for WAQC regression follow-up.

Public-safe summary:

- The existing private draft-PR command now keeps dry-run JSON output as the default.
- Explicit dispatch mode reuses the existing private GitHub repository provider, then records the returned PR URL on the private regression event row.
- Tokens are read from an environment variable, not CLI literals or repo files.
- No GitHub account, token, branch, commit, pull request, Slack alert, GTM posting, public route, public SDK/CLI/MCP behavior, billing, telemetry, or public persistence changed.

Verification:

- Private red focused tests failed first on the missing dispatch helper and CLI flag.
- Private focused helper/command tests passed with `20 passed`.
- Private focused ruff and ty checks passed for the touched helper/script/tests.
- Public docs and boundary checks passed.
- Public `make check` passed with `223` Python tests and `7` SDK tests.
- Private root `make check` passed.
- Public and private `git diff --check` passed.
