# Private Raw Router Ledger Projection

Date: 2026-06-26

## Summary

The private Syndai worktree now projects approved coding-router benchmark ledger rows that are not part of the active router snapshot into the private EvalRank `evalrank` schema as a separate raw source.

## Public Boundary

- Public EvalRank code was not coupled to Syndai internals.
- No private source text, target DB identifiers, customer data, traces, held-out tasks, or private benchmark payloads were copied here.
- The source writes only private `evalrank` rows in Syndai's private worktree.

## Private Verification

- Focused private tests passed: `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/scripts/test_evalrank_migrations.py -q` returned `27 passed`.
- Private target DB projection passed: `doppler run -- uv run python scripts/project_evalrank_coding_router_raw_ledger.py --snapshot-id coding-router-raw-ledger-2026-06-26 --generated-at 2026-06-26T00:00:00Z --limit 100` projected 2 candidates.
- Target DB proof showed 2 raw-ledger stage rows, 2 evidence rows, and 6 result rows while leaving the active `autonomous-swe-agent` cache unchanged.

## Still Private / Incomplete

- IRT/calibration, contamination checks, Stage-2+ scorer rows, telemetry, hosted routes, auth, billing, and UI remain private/incomplete.
