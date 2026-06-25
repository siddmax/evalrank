# EvalRank TypeScript SDK

TypeScript SDK package boundary for public EvalRank APIs.

## Public Surface

- Public constants for trust tiers, freshness statuses, comparability modes, evidence kinds, result-row vocabulary, use-case vocabulary, `the_call` decisions, and public Problem Details codes.
- Public TypeScript interfaces for `CapabilityFingerprint`, `RawEntry`, `TheCall`, `ProblemDetails`, `EntityRef`, `EvaluationRequest`, `CandidateSet`, `StageCandidate`, `EvidenceSet`, `Exclusion`, `EvidenceItem`, `ResultRow`, `UseCase`, `UseCaseCatalog`, `RankedEntity`, `RankingGroup`, and `Recommendation`.
- `Recommendation` includes `recommendation_id`, `recommend_id`, and `search_run_id` as public join aliases.
- `ProblemDetails` mirrors the public RFC 9457 error contract plus optional retry extensions; it does not imply a hosted service client.
- No service client, auth flow, hosted-product behavior, or private data access.
- The npm package is marked private until a built JS distribution and publish flow exist.

## Check

```sh
npm run check --prefix packages/sdk-ts
```
