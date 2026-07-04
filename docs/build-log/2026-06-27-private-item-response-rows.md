# Private Item Response Rows

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank repo remains DB-free and product-neutral.
- EvalRank persistence continues to live in the private dedicated `evalrank` schema; private projection scripts may read private source tables, but derived EvalRank rows are written only to `evalrank`.

## Built Privately

- Added `evalrank.item_response_rows` as the response-matrix substrate needed before full Bayesian IRT fitting.
- Added a stdlib builder/writer and `backend/scripts/project_evalrank_item_responses.py`.
- Derived binary/fractional item observations only from `evalrank.result_rows` with `n_items = 1`.
- Rejected aggregate result rows instead of treating them as item-level observations.
- Added FK-covering indexes for the new table after the Supabase performance advisor flagged the new FK columns.
- Kept NumPyro/JAX out of this slice; the next step is fitting and validating IRT on top of the response ledger, not adding a sampler before valid response rows exist.

## Verification

- Private item-response unit tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_item_response_rows.py -q`
- Private migration/script tests passed:
  `uv run pytest --no-cov tests/scripts/test_evalrank_migrations.py::test_w3_item_response_rows_migration_defines_private_response_rows tests/scripts/test_evalrank_migrations.py::test_w3_item_response_rows_index_migration_covers_private_fks tests/scripts/test_evalrank_migrations.py::test_item_response_projection_script_reuses_builder_and_writer -q`
- Private focused EvalRank lane passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/unit/features/evalrank/test_materializer.py tests/unit/features/evalrank/test_scorer_rows.py tests/unit/features/evalrank/test_contamination_checks.py tests/unit/features/evalrank/test_calibration_rows.py tests/unit/features/evalrank/test_item_response_rows.py tests/scripts/test_evalrank_migrations.py tests/scripts/test_validate_docs_evalrank_contract.py -q`
- Target private DB proof applied `2026_06_27_010_evalrank_item_response_rows` and `2026_06_27_011_evalrank_item_response_fk_indexes`.
- Target private DB projection wrote 15 active coding-router item responses with 15 distinct source result links, 15 distinct benchmark item keys, 12 binary rows, and 3 fractional rows.
- Target private DB policy/index proof showed the expected read/write RLS policies and four FK-covering indexes for `item_response_rows`.

## Coverage Rationale

- W3 and W5 increase because there is now a real private item-response ledger behind active result rows.
- This is not full item-level Bayesian IRT/parameter recovery yet; it is the necessary response-matrix substrate for that next gate.
- W7+ hosted surfaces remain blocked on broader scorer depth.

## Next

- Fit and validate item-level Bayesian IRT/parameter recovery from `evalrank.item_response_rows`.
- Broaden contamination/integrity checks beyond temporal/missing-metadata probes.
- Add Stage-3/4 scorer rows before treating W7+ hosted surfaces as product-ready.
