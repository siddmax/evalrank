# Private Pi Runtime Health Preflight

Date: 2026-06-27

## Summary

- Private Syndai golden-eval runner now fails fast when the Pi executor runtime is unavailable instead of writing opaque `unknown_executor_failure` evidence.
- The runner can also use sanitized executor `final_message` as private retrieved-text evidence when adapter event streams do not expose assistant text.
- Public EvalRank contracts, SDKs, CLI, MCP boundary, and schemas did not change.

## Private Verification

- Focused private regression lane passed with `96 passed`.
- Private static checks passed for the changed runner/executor files: ruff format/check, antipattern scan, and `ty check`.
- Live private Pi one-case probe now records the real blocker as `terminal=missing_binary; detail=pi-sdk-governor: cannot resolve @earendil-works/pi-coding-agent`, with `cost_usd="0"` and no retrieved text.

## Boundary

- The public repo remains storage-free and product-neutral.
- The remaining Pi gate is private runtime-image work: refresh the Daytona `syndai-sandbox` image so the pinned Pi package is present, then rerun promotion-quality refreshed coverage.
