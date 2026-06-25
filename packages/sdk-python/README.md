# EvalRank Python SDK

Python SDK package boundary for public EvalRank APIs.

The current SDK surface re-exports public contracts, vocabulary constants, and fixtures from `evalrank-core`, including `CapabilityFingerprintInput`, `RawEntry`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `EvidenceSet`, `ResultRow`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `Exclusion`, `TheCall`, `Abstention`, `RankedEntity`, `Recommendation`, `ProblemDetails`, `TRUST_TIERS`, `FRESHNESS_STATUSES`, `COMPARABILITY_MODES`, `EVIDENCE_KINDS`, `PROBLEM_CODES`, `PUBLIC_FIXTURE_KINDS`, `sample_problem_details`, and `sample_public_fixture`.

`EvalRankClient` is a dependency-free stdlib client for the public `POST /v1/recommendations` contract. It accepts only HTTP(S) base URLs, posts an `EvaluationRequest` JSON payload, and returns public recommendation JSON. Non-2xx Problem Details responses raise `EvalRankApiError`.

```python
from evalrank_sdk import EvalRankClient, sample_evaluation_request

client = EvalRankClient("https://evalrank.example")
recommendation = client.recommend(sample_evaluation_request())
```

The client does not add auth, retries, hosted receipt IDs, tenant context, private DTOs, local file URLs, or production evidence lookup.
