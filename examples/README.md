# Examples

Runnable public examples use synthetic, product-neutral fixtures only.

## Public Fixture

```sh
python3 examples/public_fixture.py
```

The command emits `fingerprint`, `observation`, `problem`, `raw_entry`, and `use_cases`.

## Decision Golden

`decision-contract-v1.golden.json` is the shared Python/TypeScript corpus for `DecisionQueryV1` restricted-JCS bytes and content-addressed `DecisionReceiptV1` identity. The local reference server accepts the receipt's exact semantic query, returns the golden receipt, and retains it only when `?share=true` is explicit.

Run the end-to-end contract exerciser with:

```sh
PYTHONPATH=packages/core/src python3 scripts/reference_server.py --port 8000
python3 -m unittest tests.test_reference_server_e2e
```
