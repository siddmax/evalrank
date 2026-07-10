# Portable Truth-Kernel Contracts

The public core now defines the storage-free interoperability boundary needed by a hosted EvalRank implementation:

- immutable source artifacts and run provenance;
- native observations without the legacy model-centric result row;
- exact evaluated-configuration passports separated from serving offers;
- reviewed, dated evaluation-to-offer links with explicit evidence basis;
- closed monthly measured/estimated usage and effective-dated pricing schedules with exact-TTL cache rates;
- fail-closed one-ceiling cost computation plus explicit zero-cache sensitivity for estimated cached usage, projected-cost vocabulary, cross-profile budget enforcement, and mandatory divergence caveats;
- normalized semantic decision queries and deterministic full-body receipt identities;
- content-addressed grouped leaderboard, entity-detail, and compare reads; and
- strict, extension-preserving Problem Details decoding.

Python and TypeScript share one restricted-JCS golden corpus. The public repository still owns no persistence, hosted scorer, customer data, deployment behavior, or private benchmark material. Hosted consumers must pin the immutable public commit containing this entry and verify every schema/catalog digest before startup.

Verification for this public slice is recorded by `make check`; paired public/private identifiers are added only after the private consumer lands independently.
