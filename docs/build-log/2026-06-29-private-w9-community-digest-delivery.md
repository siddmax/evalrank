# Private W9 Community Digest Delivery

Private Syndai work on 2026-06-29 added an explicit provider-delivery wrapper for the existing metadata-only GTM community-review digest.

Public-safe summary:

- The private command reuses the existing pending Reddit/HN digest renderer.
- Default mode prints the digest and performs no provider side effects.
- Slack and Resend delivery require explicit send flags plus environment-provided secrets.
- Resend delivery uses a deterministic digest idempotency key.
- No account setup, browser use, live send, social post, LLM reply draft, scheduler, queue mutation, public route, public SDK/CLI/MCP behavior, or public persistence was added.

Verification:

- Private red focused test failed first because the delivery module did not exist.
- Private focused delivery tests passed with `7 passed`.
- Private adjacent community digest/export/fetch tests passed with `18 passed`.
- Private focused ruff and ty checks passed.
