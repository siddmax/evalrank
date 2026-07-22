# MCP Package Agent Guide

## Scope

- Public MCP adapter for EvalRank fixtures, metadata reads, deterministic decisions, and shared-receipt retrieval.
- Keep this package as an adapter over public contracts. Runtime persistence and hosted operation are maintained in a separate private system, and this package must not bridge to it.

## Rules

- MCP tools must expose public EvalRank concepts only.
- Do not call private databases, private services, held-out fixtures, or hosted telemetry from this package.
- Add tests before adding non-trivial tool parsing or response-shape logic.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
