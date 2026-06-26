# TypeScript TheCall Branch Parity Plan

Date: 2026-06-26

## Goal

Mirror existing public Python and JSON Schema `TheCall` branch rules in the TypeScript SDK surface.

## Steps

1. Replace the loose nullable `TheCall` interface with a public discriminated union.
2. Pin `recommend` calls to numeric `confidence` and null `abstention_reason`.
3. Pin `abstain` calls to null `confidence` and string `abstention_reason`.
4. Update public docs and run the local gates.

## Public Boundary

- Safe: compile-time SDK shape parity for an existing public response contract.
- Excluded: private confidence policy, thresholds, scorer internals, hosted receipts, runtime behavior, graph lookup, and persistence.
