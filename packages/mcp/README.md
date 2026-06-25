# EvalRank MCP

Public MCP server boundary for EvalRank evidence and evaluation tools.

Current adapter:

- `list_tools()` exposes `evalrank.fixture`.
- `call_tool("evalrank.fixture", {"kind": "evidence"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "recommendation"})` returns deterministic public fixture JSON text.

This package does not start a server or call private services yet.
