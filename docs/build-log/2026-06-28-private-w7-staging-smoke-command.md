# 2026-06-28 Private W7 Staging Smoke Command

Public-safe status note: the private Syndai worktree added a local/staging smoke command for the existing EvalRank W7 recommendation read surface.

The command verifies that the private hosted/local API returns the same cached recommendation through the public-root recommendation route, the Syndai API-prefix recommendation route, and the private GET alias. It can also check keyed current-period usage when an API key is supplied through an environment variable.

No public EvalRank contract changed. The public repo still owns the storage-free contracts, schemas, SDK/CLI/MCP clients, and public route descriptions only. Hosted deployment, auth, quota data, usage facts, billing readback, and runtime secrets remain private.

Local private verification completed for the smoke harness and its focused tests. The hosted/staging W7 proof remains open until the command is run against deployed staging with real HTTP responses.
