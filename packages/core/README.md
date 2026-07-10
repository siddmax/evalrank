# EvalRank Core

Reference Python package for public EvalRank evidence and scoring contracts.

Package metadata:

- Distribution: `evalrank-core`
- Import: `evalrank_core`
- License: `Apache-2.0`

Use `evalrank_core.fixtures.sample_public_fixture(kind)` with `PUBLIC_FIXTURE_KINDS`, or individual fixture helpers such as `sample_problem_details()`, for public examples and contract tests.

Public contract surface: `CapabilityFingerprintInput`, `RawEntry`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `EvidenceSet`, `SourceArtifactV1`, `RunProvenanceV1`, `ObservationV1`, `ConfigurationPassportV1`, `EvaluatedConfigurationV1`, `ServingOfferV1`, `EvaluationToOfferLinkV1`, `DecisionQueryV1`, `DecisionReceiptV1`, `RankingGroupSnapshotRefV1`, `SnapshotSetDescriptorV1`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `Exclusion`, `TheCall`, `Abstention`, `RankedEntity`, `Recommendation`, `ProblemDetails`, `EntityRef`, and `materialize_recommendation`. Public vocabulary includes `TRUST_TIERS`, `FRESHNESS_STATUSES`, `COMPARABILITY_MODES`, `EVIDENCE_KINDS`, `PROBLEM_CODES`, and `PUBLIC_FIXTURE_KINDS`; `sample_public_fixture` exposes the synthetic fixture bundle. `canonical_json`, `restricted_jcs`, and `sha256_hex` implement the restricted cross-language hash domain. A snapshot-set descriptor hashes the UTF-16-sorted, one-to-one `ranking_group_id`/`publication_snapshot_id` ownership pairs; the read verifiers reject pair swaps, duplicate identities, invalid ranks or intervals, false eligibility gaps, and non-active top-set claims.

Candidate set payloads expose a storage-free list of public `EntityRef` candidates for a request; source adapters and graph lookup stay outside this package.

Stage candidate payloads expose one storage-free Stage-1 candidate row with RRF ranks and retrieval provenance; scorer stages, graph lookup, trust policy, and private tuning stay outside this package.

`materialize_recommendation(...)` is the public storage-free reference materializer. It consumes already-provided request, candidate, Stage-1, evidence, `ObservationV1`, and exclusion values. Only unit-interval proportion/pass-at-k observations with reported 95% intervals are eligible because the existing reference envelope labels the field `ci95`; continuous, pairwise, rank-only, interval-free, differently leveled, and derived-interval inputs cause abstention instead of silent coercion or fabricated confidence bounds. It does not fetch sources, persist rows, call networks, fit scorers, or access private evidence graphs.

Evidence set payloads expose storage-free public `EvidenceItem` rows for a request; live evidence lookup and evidence ledger persistence stay outside this package.

Evidence item `metadata` and evaluation request `constraints` are public JSON objects. Non-object values, non-string keys, and non-JSON values are rejected before serialization.

Entity references, freshness dates, public timestamps, request entity types, ranked-entity ranks, evidence counts, and caveats reject schema-incompatible Python values before serialization. Freshness dates use calendar-valid `YYYY-MM-DD`; public timestamps use calendar-valid UTC `YYYY-MM-DDTHH:MM:SSZ`. Caveat strings must be non-empty. Request entity types must be unique.

Capability fingerprint, raw entry, evidence item, evidence set, candidate set, `the_call`, and abstention public string fields must be actual non-empty strings.

Observations separate immutable source bytes, typed run provenance, exact evaluated-configuration identity, metric kind, counts, and uncertainty. Decimal measurements are canonical strings; counts are safe integers. Mutable URLs and untyped provenance maps are not accepted.

Use case catalog payloads expose public taxonomy metadata only. Benchmark weights, IRT clusters, confidence policy, synthesis rules, and storage tables stay outside this package.

Scoring stage catalog payloads expose public stage order with contiguous `1..N` ordinals, contract refs, and boundary notes only. Formulas, thresholds, graders, telemetry, and runtime scorer behavior stay outside this package.

Ranking group payloads expose within-kind ranking rows with contiguous `1..N` ranks in array order for `kind-grouped` recommendations only. Recommendation envelopes reject duplicate group keys and entity types. Cross-kind score normalization and scorer internals stay outside this package.

Exclusion payloads expose storage-free public subjects and reasons; gate policy and private reason taxonomies stay outside this package.

Public `methodology_version` values use calendar-valid `YYYY-MM-DD.SEQ.slug`, for example `2026-06-25.1.public-fixture-v1`.

Recommendation payloads expose `recommendation_id`, `recommend_id`, and `search_run_id` as the same public ID.

Recommendation envelopes reject schema-incompatible metadata before serialization: invalid depth, `shortlist_depth` count drift, blank rationale/source fields, non-boolean degradation flags, negative or non-integer snapshot lag, duplicate ranked entities, duplicate/gapped/out-of-order rank positions, and duplicate exclusions.

Ranked entity `score_components` values are a public explanation map: non-empty component names to 0-1 numeric scores. Private weights, formulas, and calibration stay out of this package.

Ranked entity freshness dates use public calendar-valid `YYYY-MM-DD` strings for `last_eval` and `next_refresh`.

Public event timestamps use UTC `YYYY-MM-DDTHH:MM:SSZ` strings for request, generated, fetched, and observed timestamps.

Recommendation `the_call` payloads expose only `decision`, `confidence`, `reason`, and `abstention_reason`; scorer thresholds and private confidence tuning stay out of this package.

Recommendation `abstention` payloads expose only a public `reason` and `detail` when no ranked answer should be returned, and must be paired with an abstaining `the_call` on an empty single-scale response. Evidence-floor thresholds, policy internals, and private reason taxonomies stay outside this package.

Problem Details payloads expose the public RFC 9457 error shape plus retry-safe public extensions. Optional `doc_url` values must be public HTTP(S) URLs. Private problem types, tenant context, hosted internals, and production telemetry stay outside this package.
