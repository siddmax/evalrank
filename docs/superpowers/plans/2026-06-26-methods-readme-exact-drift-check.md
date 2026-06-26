# Methods README Exact Drift Check Plan

Date: 2026-06-26

## Goal

Prevent `methods/README.md` from accepting stale extra public method-note filenames.

## Steps

1. Parse documented method-note filenames from `methods/README.md`.
2. Compare them to the current public method note files, excluding repo guidance docs.
3. Update public progress docs and run local gates.

## Public Boundary

- Safe: stdlib tests over public method note filenames and README text.
- Excluded: private methodology, scorer weights, thresholds, benchmark data, runtime behavior, hosted behavior, persistence, source adapters, and dependencies.
