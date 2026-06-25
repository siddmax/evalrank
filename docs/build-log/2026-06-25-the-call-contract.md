# The Call Contract

Date: 2026-06-25

## Built

- `TheCall` public dataclass in `evalrank_core.contracts`.
- Public `THE_CALL_DECISIONS` constant.
- Recommendation serialization for structured `the_call` payloads.
- Recommendation abstention now uses the same structured `TheCall` contract.
- Recommendation JSON Schema pins `the_call` to `decision`, `confidence`, `reason`, and `abstention_reason`.
- Python SDK re-export and TypeScript `TheCall` interface/decision constants.
- Public recommendation fixture includes a non-null `the_call`.

## Explicitly Not Built

- Scorer thresholds.
- Private confidence tuning.
- Held-out evidence floors.
- Route/OpenAPI behavior.
- New CLI or MCP fixture kinds.
- Database persistence, migrations, or hosted receipt behavior.

## Verification

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
make check
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture recommendation
```
