# Public MCP Docs Boundary Drift Check

Date: 2026-06-26

## What changed

- Root and MCP package docs now describe `packages/mcp` as public fixture, metadata-route, and recommendation-route tooling instead of evidence lookup tooling.
- Repo docs tests now reject stale MCP docs that advertise private evidence lookup as a public capability.

## Public boundary

This is a public docs-only guard. No live MCP server runtime, evidence lookup, private service access, DB work, hosted operations, telemetry, credentials, or runtime code moved.

## Verification

```sh
python3 -m unittest tests.test_repo_docs.RepoDocsTests.test_public_mcp_docs_do_not_advertise_private_evidence_lookup
```
