# Private W8 Live Verdict Home Link

Private Syndai work on 2026-06-28 made the authenticated EvalRank live verdict page discoverable from the signed-in home page.

Public-safe summary:

- Added a private authenticated-home CTA to the existing private `/[locale]/evalrank` live verdict page.
- Preserved the existing connection-management path as a secondary action.
- Added a focused private app test so the EvalRank route link does not disappear.
- No public EvalRank UI route, public navigation contract, public SDK/CLI/MCP behavior, public persistence, provider setup, billing, or telemetry contract changed.

Verification:

- Private red home test first failed because `Open EvalRank` was missing.
- Private focused home test passed with `1 passed`.
- Private touched-file Biome check passed.
- Private focused home/BFF/panel tests passed with `9 passed`.
- Private production web build passed.
- Private root `make check` passed.
- Public docs test, public boundary check, public `make check`, and public/private `git diff --check` passed.
