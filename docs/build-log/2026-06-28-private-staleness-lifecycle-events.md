# 2026-06-28 Private Staleness Lifecycle Events

## What Changed

- Private Syndai now writes EvalRank source lifecycle facts when the coding-router staleness sweep removes stale source evidence rows.
- The existing append-only private `evalrank.source_evidence_events` lane now covers `stale_removed` rows and `superseded` snapshots when a replacement active source snapshot exists.
- The all-stale path records row-level stale-removal facts without weakening the existing private router invariant that active snapshots are non-empty.

## What Stayed Private Or Out

- No public persistence, source adapter, hosted runtime, or private benchmark data moved into this repo.
- Tombstones were not inferred from downstream caches. They stay out until a source-owned tombstone or retention signal exists.
- Live recommendation reads remain cache-backed; lifecycle events are audit/source semantics, not request-path work.

## Verification

- Private focused red/green lane:
  - `uv run pytest --no-cov tests/unit/features/evalrank/test_source_evidence_events.py tests/unit/scripts/test_router_staleness_sweep_lifecycle.py tests/scripts/test_evalrank_projection_scripts.py::test_coding_router_lifecycle_script_reuses_source_event_writer tests/scripts/test_evalrank_migrations.py::test_w1_source_evidence_events_migration_defines_append_only_l1_ledger -q`
  - Result: `9 passed`.
- Private broader focused lane:
  - `uv run pytest --no-cov tests/unit/features/evalrank/test_source_evidence_events.py tests/unit/scripts/test_router_staleness_sweep_lifecycle.py tests/unit/features/evalrank/test_adapter_imports.py tests/scripts/test_evalrank_projection_scripts.py tests/scripts/test_evalrank_migrations.py -q`
  - Result: `56 passed`.
- Private static checks:
  - `uv run ruff check ...`
  - `uv run ty check ...`
  - `uv run python scripts/check_evalrank_migration_boundary.py`
  - Result: passed.
- Private rollback DB proof:
  - `doppler run -- uv run pytest --no-cov tests/integration/features/coding/router/test_router_staleness_sweep_cli.py -q`
  - Result: `3 passed`.

## Coverage Rationale

This moves W1/W5 lifecycle coverage forward because stale source removals are now explicit source events rather than inferred from scorer or cache state. It does not complete tombstone/retention workers, broader source-adapter coverage, or W7 hosted/auth/billing parity.
