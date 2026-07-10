# EvalRank Public Contract Gap-Closure Plan

## Purpose

This public plan covers only portable contracts, schemas, reference behavior, method notes, clients, examples, and deterministic checks. It contains no private paths, credentials, customer context, live operations, persistence layout, deployment procedure, or proprietary evaluation material.

## Locked Boundaries

- `docs/PRODUCT.md` defines the user job and exclusions.
- `catalog/manifest.json` is the only public inventory for cells, benchmark families, feeds, governance, cadence, lineage, and eligibility.
- `methods/evidence-synthesis.md` defines the public synthesis and publication method.
- Public contracts remain storage-free and product-neutral.
- Exact ranking groups prevent cross-kind and cross-policy score pooling.
- Aggregate scores never become synthetic item responses.
- Safety is a cross-cutting veto, not a catalog ranking cell.

## Work

### 1. Canonical Inventory

- Keep the exact 26-cell taxonomy and 37 explicit ranking groups schema-validated; expose only canonical cell slugs and no compatibility aliases.
- Keep professional deliverables, machine-learning engineering, and computational reproduction explorer-only until independent evidence supports a stronger policy; do not leak their families into adjacent cells.
- Keep evaluator-validation suites outside capability-family counts.
- Keep discovery, shadow, active, and quarantine states truthful.
- Require explicit rights, retention, cadence, and lineage on every feed.
- Keep all admission counts unknown until a dated admission report exists.

### 2. Portable Evidence Contracts

- Add typed source, artifact, observation, configuration-passport, publication, decision-query, and receipt schemas.
- Pin schema digests and methodology versions in every reproducible result.
- Maintain byte-identical fixtures across the reference core, SDKs, CLI, MCP adapter, and reference server.

### 3. Deterministic Decision Surface

- Accept a complete versioned structured query.
- Read one pinned publication snapshot and apply only exact ranking-group and serving-offer links.
- Return top sets, tie groups, exclusions, freshness, uncertainty, and explicit abstentions.
- Keep the request path deterministic and free of live model inference.

### 4. Verification

- Write behavior tests before each contract or bug fix.
- Run the public boundary check, all Python tests, TypeScript checks, and client/reference-server end-to-end tests.
- Verify documentation, schema, fixture, and navigation drift in the same change.
- Record paired immutable release identifiers only after each repository has landed independently.

## Completion Standard

The public contract is complete when one clean checkout can validate the manifest, replay synthetic evidence into a deterministic decision, exercise every client against the reference server, and explain every decision or abstention without any private dependency.
