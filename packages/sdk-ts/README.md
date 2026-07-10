# EvalRank TypeScript SDK

TypeScript SDK package boundary for public EvalRank APIs.

Package metadata:

- Package: `@evalrank/sdk`
- Type: `module`
- Types: `./src/index.ts`
- License: `Apache-2.0`
- Publish status: `private`

## Public Surface

- Public constants for trust tiers, freshness statuses, comparability modes, evidence kinds, use-case vocabulary, `the_call` decisions, public Problem Details codes, and `PUBLIC_FIXTURE_KINDS`.
- Public string-union type `PublicFixtureKind` mirrors the shared fixture kind list.
- Public helper type `NonEmptyArray<T>` mirrors schema `minItems: 1` arrays at TypeScript compile time.
- `AggregationInputDocument`, `BootstrapSeedDocument`, and `RankingGroupIdentity` type the portable aggregation preimages. `aggregationInputDocument`, `deriveAggregationInputDigest`, `bootstrapSeedDocument`, and `deriveBootstrapSeed` validate and hash the same restricted-JCS bytes as Python, canonicalize observation-set order, and mask the seed with `BigInt` before converting to a safe `number`.
- Public TypeScript interfaces and types include immutable `SourceArtifactV1`, typed `RunProvenanceV1` and `ObservationV1`, exact configuration passports, closed monthly `UsageProfileV1`, `PricingScheduleFactV1`, serving offers and reviewed links, semantic `DecisionQueryV1`, deterministic `DecisionReceiptV1`, pair-owned `RankingGroupSnapshotRefV1` and `SnapshotSetDescriptorV1`, and the existing `CapabilityFingerprint`, `RawEntry`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceItem`, `EvidenceSet`, `ScoringStage`, `ScoringStageCatalog`, `UseCase`, `UseCaseCatalog`, `RankingGroup`, `Exclusion`, `Abstention`, `TheCall`, `RankedEntity`, `RecommendationCallState`, and `Recommendation` metadata/reference contracts.
- `monthlyCostMicrousd` uses `BigInt` for every intermediate, joins cache writes by exact TTL, ceilings once, and returns `null` instead of treating a missing nonzero cache rate as free. Offer/link eligibility helpers parse unknown runtime input and return `false` for malformed provenance, schedules, evidence bases, or timestamps.
- `verifyLeaderboardSemantics`, `verifyEntityDetailSemantics`, and `verifyCompareResultSemantics` enforce the same post-schema invariants as Python: exact ranking-group snapshot ownership, unique group and configuration identities, rank and interval validity, truthful eligibility gaps, and no top-set claims on non-active reads.
- `UseCase` is a discriminated union for the public ranked and veto-overlay branches.
- `TheCall` is a discriminated union for the public `recommend` and `abstain` branches.
- `Recommendation` is a discriminated union for the public `single-scale` and `kind-grouped` branches, plus the public `the_call`/`abstention` state; abstaining responses are empty single-scale responses.
- `RankedEntity.axes.evidence` carries the public evidence count and trust-tier coverage shape from the JSON Schema.
- `Recommendation` includes `abstention`, `recommendation_id`, `recommend_id`, and `search_run_id` as public response fields.
- `ProblemDetails` mirrors the public RFC 9457 error contract plus optional retry extensions; it does not imply a hosted service client.
- `EvalRankClient` is a dependency-free native `fetch` client for the public metadata and recommendation route contracts. It accepts only explicit HTTP(S) base URLs, fetches `GET /v1/use-cases` and `GET /v1/scoring-stages`, can post public `EvaluationRequest` JSON to `POST /v1/recommendations`, and raises `EvalRankApiError` with public Problem Details for non-2xx responses. A successful recommendation body is future contract behavior, not the current hosted behavior.
- `PUBLIC_FIXTURE_KINDS` and its `PublicFixtureKind` union keep fixture discovery exact, while `NonEmptyArray<T>` carries schema non-emptiness into TypeScript.
- The hosted legacy recommendation operation is temporarily unavailable and surfaces public code `recommendation_not_published`; callers must preserve that typed state until the deterministic decision operation replaces the legacy route atomically.
- No auth flow, retries, service discovery, environment-variable defaults, hosted-product behavior, hosted receipt IDs, persistence, or private data access.
- The npm package is marked private until a built JS distribution and publish flow exist.

## Example

```ts
import { EvalRankClient, type EvaluationRequest } from "@evalrank/sdk";

const request: EvaluationRequest = {
  object: "evaluation_request",
  request_id: "req_public_fixture_01",
  use_case: "web-browsing",
  entity_types: ["component_configuration"],
  requested_at: "2026-06-25T00:00:00Z",
  constraints: {},
};

const client = new EvalRankClient("https://evalrank.example");
const useCases = await client.useCases();
const stages = await client.scoringStages();
// The current hosted call throws recommendation_not_published.
// const recommendation = await client.recommend(request);
```

## Check

```sh
npm ci --prefix packages/sdk-ts
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
```

Ajv is an exact, lockfile-pinned development dependency used only to validate `catalog/manifest.json` against the Draft 2020-12 schema during tests; it is not part of the SDK runtime surface.
