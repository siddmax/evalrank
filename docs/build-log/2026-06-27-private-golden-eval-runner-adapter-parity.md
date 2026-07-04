# Private Golden-Eval Runner Adapter Parity

Date: 2026-06-27

## What Changed

- Private Syndai golden-eval runner CLI now accepts the live executor adapter keys already supported by the shared executor dispatch path, including the active `pi` pair.
- Private pipeline coverage now exercises the real subprocess runner in dry-run mode for `pi / openrouter/qwen/qwen3-coder`, so a stale CLI allowlist cannot strand active rows before dispatch.

## Boundary Decision

- This is private runtime plumbing only.
- The public Apache-2.0 EvalRank repo remains product-neutral and storage-free for this slice.
- Derived EvalRank persistence still belongs in the private `evalrank` schema; source-owned coding-router metadata remains in `syndai`.

## Verification

- Private red/green parser test failed first on `pi`/`opencode` being rejected, then passed after the runner allowlist was aligned.
- Private focused runner/orchestrator lane passed with `68 passed`.
- Private touched-file antipattern scan passed with `0 error(s)`.
- Private live one-case Pi probe reached the live executor and closed the sandbox cleanly, but produced `terminal=unknown_executor_failure`, no touched paths, and no retrieved text. This is dispatch evidence, not promotion-ready golden-eval evidence.

## Coverage Rationale

- This fixes the full-refresh blocker where the active Pi evidence row could not reach the runner subprocess.
- It does not mark the semantic contamination refresh gate green; validated live candidates still need a full refresh and promotion before projection can move semantic rows from `unknown` to clean or flagged.
