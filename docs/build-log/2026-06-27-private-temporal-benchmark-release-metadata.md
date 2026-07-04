# Private Temporal Benchmark Release Metadata

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains storage-free and product-neutral.
- The public repo records status only; private database rows and source details stay in Syndai.

## Built Privately

- Added a private migration that backfills `benchmark_released_at` metadata on existing `evalrank.benchmark_catalog` rows.
- Preserved existing benchmark metadata and introduced no new table, function, grant, or RLS policy.
- Added a regression for the intended integrity UX: benchmark release known but model training cutoff missing remains `unknown`, not clean.

## Verification

- Context7 Supabase docs check confirmed that the existing RLS/grant boundary remains the relevant control for an update to an existing RLS-enabled table.
- Focused private tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_contamination_checks.py tests/scripts/test_evalrank_migrations.py::test_w3_temporal_metadata_migration_seeds_benchmark_release_dates tests/scripts/test_evalrank_migrations.py::test_live_evalrank_migrations_pass_boundary_guard -q`
- Target private DB proof applied `2026_06_27_015_evalrank_benchmark_release_metadata`.
- Target private DB contamination rerun wrote 45 active coding-router checks with this mix: 15 clean source-overlap rows, 15 clean fingerprint-overlap rows, and 15 temporal rows still `unknown`/`insufficient_metadata` with `benchmark_released_at="2026-06-26"` and `missing=["training_cutoff"]`.
- Stage-2 rescoring wrote 2 rows, and materialization emitted active cache `rec_6e56def5a33bbad1b7530c74`.

## Research Note

The implementation keeps temporal contamination conservative. Recent contamination and live-benchmark work supports treating date metadata as a useful signal, not a sufficient clean bill of health. See [LiveCodeBench](https://arxiv.org/abs/2403.07974), [LLM Data Contamination Has Already Happened](https://openreview.net/forum?id=bhR00j6Mku), and [Awesome Data Contamination](https://github.com/lyy1994/awesome-data-contamination).

## Coverage Rationale

- Spec 10 and Spec 22 move because the private benchmark catalog now carries canonical benchmark-release metadata for existing seeded rows.
- Coverage stays below launch-grade because model-training-cutoff metadata and stronger semantic contamination probes are still incomplete.
