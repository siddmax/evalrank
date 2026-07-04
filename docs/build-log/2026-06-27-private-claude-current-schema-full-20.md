# Private Claude Current-Schema Full 20

Date: 2026-06-27

## Scope

- Public EvalRank remains storage-free and product-neutral.
- Private Syndai owns the live runner, target DB writes, private golden-eval artifacts, and private `evalrank` schema cache/scorer rows.
- This public log records only public-safe status evidence and boundary decisions.

## Built Privately

- Verified the current-schema full golden snapshot for `claude_code / claude-opus-4-8` at `/tmp/syndai-evalrank/claude_opus_current_schema_full_20.json`.
- Enrolled CLI-native bare model id `claude-opus-4-8` into the private coding-router candidate lane.
- Promoted the three eligible Claude Opus rows through safe carry-forward promotion into active coding-router snapshot `4bc65212-ee5a-4ca0-bc65-8531e894bc86`.
- Rebuilt EvalRank projection, contamination checks, Stage-2 scorer rows, Stage-4 scorer rows, and the active materialized cache for `autonomous-swe-agent`.
- Risk-adjusted contamination-aware scorer rows so fresh 20/20 evidence outranks stale temporal-cliff rows.

## Evidence

- Golden snapshot: `dry_run=false`, `partial_run=false`, `task_count=20`, `pass_count=20`, `pass_rate=1.0`.
- Category pass rates: `coding_repair=10/10`, `site_clone=5/5`, `review_only=5/5`.
- Semantic provenance: benchmark and retrieved text are present for all 20 cases.
- Cost: `cost_per_task_usd_p50=0.049259`.
- Eval run id: `manual-claude-opus-current-schema-2026-06-27T09:23:54Z`.
- EvalRank input snapshot: `coding-router-active-4bc65212`.
- Active cache: `rec_2400b7cea2727fce69d23d37`.
- Ranked first: `agent:syndai-coding:claude_code:claude-opus-4-8`.

## Follow-Up

- Do not rerun the same Claude proof as the next default gate.
- Broaden task-level golden outcome rows across more entities/sources so agent-lane IRT can fit over informative responses instead of aggregate all-pass evidence.
- Keep Pi and Codex candidate-only until their behavior gates pass.

## Boundary

- Keep private golden traces, task text, retrieved text, database writes, migrations, and live adapter promotion in the Syndai worktree.
- Public EvalRank continues to own contracts, schemas, clients, public method notes, and storage-free reference behavior.
