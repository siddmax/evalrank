# EvalRank TypeScript SDK

TypeScript SDK package boundary for public EvalRank APIs.

## Public Surface

- Public constants for trust tiers, freshness statuses, comparability modes, evidence kinds, and `the_call` decisions.
- Public TypeScript interfaces for `CapabilityFingerprint`, `RawEntry`, `TheCall`, `EntityRef`, `EvaluationRequest`, `EvidenceItem`, `RankedEntity`, and `Recommendation`.
- `Recommendation` includes `recommendation_id`, `recommend_id`, and `search_run_id` as public join aliases.
- No service client, auth flow, hosted-product behavior, or private data access.
- The npm package is marked private until a built JS distribution and publish flow exist.

## Check

```sh
npm run check --prefix packages/sdk-ts
```
