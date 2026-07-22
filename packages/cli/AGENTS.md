# CLI Package Agent Guide

## Scope

- Public command-line boundary for EvalRank workflows.
- CLI commands should call public contracts or public service APIs.

## Rules

- Keep commands scriptable: deterministic output, explicit exit codes, no hidden network calls.
- Do not read runtime environment variables, runtime datastores, or local-only secrets. Runtime persistence and hosted operation are maintained in a separate private system.
- Add tests for any parser, output contract, or non-zero exit path.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
