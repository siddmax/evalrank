# Scoped Agents Drift Check Plan

Date: 2026-06-26

## Goal

Keep scoped `AGENTS.md` guidance present for the public work areas agents edit.

## Steps

1. Add a stdlib repo-doc test for scoped agent guidance coverage.
2. Update public test/status/porting docs.
3. Run local gates and pre-landing review before the direct `main` push.

## Public Boundary

- Safe: stdlib test over public directory names and public agent docs.
- Excluded: private agent instructions, private repo paths, hosted operations, runtime behavior, source adapters, persistence, telemetry, customer data, and held-out eval material.
