# MCP Public Fixtures

Date: 2026-06-25

Scope: deterministic public MCP adapter over pinned contracts.

## Built

- `packages/mcp/pyproject.toml` package metadata.
- `evalrank_mcp.list_tools()` exposing `evalrank.fixture`.
- `evalrank_mcp.call_tool()` returning public fixture JSON as MCP text content.
- MCP tests for tool manifest, result shape, and unknown-tool handling.

## Not Built

- No server process.
- No private database, hosted API, telemetry, or credential handling.
- No scoring engine or live evidence lookup.

## Verification

- Red MCP test failed before `call_tool` and `list_tools` existed.
- Focused MCP tests passed after implementation.
- `make check` passed with 26 unit tests and the public boundary scanner.
