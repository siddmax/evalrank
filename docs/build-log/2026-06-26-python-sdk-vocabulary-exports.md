# Python SDK Vocabulary Exports

Date: 2026-06-26

## What Changed

- Re-exported public vocabulary constants through `evalrank_core` and `evalrank_sdk`.
- Added a Python SDK regression that verifies `COMPARABILITY_MODES`, `EVIDENCE_KINDS`, `FRESHNESS_STATUSES`, and `TRUST_TIERS` are shared with the core contract source of truth.
- Updated package README drift checks and `TESTS.md`.

## Public Boundary

- Public: storage-free enum vocabulary already used by schemas, contracts, and TypeScript SDK types.
- Private: scorer thresholds, trust policy internals, private reason taxonomies, benchmark weights, and runtime behavior.

## Verification Intent

- `python3 -m unittest tests.test_sdk_python tests.test_core_contracts`
- `make check`
