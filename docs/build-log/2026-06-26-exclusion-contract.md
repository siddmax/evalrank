# Exclusion Contract Build Log

Date: 2026-06-26

## Built

- `Exclusion` public dataclass in `evalrank_core.contracts`.
- `sample_exclusion()` public fixture in `evalrank_core.fixtures`.
- Closed draft 2020-12 `schemas/exclusion.schema.json`.
- `Recommendation.exclusions` now serializes `Exclusion` rows through the public schema.
- Python SDK re-export and TypeScript `Exclusion` interface.
- CLI `fixture exclusion` and MCP `exclusion` fixture support.
- Public docs/status/porting updates that route exclusions-with-reasons to public/private workstreams.

## Not Built

- No Stage-0 gate policy.
- No private reason taxonomy.
- No source adapters, graph lookup, storage, telemetry, hosted auth, or live scorer behavior.
- No held-out evals, benchmark answers, private traces, or production exclusion data.

## Port Assessment

- Public Contracts owns `Exclusion` because it is a portable, storage-free subject plus public reason/detail row.
- Methods / Schemas owns the public vocabulary that ranking or abstention may emit exclusions-with-reasons.
- SDK / CLI / MCP owns deterministic fixture surfaces for `exclusion`.
- Scoring / Materializer Runtime keeps gate policy, constraint evaluation, private reason taxonomy, and live scorer behavior private until public-input-only pieces are separable.
- Evaluation Integrity keeps held-out exclusion cases, graders, traces, and benchmark outputs private.

## Verification

- `python3 -m unittest tests.test_core_contracts tests.test_core_fixtures`
- `python3 -m unittest tests.test_schema_contracts tests.test_sdk_python tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `python3 -m unittest tests.test_cli_fixture tests.test_mcp_fixture`
- `make check`
- `PYTHONPATH=packages/core/src:packages/cli/src python3 -m evalrank_cli fixture exclusion`
- Public secret scan over docs, packages, schemas, tests, scripts, and CI paths.
- `git diff --check`
- GStack pre-landing review logged clean after a contract strictness fix.
- Ponytail review.
