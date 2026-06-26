# EvalRank Tests

## Default Check

```sh
make check
```

## Test Map

- `tests/test_core_contracts.py` checks public capability fingerprint, raw entry, request, unique request entity types, candidate set, stage candidate, result row, use-case catalog, scoring stage catalog, ranking group, evidence set, exclusion, `the_call`, abstention, Problem Details, recommendation ID aliases, recommendation envelope validation, ranking, public vocabulary exports, public string-field validation, primitive/sequence field validation, score-component map validation, evidence metadata, request constraints, methodology-version contract behavior, and core README drift.
- `tests/test_core_fixtures.py` checks reusable public fixture dispatch plus capability fingerprint, raw entry, request, candidate set, stage candidate, result row, use-case catalog, scoring-stage catalog, ranking group, evidence set, exclusion, Problem Details, recommendation with `the_call` and abstention fields, and evidence fixture payloads.
- `tests/test_examples.py` checks the runnable public fixture example output and verifies `examples/README.md` lists every emitted JSON key plus nested recommendation, Problem Details, and scoring-stage contract refs.
- `tests/test_cli_fixture.py` checks deterministic public CLI fixture output, exact README fixture and route command coverage, invalid input handling, explicit HTTP(S)-only metadata commands for `GET /v1/use-cases` and `GET /v1/scoring-stages`, and the `recommend` command for public API success, route path, stdin input, malformed/non-object request JSON, and Problem Details errors.
- `tests/test_mcp_fixture.py` checks the public MCP fixture tool manifest, exact README fixture-kind and tool coverage, result shape, explicit HTTP(S)-only metadata tools for `GET /v1/use-cases` and `GET /v1/scoring-stages`, and recommendation tool behavior with Problem Details errors.
- `tests/test_package_metadata.py` checks public Python package `pyproject.toml` names, versions, licenses, Python floor, dependencies, CLI entrypoint, TypeScript package metadata, and package README metadata drift.
- `tests/test_schema_contracts.py` checks public JSON Schema files against the core payload keys, raw-entry, evaluation-request entity-type uniqueness, candidate-set, stage-candidate, result-row, use-case catalog, scoring-stage catalog, ranking-group, evidence-set, exclusion, abstention, score-component map and ranked-entity axes shapes, RFC 9457 Problem Details plus public retry-extension enum parity, structured `the_call`, recommendation alias patterns, pinned public patterns, and exact schema README drift.
- `tests/test_openapi_contract.py` checks the public OpenAPI route contracts, reusable Problem Details responses, retry/rate-limit headers, schema refs, and storage-free boundary.
- `tests/test_methods_docs.py` checks public method notes stay aligned with the use-case taxonomy and scoring-stage contracts plus private boundaries.
- `tests/test_sdk_python.py` checks the Python SDK re-exports public core contracts, vocabulary constants, public fixture dispatch helpers, and the stdlib `EvalRankClient` behavior for HTTP(S)-only `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` success plus Problem Details errors.
- `tests/test_sdk_ts.py` checks TypeScript SDK package metadata and mirrored public constants/interfaces, including public fixture kinds, Problem Details codes, abstention, `UseCase`, `the_call`, and recommendation branch typing, non-empty array helper typing, metadata-route client exports, recommendation client exports, and types.
- `tests/test_public_boundary.py` checks repository boundary rules and CLI failure output.
- `scripts/check_public_boundary.py` rejects private imports, disallowed coupling, excluded implementation markers, secret files, high-signal secret values, private data paths, and missing package license/notice files.

## Package Checks

- TypeScript SDK syntax check: `npm run check --prefix packages/sdk-ts`
- TypeScript SDK runtime test: `npm run test --prefix packages/sdk-ts`
- Public fixture example smoke check: `python3 examples/public_fixture.py`

## Update Rules

- Add or update tests with every non-trivial contract, parser, CLI, MCP, SDK, schema, or boundary change.
- Keep test fixtures public and minimal. Do not copy private Syndai fixtures, held-out eval data, customer data, or telemetry into this repo.
- If UI routes, API routes, or deeplinks come online, add `NAVIGATION.md` with route entrypoints and regression commands.
