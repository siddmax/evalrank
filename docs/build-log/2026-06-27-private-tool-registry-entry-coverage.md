# Private Tool Registry Entry Coverage Projection

Date: 2026-06-27

Scope: private Syndai EvalRank worktree only. This public log records the public-safe status update; no private source rows, customer data, hosted runtime code, secrets, or Syndai implementation files were copied into the public EvalRank repo.

## What Changed Privately

- Added a private source adapter that projects raw Syndai tool-registry entries into the private `evalrank` schema.
- Sampled source families in a balanced way across API, CLI, MCP, and skill registry rows instead of letting one large registry family dominate the snapshot.
- Labeled the rows as `metadata_tracking_not_performance` and kept them `tracking-only` unless separate behavior evidence exists.
- Added a cached recommendation caveat so users do not mistake registry metadata completeness for measured capability.

## Evidence

- Red adapter regressions failed before implementation because the registry-entry projector did not exist.
- Red projection-script and migration regressions failed before implementation because the script and benchmark-catalog migration did not exist.
- Red materializer regression failed before implementation because metadata-tracking rows did not surface a caveat.
- Focused private materializer/adapter/script/migration lane: `63 passed`.
- Focused private ruff and ty checks for touched files: passed.
- Private EvalRank migration-boundary guard: passed.
- Private target migration applied and verified benchmark catalog row `syndai-tool-registry-entries / metadata-tracking-v1`.
- Private target projection wrote 200 candidates for snapshot `tool-registry-entries-2026-06-27`, with 50 rows each for API, CLI, MCP, and skill source families.
- Private SQL invariants verified 200 entities, 200 evidence rows, 200 result rows, active input snapshot, and 200 result rows with `metadata_tracking_not_performance` provenance.
- Private materialization produced active cache `rec_ada04f92b9e9a89a6758dd75` with 200 candidates, source-snapshot lineage, top row `trust_tier=tracking-only`, and caveat `metadata_tracking_not_performance`.

## Product Decision

The best long-term UX is to show broad registry-entry coverage as tracking metadata, not capability. This gives users better discovery coverage while preserving accuracy: metadata-rich entries are visible, but EvalRank does not claim they are behaviorally better until measured evals exist. Offline projection plus cached reads keeps latency and cost bounded.
