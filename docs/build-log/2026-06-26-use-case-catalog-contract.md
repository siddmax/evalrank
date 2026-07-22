# Use Case Catalog Contract

Date: 2026-06-26

## Built

- Added `UseCase` and `UseCaseCatalog` to the public Python core.
- Added the deterministic `sample_use_case_catalog()` fixture with 21 ranked use cases plus the safety overlay.
- Added `schemas/use-case-catalog.schema.json`.
- Added `GET /v1/use-cases` to `schemas/openapi.json` as a contract-only route.
- Added `fixture use-cases` to the CLI and MCP fixture adapter.
- Re-exported the contract through the Python SDK and mirrored it in the TypeScript SDK.
- Updated README, package READMEs, `NAVIGATION.md`, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Kept Out

- Benchmark weights, IRT fit clusters, confidence policies, thin-coverage rules, and synthesis details.
- Runtime persistence, migrations, live route handlers, hosted auth, telemetry, and deployment wiring.
- Held-out tasks, graders, answers, traces, and private benchmark outputs.

## Port-Over Decision

| Source material | Public action | Owning workstream |
| --- | --- | --- |
| Public use-case names, definitions, entity-kind spans, and safety-overlay policy | Ported into this repo as storage-free contracts, fixture output, schema, SDK/CLI/MCP parity, and a contract-only OpenAPI route. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP |
| Use-case weights, IRT crosswalks, confidence policy, synthesis and thin-coverage rules | Keep private until they can be rewritten as method notes without proprietary thresholds, held-out data, or private benchmark output. | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |
| Live persistence, migrations, route handlers, auth, telemetry, deploy config, and hosted receipts | Keep private during incubation; move only after a deliberate persistence/deploy ownership cutover. Runtime persistence and hosted operation are maintained in a separate private system. | Runtime Persistence, Hosted Operations, Deploy Operations |

## Verification

- Red first: focused tests failed on the missing use-case catalog surfaces.
- Pre-landing review fixed one schema parity gap: the JSON Schema now requires overlay rows to use `veto_overlay` and non-overlay rows to use `ranked`, matching the Python core validator.
- Green: `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts tests.test_openapi_contract`
- Green: `npm run check --prefix packages/sdk-ts`
- Green: `make check`
- Pushed directly to `main` and verified the matching GitHub Actions `CI` run.
