# EvalRank Python SDK

Python SDK package boundary for public EvalRank APIs.

The current SDK surface re-exports public contracts, vocabulary constants, and fixtures from `evalrank-core`, including `CapabilityFingerprintInput`, `RawEntry`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `EvidenceSet`, `ResultRow`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `Exclusion`, `TheCall`, `Abstention`, `RankedEntity`, `Recommendation`, `ProblemDetails`, `TRUST_TIERS`, `FRESHNESS_STATUSES`, `COMPARABILITY_MODES`, `EVIDENCE_KINDS`, `PROBLEM_CODES`, `PUBLIC_FIXTURE_KINDS`, `sample_problem_details`, and `sample_public_fixture`.

`EvalRankClient` is a dependency-free stdlib client for the public metadata and recommendation route contracts. It accepts only HTTP(S) base URLs, fetches `GET /v1/use-cases` and `GET /v1/scoring-stages`, posts `EvaluationRequest` JSON to `POST /v1/recommendations`, and returns public JSON. Non-2xx Problem Details responses raise `EvalRankApiError`.

```python
from evalrank_sdk import EvalRankClient, sample_evaluation_request

client = EvalRankClient("https://evalrank.example")
use_cases = client.use_cases()
stages = client.scoring_stages()
recommendation = client.recommend(sample_evaluation_request())
```

The client does not add auth, retries, service discovery, environment-variable defaults, hosted receipt IDs, tenant context, private DTOs, local file URLs, production evidence lookup, or any private hosted behavior.
