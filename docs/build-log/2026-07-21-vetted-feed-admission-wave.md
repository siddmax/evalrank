# 2026-07-21 — Vetted feed admission wave (manifest 2026-07-21.1)

## What changed

Ten feeds moved to executable shadow contracts (rights approved with dated
license evidence, retention enabled, periodic polling cadence, declared lineage
and correlation identity). No cell, ranking group, eligibility constant, or
method rule changed: everything remains `preview`, and explorer views stay the
only publishable claim until calibration gates pass.

- `terminal-bench-2-1-discovery` — Apache-2.0 (harbor-framework/terminal-bench-2-1;
  submissions live in-repo under `leaderboard/submissions/`). Daily poll,
  stale after 14 days.
- `aider-polyglot-discovery` — Apache-2.0 (Aider-AI/aider). Weekly poll; upstream
  dormant since 2025-10-03, recorded as a provenance version-status claim; the
  periodic contract describes EvalRank's polling, not upstream activity.
- `itbench-discovery` — rights were already approved; cadence moved
  frozen → periodic weekly.
- Six Epoch Benchmarking Hub data-view feeds — `scicode-discovery`,
  `arc-agi-2-discovery`, `hle-discovery`, `frontiermath-v2-discovery`,
  `simpleqa-verified-discovery`, `theagentcompany-discovery` — CC-BY-4.0 with
  per-source pass-through (epoch.ai/benchmarks/use-this-data; data:
  epoch.ai/data/benchmark_data.zip). Each declares the underlying benchmark
  lineage as its correlated family group so an Epoch data view can never count
  as independent evidence against another feed of the same lineage, and a
  quarantined lineage stays quarantined regardless of mirror.
- `webdev-arena-discovery` — CC-BY-4.0
  (huggingface.co/datasets/lmarena-ai/leaderboard-dataset, `webdev`/`latest`;
  card verified 2026-07-21). Daily poll.

## Dated parse-probe evidence (ephemeral probes; bytes discarded)

- `aider-polyglot-discovery`: healthy at 2026-07-21T18:49:51Z; 31 rows; git blob
  `1ddb905c42025459745ecbbbc4f07c82f5a1dd4e`; SHA-256
  `85a50b25953512d18ba4bb0c23c0b8e626fcf9a5b52d287644b8a0b44b9535de` (45,725 bytes).
- `itbench-discovery`: healthy at 2026-07-21T18:50:48Z; 1 row; git blob
  `b2a4f2baaa235c82ff6412ccec98eec759688dc7`; SHA-256
  `869e760ddd2e86dbeca942e8577e1f7cf95045043f5dba288350011a7b2c3e37` (3,304 bytes).
- `terminal-bench-2-1-discovery`: healthy at 2026-07-21T19:10:40Z; 17 display
  rows reconciled against 20 repository submissions; Hub snapshot SHA-256
  `6ec26617a7ff433c0c87ec80a25aa810f2dedbf096666f30f61a61445132069c`
  (26,854 bytes) plus repository archive SHA-256
  `c217bf6a30104d297f978c771f83cf50a715236dfb66e6340442d6e96effdfa2`
  (53,297,933 bytes). The probe required accepting the Hub's additive
  `dataset_version_ids` leaderboard field (observed live 2026-07-21) as
  optional metadata in the private resolver.
- `deepswe-discovery` continues on its scheduled daily contract; its parse
  evidence is the runtime pipeline-run record, not a manual probe.
- The six Epoch data-view feeds and `webdev-arena-discovery` were admitted with
  adapter contracts landed the same day in the private runtime; their first
  dated parse evidence is recorded by the runtime's pipeline runs.

## Sources that stay unscheduled, with reasons recorded in provenance

- `livecodebench` — the served `performances_generation.json` carries no license
  grant (repo license covers code, not the leaderboard artifact).
- `bfcl-v4` — `gorilla.cs.berkeley.edu/data_overall.csv` has no license statement.
- `livebench-reasoning` — livebench.ai CSVs carry no data license.
- `swe-rebench` — the CC-BY-4.0 HF dataset contains task instances, not
  leaderboard scores (verified 2026-07-21); the site leaderboard is embedded
  RSC state without a data contract.
- `swe-bench-verified` / `swe-bench-pro` — quarantined, unchanged.

A granted permission request is the unlock for the first three; each has a
dated rights-gap claim in `catalog/research-provenance.json`.

## Paired private change (Syndai)

The same-day private runtime change fixes the deepswe counted-proportion
double-rounding crash (exact count-derived metric values; deterministic
observation validation errors now quarantine instead of retry-and-dead-letter),
adds the Epoch Hub and LMArena WebDev adapters, accepts the Hub's additive
leaderboard field, and disables the frontier digest email transport at the
worker seam while keeping the weekly cycle, watched-model registry updates, and
the EvalRank nomination intact. Paired SHAs are recorded in `docs/PORTING.md`.
