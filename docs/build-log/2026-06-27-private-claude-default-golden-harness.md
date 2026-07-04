# Private Claude Default Golden Harness

## What Changed

- Private Syndai golden-eval work established Claude as the default promotion candidate for the current EvalRank golden-eval gate.
- The private runner now preserves unknown executor cost as null so dry/not-run/unmetered rows do not distort p50 cost.
- Public EvalRank remains storage-free and product-neutral; no private traces, schemas, credentials, or hosted runtime code moved into this repo.

## Evidence

- Private live proof: `claude_code / claude-opus-4-8` reached 20/20 overall with 10/10 coding-repair, 5/5 site-clone, and 5/5 review-only.
- Pi remains candidate-only; its latest private full run improved but did not clear the promotion bar.
- Codex authenticates and runs but failed the simple off-by-one smoke by making no edit, so it is not promotion-ready.

## Caveat

- The private 20/20 artifact is pass/governance evidence, not valid for refresh by itself. This caveat was superseded later on 2026-06-27 by the current-schema Claude Opus full-20 promotion recorded in `docs/build-log/2026-06-27-private-claude-current-schema-full-20.md`.

## Verification

- Public `make check` passed after recording this public-safe status update.
- Private focused runner/worker/router validation passed with `107 passed`; private docs validation passed with `16 passed`; runner ruff and private `git diff --check` passed.

## Boundary

- Keep EvalRank public focused on contracts, schemas, clients, public method notes, and storage-free reference behavior.
- Keep private golden traces, database refreshes, and live adapter promotion in the Syndai worktree until a separable public contract is deliberately extracted.
