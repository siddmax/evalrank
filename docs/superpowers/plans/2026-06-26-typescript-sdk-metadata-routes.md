# TypeScript SDK Metadata Routes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add TypeScript SDK methods for the already-public metadata route contracts.

**Architecture:** Keep `EvalRankClient` dependency-free and native-`fetch` based. Add `useCases()` for `GET /v1/use-cases` and `scoringStages()` for `GET /v1/scoring-stages`, sharing explicit HTTP(S) base URL validation, JSON response parsing, and public Problem Details error behavior.

**Tech Stack:** Node native `fetch`, `node:test`, existing public TypeScript interfaces.

---

### Task 1: TypeScript SDK Metadata Routes

**Files:**
- Modify: `packages/sdk-ts/src/index.ts`
- Modify: `packages/sdk-ts/src/index.test.ts`
- Modify: `packages/sdk-ts/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-typescript-sdk-metadata-routes.md`

- [x] **Step 1: Write failing SDK tests**

Add tests proving:
- `new EvalRankClient(...).useCases()` calls `GET /v1/use-cases`.
- `new EvalRankClient(...).scoringStages()` calls `GET /v1/scoring-stages`.
- Metadata route Problem Details responses raise `EvalRankApiError`.

- [x] **Step 2: Verify red**

Run:

```sh
npm run test --prefix packages/sdk-ts
```

Expected: fail because the methods do not exist.

- [x] **Step 3: Implement minimal client methods**

Reuse native `fetch`, explicit HTTP(S) base URL validation, JSON response parsing, and existing Problem Details error handling. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, persistence, or hosted receipt behavior.

- [x] **Step 4: Update docs**

Update package/root READMEs, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and a dated build log.

- [x] **Step 5: Verify green**

Run:

```sh
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
python3 scripts/check_public_boundary.py --root .
make check
```
