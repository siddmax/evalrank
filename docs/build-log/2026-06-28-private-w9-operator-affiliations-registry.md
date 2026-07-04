# Private W9 Operator Affiliations Registry

Private Syndai work on 2026-06-28 added the private operator-affiliations registry required before affiliation and COI disclosure workflows can fail closed.

Public-safe summary:

- Added private table `evalrank.operator_affiliations` for operated, funded, and commercial-data relationships.
- Added a DB-backed completeness check over current Syndai-operated agent candidates.
- Refreshed 5 real private registry rows from current private candidate data; no public storage or public route was added.
- Future dispatchers/CI can use the check to block public-facing content when a Syndai-operated entity lacks an affiliation registry entry.

Verification:

- Private focused helper/migration tests passed with `3 passed`.
- Private ruff and ty checks passed for touched files.
- Private EvalRank migration-boundary and migration-validation checks passed.
- Target private DB migration applied.
- Target readback verified 5 columns, 2 RLS policies, 2 indexes, 5 current Syndai-operated candidate rows covered by registry entries, and `is_complete=True`.
- Combined private W9 focused lane passed with `64 passed`.
- Private repo-root `make check` passed.
- Public `make check` passed with 223 Python tests and 7 TypeScript SDK tests.
- Public boundary check and public/private `git diff --check` passed.

Public repo impact:

- No public API, SDK, CLI, MCP, schema, or storage contract changed.
- This file and `docs/STATUS.md` are documentation-only syncs.
