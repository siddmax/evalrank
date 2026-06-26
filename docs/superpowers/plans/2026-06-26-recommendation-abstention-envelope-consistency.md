# Recommendation Abstention Envelope Consistency Plan

**Goal:** Make the existing public recommendation envelope reject dangling or contradictory `the_call` / `abstention` states.

**Architecture:** Keep this as storage-free contract validation. Core, JSON Schema, and TypeScript types should agree that `abstention` is present only with an abstaining `the_call`, and recommending calls carry `abstention: null`.

**Boundary:** Do not add scorer thresholds, evidence-floor policy, private reason taxonomy, runtime behavior, hosted operations, or persistence.

## Steps

- [x] Add failing core, schema, and TypeScript parity tests.
- [x] Add minimal core validation.
- [x] Add JSON Schema branch constraints.
- [x] Add TypeScript recommendation call-state typing.
- [x] Update public docs and build log.
- [x] Run focused checks.
