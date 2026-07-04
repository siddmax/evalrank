# Private Golden-Eval Detached Transactions

Date: 2026-06-27

## What Changed

- Private Syndai eval-pipeline worker now runs live golden-eval adapter subprocesses outside DB transactions.
- Enrollment, candidate writes, and optional auto-promotion each use short private DB transactions.
- The per-pair subprocess timeout now covers the 20-case manifest's 5-minute per-case timeout budget, instead of killing the runner before per-case outcomes can be recorded.

## Boundary Decision

- This is private runtime orchestration only.
- Public EvalRank contracts, SDKs, CLI, MCP, fixtures, and schemas are unchanged.
- Candidate rows remain inactive until the private promotion gate validates and promotes them.

## Verification

- Private red/green tests covered the detached transaction shape and the full-manifest timeout budget.
- Private focused worker lane passed with `55 passed`.
- Private touched EvalRank lane passed with `92 passed`.
- Private touched-file antipattern scan and `ty check` passed.
- Target DB check confirmed the failed pre-fix refresh committed `0` candidate rows for `manual-evalrank-2026-06-26T22:07:03Z`.

## Coverage Rationale

- This fixes the root cause exposed by the real full-refresh attempt: holding an open transaction across long live adapter subprocesses caused `IdleInTransactionSessionTimeout`.
- The semantic refresh gate remains open until the detached live refresh produces validated candidate rows and projection/contamination are rebuilt from source-owned sanitized text.
