# Private Codex Admission Smoke

Date: 2026-06-27

Scope: private Syndai worktree `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine`.

Public EvalRank remains storage-free and product-neutral. No private benchmark text, credentials, source rows, or DB migrations moved into this repo.

## What Changed Privately

- Fixed the Codex golden-eval command shape to pass the prompt through explicit `-` stdin mode.
- Reused the product Codex subscription-auth shape for eval-only runs by writing local `auth.json` into the sandbox under `/tmp/.codex`, setting `CODEX_HOME=/tmp/.codex`, and sharing the same private-side Codex sandbox-auth path constants used by normal subscription overlays.
- Switched writable Codex runs to Codex's externally-sandboxed noninteractive mode because Syndai already runs the executor inside the Daytona sandbox and Codex's nested bubblewrap sandbox fails there.
- Kept the private worktree under its file-size gate by splitting pure golden task-data shaping and reusable golden-runner test fakes into smaller helper modules.

## Evidence

- Focused private tests:
  `uv run pytest --no-cov tests/unit/features/coding/executors/test_codex_cli_adapter.py tests/unit/features/coding/executors/test_codex_cli_stream_capture.py -q`
- Focused private runner tests:
  `uv run pytest --no-cov tests/unit/scripts/test_run_coding_golden_eval.py tests/unit/scripts/test_run_coding_golden_eval_cli.py -q`
- Private full checks:
  `make check`
- Private deterministic coding eval:
  `make eval-coding-deterministic`
- Live private smoke:
  `doppler run -- uv run python scripts/run_coding_golden_eval.py --adapter codex_cli --model gpt-5.5 --output /tmp/syndai-evalrank/codex_gpt55_off_by_one_after_auth_stdin_outer_sandbox.json --case-id off_by_one_python`

Live result: `partial_run=true`, `selected_case_ids=["off_by_one_python"]`, `pass_count=1`, `pass_rate=0.05` over the full 20-row snapshot shape, with the selected task passed and unknown Codex cost preserved as `null`. Final private local gates: `make check` passed and `make eval-coding-deterministic` passed with `240 passed, 3 skipped`.

## Product Call

This is Codex admission evidence only. It proves the harness can authenticate, edit, and validate the smallest repair case. It does not update active EvalRank projection, materialized ranking, or agent-lane IRT because one selected task is not comparable multi-entity task-bank evidence.

Next private gate: run comparable full-bank task-level outcomes across multiple entities/sources before treating Codex as promotion-ready or informative for W3/W5 agent-lane IRT.
