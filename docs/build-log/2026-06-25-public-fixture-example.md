# Public Fixture Example

Date: 2026-06-25

## Built

- Added `examples/public_fixture.py`, a checkout-runnable example that prints a synthetic recommendation and evidence item as JSON.
- Added `tests/test_examples.py` to execute the example and verify stable public fixture fields.
- Updated root, example, test, status, and porting docs.

## Boundary

- Uses only public fixture factories from the public Python SDK and core package.
- Does not require network access, credentials, private data, database access, or package installation.

## Checks

```sh
python3 -m unittest tests.test_examples
python3 examples/public_fixture.py
```
