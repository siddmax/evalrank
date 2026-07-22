# Public Progress And Porting Audit

Date: 2026-06-25

Scope: public EvalRank repo at https://github.com/siddmax/evalrank

## Done In The Public Repo

- Public Apache-2.0 repo scaffold with package boundaries for core, CLI, MCP, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` files, plus `CLAUDE.md` as the required one-line shim to `@AGENTS.md`.
- Living docs for status, repo structure, tests, package boundaries, and public/private porting decisions.
- Public boundary scanner for private imports, disallowed coupling, excluded implementation markers, secret files, high-signal secret values, private data paths, and missing package license/notice files.
- Core public contracts for ranked entities, recommendations, entity references, evidence items, and constants.
- Synthetic public fixtures for recommendation and evidence payloads.
- Public JSON Schemas for ranked entities, recommendations, and evidence items, with drift tests.
- Python SDK package metadata and public core re-exports.
- CLI package metadata and deterministic public fixture command.
- MCP package metadata and deterministic public fixture adapter.
- Public scoring-stage vocabulary and private-boundary note.
- Default local/CI gate through `make check`.

## Port To This Repo Next

| Workstream | Public move | Gate |
| --- | --- | --- |
| Public Contracts | Add the next storage-free payload only after it is pinned by a public contract. | Core tests, schema drift tests, and package docs update. |
| SDK / CLI / MCP | Replace fixture-only behavior with real public behavior one contract at a time. | Concrete contract exists first; deterministic tests cover every command/tool/client surface. |
| Public Surface Contracts | Add OpenAPI only when a first REST route contract exists. | Route schema, route tests, and `NAVIGATION.md` if routes become navigation-critical. |
| Methods / Schemas | Publish reusable method notes after removing private formulas and eval material. | No proprietary thresholds, held-out tasks, graders, answers, traces, or benchmark results. |
| Docs / Public Planning | Keep status, repo structure, porting map, package READMEs, and build logs current. | Public-safe summaries only; no raw private planning text. |

## Keep Out Of The Public Repo

| Workstream | Owner | Reason |
| --- | --- | --- |
| Runtime Persistence / Ops | Separate private system | Runtime persistence and hosted operation are maintained in a separate private system. |
| Secrets / Deploy Ops | Private ops only | Credentials, secret configuration, live project references, and deployment files must never enter Git history. |
| Evaluation Integrity | Private eval systems | Held-out tasks, graders, answers, traces, and benchmark outputs lose value if public. |
| Hosted Ops / GTM | Private hosted systems | Billing, admin, telemetry, vendor intent, and account operations are not open-core artifacts. |
| Private Integrations | Private product repos | App-specific integration code would couple the public core to private products. |

## Current Boundary Decision

EvalRank should stay a separate public repo for portable contracts, schemas, SDKs, CLI/MCP boundaries, examples, public method notes, and deterministic guardrails. Runtime persistence and hosted operation are maintained in a separate private system, which should keep private datastore bootstrap, live datastore operations, hosted product workflows, private eval integrity material, and customer or telemetry data until a public deploy path exists.

If EvalRank later owns persistence, make that a deliberate cutover: add versioned migrations in this repo, update root `AGENTS.md`, `README.md`, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`, and log the ownership change in `docs/build-log/`.
