# TypeScript Use-Case Branch Parity Plan

Date: 2026-06-26

## Goal

Mirror existing public Python and JSON Schema use-case branch rules in the TypeScript SDK surface.

## Steps

1. Replace the loose `UseCase` interface with a public discriminated union.
2. Pin ranked use cases to `rank_policy: "ranked"` and `is_overlay: false`.
3. Pin overlay use cases to `rank_policy: "veto_overlay"` and `is_overlay: true`.
4. Update public docs and run the local gates.

## Public Boundary

- Safe: compile-time SDK shape parity for an existing public metadata contract.
- Excluded: private rank-policy tuning, scorer runtime behavior, hosted behavior, graph lookup, source adapters, and persistence.
