# EvalRank TypeScript SDK

TypeScript SDK package boundary for public EvalRank APIs.

## Public Surface

- Public constants for trust tiers, freshness statuses, comparability modes, evidence kinds, result-row vocabulary, use-case vocabulary, `the_call` decisions, public Problem Details codes, and `PUBLIC_FIXTURE_KINDS`.
- Public string-union type `PublicFixtureKind` mirrors the shared fixture kind list.
- Public TypeScript interfaces for `CapabilityFingerprint`, `RawEntry`, `TheCall`, `Abstention`, `ProblemDetails`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceSet`, `Exclusion`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankedEntity`, `RankingGroup`, and `Recommendation`.
- `Recommendation` includes `abstention`, `recommendation_id`, `recommend_id`, and `search_run_id` as public response fields.
- `ProblemDetails` mirrors the public RFC 9457 error contract plus optional retry extensions; it does not imply a hosted service client.
- `EvalRankClient` is a dependency-free native `fetch` client for the public `POST /v1/recommendations` contract. It accepts only explicit HTTP(S) base URLs, posts public `EvaluationRequest` JSON, returns public `Recommendation` JSON, and raises `EvalRankApiError` with public Problem Details for non-2xx responses.
- No auth flow, retries, service discovery, environment-variable defaults, hosted-product behavior, hosted receipt IDs, persistence, or private data access.
- The npm package is marked private until a built JS distribution and publish flow exist.

## Example

```ts
import { EvalRankClient, type EvaluationRequest } from "@evalrank/sdk";

const request: EvaluationRequest = {
  object: "evaluation_request",
  request_id: "req_public_fixture_01",
  use_case: "web-browsing",
  entity_types: ["mcp_server"],
  requested_at: "2026-06-25T00:00:00Z",
  constraints: {},
};

const client = new EvalRankClient("https://evalrank.example");
const recommendation = await client.recommend(request);
```

## Check

```sh
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
```
