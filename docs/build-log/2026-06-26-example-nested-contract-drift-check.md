# Example Nested Contract Drift Check

Date: 2026-06-26

## What Changed

- Added a regression that verifies `examples/README.md` names nested public fixture refs for `recommendation.abstention`, `recommendation.the_call`, and `scoring_stages.stages[].output_contracts`.
- Updated the example README so public users can see the nested recommendation and scoring-stage contracts that matter beyond top-level fixture keys.
- Updated `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md` with the new docs/example drift guard.

## Public Boundary

- Public: deterministic synthetic fixture output and README drift checks.
- Private: live scorer behavior, hosted recommendations, private thresholds, private fixtures, and held-out evaluation material.

## Verification Intent

- `python3 -m unittest tests.test_examples`
- `make check`
