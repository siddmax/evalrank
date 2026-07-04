# Private Semantic Contamination Probe

Date: 2026-06-27

## Scope

- Private Syndai worktree: `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`
- Public EvalRank remains DB-free and product-neutral.
- Private persistence stays isolated in the dedicated `evalrank` schema in Syndai.

## Built Privately

- Added a deterministic `benchmark_semantic_overlap` check to the private contamination-check layer.
- The first semantic layer uses normalized token-Jaccard over benchmark/retrieved text metadata and emits `unknown` when sanitized text is absent.
- Added private migration `2026_06_27_018_evalrank_semantic_contamination_check`.

## Verification

- Target private DB proof applied the migration, rebuilt contamination checks, reran Stage-2 and Stage-4 scoring, and rematerialized active cache `rec_d98497141fcf9abb4028ed96`.
- Active evidence now has 60 contamination rows: 15 clean fingerprint, 15 clean source, 15 high `temporal_cliff`, and 15 medium unknown semantic rows.
- Raw ledger now has 24 contamination rows: 6 clean fingerprint, 6 clean source, 6 high `temporal_cliff`, and 6 medium unknown semantic rows.

## Boundary

- No public schemas, SDKs, CLI, MCP tools, DB runtime, benchmark text, retrieved text, or private evidence payloads were added to the public repo.
