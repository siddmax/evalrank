# Schemas

Public EvalRank JSON Schema contracts live here.

- `openapi.json` defines the public REST route contract and references the payload schemas below.

- `ranked-entity.schema.json` mirrors `RankedEntity.to_dict()` and core enum constants.
- `recommendation.schema.json` mirrors `Recommendation.to_dict()` and core enum constants.
- `exclusion.schema.json` mirrors `Exclusion.to_dict()` and is referenced from recommendations.
- `evidence-item.schema.json` mirrors `EvidenceItem.to_dict()` and core enum constants.
- `result-row.schema.json` mirrors `ResultRow.to_dict()` for public ingested benchmark/result rows.
- `evidence-set.schema.json` mirrors `EvidenceSet.to_dict()` and reuses `evidence-item.schema.json`.
- `evaluation-request.schema.json` mirrors `EvaluationRequest.to_dict()`.
- `candidate-set.schema.json` mirrors `CandidateSet.to_dict()`.
- `stage-candidate.schema.json` mirrors `StageCandidate.to_dict()`.
- `capability-fingerprint.schema.json` mirrors `CapabilityFingerprintInput.to_dict()`.
- `raw-entry.schema.json` mirrors `RawEntry.to_dict()`.
- `use-case-catalog.schema.json` mirrors `UseCaseCatalog.to_dict()`.
- `problem.schema.json` pins the RFC 9457 Problem Details error shape and public retry extensions for public route contracts.

Schemas that expose `methodology_version` require `YYYY-MM-DD.SEQ.slug`.

Recommendation schemas require `recommendation_id`, `recommend_id`, and `search_run_id` to share the public `rec_` ID shape. They also pin the nested public `the_call` shape to `decision`, `confidence`, `reason`, and `abstention_reason`, use `exclusion.schema.json` for exclusions-with-reasons, and close ranking-group rows for `kind-grouped` recommendations.

Candidate set schemas require at least one unique public `EntityRef`; source adapters and graph lookup stay outside this repo.

Stage candidate schemas define one storage-free Stage-1 row with RRF ranks and retrieval provenance. Stage-2+ scorer fields, graph lookup, source adapters, storage, telemetry, and private tuning stay outside this repo.

Evidence set schemas allow an empty `evidence_items` array for abstention or no-evidence paths. Live evidence lookup, evidence ledger persistence, and private source rows stay outside this repo.

Result row schemas expose the storage-free provenance envelope for ingested scores. Source adapters, raw production rows, private benchmark material, scorer fitting, and storage tables stay outside this repo.

Exclusion schemas describe the public row shape only. Stage-0 gate policy, private safety taxonomy, and constraint evaluation stay outside this repo.

Use case catalog schemas expose only public taxonomy metadata: slugs, names, one-line definitions, entity-kind spans, and ranked-vs-overlay policy. Benchmark weights, IRT clusters, confidence policy, synthesis/coverage rules, and live table semantics stay outside this repo.

Problem Details schemas intentionally allow extension members. Public extensions are limited to `code`, `retriable`, `retry_after`, `field`, `request_id`, and `doc_url`; private problem types, hosted error internals, auth context, and tenant details stay outside this repo.

The OpenAPI contract includes `GET /v1/use-cases` and `POST /v1/recommendations`. It reuses response components for malformed requests, validation errors, rate limits, temporary unavailability, and upstream timeouts. `429` responses expose `Retry-After`, `RateLimit`, and `RateLimit-Policy` header contracts; the repo does not implement live throttling.

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract
```
