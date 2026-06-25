# EvalRank Tests

## Default Check

```sh
make check
```

## Test Map

- `tests/test_core_contracts.py` checks public capability fingerprint, request, recommendation, ranking, evidence, and methodology-version contract behavior.
- `tests/test_core_fixtures.py` checks reusable public capability fingerprint, request, recommendation, and evidence fixture payloads.
- `tests/test_examples.py` checks the runnable public fixture example output.
- `tests/test_cli_fixture.py` checks deterministic public CLI fixture output and invalid input handling.
- `tests/test_mcp_fixture.py` checks the public MCP fixture tool manifest and result shape.
- `tests/test_schema_contracts.py` checks public JSON Schema files against the core payload keys and pinned public patterns.
- `tests/test_sdk_python.py` checks the Python SDK re-exports public core contracts.
- `tests/test_sdk_ts.py` checks TypeScript SDK package metadata and mirrored public constants/interfaces.
- `tests/test_public_boundary.py` checks repository boundary rules and CLI failure output.
- `scripts/check_public_boundary.py` rejects private imports, disallowed coupling, excluded implementation markers, secret files, high-signal secret values, private data paths, and missing package license/notice files.

## Package Checks

- TypeScript SDK syntax check: `npm run check --prefix packages/sdk-ts`
- Public fixture example smoke check: `python3 examples/public_fixture.py`

## Update Rules

- Add or update tests with every non-trivial contract, parser, CLI, MCP, SDK, schema, or boundary change.
- Keep test fixtures public and minimal. Do not copy private Syndai fixtures, held-out eval data, customer data, or telemetry into this repo.
- If UI routes, API routes, or deeplinks come online, add `NAVIGATION.md` with route entrypoints and regression commands.
