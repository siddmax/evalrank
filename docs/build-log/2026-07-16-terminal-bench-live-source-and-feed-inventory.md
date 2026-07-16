# Terminal-Bench Live Source and Feed Inventory

Date: 2026-07-16

The public catalog contract at `434fc2476c47ece2c5b756495f14854bf47fae59` and private consumer at `d85b9e2dcf019e5d268b16dee07e85b5324eeca9` form the paired Terminal-Bench 2.1 source repair.

The public repository now generates one closed, nested `catalog/feeds.json` projection from `catalog/manifest.json` and `catalog/research-provenance.json`. It contains no private runtime or probe state. The private operator can render static TSV or JSONL and can independently overlay cursor-bound last-good evidence or an ephemeral manual probe.

The accepted manual probe used the official public Hub board plus an exact GitHub commit archive. Two complete Hub reads were semantically stable and the 17 public display rows reconciled exactly against 20 current-schema repository submissions at commit `36d417f56c293b8271b306a0e4c566f58e98c153`; three validated repository-only rows were treated as unpublished history and emitted no observations. The accepted source version was `hub_d41b509716d6dd63c2fe1d3a234c676cfdaa31cad99b97fbc56f6d3304d16cff__repo_36d417f56c293b8271b306a0e4c566f58e98c153`. The exact Hub and repository-archive SHA-256 digests were `d41b509716d6dd63c2fe1d3a234c676cfdaa31cad99b97fbc56f6d3304d16cff` and `c217bf6a30104d297f978c771f83cf50a715236dfb66e6340442d6e96effdfa2`.

The probe was read-only and persistence-free. Rights remain unknown, artifact retention remains disabled, and the source remains manual-only and publication-disabled. The accepted bytes were discarded, so this evidence supports `shadow` parser status but not durable replay. Terminal-Bench remains explorer evidence for `terminal-generalist`; this change does not admit it to a published coding-model ranking.

A one-time manual fleet probe enumerated the policy-derived manual set without adding scheduling. It surfaced seven healthy feeds and one unrelated unhealthy DeepSWE feed. That result is operational evidence only and does not revise unrelated public catalog states or expand this repair into other adapters.

The private consumer also advances its EvalRank methodology authority to bind the exact public manifest and generated inventory. That authority change is append-only and deployment-gated; this public log records the paired source revisions but does not claim that a private migration or service deployment completed.
