# Schemas

Public EvalRank JSON Schema contracts live here.

- `openapi.json` defines the public REST route contract and references the payload schemas below.

- `ranked-entity.schema.json` mirrors `RankedEntity.to_dict()` and core enum constants.
- `recommendation.schema.json` mirrors `Recommendation.to_dict()` and core enum constants.
- `exclusion.schema.json` mirrors `Exclusion.to_dict()` and is referenced from recommendations.
- `evidence-item.schema.json` mirrors `EvidenceItem.to_dict()` and core enum constants.
- `evidence-set.schema.json` mirrors `EvidenceSet.to_dict()` and reuses `evidence-item.schema.json`.
- `evaluation-request.schema.json` mirrors `EvaluationRequest.to_dict()`.
- `candidate-set.schema.json` mirrors `CandidateSet.to_dict()`.
- `stage-candidate.schema.json` mirrors `StageCandidate.to_dict()`.
- `capability-fingerprint.schema.json` mirrors `CapabilityFingerprintInput.to_dict()`.
- `raw-entry.schema.json` mirrors `RawEntry.to_dict()`.
- `problem.schema.json` pins the RFC 9457 Problem Details error shape for public route contracts.

Schemas that expose `methodology_version` require `YYYY-MM-DD.SEQ.slug`.

Recommendation schemas require `recommendation_id`, `recommend_id`, and `search_run_id` to share the public `rec_` ID shape. They also pin the nested public `the_call` shape to `decision`, `confidence`, `reason`, and `abstention_reason`, and use `exclusion.schema.json` for exclusions-with-reasons.

Candidate set schemas require at least one unique public `EntityRef`; source adapters and graph lookup stay outside this repo.

Stage candidate schemas define one storage-free Stage-1 row with RRF ranks and retrieval provenance. Stage-2+ scorer fields, graph lookup, source adapters, storage, telemetry, and private tuning stay outside this repo.

Evidence set schemas allow an empty `evidence_items` array for abstention or no-evidence paths. Live evidence lookup, evidence ledger persistence, and private source rows stay outside this repo.

Exclusion schemas describe the public row shape only. Stage-0 gate policy, private safety taxonomy, and constraint evaluation stay outside this repo.

Problem Details schemas intentionally allow extension members, but this repo does not publish private problem types or hosted error internals.

Run:

```sh
python3 -m unittest tests.test_schema_contracts tests.test_openapi_contract
```
