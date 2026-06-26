# TypeScript Recommendation Client Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add dependency-free TypeScript SDK behavior for the public `POST /v1/recommendations` contract.

**Architecture:** The SDK exports `EvalRankClient` and `EvalRankApiError` from `packages/sdk-ts/src/index.ts`. The client accepts an explicit HTTP(S) base URL, posts public `EvaluationRequest` JSON with native `fetch`, returns public `Recommendation` JSON, and raises Problem Details errors for non-2xx responses.

**Tech Stack:** TypeScript source executed with Node's `--experimental-strip-types`, native `fetch`, and Node stdlib test helpers.

---

### Task 1: TypeScript SDK Client

**Files:**
- Modify: `packages/sdk-ts/src/index.ts`
- Modify: `packages/sdk-ts/package.json`
- Create: `packages/sdk-ts/src/index.test.ts`
- Modify: `packages/sdk-ts/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-typescript-recommendation-client.md`

- [x] **Step 1: Write failing runtime tests**

Add tests that prove:
- `new EvalRankClient("http://...").recommend(request)` posts JSON to `/v1/recommendations` and returns recommendation JSON.
- HTTP Problem Details errors reject with `EvalRankApiError`, preserving `status`, `problem`, and `retryAfter`.
- Non-HTTP(S) base URLs are rejected before request execution.

- [x] **Step 2: Verify red**

Run:

```sh
npm run test --prefix packages/sdk-ts
```

Expected: fail because `EvalRankClient` and `EvalRankApiError` are not exported.

- [x] **Step 3: Implement minimal client**

Use native `fetch`. Validate base URL with `new URL(baseUrl)`. Use sorted-free `JSON.stringify(request)` because the public contract is JSON shape, not canonical hashing. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, persistence, or hosted receipt behavior.

- [x] **Step 4: Verify green**

Run:

```sh
npm run test --prefix packages/sdk-ts
npm run check --prefix packages/sdk-ts
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
make check
```

- [x] **Step 5: Update docs**

Update package/root READMEs, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and the dated build log with the public/private boundary.
