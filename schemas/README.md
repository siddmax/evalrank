# Schemas

Public EvalRank JSON Schema contracts live here.

- `ranked-entity.schema.json` mirrors `RankedEntity.to_dict()` and core enum constants.
- `recommendation.schema.json` mirrors `Recommendation.to_dict()` and core enum constants.
- `evidence-item.schema.json` mirrors `EvidenceItem.to_dict()` and core enum constants.

Run:

```sh
python3 -m unittest tests.test_schema_contracts
```
