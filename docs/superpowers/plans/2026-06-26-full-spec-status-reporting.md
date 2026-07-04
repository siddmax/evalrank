# Full Spec Status Reporting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `docs/STATUS.md` report progress against the full private EvalRank spec and W0-W9 implementation plan while preserving the public/private boundary.

**Architecture:** Add a compact public-safe dashboard near the top of `docs/STATUS.md`: rubric, current gate, wave coverage, spec coverage, and next vertical slice. Add one repo-doc drift test that prevents removing this full-spec coverage view. Add one dated build log because reporting ownership changed.

**Tech Stack:** Markdown docs plus stdlib `unittest`.

---

### Task 1: Add Full-Spec Dashboard

**Files:**
- Modify: `docs/STATUS.md`

- [ ] **Step 1: Insert the dashboard after the `Last updated` line**

Add sections named `Full-Spec Dashboard`, `Coverage Rubric`, `Wave Coverage`, `Spec Coverage`, and `Next Vertical Slice`.

- [ ] **Step 2: Keep the dashboard public-safe**

Use private spec filenames, wave names, and sanitized implementation categories only. Do not copy private raw spec text, live IDs, customer data, held-out tasks, traces, pricing internals, or operational runbooks.

### Task 2: Guard The Reporting Shape

**Files:**
- Modify: `tests/test_repo_docs.py`

- [ ] **Step 1: Add a focused status-dashboard test**

Require `docs/STATUS.md` to mention `Full-Spec Dashboard`, `Wave Coverage`, `Spec Coverage`, `Spec 22`, and `W6`.

- [ ] **Step 2: Run the focused test**

Run: `python3 -m unittest tests.test_repo_docs`

### Task 3: Record The Reporting Change

**Files:**
- Add: `docs/build-log/2026-06-26-full-spec-status-reporting.md`
- Modify: `docs/STATUS.md`

- [ ] **Step 1: Add the build log**

Summarize that the status doc now reports against the full spec/wave model.

- [ ] **Step 2: Reference the build log from `docs/STATUS.md`**

The existing exact build-log drift test requires every build log to be listed.

### Task 4: Verify

- [ ] **Step 1: Run focused docs tests**

Run: `python3 -m unittest tests.test_repo_docs`

- [ ] **Step 2: Run default check**

Run: `make check`
