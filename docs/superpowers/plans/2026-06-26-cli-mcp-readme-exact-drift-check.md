# CLI and MCP README Exact Drift Check Plan

Date: 2026-06-26

## Goal

Prevent public CLI and MCP README command/tool docs from accepting stale extra public fixture kinds, route commands, or tool names.

## Steps

1. Parse documented CLI fixture commands and require exact parity with `PUBLIC_FIXTURE_KINDS`.
2. Parse documented CLI public route commands and require the current exact command set.
3. Parse documented MCP fixture kinds and `call_tool(...)` tool names and require exact parity with the current public surface.
4. Update public docs and run local gates.

## Public Boundary

- Safe: stdlib tests over public README text and public constants.
- Excluded: runtime behavior, private services, live API assumptions, hosted receipts, persistence, source adapters, and dependencies.
