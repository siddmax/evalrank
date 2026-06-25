# EvalRank Core

Reference Python package for public EvalRank evidence and scoring contracts.

Use `evalrank_core.fixtures.sample_public_fixture(kind)` with `PUBLIC_FIXTURE_KINDS`, or the individual fixture helpers, for public examples and contract tests.

Public contract surface: `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `EvidenceSet`, `ResultRow`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `Exclusion`, `TheCall`, `Abstention`, `RankedEntity`, `Recommendation`, `ProblemDetails`, `EntityRef`, and public vocabulary constants including `TRUST_TIERS`, `FRESHNESS_STATUSES`, `COMPARABILITY_MODES`, `EVIDENCE_KINDS`, and `PROBLEM_CODES`.

Candidate set payloads expose a storage-free list of public `EntityRef` candidates for a request; source adapters and graph lookup stay outside this package.

Stage candidate payloads expose one storage-free Stage-1 candidate row with RRF ranks and retrieval provenance; scorer stages, graph lookup, trust policy, and private tuning stay outside this package.

Evidence set payloads expose storage-free public `EvidenceItem` rows for a request; live evidence lookup and evidence ledger persistence stay outside this package.

Evidence item `metadata` and evaluation request `constraints` are public JSON objects. Non-object values, non-string keys, and non-JSON values are rejected before serialization.

Entity references, freshness dates, request entity types, ranked-entity ranks, evidence counts, and caveats reject schema-incompatible Python values before serialization.

Capability fingerprint, raw entry, evidence item, evidence set, candidate set, `the_call`, and abstention public string fields must be actual non-empty strings.

Result row payloads expose storage-free benchmark/result provenance. Source adapters, production rows, private benchmark material, scorer fitting, and storage tables stay outside this package.

Use case catalog payloads expose public taxonomy metadata only. Benchmark weights, IRT clusters, confidence policy, synthesis rules, and storage tables stay outside this package.

Scoring stage catalog payloads expose public stage order, contract refs, and boundary notes only. Formulas, thresholds, graders, telemetry, and runtime scorer behavior stay outside this package.

Ranking group payloads expose within-kind ranking rows for `kind-grouped` recommendations only. Cross-kind score normalization and scorer internals stay outside this package.

Exclusion payloads expose storage-free public subjects and reasons; gate policy and private reason taxonomies stay outside this package.

Public `methodology_version` values use `YYYY-MM-DD.SEQ.slug`, for example `2026-06-25.1.public-fixture-v1`.

Recommendation payloads expose `recommendation_id`, `recommend_id`, and `search_run_id` as the same public ID.

Recommendation envelopes reject schema-incompatible metadata before serialization: invalid depth, blank rationale/source fields, non-boolean degradation flags, negative or non-integer snapshot lag, and duplicate ranked entities.

Ranked entity `score_components` values are a public explanation map: non-empty component names to 0-1 numeric scores. Private weights, formulas, and calibration stay out of this package.

Recommendation `the_call` payloads expose only `decision`, `confidence`, `reason`, and `abstention_reason`; scorer thresholds and private confidence tuning stay out of this package.

Recommendation `abstention` payloads expose only a public `reason` and `detail` when no ranked answer should be returned. Evidence-floor thresholds, policy internals, and private reason taxonomies stay outside this package.

Problem Details payloads expose the public RFC 9457 error shape plus retry-safe public extensions. Private problem types, tenant context, hosted internals, and production telemetry stay outside this package.
