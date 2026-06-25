# W0 Public Exit Packet

Date: 2026-06-25

Remote: https://github.com/siddmax/evalrank

Public baseline entering this packet:

- Apache-2.0 public repo with package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md`, with `CLAUDE.md` as `@AGENTS.md`.
- Public progress docs: `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, and `docs/PORTING.md`.
- Core Python recommendation contracts in `packages/core`.
- Public JSON Schemas in `schemas/`.
- Public fixture factory at `evalrank_core.fixtures`.
- Public boundary checker for private imports, disallowed coupling, excluded methods, secret files, high-signal secret values, private data paths, and package license/notice coverage.
- Schema drift tests for payload keys and public enum constants.
- `make check` as the default local and CI gate.

Private by design:

- Finn/Supabase `evalrank` schema bootstrap and migration runner stay in Syndai during incubation.
- Secrets, Doppler config, live DB operations, production evidence rows, telemetry, customer traces, and held-out benchmark materials stay outside this repo.
- Hosted billing, admin, GTM, vendor intent, and account-operation workflows stay private unless later sanitized as public docs.

W1 entry rule:

- Start public implementation only from pinned contracts or a concrete route/API contract.
- Do not add persistence migrations here until EvalRank owns its own deploy path or Supabase project.
- Keep every port from Syndai/private systems routed through `docs/PORTING.md`.
- Run `make check` before every direct `main` push.

Next public work:

- Data-plane contracts and entity/evidence graph interfaces.
- Scorer-stage public method boundaries.
- Public CLI/MCP/SDK implementations once the first concrete public surface is pinned.
- `NAVIGATION.md` only when UI routes, API routes, deeplinks, or navigation-critical docs exist.
