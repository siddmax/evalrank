# Private W9 Community Digest Export

Private Syndai work on 2026-06-28 added a provider-free digest exporter for the GTM community-review queue.

Public-safe summary:

- The private command reads pending Reddit/HN community-review rows.
- It renders metadata-only Markdown or JSON for human review.
- It does not mutate queue status, send email or Slack, post to social platforms, draft replies with an LLM, create accounts, add a scheduler, or expose a public API.

Verification:

- Private red focused test failed first because the exporter module did not exist.
- Private focused exporter tests passed with `5 passed`.
- Private focused ruff and ty checks passed.
- Public docs and boundary checks passed.
- Public `make check` passed with `223` Python tests and `7` SDK tests.
- Private root `make check` passed.
