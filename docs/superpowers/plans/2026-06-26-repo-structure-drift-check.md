# Repo Structure Drift Check Plan

Date: 2026-06-26

## Goal

Keep `docs/REPO_STRUCTURE.md` aligned with the public repo tree as new code areas and packages are added.

## Steps

1. Check current public top-level directories against documented repo-structure references.
2. Check current package directories against the documented package ownership list.
3. Update public status and porting docs with the safe port decision.
4. Run local gates and pre-landing review before the direct `main` push.

## Public Boundary

- Safe: stdlib tests over public directory names and public docs.
- Excluded: private planning docs, private repo paths, live project refs, hosted operations, persistence, source adapters, scorer runtime, telemetry, customer data, and held-out eval material.
