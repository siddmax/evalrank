# Private Detached Golden Refresh

Date: 2026-06-27

## What Changed

- The private Syndai detached golden-eval path ran a real full refresh for `manual-detached-evalrank-2026-06-26T23:23:24Z`.
- The refresh wrote six private coding-router candidate evidence rows without holding a DB transaction open during adapter subprocess execution.
- The existing private promotion gate approved only the Claude review-only row and produced active coding-router snapshot `baebe224-dc7a-4f93-b7fc-6b487ce9bad6`.
- Private EvalRank projection, contamination checks, Stage-2 scorer rows, Stage-4 scorer rows, and materialization were rebuilt for `coding-router-active-2026-06-27-detached-refresh`, emitting active cache `rec_d03e376c9e516ffdf3d6fce5`.

## Boundary Decision

- This remains private Syndai runtime and private `evalrank` schema work.
- Public EvalRank contracts, SDKs, CLI, MCP, fixtures, and schemas are unchanged.
- Source-owned semantic text stays in the private `syndai` source table; derived projection, contamination, scorer, and cache rows stay in the private `evalrank` schema.

## Verification

- Detached dry run found 2 active pairs and made no ledger writes.
- Live refresh committed six candidate rows: three Claude rows with benchmark and retrieved text, and three Pi rows with benchmark text but no retrieved text.
- Promotion approved only `claude_code / claude-sonnet-4-6 / review_only` with pass rate `1.0`; Claude coding-repair/site-clone and all Pi rows stayed candidate-only.
- Reprojection wrote 2 candidates, 2 evidence items, and 15 result rows.
- Contamination rebuild wrote 60 rows: 15 clean source-overlap, 15 clean fingerprint-overlap, 15 high-severity temporal-cliff, 3 clean semantic-overlap, and 12 semantic `unknown`/`insufficient_metadata`.
- Stage-2 and Stage-4 scoring each wrote 2 scorer rows.
- Materialization emitted `rec_d03e376c9e516ffdf3d6fce5` with Claude ranked first and `potential_contamination` caveats preserved.
- Private focused EvalRank pytest lane passed with `88 passed`, and private docs contract lane passed with `16 passed`.
- Private root `make check` passed after the oversized worker test file was split under the repo's 800-line file-size gate.
- Public EvalRank `make check` passed with 223 Python tests plus TypeScript SDK syntax/test checks.

## Coverage Rationale

- This closes the detached-refresh execution gate and proves source-owned semantic text can move semantic checks out of `unknown` when refreshed promoted rows provide retrieved text.
- It does not close the semantic coverage gate for all active rows. Carried last-good rows without refreshed retrieved text must remain explicit `unknown` instead of being treated as clean.
- The next ordered work is to replace remaining carried active rows only when refreshed candidates clear the promotion bar, fix the Pi runtime/retrieved-text path before it can influence ranking, and add Stage-3 materialize-time tie-break behavior only after sanitized text and judge guardrails exist.
