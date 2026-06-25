# TypeScript Fixture Kind Parity

Date: 2026-06-26

## What Changed

- Added `PUBLIC_FIXTURE_KINDS` to the TypeScript SDK.
- Added `PublicFixtureKind` as the string-union type derived from that constant.
- Extended TypeScript SDK drift tests so the constant stays aligned with the core public fixture-kind list.

## Public Boundary

- This is type/constant parity only.
- No service client, network call, auth flow, hosted receipt behavior, private data access, production evidence, or held-out eval material was added.

## Verification Intent

- Run the TypeScript SDK unit drift test.
- Run the package syntax check.
- Run the full public boundary and unit-test gate before pushing.
