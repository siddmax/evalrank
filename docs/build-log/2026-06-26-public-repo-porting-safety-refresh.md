# Public Repo Porting Safety Refresh

Date: 2026-06-26

## What changed

- Refreshed the progress tracker with the latest docs-only public-repo safety and porting review.
- Clarified that GitHub secret scanning, push protection, and Dependabot security updates are enabled for `siddmax/evalrank`, but are only backstops.
- Rechecked the private Syndai worktree by path/category. The dirty set is still Memphant specs plus Memphant validation/lifecycle plans, not an EvalRank public-port candidate.
- Updated the public security policy to keep secrets, exploit details, private fixtures, customer data, and held-out material out of public reports.

## Porting decision

The next public EvalRank work should stay in these workstreams:

| Workstream | Public-safe next work |
| --- | --- |
| Public Contracts | More storage-free payload hardening where schema/core drift exists. |
| Open-Core Boundary / CI | Deterministic checks for public README drift, schema drift, and leak prevention. |
| SDK / CLI / MCP | Non-fixture `POST /v1/recommendations` client semantics only after the contract is pinned. |
| Public Surface Contracts | Additional public route or Problem Details contracts only after concrete public semantics exist. |
| Methods / Schemas | Sanitized method notes with weights, thresholds, held-out tasks, traces, and private benchmark outputs removed. |

These workstreams keep ownership outside this public repo for now:

| Workstream | Keep private |
| --- | --- |
| Memphant / memory-system | Current private dirty worktree specs and validation/lifecycle plans. |
| DB Bootstrap / Syndai Ops | Supabase schema bootstrap, migrations, grants/RLS, migration guards, and live DB checks. |
| Scoring / Materializer Runtime | Runtime scorer, source adapters, graph lookup, evidence lookup, workers, and proprietary tuning. |
| Hosted Ops / GTM | Auth, telemetry, billing/admin, vendor intent, deploy config, and live project refs. |
| Evaluation Integrity | Held-out tasks, graders, answers, traces, judge calibration, and private benchmark outputs. |
| Secrets / Deploy Ops | Credentials, Doppler config, environment files, HMAC keys, and live service identifiers. |

## Verification target

Before the next direct `main` push, run:

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
make check
```
