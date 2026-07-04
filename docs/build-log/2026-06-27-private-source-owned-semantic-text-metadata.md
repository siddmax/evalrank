# Private Source-Owned Semantic Text Metadata

Date: 2026-06-27

## What Changed

- Private Syndai now stores redacted semantic text metadata on the source-owned coding-router table, not in the public EvalRank repo.
- Private EvalRank projection scripts can read those source-owned arrays and write derived provenance, contamination rows, and caches under the private `evalrank` schema.
- The private golden-eval snapshot path now carries redacted benchmark text and assistant retrieved text so a real refresh can move semantic contamination checks from `unknown` to clean or flagged.

## Boundary Decision

- Source-owned private metadata belongs in `syndai`.
- Derived EvalRank persistence belongs in the private `evalrank` schema.
- The public Apache-2.0 EvalRank repo remains product-neutral and storage-free for this slice.

## Verification

- Private red/green tests covered model columns, projection selects, golden-eval snapshot fields, and pipeline ledger threading.
- Private touched unit lane passed with `72 passed`.
- Private EvalRank focused lane passed with `119 passed`.
- Private live-backed router evidence repository lane passed with `11 passed`.
- Private migration validation, identifier guard, touched-file antipattern scan, and `ty check` passed.
- Target DB proof applied the source metadata migration, verified both `text[]` source columns and no-null constraints, reran projection and contamination, and observed semantic rows still `unknown / insufficient_metadata` because existing active rows have empty text arrays until a real golden-eval refresh runs.
- Private live one-case probe with `claude_code / claude-sonnet-4-6` emitted both private semantic text fields (`benchmark_text_len=1074`, `retrieved_text_len=671`) and confirmed the runner cleanup fix removed the previous unclosed aiohttp session warning. The selected case failed validation, so this is extraction/lifecycle evidence, not a full refresh or promotion signal.

## Coverage Rationale

- This improves private W3/W5 integrity coverage because the source-of-truth plumbing now exists.
- It does not change public contracts or mark semantic contamination as live-clean.
