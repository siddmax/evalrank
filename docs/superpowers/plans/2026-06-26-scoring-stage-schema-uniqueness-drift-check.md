# Scoring Stage Schema Uniqueness Drift Check Plan

Date: 2026-06-26

## Goal

Pin already-public scoring-stage catalog uniqueness rules in the schema-contract tests.

## Steps

1. Assert `stages`, `input_contracts`, and `output_contracts` uniqueness in `tests/test_schema_contracts.py`.
2. Update public test, status, and porting docs.
3. Run local checks and pre-landing review before direct `main` push.

## Public Boundary

- Safe: deterministic test coverage for an existing public schema rule.
- Excluded: scorer stages, formulas, thresholds, runtime behavior, persistence, private methodology, and held-out eval material.
