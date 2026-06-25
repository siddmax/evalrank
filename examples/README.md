# Examples

Runnable public examples live here. Examples must use public fixtures only.

## Public Fixture

```sh
python3 examples/public_fixture.py
```

Prints one JSON object with synthetic public fixtures under these keys: `candidate_set`, `evidence`, `evidence_set`, `exclusion`, `problem`, `raw_entry`, `recommendation`, `request`, `result_row`, `scoring_stages`, `stage_candidate`, and `use_cases`.

Nested contract refs that examples must keep visible: `recommendation.abstention`, `recommendation.the_call`, and `scoring_stages.stages[].output_contracts`, including `Abstention`.
