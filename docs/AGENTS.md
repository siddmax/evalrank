# Docs Agent Guide

## Scope

- Project history, build logs, and durable public design notes live here.

## Rules

- Keep docs aligned with `README.md`, `TESTS.md`, and root `AGENTS.md`.
- Keep `STATUS.md` current as the living progress tracker.
- Keep `REPO_STRUCTURE.md` current as the directory ownership map.
- Keep `PORTING.md` current when work moves between the private runtime system and this public repo.
- Mark private implementation ownership clearly when public docs reference runtime persistence or hosted operation. Runtime persistence and hosted operation are maintained in a separate private system.
- Summarize private planning context; do not paste raw private docs, customer examples, held-out tasks, or live operational details.
- Do not publish secrets, private fixtures, customer data, or proprietary ranking experiment details.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
