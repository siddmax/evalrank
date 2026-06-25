# EvalRank TypeScript SDK

TypeScript SDK package boundary for public EvalRank APIs.

## Public Surface

- Public constants for trust tiers, freshness statuses, comparability modes, and evidence kinds.
- Public TypeScript interfaces for `EntityRef`, `EvidenceItem`, `RankedEntity`, and `Recommendation`.
- No service client, auth flow, hosted-product behavior, or private data access.
- The npm package is marked private until a built JS distribution and publish flow exist.

## Check

```sh
npm run check --prefix packages/sdk-ts
```
