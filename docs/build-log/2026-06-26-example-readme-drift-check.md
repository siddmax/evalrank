# Example README Drift Check

Date: 2026-06-26

## What Changed

- Updated `examples/README.md` and `README.md` so the runnable public fixture example names the raw-entry payload now emitted by `examples/public_fixture.py`.
- Added a deterministic README drift test that runs `examples/public_fixture.py`, parses the JSON output, and verifies every emitted top-level key is documented in `examples/README.md`.
- Refreshed `docs/STATUS.md`, `docs/PORTING.md`, and `TESTS.md` with the latest public fixture and port-routing state.

## Public Boundary

- This is documentation and local test coverage for synthetic public fixtures only.
- No private code, customer data, production telemetry, held-out eval material, hosted auth, persistence, source adapter, scorer runtime, or deploy wiring was added. Runtime persistence and hosted operation are maintained in a separate private system.

## Porting Decision

- README drift guards belong in this public repo because they prevent public contract skew.
- Runtime scorer/materializer code, graph lookup, source adapters, migrations, hosted receipts, auth, and eval-integrity material stay private until a separate public cutover is explicitly designed. Runtime persistence and hosted operation are maintained in a separate private system.

## Verification Intent

- Run `python3 -m unittest tests.test_examples` to prove the README drift guard.
- Run `make check` before pushing.
