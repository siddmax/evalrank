# SDK Retry-After Parser Hardening Plan

**Goal:** Keep public SDK Problem Details errors stable when a remote response sends a malformed `Retry-After` header.

**Architecture:** Preserve the existing explicit HTTP(S)-only SDK clients. Parse `Retry-After` as non-negative integer seconds only; if parsing fails, expose no retry hint while still raising the public Problem Details error.

**Boundary:** Do not add retry loops, hosted policy, auth, service discovery, telemetry, private DTOs, environment-variable defaults, or live-service assumptions.

## Steps

- [x] Add failing Python SDK regression for malformed `Retry-After`.
- [x] Add failing TypeScript SDK regression for malformed `Retry-After`.
- [x] Verify both tests fail for the current parser behavior.
- [x] Implement strict parser behavior in Python and TypeScript.
- [x] Verify focused SDK tests pass.
- [x] Update status, porting, tests, and build-log docs.
