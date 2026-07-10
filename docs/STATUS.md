# EvalRank Public Status

Last updated: 2026-07-10

Hosted contract status: the legacy `POST /v1/recommendations` operation is temporarily unavailable and returns the product-neutral RFC 9457 code `recommendation_not_published`. The public contract must not claim a request-specific answer until the deterministic decision operation replaces it atomically.

## Product Contract

Three documents are normative:

- `docs/PRODUCT.md` defines the user job, entity ontology, receipt experience, demand boundary, and exclusions.
- `catalog/manifest.json` defines the canonical 26-cell/37-ranking-group inventory, aliases, 77-family/79-feed research queue, governance, cadence, lineage, retention, and eligibility.
- `methods/evidence-synthesis.md` defines native-metric synthesis, top and tie sets, uncertainty, sensitivity, abstention, and challenger promotion.

Older build logs record historical work. They are non-normative when they conflict with these authorities.

`catalog/research-provenance.json` is the version-locked research companion to
the manifest. It records dated primary or official discovery sources and the
claim basis behind research flags; it is supporting provenance, not a fourth
normative authority or evidence of runtime lineage, rights, or admission.

## Current Public Surface

- Parser provenance records the complete sorted, role-typed retained input set. Multi-file upstream releases cannot hide auxiliary bytes in adapter metadata.
- Apache-2.0, product-neutral Python contracts and synthetic fixtures.
- Public JSON Schemas and OpenAPI description.
- Immutable artifact/run provenance, native observations, exact configuration passports, effective-dated serving-offer pricing schedules, evidence-basis evaluation-to-offer links, closed monthly usage queries, baseline and zero-cache projected-cost receipts with hard cross-profile budgets and truthful divergence caveats, and deterministic receipt identities.
- Content-addressed grouped leaderboard, exact entity-detail, and same-ranking-group compare read contracts with semantic verifiers.
- Dependency-light Python and TypeScript SDK boundaries.
- Deterministic CLI and MCP adapters over public contracts.
- A storage-free reference materializer and fixture example.
- Boundary, schema, package, documentation, client, and parity checks under `make check`.

The public repo owns portable contracts and method. Private runtime integrations, credentials, non-public data, and deployment behavior remain outside this repository.

## Evidence State

- All 26 cells are `preview`; catalog presence is not a ranking-readiness claim.
- Candidate families remain `discovered` until an adapter replays exact official bytes. BFCL V4, LiveCodeBench, LiveBench reasoning, and Terminal-Bench 2.1 are now `shadow`: their repaired official-surface adapters replay successfully, but `rank_eligible_count` remains null and none is admitted until rights, identity, lineage, overlap, health, cadence, uncertainty, and marginal decision value pass.
- Scraper recovery is mandatory before retirement. The four shadow adapters resolve official HTML-linked CSV/JSON, same-release artifact sets, or licensed repository archives; API/feed/raw-file failure alone is not benchmark-death evidence.
- Every candidate family has a dated primary or official discovery source in the manifest-version-locked research companion. Source coverage documents the research basis only and does not advance admission state.
- Professional deliverables, machine-learning engineering, and computational research reproduction are new explorer-only research jobs. GDPval, MLE-bench, PaperBench, and CORE-Bench remain discovery hypotheses and do not confer product readiness.
- CORE-Bench mainline and out-of-distribution feeds are two views of one declared correlated family and never count as independent evidence.
- SWE-bench Verified, SWE-Bench Pro, and current Steel composites are `quarantined` pending documented repair and replay.
- Eligibility thresholds are `unvalidated`. Explorer output needs at least one family; a calibrated top set needs at least three independent families; a single-winner claim needs at least four plus native practical effect and leave-one-family-out stability.
- Safety is a cross-cutting veto, not a ranking cell.
- Evaluator suites remain future calibration evidence, not capability families.

No paired public/private release identifiers are recorded for this manifest version yet.

## Current Workstreams

- Public Contracts: storage-free payloads, schemas, fixtures, and deterministic reference behavior.
- Catalog / Methods: canonical inventory, governance, provenance, and evidence synthesis.
- SDK / CLI / MCP: product-neutral clients and adapters over pinned public operations.
- Public Boundary / Docs: repository hygiene, public-safe planning, and drift checks.
- Runtime Integration: private consumer work; only portable contracts return here.
- Evaluation Integrity: non-public task material remains outside this repository.

## Next Public Work

1. Pin this public revision into the hosted build and prove backend/web conformance against its exact bytes.
2. Implement the deterministic decision operation and remove the unavailable recommendation vocabulary atomically.
3. Exercise SDK, CLI, MCP, and the reference server end to end from a clean checkout.
4. Record paired immutable release identifiers only after each repository lands independently.

## Verification

Run:

```sh
make check
```

The gate includes the public-boundary scanner, Python tests, TypeScript syntax checks, and TypeScript runtime tests.
