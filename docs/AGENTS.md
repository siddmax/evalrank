# Docs Agent Guide

## Scope

- Project history, build logs, and durable public design notes live here.

## Rules

- Keep docs aligned with `README.md`, `TESTS.md`, and root `AGENTS.md`.
- Mark private implementation ownership clearly when public docs mention Syndai or Finn.
- Do not publish secrets, private fixtures, customer data, or proprietary ranking experiment details.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
