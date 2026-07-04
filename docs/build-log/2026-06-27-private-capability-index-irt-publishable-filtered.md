# Private Capability-Index IRT Publishable Filtered Fit

Date: 2026-06-27

## What Changed

- Private Syndai EvalRank now filters non-informative binary IRT items before running the NumPyro 2PL fit.
- Private IRT batch settings now expose `target_accept_prob`, with a conservative default of `0.95` for offline calibration quality.
- This keeps all-pass/all-fail criterion items out of the sampler instead of treating them as identifiable evidence.

## Target Proof

- Private capability-index fit wrote `29` calibration rows and `3` item-parameter rows with `publishable=True`.
- Diagnostics: `response_count=203`, `binary_response_count=87`, `excluded_response_count=116`, `divergence_count=0`, `max_r_hat=1.005729`, `min_effective_sample_size=563.65863`.
- Stage-2 and Stage-4 each wrote `29` rows, and the active web-browsing recommendation stayed `rec_d055f34b9a7a7743f03b85bc`.

## What Stayed Private

- No public IRT runtime, private weights, private source rows, or private benchmark text moved to this repo.
- Public EvalRank remains the storage-free contract/reference layer; DB-backed fitting stays in Syndai during incubation.

## Verification

- Private red/green test for non-informative item exclusion.
- Private focused IRT/script tests passed with `14 passed`.
- Private type check passed.
