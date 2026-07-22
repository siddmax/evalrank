# Plan: `frozen` (once-only) cadence mode — consume the shipped primitive

**Date:** 2026-07-22
**Lane:** Heavy (cross-repo: public evalrank contract + Syndai runtime)
**Owner decision (locked):** reuse existing `frozen` mode (no `one_shot` rename); once-only gate lives in `dispatch_scheduler_tick` (keep the builder pure).

## What the Understand stage changed about the task

The prompt's design sketch is ~40% already done and one name is wrong:

- The public manifest schema **already ships `frozen`** as a cadence mode (`schemas/evalrank-manifest.schema.json`, enum `["frozen","periodic",null]`) with a full validation branch (`as_of` + `upstream_version` required, all `*_seconds` null) AND a test asserting its shape (`tests/test_catalog_manifest.py:996`). Syndai's `catalog.py` already parses `mode` as a free string, so `frozen` round-trips today.
- Therefore: **no new enum, no manifest-pin bump, no methodology migration for a schema change.** The sketch's "full wave flow" collapses.

What is genuinely missing is every *consumer* of `frozen`:
1. `feed_policy.evaluate_feed_policy` rejects `frozen` (`cadence_not_periodic` + `cadence_window_incomplete`, since frozen has null seconds) → a frozen feed can only be ingested manually.
2. `build_due_pipeline_runs` reads `cadence.expected_seconds` and **raises `RuntimeError` on null** → it crashes on any frozen feed that passes the refresh gate.
3. No once-only gate: nothing checks "already ingested" to stop re-fetching.
4. No `cadence_deadline_missed` suppression for feeds that have no deadline.

## Newly-discovered tension (belongs in eng-review, NOT resolved here)

Migration 076's `explorer_snapshot_relations_are_exact` reads each feed's freshness horizon from `evalrank.manifest_feed_cadence.stop_recommending_after_seconds` and **fails closed when it is null** (line 162). Frozen feeds have `stop_recommending_after_seconds = null` by schema. So a frozen feed's evidence, once ingested, **cannot currently enter an explorer snapshot** — which contradicts the goal ("scrape once and feed into rankings").

This is NOT a blocker for landing the primitive: no live feed is frozen today. But the explorer-freshness path for frozen evidence is unresolved. Options to raise at eng-review:
- **(A) Defer** — land the ingest primitive only; frozen evidence reaching explorer is a follow-up wired with the first real frozen feed (MedHELM). Cleanest, matches "clean standalone primitive."
- **(B) Give frozen feeds a horizon now** — frozen feeds still get a `manifest_feed_cadence` row (a long fixed horizon), so `as_of`-anchored evidence ages naturally. Requires a methodology/migration decision about how a frozen horizon is measured (from `as_of`, not from `observed_at`?).

Recommendation: **(A) defer** — the owner explicitly framed this as a primitive to add "when the first genuinely-frozen source is wired," and no downstream consumer needs frozen explorer evidence today. Landing (B) speculatively couples this to an explorer-freshness redesign with no live driver (YAGNI).

## Scope of THIS change (assuming eng-review confirms defer)

### Public repo (`/Users/sidsharma/evalrank`)
- **No schema change** (`frozen` already present). Confirm the existing frozen test still passes.
- Possibly a build-log entry recording the paired SHAs (per AGENTS.md wave rule) — but no methodology migration since the public contract does not advance.

### Syndai (`/Users/sidsharma/Syndai/backend`)
1. `feed_policy.py` — allow `frozen` through the **refresh** gate:
   - Replace `if cadence.mode != "periodic": cadence_not_periodic` with: accept `mode in {"periodic","frozen"}`; for `frozen`, skip the `*_seconds` completeness/ordering checks (they are null by contract) and require `as_of` + `upstream_version` present instead. Keep `cadence_not_validated` for `status != "validated"`.
   - Do NOT touch the `scheduled_io_allowed` (publish) gate beyond what refresh already implies — frozen feeds schedule refresh, and their once-only run is the ingest.
2. `pipeline_runs.py`:
   - `build_due_pipeline_runs` — for a `frozen` feed, `expected_seconds` is null. Mint a slot without a cadence period. Two sub-options (eng-review picks):
     - keep the run identity keyed on a stable frozen slot (e.g. floor to a fixed epoch or use `as_of`), with a synthetic/large `cadence_expected_seconds` so `pipeline_run_spec`'s `>0` invariant holds and `deadline_at` is far future → the `cadence_deadline_missed` branch can never fire.
     - OR make `cadence_expected_seconds`/`deadline_at` optional for frozen and branch the deadline logic. (Larger blast radius on `PipelineRunSpec` invariants.)
   - Prefer the **synthetic-far-future-deadline** option: smallest diff, `deadline_at` in the far future means `dispatch_time > run.deadline_at` is always false, so `cadence_deadline_missed` is structurally impossible for frozen. `ponytail:` comment naming the ceiling.
3. `dispatch_scheduler_tick` — the **once-only gate**: before inserting, for `frozen` feeds, skip if the feed already has a `source_cursors.last_good_parser_run_id` (already-ingested). One bounded query alongside the existing `feed_refresh_paused` check. Non-frozen feeds unaffected.
4. Tests (Syndai): a `frozen` feed (a) passes the refresh gate, (b) produces exactly one due run when it has no cursor, (c) produces **zero** due runs once a `last_good_parser_run_id` cursor exists, (d) **never** emits `cadence_deadline_missed`.

## Out of scope (explicitly)
- No `one_shot` rename.
- No manifest-pin bump / no new methodology version (public contract unchanged).
- Frozen explorer-freshness horizon (deferred per option A — follow-up with MedHELM).
- No manual decay logic (owner: evidence ages via existing horizons; frozen just stops being re-fetched).

## Verification
- Public: `python3 -m unittest discover tests` + `python3 scripts/check_public_boundary.py --root .` (should be a no-op diff-wise; frozen already there).
- Syndai: the new frozen scheduler tests + existing pipeline_runs / feed_policy suites green.

## Paired-SHA record
Per AGENTS.md: if the public repo gets any commit (build-log entry), record public EvalRank SHA + private Syndai SHA in a `docs/build-log/` entry. If the public repo needs NO change at all, note that in the Syndai-side record instead.
