# Private Stage-2 Scorer Rows

Date: 2026-06-26

## Summary

The private Syndai worktree added a Stage-2 scorer-row layer behind the EvalRank cache spine. This remains private because it writes the private `evalrank` schema and consumes private source snapshots. No private source text, held-out benchmark material, secrets, or Syndai imports moved into this public repo.

## Public-Safe Proof

- Private migration added `evalrank.scorer_rows` with source/snapshot lineage, RLS, grants, and Stage-2/3/4 scorer-stage vocabulary.
- Private scorer builder and writer emit deterministic fixed-parameter `stage2_evidence_rerank` rows from Stage-1 candidates, evidence, and result rows.
- Private materializer now consumes scorer rows when present and falls back to Stage-1/result aggregation when absent.
- Target private DB proof wrote 2 Stage-2 scorer rows for the active coding-router `autonomous-swe-agent` snapshot and rematerialized active cache `rec_57d1d48ec7fc02dcfe41fbb6` with a `stage2_calibrated` score component.

## Boundary

- Public EvalRank remains storage-free.
- Private DB migrations remain in Syndai while EvalRank incubates on the shared private Supabase/Postgres project.
- Full Bayesian IRT/calibration, broader contamination checks, Stage-3/4 scorer rows, telemetry, and hosted surfaces remain private/incomplete.
