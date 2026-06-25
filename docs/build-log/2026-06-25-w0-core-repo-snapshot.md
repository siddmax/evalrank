# W0 Core Repository Snapshot

Date: 2026-06-25

Remote: https://github.com/siddmax/evalrank

Initial scope:

- Public Apache-2.0 repository created through the GitHub REST API.
- Public package shape established for `core`, `mcp`, `cli`, `sdk-python`, and `sdk-ts`.
- CI boundary gate added for private imports, Smithery coupling, excluded Min-K% markers, and package license/notice coverage.
- Root README states what is not open.
- Agent guidance added through root and scoped `AGENTS.md` files, with `CLAUDE.md` as a one-line shim to `@AGENTS.md`.
- `TESTS.md` added for the current test map.

Operational placement:

- EvalRank public repo owns public contracts, schemas, SDK/API boundaries, examples, and public method notes.
- Syndai owns the shared Finn/Supabase `evalrank` schema bootstrap during incubation.
- Move DB migrations into EvalRank only after EvalRank owns its deploy/release path or moves to its own Supabase project.

Pending after first CI run:

- Turn the branch/ruleset required status check from snapshot to enforced protection once the `CI / public-boundary` check exists in GitHub.
