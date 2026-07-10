# EvalRank Public Porting Map

This Apache-2.0 repository contains portable EvalRank contracts and method. A port is acceptable only when it remains understandable, reproducible, and testable without a private service, credential, customer, or non-public dataset.

Last reviewed: 2026-07-10

Portable contract status: deterministic decisions, benchmark health, explicit shared-receipt retrieval, and all grouped explorer reads now share one seven-path public contract. A private hosted runtime must conform to this exact contract before deployment; no compatibility route is public.

## Authorities

- `docs/PRODUCT.md`: product job, ontology, receipt behavior, demand boundary, and exclusions.
- `catalog/manifest.json`: canonical cells, ranking groups, benchmark families, feeds, native-metric direction, governance, cadence, retention, lineage, and eligibility. Transitional cell aliases are retired.
- `methods/evidence-synthesis.md`: native-metric synthesis, uncertainty, staged eligibility, sensitivity, and publication.
- `schemas/`: versioned portable interoperability payloads.

Historical status notes and build logs are context, not alternate authorities.

## Public Here

- Product-neutral contracts, JSON Schemas, OpenAPI, SDKs, CLI, MCP boundary, examples, and public method notes.
- Canonical catalog policy and research-state metadata that contains no benchmark task content or non-public results.
- Public research hypotheses may name a benchmark family and more than one correlated feed, but correlated views remain one family for eligibility and never create extra independent evidence.
- Synthetic fixtures and deterministic reference behavior.
- Boundary, package, schema, documentation, and end-to-end contract checks.
- Public-safe release linkage containing immutable commit identifiers only after both sides land.

## Private Elsewhere

- Credentials, environment files, live project identifiers, deployment configuration, and operator procedures.
- Customer or tenant data, private prompts, usage events, account operations, and production traces.
- Non-public benchmark tasks, answers, graders, trajectories, observations, and proprietary experiments.
- Evaluator task suites and judge traces used for future grader calibration; these do not enter the capability-family inventory.
- Runtime-specific persistence, source ingestion, scheduling, evaluation execution, and service integration.
- Private product integrations or customer-specific policy.

Do not copy a private plan and redact it after the fact. Extract the smallest portable contract or public method, rewrite it for a clean checkout, and prove it with synthetic fixtures.

## Ownership Boundary

The public repo owns the canonical portable contract. A private runtime may implement and persist that contract, but it must pin an immutable public revision and must not create a competing taxonomy, schema, method, or public fixture vocabulary.

During private incubation, persistence migrations and service operations remain with their owning runtime. If EvalRank later owns a deploy path or project, document the cutover before adding migrations here.

## Paired Release Linkage

Cross-repository work lands without circular claims:

1. Land the public contract and record its immutable identifier.
2. Land the private consumer pinned to that identifier.
3. Add a public-safe follow-up entry containing both immutable identifiers and no operational detail.

Temporary worktrees or stale branches are not continuity records. The paired identifiers and public contract history are.

## Current Workstreams

- Public Contracts: storage-free payloads, schemas, fixtures, and deterministic reference behavior.
- Catalog / Methods: canonical inventory, governance, provenance, and evidence synthesis.
- SDK / CLI / MCP: product-neutral clients and adapters over pinned public operations.
- Public Boundary / Docs: repository hygiene, public-safe planning, and drift checks.
- Runtime Integration: private consumer work; only portable contracts return here.
- Evaluation Integrity: non-public task material remains outside this repository.

## Porting Checklist

Before moving an artifact here, verify that it:

- has no secret, credential, customer, tenant, live project, or private-service dependency;
- has no non-public task, answer, grader, trajectory, result, or production trace;
- imports no private namespace;
- is licensed for Apache-2.0 distribution;
- uses the canonical manifest rather than a private mirror;
- preserves the manifest cell boundary instead of projecting aggregate professional, ML-engineering, or reproduction evidence into adjacent domain, SWE, research, or operations cells;
- includes synthetic tests for non-trivial logic or contract shape;
- updates `docs/STATUS.md`, `docs/REPO_STRUCTURE.md`, `TESTS.md`, and the nearest `AGENTS.md` when scope changes;
- passes `python3 scripts/check_public_boundary.py --root .` and `make check`.
