# EvalRank Python SDK

Python SDK package boundary for public EvalRank APIs.

Package metadata:

- Distribution: `evalrank-sdk`
- Import: `evalrank_sdk`
- Runtime dependency: `evalrank-core==0.0.0`
- License: `Apache-2.0`

The SDK re-exports the public core: `CapabilityFingerprintInput`, `RawEntry`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `EvidenceSet`, `SourceArtifactV1`, `RunProvenanceV1`, `ObservationV1`, `ConfigurationPassportV1`, `EvaluatedConfigurationV1`, `UsageProfileV1`, `PricingScheduleFactV1`, `ServingOfferV1`, `EvaluationToOfferLinkV1`, `DecisionQueryV1`, `DecisionReceiptV1`, `RankingGroupSnapshotRefV1`, `SnapshotSetDescriptorV1`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankingGroup`, `Exclusion`, `TheCall`, `Abstention`, `RankedEntity`, `Recommendation`, `ProblemDetails`, `TRUST_TIERS`, `FRESHNESS_STATUSES`, `COMPARABILITY_MODES`, `EVIDENCE_KINDS`, `PROBLEM_CODES`, `PUBLIC_FIXTURE_KINDS`, `sample_problem_details`, and `sample_public_fixture`. It also exports `monthly_cost_microusd`, restricted canonical JSON helpers, semantic read verifiers, and the `sample_observation` fixture. Snapshot-set verification binds every publication snapshot to its owning ranking group rather than accepting an unowned set of snapshot IDs.

`EvalRankClient` is a dependency-free stdlib client for the public metadata and recommendation route contracts. It accepts only HTTP(S) base URLs, fetches `GET /v1/use-cases` and `GET /v1/scoring-stages`, and can post `EvaluationRequest` JSON to `POST /v1/recommendations`. Non-2xx Problem Details responses raise `EvalRankApiError`; a successful recommendation body is future contract behavior, not the current hosted behavior.

The hosted legacy recommendation operation is temporarily unavailable and currently raises `EvalRankApiError` with public code `recommendation_not_published`. Keeping that typed failure visible prevents clients from treating a cached use-case lookup as a decision over the full request.

```python
from evalrank_sdk import EvalRankClient, sample_evaluation_request

client = EvalRankClient("https://evalrank.example")
use_cases = client.use_cases()
stages = client.scoring_stages()
# The current hosted call raises recommendation_not_published.
# recommendation = client.recommend(sample_evaluation_request())
```

The client does not add auth, retries, service discovery, environment-variable defaults, hosted receipt IDs, tenant context, private DTOs, local file URLs, production evidence lookup, or any private hosted behavior.
