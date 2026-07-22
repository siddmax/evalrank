# 2026-07-22 — Vision-multimodal feed admission (Video-MME via Epoch hub)

## Scope

Public contract advance + paired private runtime wave. The public catalog admits
the Video-MME family/feed (`discovered` → `shadow`), lighting up the
vision-multimodal cell with explorer evidence. This entry records the cross-repo
pairing required by `AGENTS.md`.

## What changed (public EvalRank)

- Promote the `video-mme` family and `video-mme-discovery` feed to `shadow`,
  bound to the daily CC-BY-4.0 Epoch benchmark bundle
  (`https://epoch.ai/data/benchmark_data.zip`) via the existing Epoch-hub mirror
  adapter. The feed declares `correlated_family_group: video-mme`, so it is never
  counted as independent evidence against a future first-party Video-MME feed.
- Dated CC-BY-4.0 rights evidence recorded in `research-provenance.json`
  (Epoch-hub mirror pass-through), matching the six existing Epoch-hub feeds.
- Manifest/feeds/provenance regenerated; `make check` green (234 py + 44 TS).

## What changed (private Syndai runtime)

- Bind the `video-mme-discovery` feed to a one-line `EpochHubFeedSpec`
  (`video_mme_external.csv`, score column `Overall (no subtitles)`, a unit-interval
  proportion) — no new adapter, reusing the Epoch-hub machinery. Live-verified:
  50 observations parse and normalize end-to-end from the live bundle.
- New append-only methodology identity `2026-07-22.2.vision-multimodal-feed`
  (migration 078), bound to the new public contract SHA. Aggregation and
  freshness semantics are inherited unchanged from `2026-07-22.1.cadence-freshness`;
  the migration re-binds the admission-gated two-argument `enqueue_scheduler_tick`
  to the new token and inserts the newly-pinned manifest's per-feed freshness
  horizons (13 feeds, keyed by the new manifest sha).
- Test-suite DRY-ing: the pipeline-runs demote fixture and the cadence-row
  migration test now derive from the live registration set / a union across
  migrations, so future feed-admission waves do not have to touch them.

## Verification

- Public: `make check` green.
- Private: 1151 evalrank+frontier unit tests green; `make
  evalrank-integration-check` green on a disposable Postgres (migration 078
  applies in sequence after 076/077, scheduler cutover + cadence rows validated).
- Deployed: production Deploy Backend succeeded; the live DB carries migration
  078, the new methodology row, all 13 cadence rows under the new manifest sha,
  and the cron scheduler tick now calls the two-arg overload with the new token.

## Paired SHAs

- Public EvalRank: `47f2f1fc9deddab8f549e218da1c86c0be92f955`
- Private Syndai: `6fe7f78f59278c71ee00ee976799b17fa242a438`
