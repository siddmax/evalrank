# Methods Agent Guide

## Scope

- Public method notes and implementation boundaries live here.

## Rules

- Document public methodology and exclusion boundaries without leaking private fixtures or proprietary experiments.
- If a method needs private telemetry, keep the implementation outside this repo and document only the public contract.
- Do not add excluded method implementations to public packages.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
