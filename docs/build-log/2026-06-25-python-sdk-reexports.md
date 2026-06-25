# Python SDK Re-Exports

Date: 2026-06-25

Scope: public Python SDK package boundary.

## Built

- `packages/sdk-python/pyproject.toml` package metadata.
- `evalrank_sdk` package that re-exports public core contracts and fixtures.
- SDK test proving `EvidenceItem` is the core contract object, not a copied SDK type.

## Not Built

- No HTTP client.
- No auth, hosted API config, or private service integration.
- No CLI or MCP behavior.

## Verification

- Red SDK test failed before `evalrank_sdk` existed.
- Focused SDK test passed after implementation.
- `make check` passed with 20 unit tests and the public boundary scanner.
