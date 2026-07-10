# Use-Case Taxonomy Method

This note documents the public method behind `UseCaseCatalog` and its canonical source, `catalog/manifest.json`.

## Public Contract

Each public use case has:

- `id`: stable cell slug used by requests, fixtures, schemas, SDKs, CLI, MCP, and route examples.
- `name`: short display name.
- `definition`: one-line decision scope.
- `entity_kinds`: public model, tool, or agent spans that may contain separate ranking groups.
- `rank_policy`: `ranked` for every catalog cell.
- `is_overlay`: `false` for every catalog cell.

The manifest contains exactly 26 ranked cells. Public inputs use canonical cell IDs directly; the catalog defines no aliases.

Professional deliverable creation, machine-learning engineering, and computational research reproduction are distinct decision questions with explorer-only preview groups. Their candidate families stay within those cells: aggregate professional work does not become legal, finance, medical, or support evidence; ML competition work does not become SWE evidence; and computational reproduction does not become deep-research or DevOps evidence. Catalog inclusion records a research job, not ranking readiness.

Safety and robustness remain a cross-cutting safety veto. They can exclude or qualify a candidate, but they are not a catalog cell and are never averaged into capability.

## Method Rules

1. A cell is a decision question, not a product category or readiness claim.
2. Catalog state is one of `preview`, `shadow`, `active`, or `quarantined`.
3. Evidence is assessed within the exact ranking group `(cell_id, entity_kind, interaction_policy, configuration_passport_class)`.
4. A cell containing both model and agent candidates never combines their family counts or scores.
5. Every published result belongs to one exact ranking group. Different entity kinds or interaction policies are never put on one score scale.
6. Catalog membership does not imply a publishable ranking. Thin cells disclose their missing-family gap.
7. Candidate benchmark families begin as discovery hypotheses. Desk research cannot assign `shadow` or `active`.
8. Evaluator-validation suites calibrate graders separately and never count as capability families.

## Ownership

`catalog/manifest.json` is the sole inventory authority. `_USE_CASE_ROWS` is a synthetic package projection kept under exact parity tests for standalone fixture portability; it is not an independent taxonomy. SDK, CLI, and MCP fixtures consume that same public projection.

The manifest also owns source/feed governance, cadence, retention, lineage, and explicit per-ranking-group eligibility. `methods/evidence-synthesis.md` owns how admitted native evidence becomes a top set, tie group, single winner, or abstention.

## Public Boundary

Publish the taxonomy, manifest policy, schemas, synthetic fixtures, and reproducible method. Keep benchmark task contents, non-public observations, customer context, production telemetry, credentials, proprietary experiments, and persistence layout outside this repo.

## Update Checklist

When the taxonomy changes:

- Update `catalog/manifest.json` first.
- Update the portable `_USE_CASE_ROWS` projection in `packages/core/src/evalrank_core/fixtures.py` in the same change.
- Update schemas, method notes, SDK/CLI/MCP parity tests, status, and navigation when their public surface changes.
- Run `python3 -m unittest tests.test_catalog_manifest` and `make check`.
