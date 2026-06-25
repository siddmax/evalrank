# Scoring Stages Route Contract

Date: 2026-06-26

## What Changed

- Added `GET /v1/scoring-stages` to `schemas/openapi.json`.
- Added `ScoringStageCatalog` to OpenAPI schema components.
- Updated `NAVIGATION.md`, `README.md`, `schemas/README.md`, `docs/STATUS.md`, `docs/PORTING.md`, and `TESTS.md`.
- Kept this public-safe: this is a route contract only, not a live server. No auth, tenant logic, storage, rate-limit enforcement, scorer runtime, hosted deployment behavior, private DTO, or private problem type moved here.

## Verification

- Red: `python3 -m unittest tests.test_openapi_contract` failed on missing `/v1/scoring-stages` and missing `ScoringStageCatalog` component.
- Green: `python3 -m unittest tests.test_openapi_contract` passed after the OpenAPI update.
- Full local gate: `make check` passed with the public boundary scan and 142 unit tests.
- Review: gstack checklist review found no actionable issues; Greptile triage was skipped because this direct-main workflow has no PR; `bun run slop:diff origin/main` was unavailable because this repo has no `slop:diff` script.
