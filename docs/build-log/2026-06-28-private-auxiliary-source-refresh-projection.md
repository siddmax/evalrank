# Private Auxiliary Source Refresh Projection

## What Changed

- The private Syndai worktree added a projection-only auxiliary source refresh helper for current EvalRank source adapters.
- The private worker now refreshes auxiliary source snapshots after successful non-dry active coding-router cache refreshes.
- Auxiliary refreshes do not replace the served `autonomous-swe-agent` cache; the private materializer still requires `coding-router-active-*` snapshots by default for that served cache.
- Empty dogfood sources are reported as skipped instead of becoming fabricated evidence.

## Boundary

- This public repo did not gain private source adapters, DB clients, hosted scheduler code, request-path scorer code, or private fixtures.
- Derived EvalRank rows remain private-side work in the dedicated private `evalrank` schema.
- Syndai-owned private source reads remain private incubation inputs.

## Verification

- Private red regression failed before implementation.
- Focused private auxiliary refresh lane: `11 passed`.
- Broader private worker/refresh lane: `61 passed`.
- Focused private ruff and ty checks passed.
- Target DB auxiliary projection proof projected 303 real candidates and skipped 1 empty dogfood source.

## Coverage Rationale

This moves W5 source-refresh orchestration forward without over-hardening: existing source adapters now refresh from the worker path, served recommendation UX remains cache-first, and dogfood remains blocked until real terminal dogfood source rows exist.
