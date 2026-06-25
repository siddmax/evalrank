# EvalRank Core

Reference Python package for public EvalRank evidence and scoring contracts.

Use `evalrank_core.fixtures.sample_public_fixture(kind)` with `PUBLIC_FIXTURE_KINDS`, or the individual fixture helpers, for public examples and contract tests.

Candidate set payloads expose a storage-free list of public `EntityRef` candidates for a request; source adapters and graph lookup stay outside this package.

Stage candidate payloads expose one storage-free Stage-1 candidate row with RRF ranks and retrieval provenance; scorer stages, graph lookup, trust policy, and private tuning stay outside this package.

Evidence set payloads expose storage-free public `EvidenceItem` rows for a request; live evidence lookup and evidence ledger persistence stay outside this package.

Result row payloads expose storage-free benchmark/result provenance. Source adapters, production rows, private benchmark material, scorer fitting, and storage tables stay outside this package.

Use case catalog payloads expose public taxonomy metadata only. Benchmark weights, IRT clusters, confidence policy, synthesis rules, and storage tables stay outside this package.

Ranking group payloads expose within-kind ranking rows for `kind-grouped` recommendations only. Cross-kind score normalization and scorer internals stay outside this package.

Exclusion payloads expose storage-free public subjects and reasons; gate policy and private reason taxonomies stay outside this package.

Public `methodology_version` values use `YYYY-MM-DD.SEQ.slug`, for example `2026-06-25.1.public-fixture-v1`.

Recommendation payloads expose `recommendation_id`, `recommend_id`, and `search_run_id` as the same public ID.

Ranked entity `score_components` values are a public explanation map: non-empty component names to 0-1 numeric scores. Private weights, formulas, and calibration stay out of this package.

Recommendation `the_call` payloads expose only `decision`, `confidence`, `reason`, and `abstention_reason`; scorer thresholds and private confidence tuning stay out of this package.
