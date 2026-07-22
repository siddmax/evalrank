# 2026-07-22 — Vision-multimodal feed admission (Video-MME via Epoch hub)

## Scope

Public catalog advance. The public catalog admits the Video-MME family/feed
(`discovered` → `shadow`), lighting up the vision-multimodal cell with explorer
evidence.

## What changed (public EvalRank)

- Promote the `video-mme` family and `video-mme-discovery` feed to `shadow`,
  bound to the daily CC-BY-4.0 Epoch benchmark bundle
  (`https://epoch.ai/data/benchmark_data.zip`) via the existing Epoch-hub mirror
  adapter. The feed declares `correlated_family_group: video-mme`, so it is never
  counted as independent evidence against a future first-party Video-MME feed.
- Dated CC-BY-4.0 rights evidence recorded in `research-provenance.json`
  (Epoch-hub mirror pass-through), matching the six existing Epoch-hub feeds.
- Manifest/feeds/provenance regenerated; `make check` green (234 py + 44 TS).

## Verification

- `make check` green.

## Public SHA

- Public EvalRank: `47f2f1fc9deddab8f549e218da1c86c0be92f955`
