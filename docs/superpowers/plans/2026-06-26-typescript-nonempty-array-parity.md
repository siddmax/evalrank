# TypeScript Non-Empty Array Parity Plan

Date: 2026-06-26

## Goal

Mirror existing public Python and JSON Schema `minItems: 1` array contracts in the TypeScript SDK surface.

## Steps

1. Add a public `NonEmptyArray<T>` helper type to `packages/sdk-ts`.
2. Apply it only to arrays that Python and JSON Schema already require to be non-empty, including recommendation groups.
3. Add focused TypeScript surface tests.
4. Update public docs and run the local gates.

## Public Boundary

- Safe: compile-time SDK shape parity for existing public contracts.
- Excluded: runtime validation, retries, hosted service behavior, private data, scorer logic, graph lookup, and persistence.
