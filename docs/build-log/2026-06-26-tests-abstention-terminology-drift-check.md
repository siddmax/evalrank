# TESTS Abstention Terminology Drift Check

Date: 2026-06-26

## What changed

- `TESTS.md` now uses the implemented `abstention-as-empty-single-scale` contract name.
- Repo docs tests now reject the stale `abstention-as-empty-ranking` phrase in the public test map.

## Public boundary

This is a public docs-only guard. No contract shape, private scorer policy, DB work, hosted operations, telemetry, credentials, or runtime code moved.

## Verification

```sh
python3 -m unittest tests.test_repo_docs.RepoDocsTests.test_tests_map_uses_current_abstention_contract_name
```
