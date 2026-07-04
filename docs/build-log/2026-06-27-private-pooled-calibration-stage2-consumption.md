# Private Pooled-Calibration Stage-2 Consumption

Date: 2026-06-27

Scope: private Syndai EvalRank worktree only. This public log records the public-safe status update; no private schema rows, private fixtures, customer data, hosted runtime code, or Syndai implementation files were copied into the public EvalRank repo.

## What Changed Privately

- Stage-2 scoring now accepts an explicit calibration source and snapshot, separate from the active evidence source snapshot.
- Active route evidence remains scoped to the active coding-router EvalRank source.
- Pooled calibration rows may be consumed by Stage-2 only when the source and snapshot are explicitly provided.
- Stage-2 metadata records the calibration source and snapshot used for each calibrated row.
- Active candidates missing the required pooled calibration row receive `required_calibration_missing_v1` with score `0.0` and confidence `0.0` rather than the old fixed fallback.

## Evidence

- Private active source snapshot: `syndai-coding-router-evidence / coding-router-active-9d629dd4`.
- Private pooled calibration snapshot: `evalrank-pooled-item-responses / autonomous-swe-agent-pooled-current-plus-candidate-2026-06-27T115200Z`.
- Private Stage-2 rows rebuilt: 4.
- Private Stage-4 rows rebuilt: 4.
- Private active cache: `rec_93e4123d3ed37f1075e11544`.
- Active cache ranking:
  - Rank 1: Claude Opus, `stage2_calibrated=0.709694`, confidence `0.533259`.
  - Rank 2: Codex GPT-5.5, `stage2_calibrated=0.679625`, confidence `0.498494`.
- Claude Sonnet has pooled IRT score `0.094553` and remains outside the Stage-4 shortlist.
- Pi has `calibration_method=required_calibration_missing_v1`, `missing_required_calibration=true`, score `0.0`, confidence `0.0`, and is outside the active cache.

## Product Decision

When pooled calibration is explicit, missing calibration is a negative signal, not a neutral default. The best user experience is to rank only candidates with comparable measured calibration evidence ahead of candidates that lack the calibrated item-bank proof. This preserves active/candidate source boundaries while improving accuracy without extra live-eval spend or request-path latency.

Pi remains wired for future candidate evidence, but it is not rewarded in the active cache until it has comparable calibration evidence and passes the behavior gate.

## Public Boundary

The public EvalRank repo still owns product-neutral contracts, schemas, SDKs, CLI, MCP boundary, examples, and method notes. Private scorer rows, calibration rows, cache rows, and Supabase/Postgres migrations remain in Syndai's private `evalrank` schema until EvalRank has its own deploy/release path or dedicated Supabase project.
