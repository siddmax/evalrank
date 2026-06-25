# EvalRank Tests

## Default Check

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
```

## Test Map

- `tests/test_core_contracts.py` checks public recommendation and ranking contract behavior.
- `tests/test_core_fixtures.py` checks reusable public fixture payloads.
- `tests/test_schema_contracts.py` checks public JSON Schema files against the core payload keys.
- `tests/test_public_boundary.py` checks repository boundary rules and CLI failure output.
- `scripts/check_public_boundary.py` rejects private imports, disallowed coupling, excluded implementation markers, secret files, high-signal secret values, private data paths, and missing package license/notice files.

## Update Rules

- Add or update tests with every non-trivial contract, parser, CLI, MCP, SDK, schema, or boundary change.
- Keep test fixtures public and minimal. Do not copy private Syndai fixtures, held-out eval data, customer data, or telemetry into this repo.
- If UI routes, API routes, or deeplinks come online, add `NAVIGATION.md` with route entrypoints and regression commands.
