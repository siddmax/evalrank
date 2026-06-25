# Python SDK Agent Guide

## Scope

- Public Python SDK packaging boundary.
- SDK code should wrap public EvalRank APIs and contracts.

## Rules

- Do not duplicate core contract logic here; import or expose `packages/core` behavior once packaging is wired.
- Keep examples and fixtures public.
- Add tests for serialization, client behavior, and error contracts when SDK code is added.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
