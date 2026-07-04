# 2026-06-28 - Private Keyed Quota Enforcement

Private Syndai worktree update only; no public runtime or private schema was added to this repo.

## Summary

- Keyed cached recommendation reads now enforce configured private monthly quota rows before recording a successful `recommend.called` fact.
- Over-quota keyed callers receive `429` with `Retry-After`, rate-limit/quota headers, and an explicit cached recommendation fallback payload.
- Anonymous and first-party reads keep the existing active-cache path.
- The implementation reads from the private `evalrank` schema; Syndai customer API-key identity remains shared Syndai auth infrastructure.

## Validation

- Private red regressions failed first for the missing quota-state helper and route branch.
- Private focused controller/usage tests passed with `10 passed`.
- Private adjacent EvalRank unit/source lane passed with `160 passed`.
- Private focused ruff and ty checks passed.
- Private EvalRank migration-boundary check passed.
