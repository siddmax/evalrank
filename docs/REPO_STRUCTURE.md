# EvalRank Repo Structure

This repo is the public core. Private hosted operations, production evidence data, held-out fixtures, billing/admin internals, and private Syndai integrations stay out.

## Root

- `README.md` explains the project and high-level boundaries.
- `AGENTS.md` is the root agent contract.
- `CLAUDE.md` stays a one-line shim to `@AGENTS.md`.
- `TESTS.md` maps runnable checks.
- `LICENSE`, `NOTICE`, `CONTRIBUTING.md`, and `SECURITY.md` are public-repo hygiene files.

## Code And Packages

- `packages/core/` owns portable Python contracts and shared public behavior.
- `packages/mcp/` owns the public MCP adapter boundary.
- `packages/cli/` owns scriptable command-line workflows.
- `packages/sdk-python/` owns the Python SDK package boundary.
- `packages/sdk-ts/` owns the TypeScript SDK package boundary.

Package directories should keep their own `README.md`, `LICENSE`, `NOTICE`, and scoped `AGENTS.md`.

## Public Contracts

- `schemas/` owns public JSON Schema contracts.
- `methods/` owns public methodology notes and exclusion boundaries.
- `examples/` owns public runnable examples.

Schemas define interoperability payloads, not private storage tables.

## Project Docs

- `docs/STATUS.md` is the living progress tracker.
- `docs/REPO_STRUCTURE.md` is this directory ownership map.
- `docs/build-log/` stores dated progress snapshots.
- `docs/AGENTS.md` gives scoped doc-editing rules.

## Tests And Scripts

- `tests/` owns stdlib `unittest` coverage.
- `scripts/` owns deterministic repo maintenance scripts.
- `.github/workflows/` owns public CI.

## When To Add Files

- Add a scoped `AGENTS.md` when a directory has local ownership rules or commands.
- Add or update `TESTS.md` when checks change.
- Add `NAVIGATION.md` when UI routes, API routes, deeplinks, or navigation-critical docs come online.
- Do not add private data, secrets, private fixtures, or production evidence rows anywhere in this repo.
