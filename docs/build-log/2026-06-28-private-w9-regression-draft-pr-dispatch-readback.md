# Private W9 Regression Draft PR Dispatch Readback

Private Syndai work on 2026-06-28 added a local dispatch-readback marker for WAQC regression draft-PR follow-up.

Public-safe summary:

- Private operators/future provider dispatchers can now record a created draft PR URL back onto the private regression event row.
- The command stores only sanitized readback metadata and validates the URL as HTTP(S).
- No GitHub API call, branch push, remote PR, Slack alert, GTM posting, public route, public SDK/CLI/MCP behavior, billing, telemetry, or public persistence changed.

Verification:

- Private red focused tests failed first on the missing dispatch-readback mode.
- Private focused helper/command tests passed with `15 passed`.
- Private focused ruff and ty checks passed for the touched helper/script/tests.
- Public docs and boundary checks passed.
- Public `make check` passed with `223` Python tests and `7` SDK tests.
- Private root `make check` passed.
- Public and private `git diff --check` passed.
