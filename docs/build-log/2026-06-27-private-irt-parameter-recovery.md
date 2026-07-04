# Private IRT Parameter Recovery

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank repo remains DB-free and product-neutral.
- EvalRank persistence continues to live in the private dedicated `evalrank` schema; private projection scripts may read private source tables, but derived EvalRank rows are written only to `evalrank`.

## Built Privately

- Added a private NumPyro/JAX Bayesian 2PL fit path over binary `evalrank.item_response_rows`.
- Added `evalrank.irt_fit_runs` and `evalrank.irt_item_parameter_rows` with RLS, grants, input-snapshot lineage, benchmark FKs, and covering indexes.
- Split the private IRT implementation into fit/model code and a focused SQL persistence module.
- Persisted successful IRT entity posteriors as `irt_2pl_numpyro` calibration rows, while keeping the materializer hot path deterministic.
- Excluded fractional item-response rows from the Bernoulli 2PL likelihood with explicit diagnostics.
- Preserved `entity_kind` through IRT calibration rows and caught only typed sparse-matrix refusals in the live script.

## Verification

- Private IRT unit tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_irt_rows.py -q`
- Private dependency/migration/script checks passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_irt_rows.py tests/scripts/test_evalrank_migrations.py::test_w3_irt_numpyro_dependency_is_declared tests/scripts/test_evalrank_migrations.py::test_w3_irt_fit_migration_defines_private_fit_rows tests/scripts/test_evalrank_migrations.py::test_irt_fit_script_reuses_builder_and_writers -q`
- Private focused EvalRank lane passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/unit/features/evalrank/test_materializer.py tests/unit/features/evalrank/test_scorer_rows.py tests/unit/features/evalrank/test_contamination_checks.py tests/unit/features/evalrank/test_calibration_rows.py tests/unit/features/evalrank/test_item_response_rows.py tests/unit/features/evalrank/test_irt_rows.py tests/scripts/test_evalrank_migrations.py tests/scripts/test_validate_docs_evalrank_contract.py -q`
- Target private DB proof applied `2026_06_27_012_evalrank_irt_fit_rows`.
- Target private DB fit script refused the active coding-router snapshot correctly: the matrix had 2 entities and 12 binary items, below the configured 3-entity/3-item minimum, so it wrote no fit rows.
- Target private DB policy/index proof showed the expected read/write RLS policies and fit/item-parameter indexes for the new IRT tables.

## Coverage Rationale

- W3 and methodology hardening increase because a real private item-level Bayesian IRT batch path now exists with synthetic parameter-recovery evidence.
- Coverage stays below runtime/publishable levels because the active live source is too sparse for a valid IRT publication gate.
- W7+ hosted surfaces remain blocked on broader scorer depth.

## Next

- Broaden live item-response coverage enough for a publishable multi-chain IRT/SBC gate.
- Add robust contamination/integrity checks beyond temporal/missing-metadata probes.
- Add Stage-3/4 scorer rows before treating W7+ hosted surfaces as product-ready.
