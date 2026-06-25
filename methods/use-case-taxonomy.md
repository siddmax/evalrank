# Use-Case Taxonomy Method

This note documents the public method behind `UseCaseCatalog`. It explains how the catalog is organized without publishing benchmark weights, private thresholds, held-out evals, or scorer/runtime behavior.

## Public Contract

Each public use case has:

- `id`: stable slug used by requests, fixtures, schemas, SDKs, CLI, MCP, and OpenAPI examples.
- `name`: short display name.
- `definition`: one-line scope statement.
- `entity_kinds`: comparable public entity kinds from `model`, `tool`, and `agent`.
- `rank_policy`: `ranked` for ordinary use cases or `veto_overlay` for safety overlays.
- `is_overlay`: `true` only for overlay use cases.

The current public fixture contains ranked use cases plus the `safety-robustness` overlay. The overlay is not ranked as a capability task; it is a separate veto/safety dimension that can constrain or annotate recommendations.

## Method Rules

1. A use case is an evaluation question, not a product category.
2. `entity_kinds` names which public entity kinds can be compared for that question.
3. Ranked use cases may produce `single-scale` recommendations when the compared entities share one score scale.
4. Mixed-kind recommendations use `kind-grouped` response groups instead of implying false cross-kind score comparability.
5. Safety and robustness use `veto_overlay` because safety can block or qualify a recommendation rather than compete with task capability.

## Public Boundary

- Publish the catalog shape, public slugs, definitions, entity-kind spans, overlay policy, fixtures, schemas, and route contracts.
- Keep examples synthetic and reproducible.
- Keep source adapters, graph lookup, production rows, scorer weights, IRT clusters, confidence policy, synthesis rules, private thresholds, held-out tasks, graders, answers, traces, and benchmark outputs out of this repo.

## Update Checklist

When the public taxonomy changes:

- Update `_USE_CASE_ROWS` in `packages/core/src/evalrank_core/fixtures.py`.
- Update `UseCase` / `UseCaseCatalog` only if the payload shape changes.
- Update JSON Schema, SDK types, CLI/MCP fixtures, OpenAPI route docs, and tests when the shape or surfaced examples change.
- Update `docs/STATUS.md`, `docs/PORTING.md`, and a dated build log in the same change.
