# Private W7 POST Recommendations Route Parity

Date: 2026-06-27

Public boundary: no private code was ported into this repo. The private Syndai worktree added cache-backed route parity for the public EvalRank recommendation contract.

## What Changed Privately

- Added `POST /v1/recommendations` for public SDK/CLI/MCP callers that use the service root as `base_url`.
- Added `POST /api/v1/recommendations` as the Syndai API-prefix alias.
- Kept `GET /api/v1/recommend?use_case=...` as the existing internal/read convenience.
- Reused the active private `evalrank.recommendation_cache` reader and `recommend.called` telemetry path.
- Updated private backend navigation, test map, and API reference docs.

## Decision

The canonical external contract is `POST /v1/recommendations`. Requiring callers to pass a base URL ending in `/api` would be a worse long-term user experience and would diverge from the public OpenAPI, SDK, CLI, and MCP clients.

The request path remains cache-backed. Accuracy comes from offline validated evidence snapshots, scorer rows, calibration, and materialization; user latency and per-request cost stay low because reads do not run live evals or scoring.

## Private Verification

Focused private checks passed in `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine/backend`:

- Red: `POST /api/v1/recommendations` test failed with `404 == 200` before implementation.
- Red: `POST /v1/recommendations` test failed with `404 == 200` before implementation.
- Green: `uv run pytest --no-cov tests/unit/features/evalrank/test_controller.py -q` passed with `4 passed`.
- Green: `uv run pytest --no-cov tests/unit/features/evalrank/test_cache_reader.py tests/unit/features/evalrank/test_telemetry.py tests/unit/features/evalrank/test_controller.py tests/test_app_di.py -q` passed with `30 passed`.
- Green: focused `ruff check` and `ty check` passed for the touched controller/test files.

## Live Local Parity Proof

Started the private API locally with:

```bash
doppler run -- uv run granian --interface asgi --host 127.0.0.1 --port 8017 --workers 1 --http 1 src.app:app
```

Then verified:

- `curl` success on `POST /v1/recommendations`: `HTTP/1.1 200 OK`, `recommend_id=rec_cc32bb34a0b4afa8de58435a`.
- `curl` error on malformed `POST /v1/recommendations`: `HTTP/1.1 400 Bad Request`, Problem title `use_case must be non-empty`.
- `curl` success on `GET /api/v1/recommend?use_case=autonomous-swe-agent`: same `recommend_id=rec_cc32bb34a0b4afa8de58435a`.
- Public Python SDK, CLI, MCP tool, and TypeScript SDK all returned the same `recommend_id` and top row: `agent:syndai-coding:claude_code:claude-opus-4-8`.

Latency caveat: the first Python SDK proof used a 15s timeout and timed out while the private server later logged a successful 200 after about 20.8s on the local-to-Doppler/Supabase path. The 60s fixed-query parity proof passed. Count this as route/client parity, not production latency proof.

## Remaining Work

This is local route/client parity only. W7 still needs API keys, quota/billing, receipts, webhooks, hosted/staging route proof, and production-latency/load proof.
