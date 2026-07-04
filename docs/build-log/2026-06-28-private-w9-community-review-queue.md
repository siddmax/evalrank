# Private W9 Community Review Queue

Private Syndai work on 2026-06-28 added the first account-free GTM listener substrate for human-reviewed community follow-up.

Public-safe summary:

- Private EvalRank now has a `gtm_community_threads` queue table for public Reddit/HN thread metadata.
- A private ingestion command accepts sanitized JSON from future fetchers and dedupes by `(platform, thread_id)`.
- The command rejects body/comment/reply text and does not send email, post to social platforms, call Reddit/HN, run an LLM, or expose a public API.
- This is the review queue substrate only; human-gated posting and Resend delivery remain account-gated follow-up work.

Verification:

- Private red focused tests failed first on missing helper/script modules.
- Private focused helper/script/migration tests passed with `6 passed`.
- Private focused ruff, ty, and EvalRank migration-boundary checks passed.
- Public docs and boundary checks passed.
- Public `make check` passed with `223` Python tests and `7` SDK tests.
- Private root `make check` passed.
- Public and private `git diff --check` passed.
