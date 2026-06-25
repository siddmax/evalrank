# Evaluation Request Contract

Date: 2026-06-25

## Built

- Added `EvaluationRequest`, a storage-free public input payload for request normalization.
- Added `schemas/evaluation-request.schema.json`.
- Added `sample_evaluation_request()` and exposed it through Python SDK, CLI fixture, MCP fixture, and TypeScript public types.
- Updated core, schema, SDK, CLI, MCP, test, status, and porting docs.

## Boundary

- No REST route, database migration, auth flow, scorer, live evidence lookup, or private integration was added.
- The payload is synthetic-fixture compatible and public by construction.

## Porting Review

- This slice belongs in the Public Contracts workstream and fans out only to public schema, SDK, CLI, MCP, tests, and docs.
- Related private work stays private: Supabase bootstrap/migrations, live evidence graph operations, telemetry, billing/admin/GTM, credentials, customer data, and held-out evaluation material.
- Next public ports should remain contract-first: add only storage-free payloads or public route contracts before adding non-fixture SDK/CLI/MCP behavior.

## Checks

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts
python3 -m unittest tests.test_sdk_python tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```
