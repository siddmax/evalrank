# 2026-06-29 Private W7/W8 Staging Smoke Nonlocal Guard

Private Syndai worktree update only. The private W7 staging parity smoke and W8 recommendation load smoke commands now accept `--require-non-local-base-url` for hosted-proof runs.

When set, the commands reject localhost, loopback, private, link-local, reserved, multicast, unspecified IP hosts, `.localhost`, and `.local` hostnames before any request is made. Local development defaults are unchanged.

Public boundary: no public route, schema, SDK, CLI, MCP, billing, telemetry, persistence, or hosted contract changed in this repo.

Verification summary:

- Red test run failed first because the flag did not exist.
- Focused private smoke tests passed with `14 passed`.
- Focused private ruff check passed for the touched scripts/tests.

Remaining: hosted/staging proof still requires a deployed API base URL and keyed staging credential. No browser/account setup was performed.
