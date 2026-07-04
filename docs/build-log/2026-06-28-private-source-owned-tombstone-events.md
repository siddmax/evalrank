# 2026-06-28 Private Source-Owned Tombstone Events

Private Syndai work added a deterministic `tombstoned` lifecycle event hook to the existing append-only private `evalrank.source_evidence_events` ledger. No private source rows, SQL migrations, credentials, or hosted product code were copied into this public repo.

Validation evidence from the private worktree:

- Red unit test failed before implementation because the shared tombstone builder was missing.
- Snapshot-mismatch regression failed before validation because mismatched source rows were accepted.
- Focused lifecycle tests passed with `8 passed`.
- Private adapter/migration boundary smoke passed with `2 passed`.
- Public `make check` passed with 223 Python tests and 7 TypeScript SDK tests.
- Private `make check` passed.
- `git diff --check` passed in both repos.

Public impact: `docs/STATUS.md` now records that the hook exists privately, while live source retention workers and terminal dogfood source rows remain future private work.
