# Fixture Use-Case Alignment

Date: 2026-06-26

## Built

- Aligned synthetic request, candidate-set, stage-candidate, evidence-set, and recommendation fixtures to the public `web-browsing` use-case catalog slug.
- Added a regression that checks the sample request use case exists in `UseCaseCatalog`.
- Updated public implementation-plan examples that referenced the stale non-catalog fixture slug.
- Updated `docs/STATUS.md` and `docs/PORTING.md`.

## Kept Out

- No new public payload contract.
- No scorer runtime, source adapter, live route handler, database migration, private evidence row, held-out fixture, telemetry, hosted auth, or receipt behavior.

## Verification

- Red first: `python3 -m unittest tests.test_core_fixtures.CoreFixtureTests.test_sample_request_use_case_is_in_public_catalog` failed on the stale non-catalog slug.
- Green: `python3 -m unittest tests.test_core_fixtures`.
- Green: `python3 -m unittest tests.test_core_contracts tests.test_sdk_python`.
- Green: repo-wide stale-slug search found no remaining references.
