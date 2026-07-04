# Private Stage-4 Conformal Shortlist

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains storage-free and product-neutral.
- The public repo records status only; private scorer rows and target DB proofs stay in Syndai.

## Built Privately

- Added deterministic private Stage-4 `stage4_conformal_shortlist` scorer rows using pinned `alpha=0.1`, `delta=0.05`, and `max_shortlist=3` defaults.
- Added the private Stage-4 runner `backend/scripts/score_evalrank_stage4_rows.py`.
- Reused existing `evalrank.scorer_rows` persistence and writer logic.
- Updated the private materializer to apply Stage-4 `in_shortlist` membership when Stage-4 rows exist.
- Kept Stage-3 out of ledger writes because the spec requires LLM tie-breaks to be materialize-time-only.

## Verification

- Context7 psycopg docs check confirmed the existing async connection and `dict_row` script pattern.
- Focused private tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_scorer_rows.py tests/unit/features/evalrank/test_materializer.py tests/scripts/test_evalrank_migrations.py::test_stage4_scorer_script_reuses_builder_and_writer -q`
- Target private DB proof wrote 2 Stage-4 rows for the active coding-router snapshot.
- Target private DB showed both active candidates in the shortlist: one `leader` and one `within_delta`.
- Materialization emitted active cache `rec_d98497141fcf9abb4028ed96` with `stage4_conformal_shortlist` score components.

## Coverage Rationale

- W5 and W6 move because the private cache now has a real Stage-4 membership layer behind the active recommendation payload.
- Coverage stays below launch-grade because live IRT/SBC, canonical model cutoff metadata, semantic contamination probes, and Stage-3 materialize-time tie-break guardrails are not complete.
