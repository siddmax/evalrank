# Core Package Agent Guide

## Scope

- Public Python reference contracts live here.
- This package should stay dependency-light and portable.

## Rules

- Contract changes must be deterministic, serializable, and covered by the nearest core, decision, read, schema, and cross-language golden tests.
- Content-addressed identities use the shared restricted-JCS helpers; do not introduce a second hash canonicalizer.
- Keep private ranking experiments, held-out fixtures, telemetry scoring, and hosted-only behavior out of this package.
- Prefer dataclasses and stdlib unless a real public API need justifies more.

## Checks

- From repo root: `python3 -m unittest tests.test_core_contracts tests.test_canonical_json tests.test_decision_contracts tests.test_read_contracts`
- From repo root: `python3 scripts/check_public_boundary.py --root .`
