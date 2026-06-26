# Ranking Group Schema Uniqueness Plan

Date: 2026-06-26

## Goal

Align the public recommendation JSON Schema with the Python core duplicate-ranked-row guard for grouped recommendations.

## Steps

1. Pin `uniqueItems` on `Recommendation.$defs.RankingGroup.properties.ranked`.
2. Extend the existing schema-contract test for ranking groups.
3. Update public status, porting, and test docs.
4. Run local checks and pre-landing review before direct `main` push.

## Public Boundary

- Safe: schema/core parity for already-public grouped recommendation contracts.
- Excluded: cross-kind score normalization, scorer internals, private score semantics, hosted receipts, persistence, telemetry, production rows, and held-out eval material.
