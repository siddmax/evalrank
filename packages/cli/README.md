# EvalRank CLI

Command-line boundary for public EvalRank workflows.

Fixture commands:

```sh
evalrank fixture fingerprint
evalrank fixture raw-entry
evalrank fixture request
evalrank fixture candidate-set
evalrank fixture stage-candidate
evalrank fixture evidence
evalrank fixture problem
evalrank fixture result-row
evalrank fixture ranking-group
evalrank fixture evidence-set
evalrank fixture exclusion
evalrank fixture use-cases
evalrank fixture scoring-stages
evalrank fixture recommendation
```

These commands write deterministic public JSON fixtures and perform no network or database work.

Recommendation command:

```sh
evalrank recommend --base-url https://evalrank.example --request request.json
evalrank recommend --base-url https://evalrank.example --request -
```

This command posts an explicit public `EvaluationRequest` JSON payload to the public `POST /v1/recommendations` contract. It accepts only HTTP(S) base URLs, writes recommendation JSON to stdout, writes public Problem Details JSON to stderr on API errors, and does not add auth, retries, service discovery, environment-variable defaults, private DTOs, or database work.
