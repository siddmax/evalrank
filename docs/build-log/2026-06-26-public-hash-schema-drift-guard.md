# Public Hash Schema Drift Guard

Date: 2026-06-26

## What changed

- Schema tests now pin `capability_fingerprint` and raw-entry `content_hash` as 64-character lowercase hex strings.
- Public schema docs now mention the generated hash shape.

## Public boundary

This is a storage-free schema drift guard over generated public identifiers. No source adapter behavior, live fetch behavior, private entity rows, persistence, hosted receipt behavior, secrets, telemetry, or private runtime moved.

## Verification

```sh
python3 -m unittest tests.test_schema_contracts.SchemaContractTests.test_generated_hash_schemas_pin_lowercase_hex_shape
```
