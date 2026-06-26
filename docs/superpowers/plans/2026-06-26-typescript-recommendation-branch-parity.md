# TypeScript Recommendation Branch Parity Plan

Date: 2026-06-26

## Goal

Mirror existing public Python and JSON Schema recommendation comparability branch rules in the TypeScript SDK surface.

## Steps

1. Replace the loose `Recommendation` interface with a public discriminated union.
2. Pin `single-scale` recommendations to nullable `groups`.
3. Pin `kind-grouped` recommendations to empty top-level `ranked` and non-empty `groups`.
4. Update public docs and run the local gates.

## Public Boundary

- Safe: compile-time SDK shape parity for an existing public response contract.
- Excluded: scorer normalization, private score semantics, hosted receipts, runtime behavior, graph lookup, and persistence.
