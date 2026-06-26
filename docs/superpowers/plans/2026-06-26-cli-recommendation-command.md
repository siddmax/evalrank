# CLI Recommendation Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first non-fixture CLI behavior for the public `POST /v1/recommendations` contract.

**Architecture:** The CLI reuses `EvalRankClient` from the Python SDK instead of duplicating HTTP code. `evalrank recommend --base-url URL --request PATH` reads public `EvaluationRequest` JSON from a file or stdin, posts it to the explicit URL, writes public recommendation JSON to stdout, and writes public Problem Details JSON to stderr on API errors.

**Tech Stack:** Python 3.11 stdlib `argparse`/`json` plus existing `evalrank_sdk`.

---

### Task 1: CLI Recommendation Command

**Files:**
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `packages/cli/pyproject.toml`
- Modify: `tests/test_cli_fixture.py`
- Modify: `packages/cli/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-cli-recommendation-command.md`

- [x] **Step 1: Write failing tests**

Add tests that prove:
- `evalrank recommend --base-url URL --request request.json` posts the request JSON and prints recommendation JSON.
- `evalrank recommend --base-url URL --request -` reads JSON from stdin.
- HTTP Problem Details errors print the problem JSON to stderr and return non-zero.
- The CLI README lists the `recommend` command.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_cli_fixture
```

Expected: fail because the `recommend` subcommand does not exist.

- [x] **Step 3: Implement minimal command**

Add a `recommend` subcommand with required `--base-url` and `--request`. Use `EvalRankClient`; keep output minified/sorted JSON like fixture commands. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, or persistence.

- [x] **Step 4: Verify green**

Run:

```sh
python3 -m unittest tests.test_cli_fixture
python3 scripts/check_public_boundary.py --root .
python3 -m unittest discover tests
make check
```

- [x] **Step 5: Update docs**

Update CLI README, root README, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and the dated build log with the explicit public/private boundary.
