# Public Fixture Dispatch

Date: 2026-06-26

## What Changed

- Added `PUBLIC_FIXTURE_KINDS` and `sample_public_fixture(kind)` to the public core fixture surface.
- Reused that shared fixture dispatch in the CLI and MCP fixture adapters instead of keeping separate kind lists and dispatch branches.
- Re-exported the fixture dispatch helpers from the Python SDK.
- Added README drift checks for CLI fixture commands and MCP fixture kinds.

## Public Boundary

- The helper returns only existing synthetic public fixture payloads.
- No network, database, private source adapter, hosted auth, telemetry, production evidence row, or held-out eval material was added.

## Verification Intent

- Run the affected fixture, CLI, MCP, and Python SDK tests.
- Run the full public boundary and unit-test gate before pushing.
