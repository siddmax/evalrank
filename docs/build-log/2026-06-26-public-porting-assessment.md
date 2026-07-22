# Public Porting Assessment Refresh

Date: 2026-06-26

Scope: public EvalRank repo at https://github.com/siddmax/evalrank

## What Changed

- Verified the GitHub repo is public and still uses `main` as the default branch.
- Updated `docs/STATUS.md` and `docs/PORTING.md` with the current built surface through the result-row contract.
- Reclassified the next private-side planning items into public port, private incubation, and never-port workstreams.

## Built In The Public Repo Now

- Storage-free core contracts for capability fingerprints, raw entries, evaluation requests, candidate sets, stage candidates, evidence items, result rows, evidence sets, exclusions, `the_call`, ranked entities, recommendations, recommendation aliases, and entity references.
- JSON Schemas, drift tests, fixtures, Python SDK re-exports, TypeScript public types, CLI fixture output, MCP fixture output, public example output, and package docs for the current contracts.
- Public OpenAPI contract for `POST /v1/recommendations` plus reusable retry-aware RFC 9457 Problem Details responses.
- Boundary checks for private imports, disallowed coupling, secret files, high-signal secret values, private data paths, excluded implementation markers, and package license/notice hygiene.
- Living docs for status, repo structure, route navigation, tests, and public/private porting ownership.

## Next Public Port Candidates

| Candidate | Public handling | Workstream |
| --- | --- | --- |
| Use-case taxonomy catalog | Port next as a storage-free `UseCaseCatalog` contract with public slugs, names, one-line definitions, entity-kind spans, ranked-vs-overlay policy, synthetic fixture, JSON Schema, SDK/CLI/MCP parity, and `GET /v1/use-cases` route contract. | Public Contracts, Public Surface Contracts, SDK / CLI / MCP |
| Recommendation comparability and ranking groups | Review after taxonomy. Port only if the discriminated response shape is pinned without private scoring semantics. | Public Contracts, Methods / Schemas |
| Additional collection route contracts | Port only after each route has a concrete storage-free public contract. Do not imply a live server. | Public Surface Contracts |
| Public method notes for use-case taxonomy | Summarize why EvalRank ranks by use case and why safety is an overlay. Omit benchmark weights, held-out material, private thresholds, and synthesis details. | Methods / Schemas |

## Keep Private

| Source area | Reason | Workstream |
| --- | --- | --- |
| Benchmark weights and IRT fit-cluster crosswalk | Exposes proprietary evaluation strategy and depends on private benchmark inventory and tuning. | Scoring / Materializer Runtime, Evaluation Integrity |
| Thin-coverage, confidence, and synthesis policy details | Tied to held-out suites, private corpora, and scorer decisions. | Methods / Schemas, Evaluation Integrity |
| Persistence, access-control, and shared bootstrap operations | Runtime persistence and hosted operation are maintained in a separate private system. EvalRank does not yet own persistence or its own deploy path. | Runtime Persistence Ops |
| Runtime scorer, materializer, source adapters, graph lookup, and evidence ledger workers | Still coupled to production data, live workers, source credentials, and proprietary tuning. | Scoring / Materializer Runtime |
| Hosted auth, HMAC receipt IDs, billing/admin/GTM, telemetry, and deploy config | Hosted-product and operations material, not public core. | Hosted Ops / GTM, Secrets / Deploy Ops |

## Guardrails

- Treat the full Git history as public forever.
- Port summaries and contracts, not raw private planning docs.
- Keep examples synthetic and reproducible.
- Run `make check` and the public boundary scanner before any direct `main` push.
