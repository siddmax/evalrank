# Ranked Entity Axes Contract Hardening Plan

Date: 2026-06-26

## Goal

Close the public `RankedEntity.axes` shape to match the existing Python `RankedEntity.to_dict()` output.

## Steps

1. Tighten `schemas/ranked-entity.schema.json` so `axes.evidence` carries only `n_items` and trust-tier `coverage`.
2. Mirror the same structure in the TypeScript SDK `RankedEntity` interface.
3. Add focused schema and TypeScript surface tests.
4. Update public docs and run the local gates.

## Public Boundary

- Safe: public evidence count and trust-tier coverage shape.
- Excluded: private evidence scoring, weights, formulas, calibration, scorer runtime, graph lookup, and persistence.
