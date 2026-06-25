# EvalRank

EvalRank is the public core for evidence-ranked evaluation primitives. This repository holds the open schemas, scoring method interfaces, SDK boundaries, examples, and CI gates that keep the core independent from any private Syndai application code.

## Repository Layout

- `AGENTS.md` - Root agent guide and evolution rules.
- `TESTS.md` - Current test commands and test map.
- `docs/STATUS.md` - Living build progress tracker.
- `docs/REPO_STRUCTURE.md` - Directory ownership map.
- `docs/PORTING.md` - Public/private porting decisions and workstream ownership.
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

Use `docs/PORTING.md` before moving any private work into this repo.

## Database Boundary

During incubation, EvalRank uses the existing Finn/Supabase project with a private `evalrank` schema. The schema migrations and live DB bootstrap are kept in the Syndai repo because Syndai currently owns the shared Finn/Supabase deploy path and guardrails.

Move database migrations into this repo only when EvalRank owns its own deploy/release path or moves to its own Supabase project. When that happens, update `AGENTS.md`, `TESTS.md`, and this README in the same change.

## Boundary Contract

Run:

```sh
make check
```

The boundary gate rejects private imports, Smithery coupling, Min-K% implementation markers, secret files, high-signal secret values, private data paths, and public packages missing license or notice files.

## Public Fixture Surfaces

These examples use local checkout paths until the packages are published.

Runnable example:

```sh
python3 examples/public_fixture.py
```

CLI:

```sh
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture request
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture evidence
PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture recommendation
```

Python SDK:

```python
from evalrank_sdk import sample_evaluation_request

payload = sample_evaluation_request().to_dict()
```

MCP adapter:

```python
from evalrank_mcp import call_tool

result = call_tool("evalrank.fixture", {"kind": "request"})
```

TypeScript SDK:

```ts
import { type EvaluationRequest } from "@evalrank/sdk";

const request: EvaluationRequest["object"] = "evaluation_request";
```
