# Catalog Agent Guide

## Scope

- `manifest.json` is the canonical public inventory for EvalRank cells, benchmark families, feeds, governance, cadence, and publication eligibility.
- The catalog records hypotheses and policy. It does not contain benchmark tasks, result rows, private telemetry, or hosted storage details.

## Rules

- Keep every cell, family, and feed ID unique and stable.
- Treat `discovered` as research inventory, `shadow` as successfully replayed adapter evidence, `active` as publication-eligible evidence, and `quarantined` as explicitly blocked.
- Keep `metric_direction` null in discovery; require explicit `higher` or `lower` from the replayed feed contract before `shadow` or `active`. Never infer it from labels or observed values.
- Never infer rights, independence, configuration identity, cadence, retention permission, or admission from a project name or repository license.
- Keep unvalidated cadence and lineage values null; a descriptive candidate name is not lineage evidence.
- Unresolved identity is explorer-only and cannot carry top-set or single-winner eligibility.
- Resolved identity may remain explorer-only; only a single-winner-capable, calibrated group can become `active`.
- Multiple feeds for one benchmark family or declared correlation group count as one independent family.
- Keep eligibility scoped to `(cell_id, entity_kind, interaction_policy, configuration_passport_class)`; never pool unlike ranking groups.
- Update the schema, fixture-parity tests, method notes, and public status whenever the manifest contract changes.

## Checks

- From repo root: `python3 -m unittest tests.test_catalog_manifest`
- From repo root: `make check`
