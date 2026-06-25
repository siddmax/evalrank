# Scoring Stage Catalog Contract

Date: 2026-06-26

## What Changed

- Added storage-free public `ScoringStage` and `ScoringStageCatalog` contracts.
- Added deterministic synthetic `scoring-stages` fixtures across core, CLI, MCP, Python SDK, TypeScript SDK, and the runnable public example.
- Added `schemas/scoring-stage-catalog.schema.json`.
- Updated `methods/scoring-stages.md` so the public method note names the catalog and stage IDs.
- Kept this public-safe: no formulas, thresholds, graders, production telemetry, scorer runtime, source adapter, DB migration, hosted auth, private evidence rows, or held-out eval material moved here.

## Port Routing

| Artifact | Decision |
| --- | --- |
| Public stage names, order, contract refs, and boundary notes | Ported here as `ScoringStageCatalog`. |
| Stage formulas, scorer thresholds, confidence policy, graders, production telemetry, and runtime materializer behavior | Keep private in Scoring / Materializer Runtime and Evaluation Integrity workstreams. |

## Verification

- Red: focused public contract suite failed on missing `ScoringStage`, `ScoringStageCatalog`, `scoring-stages` fixture dispatch, schema, SDK type/re-export surfaces, and docs.
- Green: focused public contract suite passed after implementation.
- Full local gate: `make check` passed with the public boundary scan and 141 unit tests.
- Review: gstack checklist review and slop scan found no issues; Greptile triage was skipped because this direct-main workflow has no PR.
