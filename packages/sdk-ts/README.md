# EvalRank TypeScript SDK

TypeScript SDK package boundary for public EvalRank APIs.

Package metadata:

- Package: `@evalrank/sdk`
- Type: `module`
- Types: `./src/index.ts`
- License: `Apache-2.0`
- Publish status: `private`

## Public Surface

- Public constants for trust tiers, freshness statuses, comparability modes, evidence kinds, result-row vocabulary, use-case vocabulary, `the_call` decisions, public Problem Details codes, and `PUBLIC_FIXTURE_KINDS`.
- Public string-union type `PublicFixtureKind` mirrors the shared fixture kind list.
- Public helper type `NonEmptyArray<T>` mirrors schema `minItems: 1` arrays at TypeScript compile time.
- Public TypeScript interfaces and types for `CapabilityFingerprint`, `RawEntry`, `TheCall`, `Abstention`, `ProblemDetails`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceSet`, `Exclusion`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `ScoringStage`, `ScoringStageCatalog`, `RankedEntity`, `RankingGroup`, and `Recommendation`.
- `TheCall` is a discriminated union for the public `recommend` and `abstain` branches.
- `RankedEntity.axes.evidence` carries the public evidence count and trust-tier coverage shape from the JSON Schema.
- `Recommendation` includes `abstention`, `recommendation_id`, `recommend_id`, and `search_run_id` as public response fields.
- `ProblemDetails` mirrors the public RFC 9457 error contract plus optional retry extensions; it does not imply a hosted service client.
- `EvalRankClient` is a dependency-free native `fetch` client for the public metadata and recommendation route contracts. It accepts only explicit HTTP(S) base URLs, fetches `GET /v1/use-cases` and `GET /v1/scoring-stages`, posts public `EvaluationRequest` JSON to `POST /v1/recommendations`, returns public JSON, and raises `EvalRankApiError` with public Problem Details for non-2xx responses.
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
const useCases = await client.useCases();
const stages = await client.scoringStages();
const recommendation = await client.recommend(request);
```

## Check

```sh
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
```
