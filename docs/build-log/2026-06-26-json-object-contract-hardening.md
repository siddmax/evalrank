# JSON-Object Contract Hardening

Date: 2026-06-26

## Built

- Hardened `EvidenceItem.metadata` as a public JSON object.
- Hardened `EvaluationRequest.constraints` as a public JSON object.
- Added regression tests for non-object values, nested non-string keys, and non-JSON values.
- Updated public status, porting, test, core README, and schema README docs.

## Public Boundary

- This change only validates already-public extension fields before serialization.
- It does not add evidence lookup, source adapters, graph persistence, private policy semantics, scorer behavior, or hosted service behavior.

## Verification

```sh
python3 -m unittest tests.test_core_contracts.CoreContractTests.test_evidence_item_rejects_invalid_kind_or_score tests.test_core_contracts.CoreContractTests.test_evaluation_request_rejects_missing_required_context
python3 -m unittest tests.test_core_contracts
make check
git diff --check
```
