# W0 Core Repository Snapshot

Date: 2026-06-25

Remote: https://github.com/siddmax/evalrank

Initial scope:

- Public Apache-2.0 repository created through the GitHub REST API.
- Public package shape established for `core`, `mcp`, `cli`, `sdk-python`, and `sdk-ts`.
- CI boundary gate added for private imports, Smithery coupling, excluded Min-K% markers, and package license/notice coverage.
- Root README states what is not open.

Pending after first CI run:

- Turn the branch/ruleset required status check from snapshot to enforced protection once the `CI / public-boundary` check exists in GitHub.
