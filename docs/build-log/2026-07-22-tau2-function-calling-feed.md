# 2026-07-22 — tau2-bench + tau-voice feed admission (function-calling 2nd family, customer-support cell)

## Scope

Public catalog advance. The public catalog admits the tau2-bench and tau-voice
families/feeds (`discovered` → `shadow`), giving the function-calling cell its
second independent family (an agent-system family, distinct from the existing
model-configuration family) and lighting up the previously-empty
customer-support cell with explorer evidence.

## What changed (public EvalRank)

- Promote the `tau2-bench` family and `tau2-bench-discovery` feed to `shadow`,
  bound to the MIT-licensed Sierra Research tau2-bench leaderboard submissions
  (`https://github.com/sierra-research/tau2-bench`). tau2-bench is an
  agent-system family spanning two candidate cells (`function-calling`,
  `customer-support`) and carries both ranking-group ids.
- Promote the `tau-voice` family and `tau-voice-discovery` feed to `shadow`
  (candidate cell `customer-support`, sourced from the Sierra research site).
- Both feeds declare `correlated_family_group: tau2`, so tau2-bench and
  tau-voice are never counted as independent evidence against one another.
- Dated MIT rights evidence recorded in `research-provenance.json` for both
  families: eight direct-source/inference claims each, with
  `harness_code_license: not-applicable-repo-data-view` (the feed ingests
  published leaderboard result JSON, not harness code) and `task_data_license:
  MIT`.
- The reference server now reports the `customer-support` cell as `preview`
  (it has an implemented feed for the first time); the `benchmark-health`
  contract test is updated to reflect the one cell moving from `unavailable`
  to `preview`.
- Manifest/feeds/provenance regenerated; `make check` green (237 py + 44 TS).

## Metric shape

Per (submission, domain) proportion: each submission's per-domain `pass_1`
percentage becomes one proportion observation, keyed by the upstream submission
directory (which uniquely distinguishes configuration variants that share a
display name). Domains without a reported score are skipped; the sparse
per-submission domain matrix is handled by the ranking group's overlap logic
rather than by cross-domain averaging. Live-verified against the upstream
leaderboard: 47 text observations across 20 submissions and 36 voice
observations across 12 submissions, all in the unit interval.

## Verification

- `make check` green.

## Public SHA

- Public EvalRank: `34b17733c19d831f546524721f3f5a9e0bb2190e`
