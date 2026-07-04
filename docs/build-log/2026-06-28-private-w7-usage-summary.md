# 2026-06-28 Private W7 Usage Summary

## What Changed

- Private Syndai now exposes keyed current-period EvalRank recommendation usage from persisted `recommend.called` facts.
- The private route is `GET /api/v1/evalrank/usage/current-period` and requires a customer bearer key with `evalrank:recommendations:read`.
- The response reports current period bounds, total/keyed/unique/domain counts, top domains, and an explicit non-enforced quota object.

## Boundary

- Usage facts stay in the private `evalrank` schema.
- Customer identity and API-key authorization stay in Syndai's shared control plane.
- No public `/v1` usage route, public persistence, hosted billing provider, hard quota enforcement, or public runtime was added to this repo.

## Verification

- Private focused helper/controller/migration lane: `9 passed`.
- Private focused ruff and ty checks: passed.
- Private EvalRank migration-boundary check: passed.
- Private target migration replay: EvalRank migrations already current.
- Private target index readback: `evalrank_recommend_events_consumer_period` exists on `(consumer_class, consumer_id, occurred_at DESC)`.
- Private repo `make check`: passed.
- Public repo `make check`: passed with 223 Python tests and 7 TypeScript SDK tests.
- Private post-format focused usage lane: `9 passed`.
- `git diff --check`: passed in both repos.

## Coverage Rationale

This advances W7 quota/billing groundwork by making usage visible from existing append-only facts. It does not complete billing settlement, receipts, webhooks, hosted/staging proof, or production latency/load proof.
