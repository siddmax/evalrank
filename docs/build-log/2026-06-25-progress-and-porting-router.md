# Progress And Porting Router Update

Date: 2026-06-25

Scope: public EvalRank repo at https://github.com/siddmax/evalrank

## Done

- Refreshed the living status tracker after the capability fingerprint, evaluation request, methodology version, SDK, CLI, MCP, and fixture slices landed.
- Added an explicit workstream router to `docs/PORTING.md` so private-side EvalRank artifacts have a clear destination before any port starts.
- Updated the repo structure map to make porting ownership and build-log updates part of the directory contract.
- Reconfirmed that the public repo remains storage-free during incubation.

## Public Workstreams To Continue Here

| Workstream | Next public-safe moves |
| --- | --- |
| Public Contracts | Add storage-free payloads, schema drift tests, synthetic fixtures, and public identifier aliases after each contract is pinned. |
| Public Surface Contracts | Add OpenAPI/route schemas only after a concrete public route exists. |
| SDK / CLI / MCP | Promote fixture-only surfaces to real behavior one pinned public contract at a time. |
| Methods / Schemas | Publish sanitized method notes and public schemas without proprietary weights or held-out material. |
| Open-Core Boundary / CI | Keep strengthening checks for secrets, private imports, held-out data, package hygiene, and contract drift. |
| Docs / Public Planning | Keep status, repo structure, porting map, package READMEs, and build logs aligned with each port. |

## Workstreams That Stay Private For Now

| Workstream | Private owner | Reason |
| --- | --- | --- |
| DB Bootstrap / Syndai Ops | Syndai repo | Shared Finn/Supabase incubation still owns schema bootstrap, migrations, grants, RLS, and live DB checks. |
| Scoring / Materializer Runtime | Private incubation first | Runtime code still depends on private evidence rows, hosted workers, and proprietary tuning until split. |
| Evaluation Integrity | Private eval systems | Held-out tasks, graders, answers, traces, and benchmark outputs must not become public. |
| Hosted Ops / GTM | Private hosted systems | Billing, admin, telemetry, vendor intent, and account operations are hosted-product concerns. |
| Secrets / Deploy Ops | Private ops only | Credentials, Doppler config, live project refs, HMAC keys, and deploy files must never enter Git history. |

## Boundary Notes

- Recommendation join aliases are public-safe because they are plain interoperability fields. Hosted HMAC derivation and receipt storage are not public-safe until route and secret-handling contracts exist.
- Supabase persistence remains private because custom schema API exposure requires deliberate API settings, grants, and RLS design; that is operational ownership, not a portable public contract.
- GitHub secret scanning and push protection are useful repo-level backstops, but the local public-boundary check remains mandatory because it catches project-specific private names, paths, and held-out markers before push.

## External Guardrails Checked

- GitHub push protection and secret scanning docs.
- Supabase custom schema and API security docs, including explicit schema exposure, grants, and RLS guidance.
