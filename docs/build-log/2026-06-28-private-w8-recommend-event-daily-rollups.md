# 2026-06-28 Private W8 Recommend-Event Daily Rollups

Public-safe status note: the private Syndai worktree added a derived daily rollup substrate over private EvalRank recommendation facts.

The private rollup groups append-only `recommend.called` facts by UTC date, domain, surface, consumer class, and status. It stores count and latency summaries for later SLI/readback surfaces without mutating raw telemetry facts.

No public EvalRank contract changed. The public repo still does not own hosted telemetry export, private fact storage, deployed rollup jobs, dashboards, customer data, or runtime secrets.

Local private verification passed for the rollup helper and migration-contract tests. Target DB proof applied the rollup migration and refreshed one derived daily row from two existing recommendation facts. The broader W8 observability gate remains open for scheduled refresh ownership, hosted trace/export proof, load proof, and the live verdict/usage UI.
