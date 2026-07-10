# EvalRank CLI

Command-line boundary for public EvalRank workflows.

Package metadata:

- Distribution: `evalrank-cli`
- Import: `evalrank_cli`
- Entrypoint: `evalrank`
- Runtime dependencies: `evalrank-core==0.0.0`, `evalrank-sdk==0.0.0`
- License: `Apache-2.0`

Fixture commands:

```sh
evalrank fixture fingerprint
evalrank fixture raw-entry
evalrank fixture request
evalrank fixture candidate-set
evalrank fixture stage-candidate
evalrank fixture evidence
evalrank fixture problem
evalrank fixture observation
evalrank fixture ranking-group
evalrank fixture evidence-set
evalrank fixture exclusion
evalrank fixture use-cases
evalrank fixture scoring-stages
evalrank fixture recommendation
```

These commands write deterministic public JSON fixtures and perform no network or database work.

Legacy recommendation command:

```sh
evalrank use-cases --base-url https://evalrank.example
evalrank scoring-stages --base-url https://evalrank.example
evalrank recommend --base-url https://evalrank.example --request request.json
evalrank recommend --base-url https://evalrank.example --request -
```

These commands call explicit public route contracts. `use-cases` fetches `GET /v1/use-cases`, `scoring-stages` fetches `GET /v1/scoring-stages`, and `recommend` posts an explicit public `EvaluationRequest` JSON payload to `POST /v1/recommendations`. They accept only HTTP(S) base URLs; successful public JSON would go to stdout, while the current hosted call writes typed Problem Details to stderr and exits nonzero. They do not add auth, retries, service discovery, environment-variable defaults, private DTOs, or database work.

The hosted legacy `recommend` operation is temporarily unavailable and exits with the typed public Problem Details code `recommendation_not_published`. This is intentional until the deterministic decision operation replaces it atomically.
