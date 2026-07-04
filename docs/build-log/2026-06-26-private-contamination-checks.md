# Private Contamination Checks

Date: 2026-06-26

## Summary

The private Syndai worktree added first-pass contamination-check rows behind the EvalRank cache spine. This remains private because it writes the private `evalrank` schema and consumes private source snapshots. No private source text, held-out benchmark material, secrets, live traces, or Syndai imports moved into this public repo.

## Public-Safe Proof

- Private migration added `evalrank.contamination_checks` with source/snapshot lineage, RLS, grants, and temporal-cliff/missing-metadata check vocabulary.
- Private scanner emits deterministic contamination-check rows from private result rows, benchmark metadata, entity metadata, and provenance.
- Missing benchmark release or model cutoff metadata is recorded as `unknown`/`insufficient_metadata`, not treated as clean.
- Private Stage-2 scorer rows now merge non-clean contamination-check flags with source-declared flags.
- Target private DB proof wrote 15 contamination-check rows for the active coding-router `autonomous-swe-agent` snapshot, rescored 2 Stage-2 rows with `insufficient_metadata`, and rematerialized the active cache with `potential_contamination` caveats.

## Research Rationale

2026 contamination literature supports the product call used here: temporal cutoff checks are useful as a cheap first-pass signal, but they are not reliable enough to clear a benchmark by themselves. Recent work shows temporal signals are sensitive to benchmark construction and that reasoning-model training can hide common contamination signals. EvalRank should therefore surface missing metadata conservatively now, while the next gate adds stronger contamination/integrity probes before launch-grade scoring.

Sources reviewed:

- [Test of Time: Rethinking Temporal Signal of Benchmark Contamination](https://arxiv.org/html/2509.00072v4)
- [On The Fragility of Benchmark Contamination Detection in Reasoning Models](https://openreview.net/forum?id=bhR00j6Mku)
- [Awesome Data Contamination](https://github.com/lyy1994/awesome-data-contamination)

## Boundary

- Public EvalRank remains storage-free.
- Private DB migrations remain in Syndai while EvalRank incubates on the shared private Supabase/Postgres project.
- The implemented check is not the final contamination system. Robust probes beyond temporal metadata, Bayesian IRT/calibration, Stage-3/4 scorer rows, telemetry, and hosted surfaces remain private/incomplete.
