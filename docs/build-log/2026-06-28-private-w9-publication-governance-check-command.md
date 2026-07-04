# Private W9 Publication Governance Check Command

Private Syndai work on 2026-06-28 exposed the provider-free pre-publication governance tripwire as a runnable private operator/CI gate.

Public-safe summary:

- Added a private command that checks sanitized governance metadata JSON before future GTM, report, social, or draft-PR dispatchers create public side effects.
- The command rejects draft body/content fields and exits nonzero on missing disclosures, missing evidence, CVD blockers, or missing required human review.
- Optional private DB recording stores only sanitized decision metadata when explicitly requested.
- No public storage, route, SDK, CLI, MCP, schema, billing, or telemetry contract changed.

Verification:

- Private red test failed first on the missing script.
- Private focused command tests passed with `6 passed`.
- Private ruff and ty checks passed for the touched script/test.
- A real no-record CLI invocation with a temporary sanitized metadata file returned `PASS: publication governance allowed draft draft-cli-pass`.

Current blocker:

- Sentry dogfood remains account-gated. Current private audit still reports missing `SENTRY_PROVISION_TOKEN`, missing Sentry binding, and 0 terminal `sentry_auto` outcomes. Chrome is waiting at Sentry login for manual sign-in before token creation/provisioning can continue.
