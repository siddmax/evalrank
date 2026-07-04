# 2026-06-28 Private Dogfood Audit Exact Provision Command

## What Changed

- Private Syndai's Sentry dogfood bootstrap audit now prints the exact provision command when the repository id and webhook URL are known.

## Boundary

- No public EvalRank runtime, Sentry REST mutation, terminal dogfood outcome, or EvalRank evidence row was added.
- The live private blocker remains missing Sentry provisioning credentials and binding.

## Verification

- Private focused provisioner test file: `11 passed`.
- Private focused ruff and ty checks: passed.
- Private target read-only audit exited `1` with expected blockers and printed the exact provision command.

## Coverage Rationale

This reduces operator friction for the next W5 dogfood step. It does not complete terminal dogfood evidence, W7 hosted proof, quota enforcement, or billing settlement.
