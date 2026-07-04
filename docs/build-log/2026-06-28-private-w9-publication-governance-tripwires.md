# Private W9 Publication Governance Tripwires

Private Syndai work on 2026-06-28 added a provider-free pre-publication gate for EvalRank governance/legal risk.

Public-safe summary:

- Added a private audit table for publication-governance decisions.
- Added a deterministic checker for future GTM/report/social/draft-PR dispatchers.
- The checker blocks missing operator-COI disclosure, missing material-connection disclosure, unsupported negative labels, negative labels without dated evidence, security labels without CVD clearance, and contested social drafts without human review.
- The audit writer stores sanitized gate metadata only and does not store draft body text.
- This does not add public routes, public posting agents, legal advice, counsel sign-off, or provider dispatch.

Verification:

- Private focused governance tests passed.
- Private ruff and ty checks passed for touched files.
- Private EvalRank migration-boundary and migration-validation checks passed.
- Target private DB migration applied.
- Target readback verified the new table, policies, indexes, and a rollback-only blocked social-post audit proof that left no synthetic rows.

Public repo impact:

- No public API, SDK, CLI, MCP, schema, or storage contract changed.
- This file and `docs/STATUS.md` are documentation-only syncs.
