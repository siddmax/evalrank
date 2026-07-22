# Candidate Set Contract

Date: 2026-06-25

## Built

- `CandidateSet` public dataclass in `evalrank_core.contracts`.
- Deterministic `sample_candidate_set()` fixture over a public `EntityRef` candidate.
- Closed draft 2020-12 `schemas/candidate-set.schema.json` requiring at least one unique candidate.
- Python SDK re-export and TypeScript `CandidateSet` interface.
- CLI `fixture candidate-set` and MCP `candidate-set` fixture support.
- Public scoring-stage note now names `CandidateSet` for candidate resolution.

## Explicitly Not Built

- Source adapters.
- Live candidate resolution.
- Entity graph lookup.
- Production entity rows or evidence rows.
- Database persistence, migrations, or evidence-ledger writes.
- Scorer runtime, proprietary thresholds, hosted auth, telemetry, receipt routes, or HMAC-backed identifiers.

## Port-Over Assessment

- Public Contracts owns `CandidateSet` because it is a portable, storage-free payload between request normalization and scoring.
- Methods / Schemas owns the public vocabulary that candidate resolution emits a `CandidateSet`.
- Live candidate resolution and graph lookup stay private until separable from production data and proprietary tuning. Runtime persistence and hosted operation are maintained in a separate private system.
- Candidate persistence and the entity-graph tables stay private until EvalRank owns persistence. Runtime persistence and hosted operation are maintained in a separate private system.

## Verification

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures
python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts
python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture
npm run check --prefix packages/sdk-ts
make check
```
