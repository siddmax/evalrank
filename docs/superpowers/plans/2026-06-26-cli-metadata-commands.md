# CLI Metadata Commands Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add CLI commands for the already-public metadata route contracts.

**Architecture:** Keep CLI network behavior explicit and scriptable. Add `evalrank use-cases --base-url ...` for `GET /v1/use-cases` and `evalrank scoring-stages --base-url ...` for `GET /v1/scoring-stages`, routing through the public Python SDK client and existing Problem Details stderr behavior.

**Tech Stack:** Python stdlib `argparse`, existing `EvalRankClient`, stdlib `unittest`.

---

### Task 1: CLI Metadata Commands

**Files:**
- Modify: `packages/cli/src/evalrank_cli/__init__.py`
- Modify: `tests/test_cli_fixture.py`
- Modify: `packages/cli/README.md`
- Modify: `README.md`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-cli-metadata-commands.md`

- [x] **Step 1: Write failing CLI tests**

Add tests proving:
- README lists the metadata commands.
- `evalrank use-cases --base-url ...` calls `GET /v1/use-cases`.
- `evalrank scoring-stages --base-url ...` calls `GET /v1/scoring-stages`.
- Metadata route Problem Details responses write public Problem Details JSON to stderr.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_cli_fixture
```

Expected: fail because the metadata commands do not exist yet.

- [x] **Step 3: Implement minimal commands**

Reuse `EvalRankClient`, explicit HTTP(S) base URL validation, JSON stdout serialization, and public Problem Details stderr serialization. Do not add auth, retries, service discovery, environment-variable defaults, private DTOs, persistence, or hosted receipt behavior.

- [x] **Step 4: Update docs**

Update package/root READMEs, `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and a dated build log.

- [x] **Step 5: Verify green**

Run:

```sh
python3 -m unittest tests.test_cli_fixture
python3 scripts/check_public_boundary.py --root .
make check
```
