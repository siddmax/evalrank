# Raw Entry Contract

Date: 2026-06-25

## Built

- `RawEntry` public dataclass in `evalrank_core.contracts`.
- Deterministic `content_hash` generated from normalized content identity fields with stdlib SHA256; fetch time is serialized but does not change the content hash.
- Synthetic `sample_raw_entry()` fixture.
- Closed draft 2020-12 `schemas/raw-entry.schema.json`.
- Python SDK re-export, TypeScript `RawEntry` interface, CLI `fixture raw-entry`, and MCP `raw-entry` fixture support.

## Explicitly Not Built

- Source adapters.
- Live fetch behavior.
- Production metadata ingestion.
- Database persistence, migrations, or evidence-ledger writes.
- Private evidence rows, customer examples, telemetry, hosted auth, receipt routes, or HMAC-backed hosted identifiers.

## Verification

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
python3 -m unittest tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts
make check
npm run check --prefix packages/sdk-ts
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture raw-entry
```
