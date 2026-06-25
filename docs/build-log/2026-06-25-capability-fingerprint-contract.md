# Capability Fingerprint Contract

Date: 2026-06-25

## Built

- Added `CapabilityFingerprintInput`, a storage-free public hash-input contract.
- Added deterministic SHA256 digest generation over canonical sorted JSON using stdlib only.
- Added `sample_capability_fingerprint_input()` and exposed it through Python SDK, CLI fixture, MCP fixture, and TypeScript public types.
- Added `schemas/capability-fingerprint.schema.json`.

## Boundary

- No entity graph table, evidence ledger persistence, migration, live lookup, scorer, or private integration was added.
- This is a public join-key contract only.

## Checks

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts
make check
npm run check --prefix packages/sdk-ts
```
