# 2026-07-22 — Re-ingest replay & freshness sidecar (private runtime wave)

## Scope

Private runtime change only. No public contract advances: the manifest, feeds,
ranking groups, schemas, methodology token, and per-feed horizons are all
unchanged, and the public contract SHA does not move. This entry records the
cross-repo pairing required by `AGENTS.md`; there is no public-repo code change.

## Paired SHAs

- Private Syndai runtime: `811bff51c` on `Syndai/main` (migration
  `2026_07_22_077_parser_run_last_verified_at` plus the persist/read-path
  changes).
- Public EvalRank contract: `548fb58ba65c26ff5569b23e28a9878908f29eee`
  (unchanged — runtime-only).

## Problem

After the cadence-freshness methodology wave (`899df619f`) forced a re-parse of
previously-seen upstream content instead of short-circuiting on the
bytes-unchanged path, preview feeds (e.g. `agents-last-exam-discovery`,
`webdev-arena-discovery`) quarantined with
`RuntimeError: parser run identity conflicts with immutable document` whenever
they re-ingested content already seen under a prior run.

Root cause: a parser run's identity (`run_id`, and transitively each
`observation_id`) is content-addressed with no timestamp, so re-fetching
unchanged bytes produces the same run identity — replay-stable by design. But
`completed_at`, derived from the wall-clock fetch time, is embedded in the
immutable run document. Every re-fetch drifted it, so the persist path's
immutable-document guard rejected the replay.

## What changed (private Syndai runtime)

- **Freshness split from identity.** `parser_runs` is append-only, so a new
  mutable sidecar `parser_run_freshness` carries `last_verified_at`, written only
  through a `SECURITY DEFINER` function (`record_parser_run_verification`, the
  same pattern as `advance_source_cursor`) that advances it forward-only. The
  immutable run document and observation identities stay frozen; re-verifying
  unchanged content advances only the freshness anchor.
- **All three freshness horizons read the anchor.** The explorer exactness gate
  (SQL function + Python builder), the decision repository, and the public
  ranked projection now derive their validity window (`observed_at`/`expires_at`,
  and the public `last_eval`/`next_refresh`/`stale` fields) from
  `last_verified_at`, so a re-verified benchmark stays fresh consistently across
  every surface instead of expiring early on one. The decision-window invariant
  relaxed to `observed_at >= completed_at`.
- **Replay never silently drops evidence.** The admitted set is resolved against
  the mutable entity catalog, so an alias approved between ingests can make
  identical bytes admit new configurations. A replay reuses the persisted
  observations only when the admitted configuration multiset is unchanged;
  otherwise it fails closed and re-quarantines for review.

## Why this is the right freshness model

The cadence-freshness wave established that evidence is "valid until the feed's
own next refresh," not until an arbitrary fixed clock. Re-verifying that
unchanged upstream content is still current is exactly that next refresh, so it
should extend the horizon — which requires a mutable verification timestamp
distinct from the immutable completion instant. Anchoring the window on the
frozen first-ingest `completed_at` would let a stable slow-cadence feed expire
despite being successfully re-verified every cycle.

## Verification

`make evalrank-integration-check` (disposable loopback PostgreSQL, zero skips)
and `make check` both pass. A regression test re-ingests identical content under
a new fetch timestamp (fails before, passes after) and asserts the freshness
window extends while identity stays frozen; a second test proves the
catalog-drift replay re-quarantines instead of dropping newly-resolvable
evidence.
