# 2026-07-22 — Cadence-freshness methodology (private runtime wave)

## Scope

Private runtime change only. No public contract advances: the manifest, feeds,
ranking groups, schemas, and eligibility constants are unchanged, and the new
methodology reuses the existing public contract SHA. This entry records the
cross-repo pairing required by `AGENTS.md`; there is no public-repo code change.

## What changed (private Syndai runtime)

The explorer "freshness" validity horizon changed from a single global 7-day
cap to a **per-feed horizon** equal to each feed's own pinned
`cadence.stop_recommending_after_seconds`. The public catalog already declares
these horizons (7 days for the fast feeds, up to 730 days for slow academic
benchmarks), so the change is a runtime methodology that reads the horizons the
public manifest already publishes — the contract does not move.

- New append-only methodology identity `2026-07-22.1.cadence-freshness`, bound
  to the same public contract SHA as the vetted-feed wave. Explorer evidence is
  now valid until the feed's own next expected refresh, symmetric on the Python
  and SQL sides.
- The remaining runtime fixes let all twelve vetted-feed sources flow
  end-to-end: multi-ranking-group feeds (e.g. HLE, SimpleQA-Verified) persist
  one explorer snapshot per group; re-attested alias evidence from a new dated
  artifact no longer conflicts with the prior attestation; authenticated
  read-only egress for public GitHub and HuggingFace fetches (host-scoped, never
  forwarded across a redirect); and deterministic upstream schema drift is
  separated from transient mid-fetch races in the retry taxonomy.

## Freshness model — why per-feed, not a higher global cap

A survey of public leaderboards and aggregators (LMArena, HELM, Epoch AI
Benchmarking Hub, the archived Open LLM Leaderboard, Artificial Analysis,
LiveBench) found none that hard-expire evidence on a fixed clock: they date and
version results and let the benchmark's own cadence drive refresh. A per-feed
horizon is the exact-verification analog of that pattern — a slow academic
benchmark stays valid until its next expected update instead of being marked
stale after an arbitrary week, while a weekly arena feed still expires weekly.
The horizon is authored once, in the pinned public manifest, and enforced
identically in the runtime methodology.

## Paired SHAs

- Public EvalRank (`/Users/sidsharma/evalrank`, `main`): this entry; no code
  change, public contract SHA `548fb58ba65c26ff5569b23e28a9878908f29eee`
  unchanged.
- Private Syndai runtime: `main` at `899df619f`, methodology
  `2026-07-22.1.cadence-freshness`, migration
  `2026_07_22_076_register_cadence_freshness_methodology`.
