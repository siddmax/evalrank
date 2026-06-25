# Schemas Agent Guide

## Scope

- Public JSON schema contracts live here.

## Rules

- Schemas define public interoperability contracts, not private storage layouts.
- Keep schema changes versioned or clearly documented once schemas become consumable.
- Add tests for required fields, compatibility, and examples when schemas are added.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
