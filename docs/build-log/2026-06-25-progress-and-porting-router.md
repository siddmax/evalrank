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

| Workstream | Reason |
| --- | --- |
| Datastore Bootstrap / Runtime Ops | Runtime persistence and hosted operation are maintained in a separate private system that owns datastore bootstrap, migrations, access policies, and live datastore checks. |
| Scoring / Materializer Runtime | Runtime code still depends on private evidence rows, hosted execution, and proprietary tuning until split. |
| Evaluation Integrity | Held-out tasks, graders, answers, traces, and benchmark outputs must not become public. |
| Hosted Ops / GTM | Billing, admin, telemetry, vendor intent, and account operations are hosted-product concerns handled in the separate private system. |
| Secrets / Deploy Ops | Credentials, secret configuration, live project references, signing keys, and deploy files must never enter Git history. |

## Boundary Notes

- Recommendation join aliases are public-safe because they are plain interoperability fields. Hosted signature derivation and receipt storage are not public-safe until route and secret-handling contracts exist.
- Runtime persistence remains private because custom schema API exposure requires deliberate API settings, access grants, and row-level policy design; that is operational ownership, not a portable public contract.
- Repository secret scanning and push protection are useful repo-level backstops, but the local public-boundary check remains mandatory because it catches project-specific private names, paths, and held-out markers before push.

## External Guardrails Checked

- Repository push protection and secret scanning docs.
- Custom schema and API security docs, including explicit schema exposure, access grants, and row-level policy guidance.
