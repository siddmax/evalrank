# Private Calibration Rows

Date: 2026-06-26

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank repo remains DB-free and product-neutral.
- EvalRank persistence continues to live in the private dedicated `evalrank` schema; projection scripts may read private Syndai source tables but derived EvalRank rows are written only to `evalrank`.

## Built Privately

- Added `evalrank.calibration_rows` as the long-lived posterior-row contract for Stage-2+ scoring.
- Added an empirical-Bayes beta-binomial aggregate calibration writer for current result rows.
- Wired private Stage-2 scorer rows to consume calibration posterior mean, confidence, interval, and diagnostics when present.
- Kept the future full-fit target explicit as `irt_2pl_numpyro`; this slice does not claim full item-level 2PL IRT because the current source path is aggregate result rows, not item-response matrices.

## Verification

- Private focused red/green tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_calibration_rows.py tests/scripts/test_evalrank_migrations.py::test_w3_w5_calibration_rows_migration_defines_private_posterior_rows tests/scripts/test_evalrank_migrations.py::test_calibration_script_reuses_builder_and_writer -q`
- Private scorer/script integration tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_scorer_rows.py tests/scripts/test_evalrank_migrations.py::test_stage2_scorer_script_reuses_builder_and_writer -q`
- Private focused EvalRank lane passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/unit/features/evalrank/test_materializer.py tests/unit/features/evalrank/test_scorer_rows.py tests/unit/features/evalrank/test_contamination_checks.py tests/unit/features/evalrank/test_calibration_rows.py tests/scripts/test_evalrank_migrations.py tests/scripts/test_validate_docs_evalrank_contract.py -q`
- Target private DB proof applied `2026_06_26_009_evalrank_calibration_rows`, wrote 2 calibration rows, wrote 2 calibration-aware Stage-2 scorer rows, and materialized recommendation `rec_18445e78a012c92c8ac80955`.

## Next

- Build the item-level Bayesian IRT/parameter-recovery path behind the same posterior-row contract once item-response matrices exist.
- Broaden contamination/integrity checks beyond temporal/missing-metadata probes.
- Add Stage-3/4 scorer rows before treating W7+ hosted surfaces as product-ready.
