# CLI Public Fixtures

Date: 2026-06-25

Scope: deterministic public CLI output over pinned contracts.

## Built

- `packages/cli/pyproject.toml` package metadata.
- `evalrank_cli` package with `fixture evidence` and `fixture recommendation`.
- `evalrank` console entrypoint.
- CLI tests for JSON output and invalid fixture input.

## Not Built

- No network calls.
- No private config, database access, or hosted API integration.
- No scoring engine or MCP tool behavior.

## Verification

- Red CLI test failed before `evalrank_cli` existed.
- Focused CLI tests passed after implementation.
- `make check` passed with 23 unit tests and the public boundary scanner.
