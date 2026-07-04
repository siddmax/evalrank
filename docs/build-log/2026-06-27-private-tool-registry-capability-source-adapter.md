# Private Tool Registry Capability Source Adapter And Cache Lineage

Date: 2026-06-27

Scope: private Syndai EvalRank worktree only. This public log records the public-safe status update; no private source rows, customer data, hosted runtime code, secrets, or Syndai implementation files were copied into the public EvalRank repo.

## What Changed Privately

- Added a private source adapter that projects Syndai tool-registry capability metadata into the private `evalrank` input tables.
- Added a shared private projection contract so source adapters do not import each other cyclically.
- Added private migration coverage for the tool-registry metadata benchmark.
- Added source-snapshot lineage fields to the private recommendation cache and made active cache writes refuse stale source snapshots.
- Made cached recommendation ids and payload hashes canonical after ids are populated.
- Added real base-snapshot lag to cached payloads and bounded top-k telemetry ids while preserving the full ranked count.
- Made empty source projections fail closed by default unless an explicit `--allow-empty` flag is passed.
- Split private helper/test modules so the Syndai backend file-size guard stays green.

## Evidence

- Focused private source-adapter/cache-lineage lane: `82 passed`.
- Focused private adapter regression lane after result-provenance fix: `14 passed`.
- Focused private ruff and ty lanes for changed adapter/cache/materializer files: passed.
- Private EvalRank migration-boundary check: passed.
- Private live migration applied: `2026_06_27_022_evalrank_recommendation_cache_snapshot_lineage`.
- Private live tool-registry projection produced 100 candidates.
- Private live cache materialization produced `rec_b45288cb38b8bbce2cfbc836`.
- Private live SQL invariants verified 100 candidates, 100 evidence rows, 100 result rows, 64-hex EvalRank candidate ids, upstream source fingerprints preserved in entity/evidence/result provenance, and an active cache row with source snapshot lineage plus `base_snapshot_lag_ms=0`.
- Private `make check`: passed.
- Private `make eval-coding-deterministic`: `240 passed, 3 skipped`.
- Public `make check`: passed with 223 Python tests and 7 TypeScript SDK tests.
- Public and private `git diff --check`: passed.

## Product Decision

EvalRank should serve cached, lineage-checked recommendations rather than recomputing source projections or scorer work during the request. That is the best long-term UX and cost posture: users get fast deterministic recommendations with source-snapshot provenance, while expensive accuracy work runs offline and only publishes verified cache rows.

Tool-registry capability metadata remains a coverage/readiness signal, not a performance benchmark. Private result rows are marked as metadata coverage so the product can bootstrap useful evidence without overstating runtime quality.

## Public Boundary

The public EvalRank repo still owns product-neutral contracts, schemas, SDKs, CLI, MCP boundary, examples, and method notes. Private projection scripts may read Syndai-owned source tables while the feature incubates there, but derived EvalRank rows, cache rows, migrations, grants, and RLS stay in the private `evalrank` schema until EvalRank has its own deploy/release path or dedicated Supabase project.
