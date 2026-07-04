# Private W8 Recommendation Load SLO Smoke

The private Syndai EvalRank worktree added an account-free local/staging latency smoke command for cached recommendation reads.

Public-safe summary:

- Sends a bounded concurrent batch to the existing cached `POST /v1/recommendations` route.
- Verifies all responses share one cached recommendation id and one top-ranked id.
- Reports p50, p95, and max latency.
- Exits nonzero when configured p50 or p95 SLOs are missed.
- Adds no public route, no public storage, no provider integration, and no new dependency.

Verification in the private worktree:

- Red test first failed on missing command module.
- Focused unit lane passed with `3 passed`.
- Focused `ruff` and `ty` checks passed.
- CLI help rendered successfully.

This is reusable harness work only. The hosted/staging latency gate remains open until the command is run against deployed infrastructure.
