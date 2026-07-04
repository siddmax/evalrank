# Private Semantic Text Provenance Ingress

Date: 2026-06-27

## What Changed

- Private Syndai EvalRank now has a redacted semantic-text provenance ingress path for coding-router projection rows.
- The private adapter can carry optional sanitized benchmark/retrieved text into `evalrank.result_rows.provenance`, where existing semantic contamination checks already consume it.
- The helper stores redacted text plus stable sanitized-text fingerprints, keeping the logic source-owned and private.

## What Stayed Private

- No public EvalRank schemas, SDKs, CLI, MCP tools, or examples changed.
- No private prompts, traces, held-out tasks, answers, customer data, or raw benchmark text were copied into this repo.
- Current live aggregate coding-router rows still lack stable benchmark/retrieved text metadata, so semantic contamination rows remain `unknown` until source adapters provide real sanitized text.

## Verification

- Private red/green unit test: `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py::test_coding_router_projection_populates_sanitized_semantic_text_provenance -q`
- Private focused behavior: `uv run pytest --no-cov tests/unit/features/evalrank/test_capability_inputs.py tests/unit/features/evalrank/test_contamination_checks.py -q` passed with `22 passed`.
- Private static checks: touched-file antipattern scan and `ty check` passed.
- Target source probe confirmed the live coding-router evidence table has no dedicated text columns and only short unstructured `notes`.
- Target projection smoke wrote `2` active coding-router candidates.
- Target contamination smoke rebuilt `60` rows; the `15` semantic rows remain `unknown / insufficient_metadata`, which confirms the new ingress does not fake semantic cleanliness when source text is absent.

## Coverage Rationale

- This moves the private semantic contamination path from checker-only to adapter-ingress-ready.
- It does not justify marking the live semantic contamination gate green because the current target source still cannot supply truthful sanitized text.
