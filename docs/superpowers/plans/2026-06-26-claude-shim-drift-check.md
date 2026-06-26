# Claude Shim Drift Check Plan

Date: 2026-06-26

## Goal

Keep `CLAUDE.md` as the required one-line `@AGENTS.md` shim.

## Steps

1. Add a stdlib repo-doc test for the exact shim contents.
2. Update public test/status/porting docs.
3. Run local gates and pre-landing review before the direct `main` push.

## Public Boundary

- Safe: stdlib test over public root agent docs.
- Excluded: private agent instructions, private repo paths, hosted operations, runtime behavior, source adapters, persistence, telemetry, customer data, and held-out eval material.
