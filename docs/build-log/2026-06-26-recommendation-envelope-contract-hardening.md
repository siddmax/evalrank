# Recommendation Envelope Contract Hardening

Date: 2026-06-26

## Built

- Added core regression tests for schema-incompatible `Recommendation` envelope fields.
- Added duplicate ranked-entity rejection for single-scale recommendations.
- Hardened `Recommendation.__post_init__` so Python payloads reject invalid public envelope metadata before serialization.
- Updated public status, porting, tests, core README, and schema README docs.

## Public Boundary

- This change is public-safe contract hardening only.
- It does not add scorer formulas, benchmark weights, source adapters, graph lookup, persistence, hosted receipts, auth, telemetry, private evidence rows, or held-out evaluation material.
- Keyed duplicate ranked-entity rejection stays in the core contract because standard JSON Schema `uniqueItems` validates whole item uniqueness, not uniqueness by `entity_id`.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_schema_incompatible_envelope_fields tests.test_core_contracts.CoreContractTests.test_recommendation_rejects_duplicate_ranked_entities
```

Expected: `OK`.

Run before push:

```sh
python3 -m unittest tests.test_core_contracts
python3 scripts/check_public_boundary.py --root .
make check
git diff --check
```
