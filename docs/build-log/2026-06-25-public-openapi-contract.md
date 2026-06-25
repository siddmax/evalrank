# Public OpenAPI Contract

Date: 2026-06-25

## Built

- `schemas/openapi.json` using OpenAPI 3.1.1.
- Public `POST /v1/recommendations` route contract.
- Request body references the existing `EvaluationRequest` schema.
- `200` response references the existing `Recommendation` schema.
- `NAVIGATION.md` route entrypoint map.
- OpenAPI route-contract regression tests.

## Explicitly Not Built

- Live server runtime.
- Hosted auth, tenant routing, or billing/admin behavior.
- Scorer engine or private confidence tuning.
- Database persistence, migrations, or receipt storage.
- HMAC-backed hosted identifiers.
- Error taxonomy beyond the successful public payload contract.

## Verification

```sh
python3 -m unittest tests.test_openapi_contract
make check
npm run check --prefix packages/sdk-ts
```
