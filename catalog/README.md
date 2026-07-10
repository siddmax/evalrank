# Benchmark Catalog

`manifest.json` is the canonical public inventory and policy contract for cells,
ranking groups, benchmark families, feeds, governance, cadence, lineage,
retention, and publication eligibility.

`rank_eligible_count` is deliberately row-specific: on a ranking group it is
the number of exact evaluated configurations left after identity and evidence
gates; on a benchmark family or feed it is the number of validated native
observations. An active ranking group must meet its configured top-set overlap.

Cadence is fail-closed. An unvalidated feed has no cadence mode. A validated
`periodic` feed carries ordered refresh, stale, and stop-recommending windows.
A validated `frozen` feed instead pins an upstream version and UTC as-of time;
all recency windows remain null, so a static benchmark cannot imply freshness.

Feed lifecycle is independent. A family is a derived aggregate: `active` when
any feed is active, otherwise `shadow` when any feed has replayed, otherwise
`discovered` when any lead remains, and `quarantined` only when every feed is
quarantined. Feed validation status and quarantine reasons stay feed-specific;
the correlated-family group remains consistent across the family and its feeds.

`research-provenance.json` is its non-normative research companion. It records
the dated primary or official sources used to discover every manifest family
and links each manifest `research_flag` and non-null `quarantine_reason` to a
source-backed claim. Claims mark whether their wording comes directly from a
cited source or is an explicit EvalRank inference. A family with an empty
`claims` array has a discovery source only; no additional source claim is being
made.

Research provenance is not result-row lineage, an adapter admission report, a
rights grant, a configuration passport, or evidence of ranking readiness. None
of those states may be inferred from a source URL or claim. The manifest remains
the authority for fail-closed admission and publication state.

The companion is version-locked to the manifest and must cover its benchmark
families exactly, in manifest order. When a manifest release changes the family
inventory or research flags, update the companion in the same change and cite
new primary or official sources rather than secondary summaries.

Run:

```sh
python3 -m unittest tests.test_catalog_manifest tests.test_catalog_research_provenance
```
