# Private Stage-3 Materialize-Time Tie-Break

Date: 2026-06-27

## What Changed

- Private Syndai added a materialize-time Stage-3 tie-break hook behind the private EvalRank cache builder.
- Stage-3 remains outside the scorer ledger; no `stage3_llm_tiebreak` scorer rows are written or accepted.
- The private materializer can now accept a local `--stage3-tiebreak-file` adjudication artifact during cache builds.
- Public EvalRank contracts, SDKs, CLI, MCP, fixtures, and schemas are unchanged.

## Guardrails

- Stage-3 only applies to near-tied candidates that already passed Stage-4 shortlist membership.
- Stage-3 refuses unverified judge artifacts unless they declare blinded candidate identity, position-consistency pass, sanitized-only inputs, a rubric version, and rationale codes.
- Stage-3 does not apply when candidates carry contamination flags or when the score gap is not a tie.
- Stage-3 never changes persisted capability scores; when applied, it only changes materialized order and records `score_components.stage3_tiebreak`.

## Verification

- Private red/green materializer tests first failed on missing `stage3_tiebreak_decisions`, then passed.
- Private focused Stage-3/materializer/script lane passed with `17 passed`.
- The private materializer CLI help exposes `--stage3-tiebreak-file`.
- Target DB guardrail proof ran a valid Stage-3 decision file preferring Pi against active snapshot `coding-router-active-2026-06-27-detached-refresh`; the cache remained `rec_d03e376c9e516ffdf3d6fce5`.
- Read-only target DB proof showed no `stage3_tiebreak` score component in the active cache because the current active rows are not eligible for tie-break.

## Coverage Rationale

- This closes the materialize-time Stage-3 guardrail path without adding request-path latency, a new persistence layer, or fake LLM judge authority.
- Remaining work is promotion-quality refreshed evidence for carried active rows, Pi retrieved-text/runtime reliability, and broader source coverage.
