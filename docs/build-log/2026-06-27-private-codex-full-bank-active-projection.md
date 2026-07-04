# Private Codex Full-Bank Active Projection

Date: 2026-06-27

Scope: private Syndai worktree `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`.

Public EvalRank remains storage-free and product-neutral. No private benchmark text, retrieved text, traces, credentials, source rows, or DB migrations moved into this repo.

## What Changed Privately

- Reused the existing golden-eval pipeline writer to ingest a full `codex_cli / gpt-5.5` golden snapshot.
- Persisted the private Codex golden baseline in the Syndai worktree.
- Promoted measured Codex rows through the existing safe carry-forward router promotion path.
- Rebuilt the private EvalRank projection, item responses, contamination rows, Stage-2 rows, Stage-4 rows, and active materialized cache for `autonomous-swe-agent`.

## Evidence

- Codex full-bank artifact: `task_count=20`, `pass_count=19`, `pass_rate=0.95`.
- Category results: `coding_repair=10/10`, `site_clone=4/5`, `review_only=5/5`.
- Active private router snapshot: `9d629dd4-8b0e-40c9-ada1-c2b6d33790e0`.
- EvalRank snapshot: `coding-router-active-9d629dd4`.
- Projection counts: 4 stage candidates, 67 result rows, 40 task results, 61 item responses, 268 contamination rows, 4 Stage-2 rows, and 4 Stage-4 rows.
- Active cache: `rec_bc07b8cef6253fa87584049a`, with Claude Opus ranked first and Codex GPT-5.5 ranked second.
- IRT behavior: correctly skipped because the comparable agent task matrix still has 2 entities and 1 informative item.

## Product Call

Codex is now active measured evidence, not only an admission smoke. It is not the default winner: Claude Opus remains rank 1 in the private active cache.

The best next long-term slice is another comparable full-bank entity/source that adds informative task outcomes for agent-lane IRT. Do not lower IRT thresholds, rerun the same Claude proof as default work, or promote Pi until its full-bank behavior gate clears.
