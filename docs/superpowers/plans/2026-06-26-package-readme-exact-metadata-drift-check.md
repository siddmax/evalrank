# Package README Exact Metadata Drift Check Plan

Date: 2026-06-26

## Goal

Prevent package READMEs from accepting stale extra public package metadata.

## Steps

1. Parse each package README `Package metadata` block.
2. Compare documented metadata exactly to the current Python `pyproject.toml` or TypeScript `package.json`.
3. Update public progress docs and run local gates.

## Public Boundary

- Safe: stdlib tests over public package manifests and README metadata blocks.
- Excluded: runtime behavior, publishing workflow, private package indexes, credentials, hosted behavior, persistence, source adapters, and dependencies.
