# Private Stage-3 Ledger Boundary

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains storage-free and product-neutral.
- The public repo records status only; private DB constraint changes stay in Syndai.

## Built Privately

- Added a private migration that removes `stage3_llm_tiebreak` from persisted `evalrank.scorer_rows` values.
- Updated the private materializer to reject persisted Stage-3 scorer rows.
- Kept Stage-2 and Stage-4 persisted scorer rows intact.

## Verification

- Focused private tests passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_materializer.py::test_materializer_rejects_persisted_stage3_scorer_rows tests/scripts/test_evalrank_migrations.py::test_w5_stage3_no_ledger_guard_migration_tightens_scorer_stage_constraint tests/scripts/test_evalrank_migrations.py::test_live_evalrank_migrations_pass_boundary_guard -q`
- Target private DB preflight showed `stage3_scorer_rows=0`.
- Target private DB applied `2026_06_27_016_evalrank_stage3_no_ledger_guard`.
- Live `scorer_rows_stage_check` now admits only `stage2_evidence_rerank` and `stage4_conformal_shortlist`.

## Coverage Rationale

- This closes a W5/W6 boundary bug: Stage-3 LLM tie-break is materialize-time-only and never a scorer-ledger write.
- Coverage stays below launch-grade because the actual Stage-3 materialize-time tie-break path still needs sanitized text and judge guardrails before implementation.
