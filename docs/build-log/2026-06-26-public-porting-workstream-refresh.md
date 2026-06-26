# Public Porting Workstream Refresh

Date: 2026-06-26

## What changed

- Refreshed `docs/STATUS.md` and `docs/PORTING.md` with the current public/private routing checkpoint.
- Rechecked the private Syndai worktree by category only. Current dirty work routes to coding worker/recovery reliability, repo-guidance/doc-validation, and Memphant memory-system planning workstreams.
- Rechecked the public repo metadata for `siddmax/evalrank`: repository visibility is public, secret scanning is enabled, push protection is enabled, and Dependabot security updates are enabled.

## Porting decision

The public EvalRank repo should continue accepting:

- Storage-free contracts, JSON Schemas, synthetic fixtures, SDK/CLI/MCP surfaces, OpenAPI route contracts, sanitized method notes, and deterministic public-boundary checks.
- Public doc checks only when the matching public doc claim exists.

Keep these out of the public repo for now:

- Syndai coding worker/recovery/runtime reliability edits.
- Memphant or other memory-system specs and plans, unless a concrete EvalRank storage-free contract is explicitly extracted.
- DB bootstrap, Supabase migrations, migration runners, grants/RLS, live checks, source adapters, graph/evidence lookup, scorer/materializer runtime, hosted ops, GTM, telemetry, credentials, and held-out eval material.

## Verification target

Before pushing this public docs sync:

```sh
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
make check
```
