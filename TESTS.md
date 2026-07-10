# EvalRank Tests

## Default Check

```sh
make check
```

## Test Map

- `tests/test_core_contracts.py` checks public capability fingerprint, raw entry, request, unique request entity types, candidate set, stage candidate, result row, result row HTTP(S) source URL validation, use-case catalog, scoring stage catalog ordinal contiguity, ranking group, evidence set, exclusion, `the_call`, abstention, Problem Details with public HTTP(S) doc URLs, recommendation ID aliases, recommendation envelope validation, recommendation rank contiguity/order, recommendation group/exclusion uniqueness, recommendation `shortlist_depth` count consistency, abstention envelope consistency, abstention-as-empty-single-scale behavior, ranking, public vocabulary exports, public string-field validation, primitive/sequence field validation, freshness date and timestamp format validation, candidate/evidence set tuple backing, score-component map validation, evidence metadata, request constraints, calendar-valid methodology-version contract behavior, and core README drift.
- `tests/test_core_materializer.py` checks the public reference materializer emits deterministic `materialized-cache` recommendations from storage-free public inputs, preserves Stage-1 ordering with stable tie-breaks, carries methodology/evidence/result metadata, returns public abstentions when evidence is empty, and rejects inputs outside the request/candidate/evidence/result boundary.
- `tests/test_catalog_manifest.py` checks the canonical 26-cell taxonomy, exact 77-family/79-feed inventory, aliases, unique cell/ranking-group/family/feed IDs, preview/discovery/quarantine truth, coherent identity triples, resolved explorer ceilings, exact research-job mappings, multi-feed correlation, fail-closed admission states, independently counted active-family gates, cross-record links, rights/retention completeness, closed schema surface, and exact core-fixture projection.
- `tests/test_catalog_research_provenance.py` validates the closed Draft 2020-12 research-provenance companion with Ajv and checks exact manifest-version/family coverage, dated primary or official HTTPS sources, direct-versus-inference claim categorization, claim-source joins, and one exact linked claim for every manifest research flag.
- `tests/test_core_fixtures.py` checks reusable public fixture dispatch plus capability fingerprint, raw entry, request, candidate set, stage candidate, exact manifest-aligned 26-cell use-case catalog, scoring-stage catalog, ranking group, evidence set, exclusion, Problem Details, recommendation with `the_call` and abstention fields, and evidence fixture payloads.
- `tests/test_examples.py` checks the runnable public fixture example output and verifies `examples/README.md` lists every emitted JSON key plus nested recommendation, Problem Details, and scoring-stage contract refs.
- `tests/test_cli_fixture.py` checks deterministic public CLI fixture output, exact README fixture and route command coverage, invalid input handling, explicit HTTP(S)-only metadata commands for `GET /v1/use-cases` and `GET /v1/scoring-stages`, and the `recommend` command for public API success, route path, stdin input, malformed/non-object request JSON, and Problem Details errors.
- `tests/test_mcp_fixture.py` checks the public MCP fixture tool manifest, exact README fixture-kind and tool coverage, result shape, explicit HTTP(S)-only route-tool `base_url` schemas, the recommendation tool `EvaluationRequest` input schema, metadata tools for `GET /v1/use-cases` and `GET /v1/scoring-stages`, and recommendation tool behavior with Problem Details errors.
- `tests/test_package_metadata.py` checks public Python package `pyproject.toml` names, versions, licenses, Python floor, dependencies, CLI entrypoint, TypeScript package metadata, and exact package README metadata drift.
- `tests/test_schema_contracts.py` checks public JSON Schema files against the core payload keys, raw-entry, generated hash patterns, evaluation-request entity-type uniqueness, candidate-set, stage-candidate, result-row, result-row HTTP(S) source URL shape, use-case catalog, scoring-stage catalog uniqueness, recommendation ranked-row/group/exclusion uniqueness, ranking-group uniqueness, evidence-set, exclusion, abstention shape and envelope consistency, abstention-as-empty-single-scale shape, score-component map, confidence interval tuple shape, ranked-entity axes, freshness-date, and timestamp shapes, RFC 9457 Problem Details plus public retry-extension enum/doc-url parity, structured `the_call`, exact recommendation alias patterns, pinned public patterns, and exact schema README drift.
- `tests/test_openapi_contract.py` checks the public OpenAPI route contracts, reusable Problem Details responses, retry/rate-limit headers, schema refs, and storage-free boundary.
- `tests/test_methods_docs.py` checks exact method README note coverage and verifies public method notes stay aligned with the use-case taxonomy, native-metric evidence synthesis, staged eligibility, and scoring-stage contracts.
- `tests/test_repo_docs.py` checks `CLAUDE.md` stays a one-line `@AGENTS.md` shim, scoped `AGENTS.md` files cover public work areas, `docs/REPO_STRUCTURE.md` tracks the public top-level directories and package directories exactly, `docs/STATUS.md` points to the canonical public authorities without private runtime traces, `docs/STATUS.md` mentions every current porting workstream from `docs/PORTING.md`, and public MCP docs do not advertise private evidence lookup.
- `tests/test_sdk_python.py` checks the Python SDK re-exports public core contracts, vocabulary constants, public fixture dispatch helpers, and the stdlib `EvalRankClient` behavior for HTTP(S)-only `GET /v1/use-cases`, `GET /v1/scoring-stages`, and `POST /v1/recommendations` success plus Problem Details errors, including strict numeric `Retry-After` parsing.
- `tests/test_sdk_ts.py` checks TypeScript SDK package metadata and mirrored public constants/interfaces, including public fixture kinds, Problem Details codes, abstention, `UseCase`, `the_call`, recommendation branch typing, `RecommendationCallState` abstention parity, abstention/the-call state typing, abstention-as-empty-single-scale typing, non-empty array helper typing, metadata-route client exports, recommendation client exports, and types.
- `tests/test_public_boundary.py` checks repository boundary rules and CLI failure output.
- `scripts/check_public_boundary.py` rejects private imports, disallowed coupling, excluded implementation markers, secret files, high-signal secret values, private data paths, and missing package license/notice files.

## Package Checks

- TypeScript SDK syntax check: `npm run check --prefix packages/sdk-ts`
- Locked TypeScript test install: `npm ci --prefix packages/sdk-ts` installs the exact dev dependency graph from `packages/sdk-ts/package-lock.json` without changing the lock.
- TypeScript SDK runtime test: `npm run test --prefix packages/sdk-ts` uses Ajv 2020 to validate the canonical manifest against its real Draft 2020-12 schema, mutation-tests identity and admission state machines, checks exact taxonomy projection, public route behavior, and strict numeric `Retry-After` parsing.
- Public fixture example smoke check: `python3 examples/public_fixture.py`

## Update Rules

- Add or update tests with every non-trivial contract, parser, CLI, MCP, SDK, schema, or boundary change.
- Keep test fixtures public and minimal. Do not copy private Syndai fixtures, held-out eval data, customer data, or telemetry into this repo.
- If UI routes, API routes, or deeplinks come online, add `NAVIGATION.md` with route entrypoints and regression commands.
