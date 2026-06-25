# Core Package Agent Guide

## Scope

- Public Python reference contracts live here.
- This package should stay dependency-light and portable.

## Rules

- Contract changes must be deterministic, serializable, and covered by tests in `tests/test_core_contracts.py`.
- Keep private ranking experiments, held-out fixtures, telemetry scoring, and hosted-only behavior out of this package.
- Prefer dataclasses and stdlib unless a real public API need justifies more.

## Checks

- From repo root: `python3 -m unittest tests.test_core_contracts`
- From repo root: `python3 scripts/check_public_boundary.py --root .`
