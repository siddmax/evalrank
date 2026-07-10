# Schemas

Public EvalRank JSON Schema contracts live here.

- `openapi.json` defines the public REST route contract and references the payload schemas below.

- `evalrank-manifest.schema.json` defines Manifest V1 for the canonical public cell, benchmark-family, feed, governance, cadence, lineage, and eligibility inventory in `catalog/manifest.json`.
- `benchmark-research-provenance.schema.json` defines the closed V1 companion contract for dated primary/official family sources and categorized source-backed or EvalRank-inference claims in `catalog/research-provenance.json`.
- `ranked-entity.schema.json` mirrors `RankedEntity.to_dict()` and core enum constants.
- `recommendation.schema.json` mirrors `Recommendation.to_dict()` and core enum constants.
- `exclusion.schema.json` mirrors `Exclusion.to_dict()` and is referenced from recommendations.
- `evidence-item.schema.json` mirrors `EvidenceItem.to_dict()` and core enum constants.
- `source-artifact.schema.json` content-addresses replayable upstream bytes and their canonical source coordinates.
- `run-provenance.schema.json` records one closed parser/run envelope referencing a source artifact exactly once.
- `observation.schema.json` defines closed metric and uncertainty unions for one evaluated configuration.
- `configuration-passport.schema.json` pins one resolved manifest identity and reproducible configuration.
- `evaluated-configuration.schema.json` content-addresses a configuration passport.
- `serving-offer.schema.json` separates dated context and availability from effective-dated integer-microusd pricing schedules, including nullable cached-read/storage rates and TTL-qualified cache-write rates.
- `evaluation-to-offer-link.schema.json` records reviewed exact, incompatible, or unresolved configuration-to-offer evidence with an explicit evidence basis; inferred links are never decision-eligible.
- `decision-query.schema.json` defines transport-free semantic decision intent for one exact ranking group and a closed monthly usage profile. Estimated cache usage requires an explicit zero-cache profile; measured usage forbids one.
- `decision-receipt.schema.json` defines a deterministic, typed top-set or abstention receipt, including nullable baseline and zero-cache projected monthly costs on every selection.
- `leaderboard.schema.json` defines a cell snapshot set with separate ranking-group publication sections. Its content-addressed descriptor carries a closed, UTF-16-sorted list of exact `ranking_group_id`/`publication_snapshot_id` ownership pairs.
- `entity-detail.schema.json` defines one exact evaluated configuration and ranking projection.
- `compare-result.schema.json` defines a two-to-four configuration comparison on one group scale.
- `evidence-set.schema.json` mirrors `EvidenceSet.to_dict()` and reuses `evidence-item.schema.json`.
- `evaluation-request.schema.json` mirrors `EvaluationRequest.to_dict()`.
- `candidate-set.schema.json` mirrors `CandidateSet.to_dict()`.
- `stage-candidate.schema.json` mirrors `StageCandidate.to_dict()`.
- `capability-fingerprint.schema.json` mirrors `CapabilityFingerprintInput.to_dict()`.
- `raw-entry.schema.json` mirrors `RawEntry.to_dict()`.
- `use-case-catalog.schema.json` mirrors `UseCaseCatalog.to_dict()`.
- `scoring-stage-catalog.schema.json` mirrors `ScoringStageCatalog.to_dict()`.
- `problem.schema.json` pins the RFC 9457 Problem Details error shape and public retry extensions for public route contracts.

Schemas that expose `methodology_version` require `YYYY-MM-DD.SEQ.slug`.

Generated public hashes use 64-character lowercase hex strings.

Ranked entity schemas require `score_components` to be a public explanation map with non-empty names and 0-1 numeric scores, and `axes.evidence` to carry only public evidence count plus trust-tier coverage. Private weights, formulas, and scorer calibration stay outside this repo.

Ranked entity `ci95` fields are exactly two numeric unit-interval scores: `[low, high]`. Observation uncertainty is a closed typed object and decimal measurements remain canonical strings.

Ranked entity freshness dates use public `YYYY-MM-DD` strings for `last_eval` and `next_refresh`; Python core validation requires calendar-valid dates, while timestamps and private scheduler details stay outside the schema.

Public event timestamp fields use UTC `YYYY-MM-DDTHH:MM:SSZ` strings; private scheduler cadence and runtime refresh policy stay outside the schemas.

Artifact, evaluated-configuration, semantic-query, and receipt identities use the shared restricted RFC 8785 subset: UTF-16 object-key ordering, UTF-8 without whitespace, safe integers, no floats, valid Unicode, and no normalization. Set-valued query fields reject duplicates and serialize sorted.

Monthly cost is computed from uncached input, cached reads, output, exact-TTL cache writes, and cache-storage token-seconds using integer arithmetic over one common denominator and one final ceiling. A missing rate for any nonzero component is an abstention condition, never a zero-price default. The receipt calls these values projections under declared profiles, requires a hard monthly budget to cover both the baseline and any declared zero-cache profile, and discloses `cost_sensitive_to_usage` whenever estimated projections differ. Cross-field total-input/output equality, duplicate TTL rejection, exact cost recomputation, cross-profile budget comparison, caveat truth, and pricing `effective_at` validity are enforced by the Python and TypeScript semantic validators where JSON Schema cannot express them.

