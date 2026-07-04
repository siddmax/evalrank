# 2026-06-28 Private W8 OTel Semantic Attributes

Public-safe status note: the private Syndai worktree standardized EvalRank recommendation telemetry on official OpenTelemetry HTTP server attribute names for successful cached recommendation reads.

The private route path now attaches `http.request.method`, `http.route`, and `http.response.status_code` alongside existing private EvalRank span fields. It also adds a safe helper for future GenAI scorer or judge spans that emits non-content operation/model/token attributes only.

Cached recommendation reads remain cache reads, not live inference, so they intentionally do not set `gen_ai.*` attributes. No public EvalRank contract, hosted telemetry export, private fact table, runtime secret, or UI route was added in this public repo.

Local private verification passed for the OTel helper, telemetry emission, and controller route wiring. The broader W8 observability gate remains open for hosted trace export, daily rollups, load proof, and live verdict/usage UI.
