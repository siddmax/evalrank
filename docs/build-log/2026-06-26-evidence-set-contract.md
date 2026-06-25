# Evidence Set Contract Build Log

Date: 2026-06-26

## Built

- `EvidenceSet` public dataclass in `evalrank_core.contracts`.
- `sample_evidence_set()` public fixture in `evalrank_core.fixtures`.
- Closed draft 2020-12 `schemas/evidence-set.schema.json` that references `evidence-item.schema.json`.
- Python SDK re-export and TypeScript `EvidenceSet` interface.
- CLI `fixture evidence-set` and MCP `evidence-set` fixture support.
- Public docs/status/porting updates that route private-side EvalRank planning categories to public/private workstreams.

## Not Built

- No live evidence lookup.
- No evidence ledger persistence.
- No source adapters or graph lookup.
- No scorer runtime, proprietary thresholds, held-out evals, telemetry, or hosted auth behavior.

## Port Assessment

- Public Contracts owns `EvidenceSet` because it is a portable, storage-free payload that groups public `EvidenceItem` rows for a request.
- Methods / Schemas owns the public vocabulary that evidence attachment emits an `EvidenceSet`.
- SDK / CLI / MCP owns deterministic fixture surfaces for `evidence-set`.
- Scoring / Materializer Runtime keeps live evidence lookup, graph behavior, and evidence-ledger runtime private until public-input-only pieces are separable.
- Evaluation Integrity keeps held-out evidence, graders, answers, traces, and benchmark outputs private.

## Verification

- `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures`
- `python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture`
- `make check`
- `PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture evidence-set`
- Public secret scan over docs, packages, schemas, tests, scripts, and CI paths.
- `git diff --check`
- GStack pre-landing review logged clean after one mechanical line-wrap auto-fix.
- Ponytail review: lean already; no extra abstractions, dependencies, storage, or runtime layers to cut.
