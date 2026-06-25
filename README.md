# EvalRank

EvalRank is the public core for evidence-ranked evaluation primitives. This repository holds the open schemas, scoring method interfaces, SDK boundaries, examples, and CI gates that keep the core independent from any private Syndai application code.

## Repository Layout

- `packages/core` - Python reference package for evidence objects and scoring contracts.
- `packages/mcp` - MCP server boundary for evaluation and evidence lookup tools.
- `packages/cli` - Command-line entrypoints that call the public APIs.
- `packages/sdk-python` - Python SDK packaging boundary.
- `packages/sdk-ts` - TypeScript SDK packaging boundary.
- `methods` - Public method notes and implementation boundaries.
- `schemas` - Public JSON schema contracts.
- `examples` - Minimal runnable examples.

## What Is Not Open

The hosted product, private Syndai application integrations, private benchmark fixtures, held-out eval data, production telemetry, customer data, and proprietary ranking experiments are not part of this repository. Public packages must not import private Syndai namespaces or depend on private services.

## Boundary Contract

Run:

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
```

The boundary gate rejects private imports, Smithery coupling, Min-K% implementation markers, and public packages missing license or notice files.