Manifest identity triples are one of five explicit versioned resolved combinations (model, agent, system, component, or arena) or exactly `unresolved`/`unresolved`/`unresolved-v1`; mixed or invented combinations are invalid. Unresolved identities must be explorer-only, and resolved identities may also be explorer-only when the evidence policy cannot support a top set. Every explorer ceiling keeps top-set, winner, superiority, practical-effect, and leave-one-family-out fields null; active groups must use the single-winner-capable policy. Discovery keeps adapter IDs, rank counts, cadence thresholds, and task/environment/grader lineage IDs null. Shadow feeds require an adapter. Active feeds require an adapter, a positive rank count, approved rights, validated ordered cadence, validated lineage, and a validated correlation group; active ranking groups require calibrated evidence, a positive rank count, and enough independently counted active families for their top-set gate. Quarantine requires an explicit reason and null rank count, while non-quarantined records keep the reason null. A family may expose multiple feeds, but feeds sharing a declared correlation group count once.

`npm run test --prefix packages/sdk-ts` compiles the manifest schema with Ajv's Draft 2020-12 implementation, validates the canonical manifest, and mutation-tests the closed identity, cadence, lineage, correlation, quarantine, and admission branches. `tests/test_catalog_manifest.py` guards cross-record cell, family, feed, ranking-group, and independent-family joins that JSON Schema cannot express.

`tests/test_catalog_research_provenance.py` validates the research companion with Ajv's Draft 2020-12 implementation and guards exact manifest-version/family coverage, dated HTTPS source references, claim-source joins, direct-versus-inference categorization, and exact research-flag linkage. Research sources do not establish runtime lineage, rights, or admission.

Core contract tests also guard primitive and sequence fields that JSON Schema already constrains, including entity refs, freshness dates, unique request entity-type arrays, ranked-entity integer fields, and caveats arrays.

Core contract tests also guard public string fields that JSON Schema already constrains; those values must be actual non-empty strings before serialization.

Recommendation schemas require `recommendation_id`, `recommend_id`, and `search_run_id` to share the public `rec_` ID shape. They also pin the nested public `the_call` shape to `decision`, `confidence`, `reason`, and `abstention_reason`, require the `abstention` field to be either null or a closed public `reason`/`detail` object, require `the_call` and `abstention` to agree on abstention state, require abstentions to be empty single-scale responses, require schema-compatible envelope metadata, use unique grouped rows and unique `exclusion.schema.json` rows, and close ranking-group rows for `kind-grouped` recommendations. Keyed duplicate ranked-entity, group, and duplicate-exclusion rejection lives in the core contract because JSON Schema `uniqueItems` only checks whole item identity.

Candidate set schemas require at least one unique public `EntityRef`; source adapters and graph lookup stay outside this repo.

Stage candidate schemas define one storage-free Stage-1 row with RRF ranks and retrieval provenance. Stage-2+ scorer fields, graph lookup, source adapters, storage, telemetry, and private tuning stay outside this repo.

Evidence set schemas allow an empty `evidence_items` array for abstention or no-evidence paths. Live evidence lookup, evidence ledger persistence, and private source rows stay outside this repo.

Evidence item `metadata` and evaluation request `constraints` are public JSON-object extension points only. Private evidence rows, source-adapter state, and policy internals stay outside this repo.

Observation schemas never duplicate mutable source URLs or hashes inside run provenance. They preserve proportion, continuous, pass-at-k, pairwise-preference, and rank-only evidence without coercing unlike metrics onto one scale. Unknown, standard-error, and interval uncertainty remain explicit.

Exclusion schemas describe the public row shape only. Stage-0 gate policy, private safety taxonomy, and constraint evaluation stay outside this repo.

Use case catalog schemas expose public taxonomy metadata: slugs, names, one-line definitions, entity-kind spans, and rank policy. The canonical cell inventory and calibrated-gate policy live in `catalog/manifest.json`; evidence synthesis lives in `methods/evidence-synthesis.md`. Private observations and persistence semantics stay outside this repo.

Scoring stage catalog schemas expose only public stage order, contract refs, and boundary notes. Formulas, thresholds, graders, production telemetry, and runtime scorer behavior stay outside this repo.

Problem Details schemas intentionally allow extension members. Public extensions are limited to `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url`; optional `doc_url` values are public HTTP(S) URLs. Private problem types, hosted error internals, auth context, and tenant details stay outside this repo.

The OpenAPI contract includes metadata reads, grouped leaderboard/entity/compare reads, and the staged `POST /v1/recommendations` contract. It reuses response components for malformed requests, unsupported media, validation errors, not-found reads, rate limits, temporary unavailability, and upstream timeouts. `429` responses expose `Retry-After`, `RateLimit`, and `RateLimit-Policy` header contracts; the repo does not implement live throttling.

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract
```
