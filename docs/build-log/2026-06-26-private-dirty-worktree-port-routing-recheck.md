# Private Dirty-Worktree Port-Routing Recheck

Date: 2026-06-26

## What changed

- Rechecked the private Syndai dirty worktree by path category and count only.
- Updated `docs/STATUS.md` and `docs/PORTING.md` so the public repo routes current private-side work without copying private file contents.

## Current public-safe routing

| Private-side category | Count | Public handling |
| --- | ---: | --- |
| Repo guidance, preflight, and test-map docs | 5 | Keep private unless a public-safe EvalRank repo check is extracted. |
| Backend runtime reliability, orchestration, and tools | 26 | Keep in Syndai runtime workstreams. |
| Private backend regression tests | 31 | Keep with private runtime work unless a public invariant is extracted. |
| Private DB migration/bootstrap | 1 | Keep in DB Bootstrap / Syndai Ops. |
| Coding runtime/governance docs | 3 | Keep private unless a product-neutral public contract is extracted. |
| Private plans and architecture notes | 5 | Use only as private inputs for sanitized summaries. |
| Memphant memory-system planning | 19 | Route to the memory-system workstream, not EvalRank by default. |
| Mobile/web auth or connection UI | 5 | Keep in hosted/private app workstreams unless a public UI/API contract exists. |

## Public boundary

This is a category-only public routing update. No private file contents, raw plans, live migration scripts, private worktree diffs, customer data, secrets, telemetry, credentials, hosted operations, or runtime code moved.

## Verification

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest tests.test_repo_docs.RepoDocsTests.test_status_lists_build_logs_exactly
```
