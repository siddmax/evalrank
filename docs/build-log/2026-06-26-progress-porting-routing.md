# Progress And Porting Routing Refresh

Date: 2026-06-26

## What Changed

- Refreshed `docs/STATUS.md` with an explicit progress snapshot that separates built public surface, next owning workstreams, private persistence/hosted operations, and private evaluation-integrity material.
- Refreshed `docs/PORTING.md` with an immediate port-routing queue for the next public-repo decisions.
- Kept the update documentation-only and public-safe: no raw private planning text, live identifiers, secrets, customer examples, production evidence rows, hosted runbooks, or held-out evaluation material were copied.

## Routing Summary

| Decision area | Current handling |
| --- | --- |
| README, fixture, schema, and boundary drift checks | Port now when they protect already-public contracts or prevent private leakage. |
| New storage-free payload contracts | Port one at a time only when synthetic fixtures, schemas, and SDK/CLI/MCP surfaces can remain private-data-free. |
| Non-fixture SDK/CLI/MCP behavior | Wait for pinned public client semantics before implementing. |
| Scorer/materializer runtime | Incubate privately until public-input-only components are separable. |
| Migrations, hosted ops, deploy config, telemetry, billing/admin, and credentials | Keep private until a deliberate public cutover exists, if ever. Runtime persistence and hosted operation are maintained in a separate private system. |
| Held-out tasks, graders, traces, answers, and private benchmark outputs | Never port. |

## Verification Intent

- Run the public boundary check and full repo gate before committing this doc refresh.
