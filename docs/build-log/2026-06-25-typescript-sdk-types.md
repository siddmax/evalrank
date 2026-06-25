# TypeScript SDK Public Types

Date: 2026-06-25

## Built

- Added `packages/sdk-ts/package.json` for the public `@evalrank/sdk` package boundary.
- Added `packages/sdk-ts/src/index.ts` with mirrored public constants and interfaces for current EvalRank payload contracts.
- Added `tests/test_sdk_ts.py` to keep TypeScript package metadata, public constants, and public interfaces aligned with core contracts.
- Updated package, root, test, status, and porting docs.

## Boundary

- This is a source/type surface only.
- No service client, auth flow, hosted-product behavior, private integration, production evidence lookup, or private data access was added.
- Built JS output and package publishing remain later work.

## Checks

```sh
python3 -m unittest tests.test_sdk_ts
npm run check --prefix packages/sdk-ts
```
