# Python SDK Metadata Routes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Python SDK methods for the already-public metadata route contracts.

**Architecture:** Keep `EvalRankClient` dependency-free. Add `use_cases()` for `GET /v1/use-cases` and `scoring_stages()` for `GET /v1/scoring-stages`, sharing the existing HTTP(S)-only base URL and Problem Details error behavior.

**Tech Stack:** Python stdlib `urllib`, existing public fixtures, stdlib `unittest`.

---

### Task 1: Python SDK Metadata Routes

**Files:**
- Modify: `packages/sdk-python/src/evalrank_sdk/__init__.py`
- Modify: `tests/test_sdk_python.py`
- Modify: `packages/sdk-python/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-python-sdk-metadata-routes.md`

- [x] **Step 1: Write failing SDK tests**

Add tests proving:
- `EvalRankClient(...).use_cases()` calls `GET /v1/use-cases`.
- `EvalRankClient(...).scoring_stages()` calls `GET /v1/scoring-stages`.
- Metadata route Problem Details errors raise `EvalRankApiError`.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_sdk_python
```

Expected: fail because the methods do not exist.

- [x] **Step 3: Implement minimal client methods**

Reuse `urllib.request`, explicit HTTP(S) base URL validation, JSON response parsing, and existing Problem Details error handling. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, persistence, or hosted receipt behavior.

- [x] **Step 4: Update docs**

Update package/root READMEs, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and a dated build log.

- [x] **Step 5: Verify green**

Run:

```sh
python3 -m unittest tests.test_sdk_python
python3 scripts/check_public_boundary.py --root .
make check
```
