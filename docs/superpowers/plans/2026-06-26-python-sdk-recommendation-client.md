# Python SDK Recommendation Client Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first non-fixture Python SDK behavior for the public `POST /v1/recommendations` contract.

**Architecture:** Keep it dependency-free and public-only. `EvalRankClient.recommend()` posts an existing `EvaluationRequest` payload to `/v1/recommendations`, returns raw public recommendation JSON, and raises an SDK exception carrying public `ProblemDetails` JSON for non-2xx responses.

**Tech Stack:** Python 3.11 stdlib `json`, `urllib.request`, `urllib.error`, and existing `evalrank_core` contracts.

---

### Task 1: Python SDK Recommendation Client

**Files:**
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `packages/sdk-python/README.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-python-sdk-recommendation-client.md`

- [x] **Step 1: Write failing tests**

Add tests that prove:
- `EvalRankClient.recommend()` posts an `EvaluationRequest` JSON body to `/v1/recommendations`.
- 2xx JSON responses are returned as public recommendation dictionaries.
- HTTP Problem Details responses raise `EvalRankApiError` with `status`, `problem`, and `retry_after`.
- Non-HTTP(S) base URLs are rejected before reaching `urllib`.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_sdk_python
```

Expected: fail because `EvalRankClient` and `EvalRankApiError` do not exist.

- [x] **Step 3: Implement minimal client**

Use `urllib.request.Request`/`urlopen`, JSON encoding, `urllib.parse.urlparse()` for HTTP(S)-only base URL validation, and existing `EvaluationRequest.to_dict()`. Do not add auth, retries, service discovery, async support, hosted receipts, or private DTOs.

- [x] **Step 4: Verify green**

Run:

```sh
python3 -m unittest tests.test_sdk_python
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
make check
```

- [x] **Step 5: Update docs**

Update SDK README, status, porting map, and the dated build log with the exact public/private boundary.
