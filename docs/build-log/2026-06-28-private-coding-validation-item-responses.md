# 2026-06-28 Private Coding Validation Item Responses

## What Changed

- Private Syndai now projects terminal coding-validation observations into item-response rows for active coding-router agent identities.
- The private coding cache refresh runs that projection before pooled IRT, allowing validation evidence to influence calibration.
- Served cache replacement remains restricted to `coding-router-active-*`.

## Boundary

- This is private EvalRank schema work in Syndai.
- No public OpenAPI/SDK/CLI/MCP contract changed.
- No raw command/output/customer data is copied into the public repo.

## Verification

- Focused private validation/cache-refresh/projection tests: `8 passed`.
- Broader adjacent private source/projection lane: `30 passed`.
- Focused ruff and ty checks: passed.
- Private EvalRank migration-boundary check: passed.
- Private repo `make check`: passed.
- Public repo `make check`: passed with 223 Python tests and 7 TypeScript SDK tests.
- `git diff --check`: passed in both repos.
- Explicit touched-file trailing-whitespace scans: clean.

## Coverage Rationale

This improves recommendation accuracy before adding receipt readback or quota enforcement. It reuses the existing item-response and pooled-IRT path rather than adding a parallel scoring subsystem.
