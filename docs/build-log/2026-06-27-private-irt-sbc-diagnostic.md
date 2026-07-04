# Private IRT SBC Diagnostic

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains DB-free and product-neutral.
- Private persistence stays isolated in the dedicated `evalrank` schema in Syndai.

## Built Privately

- Added an offline simulation-based calibration diagnostic for the private NumPyro/JAX 2PL IRT path.
- The pooled private IRT batch can opt into SBC and stamp `diagnostics.sbc` on the private fit-run JSON.
- SBC remains out of public SDKs, CLI, MCP tools, schemas, and request/materialization paths.

## Verification

- Focused private tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank tests/scripts/test_evalrank_migrations.py tests/scripts/test_evalrank_pooled_irt_rows.py tests/scripts/test_validate_docs_evalrank_contract.py -q`
- Target private DB proof:
  `doppler run -- uv run python scripts/fit_evalrank_pooled_irt_rows.py --use-case autonomous-swe-agent --source-name evalrank-pooled-item-responses --snapshot-id autonomous-swe-agent-pooled-2026-06-27 --fitted-at 2026-06-27T00:00:00Z --min-entities 3 --min-items 3 --num-warmup 500 --num-samples 500 --num-chains 2 --rng-seed 17 --sbc-repetitions 8 --sbc-num-warmup 1000 --sbc-num-samples 1000 --sbc-num-chains 2 --sbc-rng-seed 20260627 --sbc-min-rank-count 200 --sbc-target-accept-prob 0.95`
- Persisted `diagnostics.sbc` on fit `irt_b2e568cb41037afc55f1d76c` with `publishable=true`, 312 rank checks, 8/8 publishable refits, `mean_rank_fraction=0.491503`, `max_mean_rank_z=1.835769`, `edge_rank_fraction=0.00641`, and no publishability reasons.

## Boundary

- No public persistence, private source data, private scorer weights, hosted API behavior, or customer-specific evidence moved into the public repo.
