# EvalRank Agent Guide

## Scope

- This is the public Apache-2.0 EvalRank core repository.
- Keep the public core product-neutral: contracts, schemas, SDKs, CLI, MCP boundary, examples, and public method notes.
- Do not add private Syndai, Finn, Savida, customer, held-out benchmark, production telemetry, or hosted-product-only code here.
- Use the nearest scoped `AGENTS.md` for local rules.

## Architecture Boundary

- EvalRank public repo owns public APIs and portable evaluation contracts.
- Syndai currently owns the shared Finn/Supabase database bootstrap for the private `evalrank` schema.
- During private incubation, Syndai projection scripts may read Syndai-owned source tables as private inputs, but all derived EvalRank rows, caches, catalog rows, grants, RLS policies, and migrations belong in the dedicated private `evalrank` schema.
- Private Syndai customer identity/control-plane objects, including customer API-key scope catalogs used to authenticate EvalRank routes during incubation, remain in Syndai's own schema because they are shared auth infrastructure, not EvalRank persistence.
- Keep DB migrations in Syndai until EvalRank has its own deploy/release path or its own Supabase project.
- If EvalRank later owns persistence, add versioned migrations, update this file, and document the cutover in `README.md` and `docs/build-log/`.

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
- When porting work from Syndai/private systems, update `docs/PORTING.md` and run the public boundary check before committing.
- When scanning private-side work, route adjacent Memphant, AgentsDB, memory, or general agent-system docs to their own workstream unless there is an explicit storage-free EvalRank contract to port here.
- When tests or navigable surfaces change, update `TESTS.md` or create/update `NAVIGATION.md` in the same change.
