# MCP Package Agent Guide

## Scope

- Public MCP server boundary for EvalRank evidence and evaluation tools.
- Keep this package as an adapter over public contracts, not a private Syndai bridge.

## Rules

- MCP tools must expose public EvalRank concepts only.
- Do not call private databases, private services, held-out fixtures, or hosted telemetry from this package.
- Add tests before adding non-trivial tool parsing or response-shape logic.

## Checks

- From repo root: `python3 scripts/check_public_boundary.py --root .`
- From repo root: `python3 -m unittest discover tests`
