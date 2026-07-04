# Private Contamination Integrity Expansion

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains DB-free and product-neutral.
- EvalRank persistence continues to live in the private dedicated `evalrank` schema.

## Built Privately

- Expanded private contamination checks from one temporal row per result to three independent rows per result: temporal cliff, benchmark source overlap, and benchmark fingerprint overlap.
- Kept missing metadata as `unknown`/`insufficient_metadata` instead of treating absent provenance as clean.
- Added exact URL and fingerprint normalization for deterministic overlap checks.
- Added private FK-covering indexes for contamination-check lineage after the Supabase performance advisor flagged the new table's FK columns.

## Verification

- Private focused contamination lane passed:
  `uv run pytest --no-cov tests/unit/features/evalrank/test_contamination_checks.py tests/scripts/test_evalrank_migrations.py::test_w3_contamination_integrity_migration_extends_check_taxonomy tests/scripts/test_evalrank_migrations.py::test_w3_contamination_integrity_indexes_cover_private_fks -q`
- Target private DB proof applied `2026_06_27_013_evalrank_contamination_integrity_checks` and `2026_06_27_014_evalrank_contamination_check_fk_indexes`.
- Target private DB scan wrote 45 checks for the active coding-router agent snapshot: 15 temporal, 15 source-overlap, and 15 fingerprint-overlap checks.
- Current live metadata has no source URL/fingerprint coverage, so all 45 checks stayed `unknown`/`insufficient_metadata` and the active cache retained `potential_contamination` caveats.
- Target private DB index proof showed covering indexes for the contamination-check result FK and input-snapshot FK.
- Public `make check` passed after the status/build-log update: boundary scanner, 223 Python tests, TypeScript syntax check, and 7 TypeScript runtime tests.

## Coverage Rationale

- W3, W5, Spec 10, and Spec 22 move because the private scorer path now carries exact source/fingerprint integrity rows, not just temporal metadata.
- Coverage stays below launch-grade because live provenance still needs source URLs/fingerprints and stronger semantic contamination probes.

## Next

- Populate live source URL and fingerprint provenance from private adapters.
- Broaden live response coverage enough for publishable multi-chain IRT/SBC.
- Add Stage-3/4 scorer rows before treating W7+ hosted surfaces as product-ready.
