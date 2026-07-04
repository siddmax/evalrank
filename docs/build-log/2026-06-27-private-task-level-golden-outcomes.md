# Private Task-Level Golden Outcomes

Date: 2026-06-27

## Scope

- Public EvalRank remains storage-free and product-neutral.
- Private Syndai owns source evidence storage, DB migrations, live golden-eval artifacts, projection scripts, scorer rows, and cache materialization during incubation.
- This public log records only sanitized status evidence and boundary decisions.

## Built Privately

- Added a source-owned `golden_eval_case_results` payload on private coding-router evidence rows.
- Added a private EvalRank benchmark catalog row for task-level golden outcomes.
- Projected per-case golden outcomes into `golden-eval-task-v1` result rows and stable case-id item responses.
- Kept aggregate golden pass-rate rows as summaries, with `n_items` reflecting the number of underlying cases when case results exist.
- Backfilled the verified Claude Opus 20/20 proof into task-level rows, rebuilt projection, contamination, Stage-2, Stage-4, and materialized cache outputs, and verified Claude Opus remains ranked first.

## Evidence

- Golden result source: the previously verified current-schema Claude Opus 20-case snapshot.
- Task-level projection: 20 case-level golden result rows and 20 task-level item responses.
- Active input snapshot after projection: 3 candidates, 3 evidence rows, and 41 result rows.
- IRT behavior: correctly skipped because only one entity has task-level golden outcomes; the fix is broader comparable entity coverage, not lowering the model gate.
- Ranking behavior: risk-adjusted materialization still ranks `agent:syndai-coding:claude_code:claude-opus-4-8` first for `autonomous-swe-agent`.

## Boundary

- Keep private case text, retrieved text, traces, DB row ids, source migrations, and live adapter details in Syndai.
- Public EvalRank should only receive portable contracts, schemas, clients, public method notes, and storage-free reference behavior.

## Follow-Up

- Add comparable task-level outcomes for more entities/sources before publishing agent-lane IRT.
- Keep Pi and Codex candidate-only until their behavior gates pass.
- Do not rerun the same Claude proof as the default next slice.
