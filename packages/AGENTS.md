# Packages Agent Guide

## Scope

- Applies to all public package directories under `packages/`.
- Each package must remain independently understandable and keep its own `README.md`, `LICENSE`, and `NOTICE`.

## Rules

- Do not import private code or depend on private services. Runtime persistence and hosted operation are maintained in a separate private system.
- Keep shared behavior in `packages/core`; SDKs and CLI should wrap public APIs, not fork contracts.
- Avoid new dependencies until a package has real implementation that needs them.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
