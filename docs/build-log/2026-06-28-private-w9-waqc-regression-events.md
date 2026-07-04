# Private W9 WAQC Regression Events

Private Syndai work on 2026-06-28 added the provider-free W9 regression substrate for EvalRank.

Public-safe summary:

- Added a private `evalrank.regression_events` table for human-gated regression facts.
- Added a private WAQC detector that compares the latest completed external WAQC week with the prior completed week.
- Drops are recorded as deterministic `waqc_drop` facts with `draft_pr_required=true`.
- The weekly WAQC worker now refreshes enough history before running the detector.
- Missing windows, zero baselines, and non-drops fail closed and do not fabricate regression evidence.
- GitHub draft-PR dispatch, Slack alerts, GTM posting, and other provider side effects remain unimplemented and account-gated.

Verification:

- Private focused regression tests passed.
- Private ruff and ty checks passed for touched files.
- Private EvalRank migration-boundary and migration-validation checks passed.
- Target private DB migration applied.
- Target readback verified the new table, policies, indexes, and a no-fabrication detector run over real zero-count WAQC rows.

Public repo impact:

- No public API, SDK, CLI, MCP, schema, or storage contract changed.
- This file and `docs/STATUS.md` are documentation-only syncs.
