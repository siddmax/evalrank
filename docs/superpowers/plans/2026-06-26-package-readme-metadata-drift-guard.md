# Package README Metadata Drift Guard Plan

Date: 2026-06-26

## Goal

Keep public package READMEs aligned with package manifests without adding publish automation, private package indexes, credentials, hosted deploy wiring, or private source material.

## Steps

1. Add concise package metadata blocks to public package READMEs.
2. Add deterministic manifest-to-README tests for Python packages and the TypeScript SDK.
3. Update `TESTS.md`, `docs/STATUS.md`, and `docs/PORTING.md`.
4. Run the focused metadata test, public boundary check, full local check, and pre-landing review before push.

## Public Boundary

- Safe: distribution names, imports, public dependencies, entrypoint, license, TypeScript module/type metadata, and private publish status.
- Excluded: release credentials, private package indexes, deployment wiring, hosted ops, private SDK routes, and live service defaults.
