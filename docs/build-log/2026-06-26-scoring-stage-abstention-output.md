# Scoring Stage Abstention Output Alignment

Date: 2026-06-26

## What Changed

- Added `Abstention` to the public `ranking-or-abstention` stage output contracts in the synthetic `ScoringStageCatalog` fixture.
- Added a regression so the public fixture cannot drift away from the public abstention response contract again.
- Updated status and porting docs with the public/private boundary.

## Public Boundary

- Public: storage-free stage vocabulary and contract refs.
- Private: evidence-floor thresholds, scorer policy, private reason taxonomy, runtime scorer behavior, persistence, telemetry, and held-out evaluation material.

## Verification

- Red: `python3 -m unittest tests.test_core_fixtures.CoreFixtureTests.test_sample_scoring_stage_catalog_is_public_contract_payload` failed because `Abstention` was missing from `ranking-or-abstention`.
- Green: `python3 -m unittest tests.test_core_fixtures.CoreFixtureTests.test_sample_scoring_stage_catalog_is_public_contract_payload`
- Green: `make check`
