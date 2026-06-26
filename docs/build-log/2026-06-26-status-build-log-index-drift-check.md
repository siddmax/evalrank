# Status Build-Log Index Drift Check

Date: 2026-06-26

## What changed

- Repo docs tests now require `docs/STATUS.md` to list every `docs/build-log/*.md` file exactly.
- `docs/STATUS.md` now indexes two older build logs that were present but unlisted.

## Public boundary

This is a docs-only public drift guard. No private plan text, private runbooks, hosted ops, telemetry, credentials, DB work, or runtime code moved.

## Verification

```sh
python3 -m unittest tests.test_repo_docs.RepoDocsTests.test_status_lists_build_logs_exactly
```
