# Result Row Contract

Date: 2026-06-26

## Built

- Added `ResultRow` as the public storage-free ingested result-row envelope.
- Added public constants for result entity kinds, verification states, and flag keys.
- Added `schemas/result-row.schema.json`.
- Added `sample_result_row()` and exposed it through Python SDK, TypeScript SDK, CLI fixture output, and MCP fixture output.
- Hardened `ResultRow` validation so required string fields and flag objects reject non-schema-compatible values before serialization.
- Updated status, porting, schema, package, root, and test docs.

## Public Boundary

- This contract carries benchmark, harness, raw-score unit, provenance, public flags, and verification state.
- Source adapters, production result rows, private benchmark material, scorer fitting, evidence-ledger persistence, and storage tables stay private.
- No database migration, live service client, hosted route, auth flow, or runtime scoring behavior was added.

## Verification

- Red check before implementation: `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts` failed on missing `ResultRow`, `result-row.schema.json`, fixture kind, and SDK exports.
- Review-hardening red check: `python3 -m unittest tests.test_core_contracts.CoreContractTests.test_result_row_rejects_invalid_public_shape` failed until non-string `source_url` and non-object `flags` were rejected.
- Focused check after implementation: `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts`.
- TypeScript check: `npm run check --prefix packages/sdk-ts`.
- Public boundary check: `python3 scripts/check_public_boundary.py --root .`.
- Full local gate: `make check`.
