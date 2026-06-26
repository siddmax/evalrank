# Recommendation Ranked Schema Uniqueness Plan

Date: 2026-06-26

## Goal

Align the top-level public recommendation JSON Schema with the Python core duplicate ranked-entity guard.

## Steps

1. Pin `uniqueItems` on `Recommendation.properties.ranked`.
2. Extend the existing recommendation branch schema test.
3. Update public status, porting, and test docs.
4. Run local checks and pre-landing review before direct `main` push.

## Public Boundary

- Safe: schema/core parity for already-public single-scale recommendation contracts.
- Excluded: scorer normalization, private score semantics, hosted receipts, source adapters, persistence, telemetry, production rows, and held-out eval material.
