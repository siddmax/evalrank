# Abstention No Ranked Answer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure public recommendation abstentions cannot also carry ranked answers or grouped rankings.

**Architecture:** Keep the invariant storage-free and public: core validation, JSON Schema branch rules, and TypeScript types must all agree that an abstention is a single-scale empty recommendation with `shortlist_depth: 0`, `ranked: []`, and `groups: null`. Do not add scorer thresholds, evidence-floor policy, runtime behavior, hosted operations, persistence, or private reason taxonomy.

**Tech Stack:** Python stdlib dataclasses and `unittest`, JSON Schema 2020-12 documents, TypeScript type declarations checked by the existing Node strip-types gate.

---

### Task 1: Pin the Contract

**Files:**
- Modify: `tests/test_core_contracts.py`
- Modify: `tests/test_schema_contracts.py`
- Modify: `tests/test_sdk_ts.py`
- Modify: `packages/core/src/evalrank_core/contracts.py`
- Modify: `schemas/recommendation.schema.json`
- Modify: `packages/sdk-ts/src/index.ts`

- [x] **Step 1: Write failing tests**

Add core, schema, and TypeScript surface assertions that reject or disallow abstention with non-zero `shortlist_depth`, non-empty `ranked`, non-null `groups`, or `comparability: "kind-grouped"`.

- [x] **Step 2: Verify red**

Run:

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_abstention_with_ranked_answer tests.test_schema_contracts.SchemaContractTests.test_recommendation_schema_pins_abstention_as_empty_single_scale tests.test_sdk_ts.TypeScriptSdkTests.test_public_interfaces_cover_schema_payloads
```

Expected: fail because the invariant is not implemented yet.

- [x] **Step 3: Implement minimal contract changes**

Add core validation, schema branch constraints, and TypeScript state typing for abstention-as-empty-single-scale only.

- [x] **Step 4: Verify green**

Run the focused command from Step 2, then:

```sh
npm run check --prefix packages/sdk-ts
npm run test --prefix packages/sdk-ts
```

Expected: all pass.

### Task 2: Update Public Docs

**Files:**
- Modify: `TESTS.md`
- Modify: `docs/STATUS.md`
- Modify: `docs/PORTING.md`
- Modify: `packages/core/README.md`
- Modify: `packages/sdk-ts/README.md`
- Modify: `schemas/README.md`
- Create: `docs/build-log/2026-06-26-abstention-no-ranked-answer.md`

- [x] **Step 1: Update docs**

Record that abstention means an empty single-scale response and explicitly keep private scorer thresholds, evidence floors, runtime, DB, hosted ops, and private reason taxonomy out.

- [x] **Step 2: Verify full gate**

Run:

```sh
python3 scripts/check_public_boundary.py --root .
make check
```

Expected: boundary scan and full test gate pass.

## Self-Review

- Spec coverage: covered by core validation, schema branch rules, TypeScript types, tests, and docs.
- Placeholder scan: no TBD/TODO placeholders.
- Type consistency: uses existing `Recommendation`, `Abstention`, `TheCall`, `SingleScaleRecommendation`, and `KindGroupedRecommendation` names.
