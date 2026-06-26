# Python Package Metadata Drift Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic tests that keep public Python package metadata and dependencies aligned.

**Architecture:** Add one stdlib `unittest` module that parses each Python package `pyproject.toml` with `tomllib` and checks public package name, version, license, Python floor, dependencies, and CLI script entrypoint.

**Tech Stack:** Python 3.11+ `tomllib`, stdlib `unittest`, existing `make check`.

---

### Task 1: Package Metadata Guard

**Files:**
- Create: `tests/test_package_metadata.py`
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Create: `docs/build-log/2026-06-26-python-package-metadata-drift-guard.md`

- [x] **Step 1: Write failing metadata/docs test**

Add tests that parse `packages/core`, `packages/sdk-python`, `packages/cli`, and `packages/mcp` `pyproject.toml` files and verify public metadata plus dependency edges.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_package_metadata
```

Expected: fail until the test map documents the new guard.

- [x] **Step 3: Update docs**

Update `TESTS.md`, `docs/STATUS.md`, `docs/PORTING.md`, and a build log with the package metadata guard.

- [x] **Step 4: Verify green**

Run:

```sh
python3 -m unittest tests.test_package_metadata
python3 scripts/check_public_boundary.py --root .
make check
```
