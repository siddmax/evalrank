# TypeScript SDK Agent Guide

## Scope

- Public TypeScript SDK packaging boundary.
- Keep generated or mirrored types aligned with public schemas and core contracts.

## Rules

- Do not add private service clients or hosted-product assumptions.
- Add a package-level test command before adding non-trivial TypeScript implementation.
- Keep schema-derived types traceable to `schemas/`.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
