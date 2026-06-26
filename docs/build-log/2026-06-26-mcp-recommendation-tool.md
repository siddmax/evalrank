# MCP Recommendation Tool

Date: 2026-06-26

## What changed

- Added `evalrank.recommend` to the public MCP tool manifest.
- Routed the tool through the existing public Python SDK `EvalRankClient`.
- Added MCP tests for success, Problem Details tool errors, route path, headers, posted request JSON, argument validation, and README drift.
- Added the public SDK package as an MCP package dependency.

## Boundary

This is explicit HTTP(S)-only public API plumbing. It does not add auth, retries, service discovery, environment-variable defaults, tenant context, hosted receipt IDs, private DTOs, database work, production evidence lookup, scorer runtime, persistence, source adapters, or a live MCP server runtime.
