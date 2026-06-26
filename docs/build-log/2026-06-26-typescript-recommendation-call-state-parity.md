# TypeScript Recommendation Call-State Parity

Date: 2026-06-26

## Built

- Updated the public TypeScript SDK `RecommendationCallState` helper type so it includes the already-public abstention branch.
- Updated the TypeScript SDK README and drift tests to keep the exported helper type documented.
- Updated `TESTS.md` and `docs/STATUS.md` so public progress and validation docs match the shipped surface.

## Boundary

- This is compile-time TypeScript parity for existing public `the_call` and `abstention` response-state contracts.
- No scorer policy, abstention thresholds, private reason taxonomy, hosted receipt behavior, route runtime, persistence, telemetry, or private Syndai data moved into this repo.

## Verification

- `python3 -m unittest tests.test_sdk_ts`
- `npm run check --prefix packages/sdk-ts`
- `npm run test --prefix packages/sdk-ts`
- `python3 -m unittest tests.test_repo_docs`
- `python3 scripts/check_public_boundary.py --root .`
- `git diff --check`
- `make check`
