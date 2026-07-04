# Private Raw-Ledger Item Response Coverage

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank repo remains DB-free and product-neutral.
- Private persistence stays isolated in the dedicated `evalrank` schema in Syndai.

## Built Privately

- Reused the existing private item-response projector for the raw coding-router ledger source.
- Projected 6 raw-ledger `n_items = 1` result rows into `evalrank.item_response_rows`.
- Re-ran the private IRT gate for the raw-ledger source. It correctly skipped because the live matrix still has only 2 entities.

## Verification

- Private focused item-response/script check passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_item_response_rows.py tests/scripts/test_evalrank_migrations.py::test_item_response_projection_script_reuses_builder_and_writer -q`
- Target private DB migrations were already current.
- Target private DB raw-ledger projection wrote 6 rows:
  `doppler run -- uv run python scripts/project_evalrank_item_responses.py --use-case autonomous-swe-agent --source-name syndai-coding-router-raw-ledger --snapshot-id coding-router-raw-ledger-2026-06-26 --observed-at 2026-06-27T00:00:00Z`
- Target private DB raw-ledger IRT gate skipped with `got 2 entities and 6 items`:
  `doppler run -- uv run python scripts/fit_evalrank_irt_rows.py --use-case autonomous-swe-agent --source-name syndai-coding-router-raw-ledger --snapshot-id coding-router-raw-ledger-2026-06-26 --fitted-at 2026-06-27T00:00:00Z --min-entities 3 --min-items 3`
- Target private DB response totals are now 21 item-response rows: 18 binary and 3 fractional.

## Boundary

- No public schemas, SDKs, CLI, MCP tools, or DB runtime were added.
- The public repo records the status only; source adapters and persistence remain private.
