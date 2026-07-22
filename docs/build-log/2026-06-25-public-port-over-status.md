# Public Port-Over Status

Date: 2026-06-25

Scope: public EvalRank repo at https://github.com/siddmax/evalrank

## Done In This Public Repo

- Public Apache-2.0 repo scaffold, root/scoped agent guidance, and `CLAUDE.md` shim.
- Public package boundaries for core, Python SDK, TypeScript SDK, CLI, MCP, schemas, methods, examples, tests, and scripts.
- Deterministic public-boundary check for private imports, disallowed coupling, secret files, high-signal secret values, private data paths, excluded method markers, and package license/notice hygiene.
- Storage-free public contracts: capability fingerprint, methodology version, evaluation request, ranked entity, recommendation, recommendation ID aliases, entity reference, and evidence item.
- JSON Schemas and drift tests for the current public contracts.
- Synthetic fixtures, runnable public example, CLI fixture command, MCP fixture adapter, Python SDK re-exports, and TypeScript public types/constants.
- Public scoring-stage vocabulary and method-boundary note.
- Living docs: status tracker, repo structure map, porting map, package READMEs, tests map, public implementation plans, and dated build logs.

## Port Next

| Candidate | Public condition | Workstream |
| --- | --- | --- |
| `RawEntry` ingestion-normalization contract | Keep it storage-free, deterministic, JSON-compatible, and backed only by synthetic fixtures. | Public Contracts |
| Additional JSON Schemas for pinned public payloads | Add only after the Python contract shape exists and schema drift tests cover it. | Public Contracts, Methods / Schemas |
| SDK/CLI/MCP behavior beyond fixtures | Add one pinned public contract at a time, with no live private service dependency. | SDK / CLI / MCP |
| OpenAPI skeleton | Wait until the first concrete public REST route contract exists. | Public Surface Contracts |
| `NAVIGATION.md` | Wait until UI routes, API routes, deeplinks, or navigation-critical docs exist. | Public Surface Contracts, Docs / Public Planning |

## Keep Private

| Area | Why it stays out | Workstream |
| --- | --- | --- |
| Datastore bootstrap, migrations, access policies, and shared operational database setup | Runtime persistence and hosted operation are maintained in a separate private system. | Persistence / Ops |
| Entity graph persistence, evidence-ledger runtime, scorer, and materializer | These still depend on private data, private runtime components, or proprietary tuning until split. | Scoring / Materializer Runtime |
| Hosted receipt routes, cryptographic ID derivation, auth, billing/admin/GTM, telemetry, deploy wiring, and credentials | These are hosted-product or secret-handling concerns maintained in a separate private system. | Hosted Ops / GTM, Secrets / Deploy Ops |
| Held-out suites, graders, answer keys, traces, private benchmark outputs, and judge-calibration material | Publishing these would compromise evaluation integrity. | Evaluation Integrity |

## Public-Safety Notes

- Do not copy raw private planning docs into this repo. Summarize decisions in public-safe language.
- Do not port private fixtures, production evidence rows, customer examples, live project identifiers, or runbooks.
- Hosted platform secret scanning and push protection are useful backstops, but local boundary checks remain mandatory because they catch EvalRank-specific private names, paths, and held-out markers before push.
- Custom-schema/API exposure remains private until EvalRank has an explicit persistence ownership plan and public route contract.
