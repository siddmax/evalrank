# Examples

Runnable public examples live here. Examples must use public fixtures only.

## Public Fixture

```sh
python3 examples/public_fixture.py
```

Prints one JSON object with synthetic public fixtures under these keys: `candidate_set`, `evidence`, `evidence_set`, `exclusion`, `observation`, `problem`, `raw_entry`, `recommendation`, `request`, `scoring_stages`, `stage_candidate`, and `use_cases`.

Nested contract refs that examples must keep visible: `recommendation.abstention`, `recommendation.the_call`, and `scoring_stages.stages[].output_contracts`, including `Abstention`.

`decision-contract-v1.golden.json` is the shared Python/TypeScript restricted-JCS corpus for monthly usage, effective-dated schedule pricing, baseline and zero-cache projected costs, cross-profile hard budgets, truthful cost-sensitivity caveats, evidence-basis links, and deterministic receipt identity.
