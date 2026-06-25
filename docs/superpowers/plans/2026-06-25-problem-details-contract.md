# Problem Details Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin the public error response shape for EvalRank route contracts using RFC 9457 Problem Details.

**Architecture:** Add `schemas/problem.schema.json` as a small public wire contract and reference it from the existing `POST /v1/recommendations` OpenAPI route for invalid request payloads. Use `application/problem+json` and the standard members instead of inventing a custom EvalRank error envelope. Do not add a server runtime, auth, private error taxonomy, persistence, telemetry, or hosted receipt behavior.

**Tech Stack:** RFC 9457 Problem Details, OpenAPI 3.1.1 JSON, JSON Schema 2020-12, Python stdlib `unittest`.

---

### Task 1: Pin Public Problem Details Schema

**Files:**
- Modify: `tests/test_schema_contracts.py`
- Create: `schemas/problem.schema.json`
- Modify: `schemas/README.md`

- [x] **Step 1: Write failing schema tests**

Add schema tests that require `problem.schema.json` to:

- use draft 2020-12,
- be an object,
- allow extension members,
- require `type`, `title`, `status`, and `detail`,
- define optional `instance`,
- constrain `status` to HTTP error codes `400..599`.

- [x] **Step 2: Run red schema test**

Run:

```sh
python3 -m unittest tests.test_schema_contracts
```

Expected: fail because `schemas/problem.schema.json` does not exist.

- [x] **Step 3: Add minimal schema**

Create `schemas/problem.schema.json` with only RFC 9457 members and extension allowance. Do not add EvalRank-specific `code`, `request_id`, validation-error arrays, or private problem type URIs yet.

- [x] **Step 4: Run focused schema test**

Run:

```sh
python3 -m unittest tests.test_schema_contracts
```

Expected: pass.

### Task 2: Wire Problem Details Into OpenAPI

**Files:**
- Modify: `tests/test_openapi_contract.py`
- Modify: `schemas/openapi.json`

- [x] **Step 1: Write failing OpenAPI tests**

Add OpenAPI tests that require:

- `components.schemas.ProblemDetails.$ref == "problem.schema.json"`,
- `POST /v1/recommendations` has a `400` response,
- the `400` response uses `application/problem+json`,
- the `400` response schema references `#/components/schemas/ProblemDetails`.

- [x] **Step 2: Run red OpenAPI test**

Run:

```sh
python3 -m unittest tests.test_openapi_contract
```

Expected: fail because the component and `400` response are not wired.

- [x] **Step 3: Add minimal OpenAPI response**

Add a `400` invalid request response to `schemas/openapi.json` and add the `ProblemDetails` component ref. Do not add `401`, `403`, `422`, `500`, auth schemes, or private hosted errors.

- [x] **Step 4: Run focused OpenAPI test**

Run:

```sh
python3 -m unittest tests.test_openapi_contract
```

Expected: pass.

### Task 3: Document And Ship

**Files:**
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-25-problem-details-contract.md`

- [x] **Step 1: Update docs**

Document that public route errors use RFC 9457 Problem Details for invalid request payloads. Keep private error taxonomy, hosted auth errors, receipt lookup errors, telemetry, and runtime details out of scope.

- [x] **Step 2: Run full checks**

Run:

```sh
make check
npm run check --prefix packages/sdk-ts
```

Expected: pass.

- [x] **Step 3: Run public boundary, secret scan, review, commit, push**

Run public boundary, high-signal secret scan from shell history, gstack review, and Ponytail review. Then commit and push directly to `main`, and verify the matching GitHub Actions run.

## Self-Review

- Spec coverage: Covers the first public error response contract for the existing OpenAPI route.
- Placeholder scan: No placeholders.
- Type consistency: Uses `ProblemDetails`, `problem.schema.json`, `application/problem+json`, and `400` consistently.

## GSTACK REVIEW REPORT

Plan review: PASS. RFC 9457 avoids a custom error envelope and keeps this slice to a wire contract only.

NO UNRESOLVED DECISIONS
