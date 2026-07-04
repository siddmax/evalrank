# Private Integrity Provenance Ingestion

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains DB-free and product-neutral.
- The public repo records only status; private source identifiers, schema details, and live data stay in Syndai.

## Built Privately

- Added a private helper for stable EvalRank benchmark source identifiers, Syndai source identifiers, and SHA-256 fingerprints.
- Wired capability-search, admission-eval, capability-index, and coding-router result provenance to include benchmark source URLs, retrieved source URLs, benchmark item fingerprints, and retrieved fingerprints.
- Kept the approach exact and auditable: no embeddings, judges, or fuzzy contamination claims were added.

## Verification

- Private BDD test first failed on missing provenance fields, then passed after implementation.
- Focused private projection/contamination lane passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/unit/features/evalrank/test_contamination_checks.py tests/scripts/test_evalrank_migrations.py::test_live_evalrank_migrations_pass_boundary_guard -q`
- Target private DB proof reran the active coding-router projection, wrote 45 contamination checks, and produced this mix: 15 clean source-overlap rows, 15 clean fingerprint-overlap rows, and 15 temporal rows still `unknown`/`insufficient_metadata`.
- Stage-2 rescoring wrote 2 rows and materialization emitted active cache `rec_6e56def5a33bbad1b7530c74`.
- Cross-adapter unit coverage first failed on three non-coding adapters with `insufficient_metadata`, then passed after reusing the helper.
- Target private DB capability-index proof reran 29 live rows, wrote 87 contamination checks, and produced this mix: 29 clean source-overlap rows, 29 clean fingerprint-overlap rows, and 29 temporal rows still `unknown`/`insufficient_metadata`.

## Coverage Rationale

- This raises W3/W5 integrity coverage because exact source/fingerprint checks now carry live provenance instead of unknown metadata.
- Coverage remains below launch-grade because temporal release/cutoff metadata and semantic contamination probes are still incomplete.

## Next

- Add canonical benchmark-release and model-training-cutoff metadata.
- Broaden live item-response coverage enough for publishable multi-chain IRT/SBC.
- Add Stage-3/4 scorer rows before treating W7+ hosted surfaces as product-ready.
