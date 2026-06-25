# W1 Entity Evidence Contracts

Date: 2026-06-25

Scope: public, storage-free contracts only.

## Built

- `EntityRef` and `EvidenceItem` dataclasses in `packages/core`.
- Public fixture helpers for reusable entity and evidence examples.
- `schemas/evidence-item.schema.json` with strict top-level payload keys.
- Schema drift tests tying `EvidenceItem.to_dict()` and `EVIDENCE_KINDS` to the public schema.

## Not Built

- No database migrations.
- No private evidence rows, telemetry, customer traces, or held-out eval material.
- No scorer engine, graph materializer, API route, CLI command, SDK method, or MCP tool.

## Verification

- Red tests failed before implementation on missing contract exports and missing schema.
- Focused core and schema tests passed after implementation.
- `make check` passed with 19 unit tests and the public boundary scanner.
