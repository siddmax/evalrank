# Methodology Version Format

Date: 2026-06-25

## Built

- Enforced the pinned public `methodology_version` shape `YYYY-MM-DD.SEQ.slug` in core recommendation/ranked-entity contracts.
- Updated public fixture methodology version to `2026-06-25.1.public-fixture-v1`.
- Mirrored the anchored pattern in ranked-entity and recommendation JSON Schemas.
- Added regression coverage for old-format rejection, fixture value drift, and schema pattern drift.

## Boundary

- No database migration, API route, scorer, storage model, live telemetry, or private integration was added.
- The change is a public contract freeze only.

## Checks

```sh
python3 -m unittest tests.test_core_contracts tests.test_core_fixtures tests.test_schema_contracts
```
