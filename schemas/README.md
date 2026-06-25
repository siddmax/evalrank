# Schemas

Public EvalRank JSON Schema contracts live here.

- `ranked-entity.schema.json` mirrors `RankedEntity.to_dict()` and core enum constants.
- `recommendation.schema.json` mirrors `Recommendation.to_dict()` and core enum constants.
- `evidence-item.schema.json` mirrors `EvidenceItem.to_dict()` and core enum constants.
- `evaluation-request.schema.json` mirrors `EvaluationRequest.to_dict()`.
- `capability-fingerprint.schema.json` mirrors `CapabilityFingerprintInput.to_dict()`.

Schemas that expose `methodology_version` require `YYYY-MM-DD.SEQ.slug`.

Run:

```sh
python3 -m unittest tests.test_schema_contracts
```
