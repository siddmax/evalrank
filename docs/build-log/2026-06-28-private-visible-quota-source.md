# 2026-06-28 Private Visible Quota Source

## What Changed

- Private Syndai added `evalrank.recommendation_quota_limits` in the dedicated private EvalRank schema.
- The private usage route now returns configured `quota.enforced`, `quota.limit`, and `quota.remaining` values from that source.
- Requests are not denied in this slice.

## Boundary

- Quota persistence, grants, RLS, and derived usage behavior stay in the private `evalrank` schema.
- Syndai customer API-key identity stays in Syndai's shared control plane.
- No public OpenAPI/SDK/CLI/MCP contract changed.

## Verification

- Private focused helper/migration lane: `5 passed`.
- Private focused ruff and ty checks: passed.
- Private EvalRank migration-boundary check: passed.
- Private repo `make check`: passed.
- Public repo `make check`: passed with 223 Python tests and 7 TypeScript SDK tests.
- `git diff --check`: passed in both repos.
- Explicit touched-file trailing-whitespace scans: clean.

## Coverage Rationale

This is the W7 quota source-of-truth step before enforcement, billing settlement, receipts, webhooks, and hosted/staging proof.
