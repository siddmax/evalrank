# Receipt-First Public Contract

Date: 2026-07-10

EvalRank's portable surface now has one seven-path launch contract: taxonomy, grouped leaderboard/entity/compare reads, benchmark health, deterministic decision creation, and explicitly shared receipt retrieval.

The Python and TypeScript SDKs validate semantic reads and content-addressed decision receipts. CLI and MCP adapters expose decide, health, and receipt operations without compatibility aliases. Recommendation/scoring-stage routes, client methods, commands, tools, fixture kinds, transitional cell aliases, and their route-only Problem Details codes are retired. Their superseded request, candidate-set, stage-candidate, request-scoped evidence, generic ranked-entity/group, recommendation envelope/catalog contracts, schemas, reference materializer, and method note are deleted rather than retained as a second public authority. Independent discovery records and native observation/provenance contracts remain because they do not encode the retired pipeline.

The stdlib reference server exercises the contract without persistence or private services. It validates `DecisionQueryV1`, returns canonical bytes for the shared golden `DecisionReceiptV1`, retains a receipt only for explicit `?share=true`, and serves schema-valid synthetic reads. Tests prove non-shared receipts are not retrievable, shared receipt bytes are stable, malformed transport fails closed, and deleted routes return `404`.

Manifest `2026-07-10.1` adds a closed nullable `metric_direction` to feed admission. Replayed BFCL V4, LiveCodeBench, LiveBench reasoning, and Terminal-Bench 2.1 feeds declare `higher`; discovery feeds remain null, and the schema rejects an implemented feed without an explicit higher/lower direction.

Verification:

```sh
python3 -m unittest tests.test_openapi_contract tests.test_reference_server_e2e tests.test_sdk_python tests.test_cli_fixture tests.test_mcp_fixture
npm run test --prefix packages/sdk-ts
make check
```
