# Private Coding Router Evidence Projection

Date: 2026-06-26

Scope: public-safe status update only.

## Built

- In the separate private Syndai worktree, added a private source adapter that projects the active approved coding-router evidence snapshot into the private `evalrank` input snapshot path.
- Added private benchmark catalog rows for coding conformance, golden eval, cross-validation, and tail-risk evidence.
- Reused the same private input snapshot writer and W6 materializer path already proven for capability-search and capability-index inputs.
- Target private DB proof materialized an `autonomous-swe-agent` cached recommendation from 2 projected agent candidates and 15 benchmark result rows.

## Boundary

- No private Syndai imports, raw evidence rows, customer data, held-out evals, traces, secrets, or hosted runtime code were copied into this public repo.
- Public EvalRank remains storage-free: contracts, schemas, SDK/CLI/MCP boundaries, examples, method notes, and status reporting only.
- The private DB migration, source adapter, target DB projection, and cache write stay in Syndai until EvalRank owns a deploy/release path.

## Verification

- Private focused tests passed: `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/scripts/test_evalrank_migrations.py -q` returned `24 passed`.
- Private type check passed: `uv run --project backend ty check --config-file ty.toml`.
- Private antipattern and EvalRank migration-boundary checks passed.
- Target private DB migration applied `2026_06_26_006_evalrank_coding_router_benchmarks`.
- Target private DB projection emitted 2 candidates, and the W6 materializer emitted `rec_1633fe9da4154ff0901c0358`.
