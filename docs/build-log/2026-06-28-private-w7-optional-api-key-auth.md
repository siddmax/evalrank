# 2026-06-28 Private W7 Optional API-Key Auth

## What Changed

- Private Syndai cached EvalRank recommendation routes remain anonymous-first.
- If a request sends `Authorization: Bearer ...`, Syndai now resolves it through the existing customer API-key control plane with `evalrank:recommendations:read`.
- Keyed recommendation calls emit external keyed `recommend.called` telemetry and persist key usage on successful cache-backed reads.
- The shared Syndai API-key scope catalog and plan/key DB constraints now admit the EvalRank read scope.

## Boundary

- EvalRank recommendation data, caches, scoring rows, grants, RLS, and EvalRank migrations stay in the private `evalrank` schema.
- The scope migration touches Syndai's existing `syndai` customer API-key control plane because identity and entitlement are shared Syndai infrastructure during incubation.
- No public OpenAPI auth scheme, public hosted auth flow, billing surface, or private credentials were added to this repo.

## Verification

- Private focused route/auth/migration/docs lane:
  - `uv run pytest --no-cov tests/unit/features/evalrank/test_controller.py tests/unit/features/evalrank/test_cache_reader.py tests/unit/features/evalrank/test_telemetry.py tests/test_app_di.py tests/unit/features/coding/test_customer_api_keys.py::test_default_customer_api_scopes_cover_public_run_lifecycle tests/unit/features/coding/test_customer_api_keys.py::test_coding_tenant_resolver_scopes_are_declared tests/unit/features/coding/test_customer_api_keys.py::test_scope_registry_matches_customer_api_key_db_check tests/unit/features/coding/test_evalrank_scope_migration.py tests/unit/features/coding/test_migration_contract.py::test_caas_entitlement_migration_registry_checks_plan_and_key_scopes tests/scripts/test_validate_docs_evalrank_contract.py -q`
  - Result: `52 passed`.
- Private static checks:
  - `uv run ruff check ...`
  - `uv run ty check ...`
  - `uv run python scripts/validate_migrations.py`
  - `uv run python scripts/check_evalrank_migration_boundary.py`
  - Result: passed.
- Full gates:
  - Private `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine` `make check`: passed after formatting, lint, type checking, static security guards, file-size checks, EvalRank migration-boundary checks, repository audits, and documentation checks.
  - Public `/Users/sidsharma/evalrank` `make check`: passed with 223 Python tests and 7 TypeScript SDK tests.
  - `git diff --check` in both repos: passed.

## Coverage Rationale

This advances W7 auth parity for cache-backed reads. It does not complete quota/billing, receipts, webhooks, hosted/staging proof, or production latency/load proof.
