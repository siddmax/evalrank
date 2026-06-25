# EvalRank Navigation

## Public API Routes

| Route | Source | Status |
| --- | --- | --- |
| `GET /v1/use-cases` | `schemas/openapi.json` | Public contract only; returns `UseCaseCatalog` on `200` and reusable RFC 9457 Problem Details responses for `429` and `503`; no live server is declared here. |
| `POST /v1/recommendations` | `schemas/openapi.json` | Public contract only; returns `Recommendation` on `200` and reusable RFC 9457 Problem Details responses for `400`, `422`, `429`, `503`, and `504`; no live server is declared here. |

## Update Rules

- Update this file when public API routes, UI routes, deeplinks, or navigation-critical docs change.
- Keep hosted auth, tenant logic, private receipt IDs, persistence, and deploy details out of this file unless they become public contracts.
- Run `python3 -m unittest tests.test_openapi_contract` after route-contract changes.
