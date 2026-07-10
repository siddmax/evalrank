# TypeScript SDK Agent Guide

## Scope

- Public TypeScript SDK packaging boundary.
- Keep generated or mirrored types aligned with public schemas and core contracts.

## Rules

- Do not add private service clients or hosted-product assumptions.
- Keep Python/TypeScript identity and receipt behavior byte-identical through the shared golden corpus.
- Keep schema-derived types traceable to `schemas/`.

## Checks

- From repo root: `npm run check --prefix packages/sdk-ts`
- From repo root: `npm run test --prefix packages/sdk-ts`
- From repo root: `python3 scripts/check_public_boundary.py --root .`
