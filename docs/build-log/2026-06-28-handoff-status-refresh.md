# 2026-06-28 - Handoff Status Refresh

Docs-only public status update for the next session.

## Summary

- Refreshed `docs/STATUS.md` with explicit next-session handoff notes.
- Clarified that private EvalRank persistence belongs in the private `evalrank` schema, while shared Syndai API-key/customer control-plane tables remain in `syndai`.
- Preserved the current work order: broader real source-adapter coverage first, then hosted/staging W7 proof plus billing settlement, then W8/W9 surfaces.
- Recorded that Claude Opus is the promotion-quality default evidence lane, Codex GPT-5.5 is active measured evidence, and Pi remains quarantined from default promotion.

## Boundary

- No public runtime, schema, SDK, CLI, MCP, or OpenAPI contract changed.
- No private Syndai source text, secrets, customer data, held-out eval material, or live operational identifiers were copied into this repo.

## Verification

- Public `python3 -m unittest tests.test_repo_docs`: passed, `9` tests.
- Public `make check`: passed, `223` Python tests and `7` TypeScript SDK tests.
- Public `git diff --check`: passed.
- Private `/Users/sidsharma/Syndai/.wt/codex-evalrank-w6-spine` `git diff --check`: passed.
- Explicit trailing-whitespace scans on touched public/private docs: clean.
