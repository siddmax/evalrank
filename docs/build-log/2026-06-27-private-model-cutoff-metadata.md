# Private Model Cutoff Metadata

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank repo remains DB-free and product-neutral.
- Private persistence stays isolated in the dedicated `evalrank` schema in Syndai.

## Built Privately

- Added a private model metadata helper for current coding-router agents.
- Wired active and raw-ledger coding-router projections to write cutoff metadata into `evalrank.entities.metadata`.
- Added a private migration that backfills current target coding entities.
- Extended temporal contamination details to include cutoff source kind and source URL.

## Verification

- Focused private red/green tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py::test_coding_router_projection_populates_model_cutoff_metadata tests/unit/features/evalrank/test_capability_inputs.py::test_projects_raw_coding_router_ledger_rows_as_separate_source tests/unit/features/evalrank/test_contamination_checks.py::test_temporal_cliff_carries_training_cutoff_source_metadata tests/scripts/test_evalrank_migrations.py::test_w3_model_cutoff_metadata_migration_seeds_current_coding_entities -q`
- Target private DB applied `2026_06_27_017_evalrank_model_cutoff_metadata`.
- Target private DB now has cutoff metadata for current Claude, Qwen, and GPT-5-Codex coding entities.
- Target contamination checks are no longer unknown for temporal metadata:
  - Active coding-router evidence: 15 high-severity `temporal_cliff` rows plus 30 clean exact-overlap rows.
  - Raw coding-router ledger: 6 high-severity `temporal_cliff` rows plus 12 clean exact-overlap rows.
- Active cache remained `rec_d98497141fcf9abb4028ed96` with `potential_contamination` caveats grounded in temporal flags.

## Boundary

- No public schemas, SDKs, CLI, MCP tools, or DB runtime were added.
- The public repo records the status only; source adapters and persistence remain private.
