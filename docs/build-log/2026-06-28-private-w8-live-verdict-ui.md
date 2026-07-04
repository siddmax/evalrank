# Private W8 Live Verdict UI

Private Syndai work on 2026-06-28 added the first authenticated web proof for the cached EvalRank recommendation path.

Public-safe summary:

- Added a private Syndai web BFF route that forwards an authenticated Supabase bearer session server-side to backend `POST /api/v1/recommendations`.
- Added a private authenticated `/[locale]/evalrank` page that renders recommendation id, methodology/cache metadata, top candidates, BFF failures, and keyed-quota cached fallback bodies.
- The browser does not receive backend base URLs, provider tokens, API keys, or database details.
- This did not add a public EvalRank UI route, public navigation contract, public SDK/CLI/MCP behavior, public persistence, billing, telemetry, or hosted receipt surface.

Verification:

- Private red BFF route test failed first on the missing route module.
- Private red component test failed first on the missing panel module.
- Private focused BFF route tests passed with `4 passed`.
- Private focused live verdict component tests passed with `4 passed`.
- Private combined web route/component tests passed with `8 passed`.
- Private touched-file Biome check, `velite && tsc --noEmit`, full `npm run lint`, `make web-check` with `68 passed` Playwright tests, and private root `make check` passed.
- Public repo docs test, public boundary check, public `make check` with `223` Python tests plus `7` TypeScript SDK tests, and `git diff --check` in both repos passed.

Current blocker:

- Hosted/staging proof still needs deployed staging plus account/provider setup. Public EvalRank remains storage-free and UI-free until a public UI contract is explicitly pinned.
