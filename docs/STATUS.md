# EvalRank Status

Last updated: 2026-06-25

## Built

- Public Apache-2.0 repository scaffold.
- Public package boundaries for core, MCP, CLI, Python SDK, and TypeScript SDK.
- Root and scoped `AGENTS.md` guidance.
- `CLAUDE.md` shim to `@AGENTS.md`.
- Public boundary checker for private imports, disallowed coupling, excluded method markers, and missing package license/notice files.
- Public boundary checker guards for secret files, high-signal secret values, and held-out/private data paths.
- Core Python recommendation contracts in `packages/core`.
- Public core fixture factory for canonical example recommendation payloads.
- Public JSON Schemas for ranked entities and recommendations.
- Schema drift tests for core payload keys and public enum constants.
- Tests for core contracts, schema-contract drift, and public boundary rules.
- Public progress tracker and repo structure map.
- Public porting map for deciding what moves from Syndai/private workstreams into this repo.
- Direct `main` push workflow during scratch-build phase; branch protection is currently removed.
- `make check` local gate shared with CI.

## In Progress

- W0 public contract freeze.
- Public/private porting triage.
- Current source of truth is split between:
  - Python contracts in `packages/core/src/evalrank_core/contracts.py`
  - Public JSON Schemas in `schemas/`
  - Public porting decisions in `docs/PORTING.md`
  - Build-readiness docs in Syndai under `docs/superpowers/plans/evalrank/`

## Next

- Add an OpenAPI skeleton only when the first REST surface exists or a concrete route contract is ready.
- Add package-level implementation for the next public surface only after its contract is pinned.
- Add `NAVIGATION.md` when EvalRank has UI routes, API routes, deeplinks, or navigation-critical docs.

## Left

- W0: finish source-of-truth wiring, CI gate expansion, and W0 exit packet.
- W1+: data-plane tables, entity graph, evidence ledger, trust/security primitives, scorer stages, engine materializer, public surfaces, web, telemetry, governance, and GTM fleet.

## Update Rules

- Update this file when a feature lands, a wave gate changes, or an item moves between `Next`, `In Progress`, and `Built`.
- Keep dated build logs under `docs/build-log/` for immutable-ish snapshots; keep this file current.
