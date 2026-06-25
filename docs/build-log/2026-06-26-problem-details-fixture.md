# Public Problem Details Fixture

Date: 2026-06-26

## Built

- Added `sample_problem_details()` as a deterministic public RFC 9457 fixture.
- Added the shared `problem` fixture kind for core dispatch, Python SDK re-export, TypeScript fixture-kind parity, CLI output, MCP output, and the runnable public fixture example.
- Added focused tests for the core fixture, Python SDK re-export, CLI, MCP, TypeScript fixture-kind parity, and example README drift.

## Kept Private

- Hosted error telemetry.
- Tenant, account, auth, or deployment context.
- Private problem types.
- Live route handling or rate-limit enforcement.
