# EvalRank MCP

Public MCP adapter for EvalRank fixture, metadata-route, and recommendation-route tools.

Package metadata:

- Distribution: `evalrank-mcp`
- Import: `evalrank_mcp`
- Runtime dependencies: `evalrank-core==0.0.0`, `evalrank-sdk==0.0.0`
- License: `Apache-2.0`

Current adapter:

- `list_tools()` exposes `evalrank.fixture`, `evalrank.recommend`, `evalrank.use_cases`, and `evalrank.scoring_stages`.
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
- `call_tool("evalrank.recommend", {"base_url": "https://evalrank.example", "request": {...}})` calls the public `POST /v1/recommendations` contract with an `EvaluationRequest`-shaped payload. A successful recommendation body is future contract behavior; the current hosted operation surfaces typed Problem Details instead.
- `call_tool("evalrank.use_cases", {"base_url": "https://evalrank.example"})` calls the public `GET /v1/use-cases` contract and returns use-case catalog JSON text.
- `call_tool("evalrank.scoring_stages", {"base_url": "https://evalrank.example"})` calls the public `GET /v1/scoring-stages` contract and returns scoring-stage catalog JSON text.
- Route tool input schemas advertise explicit non-empty HTTP(S) `base_url` values.

The hosted legacy `evalrank.recommend` operation is temporarily unavailable and returns the typed public Problem Details code `recommendation_not_published`. MCP callers must preserve that state rather than presenting it as insufficient evidence or a successful recommendation.

This package does not start a server, discover services, read environment defaults, add auth, retry requests, create hosted receipts, persist data, or call private services.
