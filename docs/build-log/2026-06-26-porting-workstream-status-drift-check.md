# Porting Workstream Status Drift Check

Date: 2026-06-26

## What changed

- Repo docs tests now require `docs/STATUS.md` to mention every current workstream listed in `docs/PORTING.md`.
- `docs/PORTING.md` now records the status build-log index guard and this workstream/status guard as already-public drift checks.

## Public boundary

This is a public docs-only guard. No private plan text, private worktree contents, live DB work, hosted operations, telemetry, credentials, or runtime code moved.

## Verification

```sh
python3 -m unittest tests.test_repo_docs.RepoDocsTests.test_status_mentions_current_porting_workstreams
```
