# 2026-06-28 Private W7 Billing Settlement

Public-safe summary of private Syndai EvalRank progress.

- Added a private async settlement/readback path over successful keyed external `evalrank.recommend_events`.
- Kept Stripe meter-event calls out of the ranking request path.
- Stored provider event, invoice, and receipt readback in private `evalrank.recommend_billing_settlements`.
- Reused the existing private coding webhook worker to dispatch due EvalRank billing settlements instead of adding another worker or queue.
- Applied the private target DB migration and verified the settlement table, two RLS policies, and three indexes.
- Target DB currently has zero billable keyed external recommendation facts, so no real settlement row was enqueued.
- Ran a rollback-only target proof that enqueued one synthetic pending settlement row and rolled back to zero synthetic recommend/settlement rows.
- Remaining work: provision Stripe meter/product configuration, produce real billable keyed recommendation facts, run a live settlement cycle, and pin any authenticated receipt/readback contract before exposing it.

No public API, SDK, CLI, MCP, schema, hosted billing route, or public storage contract changed.
