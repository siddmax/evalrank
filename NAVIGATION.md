# EvalRank Navigation

## Public API Routes

| Route | Source | Status |
| --- | --- | --- |
| `POST /v1/recommendations` | `schemas/openapi.json` | Public contract only; no live server is declared here. |

## Update Rules

- Update this file when public API routes, UI routes, deeplinks, or navigation-critical docs change.
- Keep hosted auth, tenant logic, private receipt IDs, persistence, and deploy details out of this file unless they become public contracts.
- Run `python3 -m unittest tests.test_openapi_contract` after route-contract changes.
