# Public OpenAPI Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first public REST contract as an OpenAPI document for evaluating a request into a recommendation.

**Architecture:** Keep the route contract in `schemas/openapi.json` and reference the existing public JSON Schemas instead of duplicating payload shapes. Add one root `NAVIGATION.md` entry because API route docs now exist. Do not add a server, auth, scorer, database persistence, hosted receipts, HMAC IDs, or private error behavior.

**Tech Stack:** OpenAPI 3.1.1 JSON, existing JSON Schema files, Python stdlib `unittest`.

---

### Task 1: Pin OpenAPI Route Shape

**Files:**
- Create: `tests/test_openapi_contract.py`
- Create: `schemas/openapi.json`
- Modify: `schemas/README.md`

- [x] **Step 1: Write failing OpenAPI contract tests**

Add `tests/test_openapi_contract.py` with assertions that:

- `schemas/openapi.json` exists.
- `openapi` is `3.1.1`.
- `POST /v1/recommendations` exists.
- Request body is required and references `#/components/schemas/EvaluationRequest`.
- `200` response references `#/components/schemas/Recommendation`.
- Component refs point to `evaluation-request.schema.json` and `recommendation.schema.json`.
- Relative schema refs resolve to real files under `schemas/`.

- [x] **Step 2: Run red test**

Run:

```sh
python3 -m unittest tests.test_openapi_contract
```

Expected: fail because `schemas/openapi.json` does not exist.

- [x] **Step 3: Add minimal OpenAPI JSON**

Create `schemas/openapi.json` with only:

- `openapi`
- `info`
- one `recommendations` tag
- `POST /v1/recommendations`
- component refs to existing request/response schemas

Do not add `servers`, `security`, private auth, persistence semantics, or implementation-only errors.

- [x] **Step 4: Run focused route contract test**

Run:

```sh
python3 -m unittest tests.test_openapi_contract
```

Expected: pass.

### Task 2: Document Navigation And Porting State

**Files:**
- Create: `NAVIGATION.md`
- Create: `docs/build-log/2026-06-25-public-openapi-contract.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: `docs/REPO_STRUCTURE.md`

- [x] **Step 1: Add route navigation**

Create `NAVIGATION.md` with the route source of truth:

```text
POST /v1/recommendations -> schemas/openapi.json
```

State that this is a public contract only, not a live server.

- [x] **Step 2: Update docs**

Move REST/OpenAPI from "wait" to "first route contract ported." Keep hosted auth, tenant logic, HMAC receipt derivation, persistence, error taxonomy, and deploy wiring private/deferred.

- [x] **Step 3: Run full checks**

Run:

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: pass.

### Task 3: Review And Ship

**Files:**
- All files changed by Tasks 1 and 2.

- [x] **Step 1: Run public boundary and secret checks**

Run:

```sh
python3 scripts/check_public_boundary.py --root .
```

Expected: boundary check exits 0. Run the high-signal secret scan from shell history or the boundary checker when needed; do not store scanner regexes in repo docs because they self-match.

- [x] **Step 2: Run pre-push review**

Run the available gstack/superpower review gate on the diff. Fix only concrete issues.

- [ ] **Step 3: Commit and push**

Commit with:

```sh
git add README.md TESTS.md NAVIGATION.md docs/PORTING.md docs/REPO_STRUCTURE.md docs/STATUS.md docs/build-log/2026-06-25-public-openapi-contract.md docs/superpowers/plans/2026-06-25-public-openapi-contract.md schemas/README.md schemas/openapi.json tests/test_openapi_contract.py
git commit -m "feat: add public openapi contract"
git push origin main
```

Verify the matching GitHub Actions run for the pushed SHA.

## Self-Review

- Spec coverage: Covers one concrete public route contract over existing public payload schemas.
- Placeholder scan: No placeholders.
- Type consistency: Uses `EvaluationRequest`, `Recommendation`, `POST /v1/recommendations`, and `schemas/openapi.json` consistently.

## GSTACK REVIEW REPORT

Plan review: PASS. This uses existing request/response schemas and adds no speculative server, auth, persistence, scorer, or hosted receipt behavior.

NO UNRESOLVED DECISIONS
