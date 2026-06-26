# EvalRank MCP

Public MCP server boundary for EvalRank evidence and evaluation tools.

Current adapter:

- `list_tools()` exposes `evalrank.fixture` and `evalrank.recommend`.
- `call_tool("evalrank.fixture", {"kind": "fingerprint"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "raw-entry"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "request"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "candidate-set"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "stage-candidate"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "evidence"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "problem"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "result-row"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "ranking-group"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "evidence-set"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "exclusion"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "use-cases"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "scoring-stages"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.fixture", {"kind": "recommendation"})` returns deterministic public fixture JSON text.
- `call_tool("evalrank.recommend", {"base_url": "https://evalrank.example", "request": {...}})` calls the public `POST /v1/recommendations` contract and returns recommendation JSON text.

This package does not start a server, discover services, read environment defaults, add auth, retry requests, create hosted receipts, persist data, or call private services.
