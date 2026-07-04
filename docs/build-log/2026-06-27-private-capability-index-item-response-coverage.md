# 2026-06-27 Private Capability-Index Item-Response Coverage

## Scope

Updated the private Syndai EvalRank worktree to broaden live response coverage beyond the prior agent-lane proof. This is a public-safe status record only; source code, database migrations, and private row contents remain in Syndai.

## What Changed Privately

- Added a source-specific capability-index item-response projector.
- Kept the generic item-response projector strict: aggregate result rows are still rejected unless a source adapter can map each component to real criterion items.
- Decomposed capability-index score components into normalized criterion responses with separate response weights.

## Target Proof

- Projected 203 capability-index criterion responses into the private `evalrank.item_response_rows` table.
- Matrix shape: 29 tool entities, 7 criterion items, 200 binary responses, and 3 fractional responses.
- Fit a two-chain private Bayesian 2PL batch over the eligible binary subset.
- The fit wrote 29 calibration rows and 7 item-parameter rows, but remained non-publishable because diagnostics still reported sampler divergences.
- Rebuilt capability-index contamination rows: 29 clean source rows, 29 clean fingerprint rows, 29 temporal unknown rows, and 29 semantic unknown rows.
- Rebuilt 29 Stage-2 scorer rows and 29 Stage-4 conformal-shortlist rows.
- Rematerialized the private `web-browsing` capability-index cache as recommendation `rec_d055f34b9a7a7743f03b85bc`.

## Status

This improves W1-W5 response coverage and proves the tool-lane scoring path can run through item responses, IRT persistence, contamination checks, Stage-2, Stage-4, and materialization. It does not mark broader IRT complete; only the earlier pooled agent-lane fit currently has publishable multi-chain plus SBC diagnostics.
