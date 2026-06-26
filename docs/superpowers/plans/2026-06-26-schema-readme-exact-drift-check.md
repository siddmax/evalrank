# Schema README Exact Drift Check Plan

Date: 2026-06-26

## Goal

Prevent `schemas/README.md` from accepting stale extra public schema or OpenAPI filename references.

## Steps

1. Parse documented schema/OpenAPI filenames from `schemas/README.md`.
2. Compare them to the actual public `schemas/*.schema.json` files plus `openapi.json`.
3. Update public docs and run local gates.

## Public Boundary

- Safe: stdlib test over public README text and current public filenames.
- Excluded: schema shape changes, runtime behavior, private services, hosted behavior, persistence, source adapters, and dependencies.
