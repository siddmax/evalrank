# Use-Case Taxonomy Method Note

Date: 2026-06-26

## Built

- Added `methods/use-case-taxonomy.md` as the public method note for `UseCaseCatalog`.
- Documented public fields, ranked versus overlay policy, and `kind-grouped` comparability guidance.
- Added a small docs regression test for the method note.
- Updated `methods/README.md`, `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.

## Kept Out

- Benchmark weights, IRT clusters, confidence policy, synthesis rules, private thresholds, held-out tasks, graders, answers, traces, and benchmark outputs.
- Source adapters, graph lookup, production rows, scorer runtime, storage, telemetry, hosted auth, receipts, and deployment wiring.

## Port-Over Decision

| Source material | Public action | Owning workstream |
| --- | --- | --- |
| Public use-case taxonomy method | Ported as a sanitized method note tied to `UseCaseCatalog`. | Methods / Schemas, Docs / Public Planning |
| Benchmark weighting, confidence, synthesis, and evaluation-integrity details | Keep private until a separate sanitized note can omit proprietary tuning and held-out signal. | Methods / Schemas, Scoring / Materializer Runtime, Evaluation Integrity |

## Verification

- Green: gstack pre-landing checklist review found no unresolved issues.
- Green: `python3 -m unittest tests.test_methods_docs`.
- Green: `npm run check --prefix packages/sdk-ts`.
- Green: `make check` passed public boundary scan and 118 tests.
- Green: `git diff --check`.
