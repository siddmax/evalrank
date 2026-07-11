# Independent Family Admission Research

Date: 2026-07-10

Primary-source review separated benchmark quality from publication readiness. A useful benchmark does not become top-set evidence until its result artifact, configuration identity, rights, native sampling unit, lineage, cadence, overlap, and residual independence are all validated.

## Admitted to shadow replay

- **Aider Polyglot** is a code-editing **agent-system** family, not a direct-prompt model family. Its Apache-2.0 result YAML preserves model, Aider version, edit format, command, harness commit, date, pass counts, cost, and task count. Dirty harness commits are excluded. The copied exercise corpus has no root license, so only the licensed result artifact is retained. Its fixed 225-task corpus and October 2025 evidence make it low-weight and stale-aware.
- **ITBench SRE** is a licensed incident-response family. The Apache-2.0 `LEADERBOARD_SRE.md` artifact preserves multiple-trial incident count, resolution rate, NTAM diagnosis effects, standard errors, and standard deviations. Its February 2025 result is frozen and stale; unresolved exact agent/model identity keeps it out of ranked publication.

## Corrected decision cells

The former `devops-sre-terminal` cell pooled three different jobs. It is replaced by:

- `sre-incident-response`: diagnose and repair live service or infrastructure incidents;
- `devops-lifecycle`: build, configure, test, deploy, and monitor delivery systems;
- `terminal-generalist`: complete heterogeneous computer tasks through a shell.

Terminal-Bench 2.1 now belongs only to `terminal-generalist`. It does not count as autonomous issue-resolution or SRE evidence. Aider Polyglot uses a new agentic code-generation ranking group.

## Relevant candidates that remain unadmitted

- **Reasoning:** LiveBench reasoning is the best current active candidate but needs aligned task-level question/judgment snapshots and calibrated task-block uncertainty. HLE is valuable expert-knowledge evidence but its fixed public set, weak run identity, and score-redistribution gap keep it shadow-only. ARC-AGI-2 is highly independent fluid-reasoning evidence, but the official site's terms prohibit automated retrieval and database compilation without permission. No scraper is added.
- **Code:** BigCodeBench is rejected as top-set input because its public scores are stale, aggregate-only, version-lagged, weakly identified, and unlicensed. SciCode is a small stale science/code hybrid and is not independent of science reasoning plus generic code generation. LiveCodeBench remains useful shadow evidence but its official score feed is stale and task redistribution rights are ambiguous.
- **Function calling:** BFCL remains the model-configuration anchor. ComplexFuncBench has useful long-context constraints but no licensed machine-readable result artifact or exact run identity. τ²/τ³ is strong interactive agent/customer-support evidence and must be evaluated in its agent ranking group, not used to inflate BFCL's model-family count.
- **Autonomous SWE:** SWE-bench Live and SWE-rebench are high-quality but correlated GitHub-issue families; absent residual-independence calibration they count as one. Their submitted score bytes lack an explicit reusable license. SWE-Lancer is relevant but static, single-codebase, and lacks a neutral machine-readable cross-vendor leaderboard. LiveSWEBench is added as a research candidate because it separates agentic programming, targeted editing, and autocompletion.
- **SRE/DevOps:** AIOpsLab is a harness without a maintained result family. SREGym imports ITBench and AIOpsLab, so only a hash-deduplicated `SREGym-new` stratum could become independent. DevOps-Gym is relevant to the separate lifecycle cell but lacks explicit result rights and a stable machine-readable artifact.

## Remaining top-set gaps

No ranking group currently has three independently calibrated, rights-cleared families with exact overlapping configurations. The shortest honest paths are:

1. Reasoning: task-level LiveBench + rights-cleared HLE + permissioned ARC-AGI-2, with exact configuration overlap and block-bootstrap calibration.
2. Code-editing agents: Aider Polyglot + a licensed fresh repository-editing family + a distinct integration/task family; do not substitute one-shot model code generation.
3. Function-calling models: BFCL + reproducible ComplexFuncBench + a genuinely distinct model-level function-call family; τ-bench is not that family.
4. Autonomous SWE: one GitHub-issue family + SWE-Lancer IC-SWE + a separately sourced agentic programming family, each with repeated runs.
5. SRE: ITBench + first-party fixed AIOpsLab runs + de-overlapped SREGym-new. Full SREGym cannot count independently.

Until those gates pass, EvalRank should show explorer evidence and the missing-family gap, never manufacture a top set.
