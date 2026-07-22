# EvalRank Agent Guide

## Scope

- This is the public Apache-2.0 EvalRank core repository.
- Keep the public core product-neutral: contracts, schemas, SDKs, CLI, MCP boundary, examples, and public method notes.
- Do not add private runtime, customer, held-out benchmark, production telemetry, or hosted-product-only code here.
- Use the nearest scoped `AGENTS.md` for local rules.

## Architecture Boundary

- The EvalRank public repo owns public APIs and portable evaluation contracts only.
- Runtime persistence — databases, schemas, migrations, roles, grants, access policies, deploy wiring, and any live-datastore detail — lives in the private runtime and is never described here.
- The public repo must never name a private datastore, schema, table, column, role, migration identifier, deploy target, or infrastructure provider. Public docs describe portable contracts and public method notes, not how any private system is built or operated.
- Public EvalRank work lands on this repo's `main`. Private runtime work stays entirely in its own private repository; do not record private SHAs, migration IDs, or runtime-proof results in this public repo.
- If EvalRank later owns its own persistence, describe only the public, product-neutral contract surface here and keep operational detail private.

## Commands

- Boundary check: `python3 scripts/check_public_boundary.py --root .`
- Tests: `python3 -m unittest discover tests`
- Full local check: `make check`

See `TESTS.md` for the current test map.

## Rules

- Preserve the public boundary: no private imports, no secrets, no private fixtures, no hosted-only behavior.
- Keep package READMEs, `NOTICE`, and `LICENSE` current when package contents change.
- Prefer stdlib and small contracts over new dependencies.
- Add tests for non-trivial contract logic, boundary rules, parsers, CLI behavior, and security-sensitive code.
- Push directly to `main` only with explicit owner instruction in the current task; first run a pre-landing review with the available gstack or superpower review skill, then run the default checks.
- Keep `CLAUDE.md` as a one-line shim to `@AGENTS.md`.
- Add `NAVIGATION.md` only when EvalRank has UI routes, API routes, deeplinks, or navigation-critical docs to maintain.

## Evolution

- Root docs are cross-repo guidance only. Put package-specific rules in the nearest package `AGENTS.md`.
- When a new top-level code area is added, add a scoped `AGENTS.md` if agents need different commands, boundaries, or ownership rules there.
- When build progress changes, update `docs/STATUS.md`; when directory ownership changes, update `docs/REPO_STRUCTURE.md`.
- When porting a contract in from private systems, port only the public, product-neutral surface, run the public boundary check before committing, and do not reference private runtime internals (datastores, schemas, migrations, roles, or private SHAs) in any public doc or commit message.
- Land public work on this repo's `main`; keep private runtime work in its own private repository. Do not preserve stale branches or worktrees for continuity, and delete temporary worktrees after verification.
- When tests or navigable surfaces change, update `TESTS.md` or create/update `NAVIGATION.md` in the same change.
