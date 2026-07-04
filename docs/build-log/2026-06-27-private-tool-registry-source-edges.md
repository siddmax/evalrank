# Private Tool Registry Source Edge Projection

Date: 2026-06-27

Scope: private Syndai EvalRank worktree only. This public log records the public-safe status update; no private source rows, customer data, hosted runtime code, secrets, or Syndai implementation files were copied into the public EvalRank repo.

## What Changed Privately

- Preserved per-upstream tool-registry source edges when projecting private Syndai tool-registry capabilities into the private `evalrank` schema.
- Derived source counts from the actual source-edge array instead of trusting a separate count field.
- Kept the existing private projection writer, materializer, and cache-backed recommendation read path.

## Evidence

- Red adapter regression failed before implementation with stale `source_count` behavior.
- Red projection-script regression failed before implementation because the SQL did not aggregate source edges.
- Focused private adapter/script/migration lane: `45 passed`.
- Focused private ruff and ty checks for touched adapter/script/test files: passed.
- Private target projection wrote 100 candidates for snapshot `tool-registry-capabilities-source-edges-2026-06-27`.
- Private SQL invariants verified 100 entities, 100 result rows, active input snapshot, source-edge arrays on entities/results, source-edge count range `4..2375`, and retrieved-source-url count range `5..2376`.
- Private materialization first refused an intentionally stale cache write, then accepted the fresh source-edge snapshot and produced active cache `rec_02a413e747daad5a1a99ff53`.

## Product Decision

The best long-term UX is still cached reads over offline evidence projection. Source-edge detail improves auditability and source-adapter breadth, but it stays out of the public request path so users get fast, stable recommendations without live projection cost or latency.
