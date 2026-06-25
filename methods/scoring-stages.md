# Public Scoring Stages

This note names the public EvalRank scoring pipeline and mirrors the storage-free `ScoringStageCatalog` contract without exposing private formulas, held-out evals, production telemetry, or hosted-product behavior.

## Stages

1. `request-normalization`: convert a public use case into comparable entity types and constraints.
2. `candidate-resolution`: identify a public `CandidateSet` of `EntityRef` rows that can be evaluated for the request; Stage-1 retrieval can expose each storage-free `StageCandidate` row with RRF ranks and retrieval provenance; excluded candidates surface as public `Exclusion` rows with reasons.
3. `evidence-attachment`: collect a public `EvidenceSet` of `EvidenceItem` rows with source, kind, observation time, summary, optional score, and metadata; ingested benchmark results can expose a storage-free `ResultRow` provenance envelope.
4. `component-scoring`: produce named `score_components` on a 0-1 scale.
5. `ranking-or-abstention`: return ranked entities when evidence is sufficient; return an abstention reason or exclusions-with-reasons when it is not.
6. `freshness-trust-labeling`: attach freshness, trust tier, caveats, and evidence counts to make the score inspectable.

## Public Boundaries

- Public contracts define payload shape, value ranges, and explainability fields.
- Public schemas define interoperability, not storage tables.
- Public fixtures are synthetic examples, not benchmark results.
- Public adapters may return deterministic fixtures until live public APIs exist.

## Private Boundaries

- Proprietary weights, thresholds, graders, held-out tasks, and benchmark answers stay outside this repo.
- Production evidence rows, customer traces, account context, and telemetry stay outside this repo.
- Database migrations stay private until EvalRank owns a deploy path or its own project.
