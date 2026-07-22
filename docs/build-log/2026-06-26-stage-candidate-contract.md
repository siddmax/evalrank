# Stage Candidate Contract Build Log

Date: 2026-06-26

## Built

- `StageCandidate` public dataclass in `evalrank_core.contracts`.
- `sample_stage_candidate()` public fixture in `evalrank_core.fixtures`.
- Closed draft 2020-12 `schemas/stage-candidate.schema.json`.
- Python SDK re-export and TypeScript `StageCandidate` interface.
- CLI `fixture stage-candidate` and MCP `stage-candidate` fixture support.
- Public docs/status/porting updates that route Stage-1 candidate metadata to public and private workstreams.

## Not Built

- No Stage-2 IRT, theta, trust, or calibrated score rows.
- No Stage-3 LLM tie-break fields.
- No Stage-4 shortlist, conformal, or diversity metadata.
- No source adapters, graph lookup, storage, telemetry, hosted auth, or live scorer behavior.
- No held-out evals, benchmark answers, private traces, production entity rows, or private tuning.

## Port Assessment

- Public Contracts owns `StageCandidate` because it is a portable, storage-free Stage-1 row.
- Methods / Schemas owns the public vocabulary that explains how `CandidateSet` membership can produce `StageCandidate` rows before evidence and scoring stages.
- SDK / CLI / MCP owns deterministic fixture surfaces for `stage-candidate`.
- Scoring and materializer work keeps graph lookup, source adapters, Stage-2+ rows, materializer behavior, scorer thresholds, and private tuning out of the public core. Runtime persistence and hosted operation are maintained in a separate private system.
- Persistence bootstrap keeps migrations, access-control policies, and data-layer verification out of the public core until EvalRank owns persistence or a dedicated deploy path. Runtime persistence and hosted operation are maintained in a separate private system.
- Evaluation integrity keeps held-out candidate cases, graders, traces, and benchmark outputs private.

## Verification

- `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures`
- `python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture`
- `make check`
- `PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture stage-candidate`
- Public secret scan over docs, packages, schemas, tests, scripts, and CI paths.
- `git diff --check`
- Pre-landing review.
- Over-engineering review.
