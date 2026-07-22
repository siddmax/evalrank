# Ranking Group Contract

Date: 2026-06-26

## Built

- Added `RankingGroup` to the public Python core.
- Added `Recommendation.kind_grouped()` for storage-free grouped recommendation payloads.
- Added deterministic `sample_ranking_group()` fixture output.
- Closed the `groups` row shape in `schemas/recommendation.schema.json`.
- Added `fixture ranking-group` to CLI and MCP fixture surfaces.
- Re-exported the contract through the Python SDK and mirrored it in the TypeScript SDK.
- Updated README, package READMEs, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Kept Out

- Cross-kind score normalization, scorer math, benchmark weights, thresholds, and IRT details.
- DB tables, migrations, hosted route handlers, telemetry, auth, receipts, and deployment wiring.
- Held-out tasks, graders, answers, traces, private benchmark outputs, and production entity rows.

## Port-Over Decision

| Source material | Public action | Owning workstream |
| --- | --- | --- |
| Public recommendation comparability discriminator and ranking-group row shape | Ported as closed `RankingGroup` rows for within-kind ranking only. | Public Contracts, Methods / Schemas, SDK / CLI / MCP |
| Cross-kind normalization, score calibration, scorer thresholds, and confidence policy | Keep private until publishable as sanitized method notes without proprietary tuning or held-out signal. | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |
| Runtime scorer, entity graph lookup, source adapters, storage, and hosted receipts | Keep private during incubation. | Scoring / Materializer Runtime, Private Runtime Ops, Hosted Ops / Deploy Ops |

## Verification

- Red first: focused tests failed on missing ranking-group contract, fixture, schema, CLI/MCP, and SDK surfaces.
- Green: `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts tests.test_cli_fixture tests.test_mcp_fixture tests.test_sdk_python tests.test_sdk_ts` passed 104 tests.
- Green: `npm run check --prefix packages/sdk-ts`.
- Green: `make check` passed public boundary scan and 117 tests.
- Green: `git diff --check`.
- Review: gstack pre-landing checklist plus Ponytail scope pass found no unresolved issues; no PR existed, so Greptile triage was skipped.
