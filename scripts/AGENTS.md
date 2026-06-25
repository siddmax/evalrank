# Scripts Agent Guide

## Scope

- Repository maintenance scripts live here.
- Scripts should be deterministic and safe to run from a clean checkout.

## Rules

- Keep scripts stdlib-only unless a dependency already exists for the repo.
- Boundary/security scripts need tests in `tests/`.
- Do not make scripts mutate private services or pull private data into this repo.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest tests.test_public_boundary`
