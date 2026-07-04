# Private Pooled IRT Fit Scope

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank repo remains DB-free and product-neutral.
- Private persistence stays isolated in the dedicated `evalrank` schema in Syndai.

## Built Privately

- Fixed private NumPyro multi-chain diagnostics extraction for array-valued R-hat and effective sample size fields.
- Added settings-aware IRT fit IDs.
- Added a pooled IRT batch script that fits over active item-response rows across source snapshots while preserving source lineage.
- The pooled script writes a pooled `evalrank.input_snapshots` fit scope and persists IRT fit/item-parameter plus calibration rows.

## Verification

- Focused private tests passed:
  `uv run pytest --no-cov tests/scripts/test_evalrank_pooled_irt_rows.py tests/scripts/test_evalrank_migrations.py::test_pooled_irt_fit_script_reuses_fit_scope_and_writers tests/unit/features/evalrank/test_irt_rows.py::test_irt_fit_records_multichain_diagnostics -q`
- Target private DB pooled IRT proof:
  `doppler run -- uv run python scripts/fit_evalrank_pooled_irt_rows.py --use-case autonomous-swe-agent --source-name evalrank-pooled-item-responses --snapshot-id autonomous-swe-agent-pooled-2026-06-27 --fitted-at 2026-06-27T00:00:00Z --min-entities 3 --min-items 3 --num-warmup 500 --num-samples 500 --num-chains 2 --rng-seed 17`
- Persisted fit `irt_b2e568cb41037afc55f1d76c` with 3 entities, 18 binary items, 21 response rows, 3 calibration rows, and 18 item-parameter rows.
- Publishability is true: `max_r_hat=1.009673`, `min_effective_sample_size=418.515228`, `divergence_count=0`, with no publishability reasons. SBC was added in the follow-up private build log `2026-06-27-private-irt-sbc-diagnostic.md`.

## Boundary

- No public schemas, SDKs, CLI, MCP tools, or DB runtime were added.
- The public repo records the status only; source adapters, IRT persistence, and batch execution remain private.
