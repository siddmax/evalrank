# Private W9 Community Listener Fetch

Private Syndai work on 2026-06-28 added an account-free metadata fetch mode for the existing GTM community-review queue.

Public-safe summary:

- The private ingestion command can fetch public Hacker News and Reddit listing/search metadata by query.
- It normalizes only thread/post id, URL, title, author, and source query into the existing private review queue.
- It does not store body/comment/reply text.
- It does not add Reddit OAuth, account login, scheduler, email/Slack delivery, social posting, LLM reply drafting, a public API, or public persistence.

Verification:

- Private red tests failed first on missing parser/fetch functions.
- Private focused script tests passed with `6 passed`.
- Private community queue/fetch/migration focused lane passed with `9 passed`.
- Private focused ruff and ty checks passed.
- Public docs and boundary checks passed.
- Public `make check` passed with `223` Python tests and `7` SDK tests.
- Private root `make check` passed.
