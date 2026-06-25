# Public Fixture Bundle Example

Date: 2026-06-26

## Built

- Expanded `examples/public_fixture.py` from recommendation-plus-evidence output to the current synthetic public fixture bundle.
- The example now prints request, candidate set, stage candidate, evidence item, evidence set, result row, use-case catalog, exclusion, and recommendation JSON.
- Updated example tests, `examples/README.md`, root `README.md`, and `docs/STATUS.md`.

## Kept Out

- No live API client, scorer runtime, source adapter, persistence, network call, private fixture, hosted auth, telemetry, or receipt behavior.

## Verification

- Red first: `python3 -m unittest tests.test_examples` failed while the example only printed evidence and recommendation keys.
- Green: `python3 -m unittest tests.test_examples`.
