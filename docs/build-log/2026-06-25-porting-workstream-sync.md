# Public Porting Workstream Sync

Date: 2026-06-25

Scope: public EvalRank repo at https://github.com/siddmax/evalrank

## Done In The Public Repo

- Public Apache-2.0 repository scaffold with package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` files plus `CLAUDE.md` as a shim to `@AGENTS.md`.
- Living docs for status, repo structure, and public/private porting decisions.
- Core recommendation contracts, public fixtures, and JSON Schemas for ranked entities and recommendations.
- Schema drift tests and public boundary tests.
- `make check` local and CI gate.
- W0 public exit packet.
- W1 public entity/evidence contract implementation plan.

## Port To This Repo Next

| Workstream | Public artifact | Notes |
| --- | --- | --- |
| Public Contracts | `EntityRef`, `EvidenceItem`, evidence schema, fixtures, and drift tests | Keep storage-free and synthetic. |
| Methods / Schemas | Public scoring-stage vocabulary and method-boundary notes | Remove proprietary thresholds, held-out eval details, and private ranking experiments. |
| SDK / CLI / MCP | Minimal public surfaces that consume pinned contracts | Wait until contracts are stable enough to avoid churn. |
| Docs / Public Planning | Sanitized build logs, status, repo structure, and porting map updates | Summarize private planning; do not paste raw private docs. |

## Keep Private For Now

| Workstream | Private owner | Reason |
| --- | --- | --- |
| DB Bootstrap / Runtime Ops | Separate private system | Runtime persistence and hosted operation are maintained in a separate private system, including its deploy path and datastore guardrails. |
| Evaluation Integrity | Private eval systems | Held-out tasks, graders, answers, traces, and benchmark results lose value if public. |
| Hosted Ops / GTM | Private hosted systems | Billing, admin, telemetry, vendor intent, and account operations are hosted-product concerns. |
| Secrets / Deploy Ops | Private ops only | Credentials, live project refs, secret-management config, and environment files must never enter this repo. |

## Public Repo Safety Notes

- Treat every committed byte as public indefinitely.
- Use synthetic examples for docs, fixtures, tests, and demos.
- Do not include customer data, production evidence rows, production telemetry, held-out eval material, live project identifiers, or private integration code.
- If sensitive data reaches Git history, rotate affected credentials and coordinate history cleanup instead of only deleting the current file.
- Run `make check` before direct `main` pushes.
