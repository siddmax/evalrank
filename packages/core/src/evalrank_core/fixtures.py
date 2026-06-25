from __future__ import annotations

from evalrank_core.contracts import (
    CapabilityFingerprintInput,
    CandidateSet,
    ConfidenceInterval,
    EntityRef,
    Exclusion,
    EvidenceItem,
    EvidenceSet,
    EvaluationRequest,
    Freshness,
    RawEntry,
    RankedEntity,
    Recommendation,
    RankingGroup,
    ResultRow,
    StageCandidate,
    TheCall,
    UseCase,
    UseCaseCatalog,
)


PUBLIC_METHODOLOGY_VERSION = "2026-06-25.1.public-fixture-v1"
PUBLIC_GENERATED_AT = "2026-06-25T00:00:00Z"
PUBLIC_USE_CASE_ID = "web-browsing"
PUBLIC_FIXTURE_KINDS = (
    "candidate-set",
    "evidence",
    "evidence-set",
    "exclusion",
    "fingerprint",
    "raw-entry",
    "recommendation",
    "ranking-group",
    "result-row",
    "request",
    "stage-candidate",
    "use-cases",
)


_USE_CASE_ROWS = (
    ("code-generation", "Code generation", "Produce correct code from a spec or prompt", ("model", "tool", "agent")),
    ("autonomous-swe-agent", "Autonomous SWE agent", "End-to-end repo-level engineering", ("model", "agent")),
    ("function-calling", "Function / tool calling", "Emit correct schema-valid tool calls", ("model", "tool")),
    ("mcp-tool-orchestration", "MCP tool orchestration", "Chain MCP tools to complete a task", ("model", "tool", "agent")),
    ("web-browsing", "Web browsing / navigation", "Retrieve and act on live web content", ("model", "tool", "agent")),
    ("computer-use", "Computer use", "Operate a GUI or desktop to accomplish a task", ("model", "agent")),
    ("deep-research", "Deep research", "Multi-source synthesis with citations", ("model", "tool", "agent")),
    ("customer-support", "Customer support agent", "Resolve user issues end to end", ("model", "agent")),
    ("enterprise-crm-workflow", "Enterprise / CRM workflow", "Execute business workflows over SaaS systems", ("tool", "agent")),
    ("math-reasoning", "Math / quant reasoning", "Solve quantitative or symbolic problems", ("model",)),
    ("general-knowledge-qa", "General knowledge / QA", "Answer factual questions accurately", ("model", "tool")),
    ("rag-retrieval", "RAG / retrieval", "Retrieve relevant context and ground answers", ("model", "tool")),
    ("long-term-memory", "Long-term memory", "Persist and recall across sessions", ("model", "tool", "agent")),
    ("finance", "Finance", "Domain-grounded financial reasoning and workflows", ("model", "tool", "agent")),
    ("legal", "Legal", "Domain-grounded legal reasoning and drafting", ("model", "tool", "agent")),
    ("medical", "Medical", "Domain-grounded clinical reasoning and QA", ("model", "tool", "agent")),
    ("multilingual", "Multilingual", "Quality across languages including translation", ("model", "tool", "agent")),
    ("vision-multimodal", "Vision / multimodal", "Reason over images, audio, or video", ("model", "agent")),
    ("web-frontend-code-generation", "Web / frontend code generation", "Build and iterate web UIs from a spec", ("model", "agent")),
    ("devops-sre-terminal", "DevOps / SRE / terminal", "Resolve infra or incident tasks in a terminal", ("model", "agent")),
    ("mobile-codegen", "Mobile app code generation", "Build and iterate native or cross-platform mobile apps", ("model", "agent")),
)


def sample_capability_fingerprint_input() -> CapabilityFingerprintInput:
    return CapabilityFingerprintInput(
        id_scheme="reverse_dns",
        canonical_id="io.evalrank.public-search-demo",
        entity_kind="mcp_server",
        declared_capability_shape={
            "tool_names": ["search"],
            "param_schemas": {"search": {"type": "object"}},
            "declared_scopes": ["web.search"],
            "commit_sha": "abc123",
        },
    )


def sample_raw_entry() -> RawEntry:
    return RawEntry(
        source="public-fixture",
        source_id="public-fixture:search-demo:2026-06-25",
        entity_kind="mcp_server",
        canonical_id="io.evalrank.public-search-demo",
        raw_metadata={
            "display_name": "Public Search Demo",
            "homepage": "https://example.com/evalrank/public-search-demo",
        },
        declared_capability_shape={
            "tool_names": ["search"],
            "param_schemas": {"search": {"type": "object"}},
        },
        fetched_at=PUBLIC_GENERATED_AT,
    )


def sample_use_case_catalog() -> UseCaseCatalog:
    use_cases = tuple(
        UseCase(
            id=use_case_id,
            name=name,
            definition=definition,
            entity_kinds=entity_kinds,
        )
        for use_case_id, name, definition, entity_kinds in _USE_CASE_ROWS
    )
    safety_overlay = UseCase(
        id="safety-robustness",
        name="Safety / robustness",
        definition="Resistance to injection, jailbreak, tool-poisoning, SSRF, rug-pull, or harmful output",
        entity_kinds=("model", "tool", "agent"),
        rank_policy="veto_overlay",
        is_overlay=True,
    )
    return UseCaseCatalog(
        methodology_version=PUBLIC_METHODOLOGY_VERSION,
        generated_at=PUBLIC_GENERATED_AT,
        use_cases=(*use_cases, safety_overlay),
    )


def sample_ranked_entity() -> RankedEntity:
    return RankedEntity(
        entity_type="mcp_server",
        entity_id="tool:public-search-demo",
        rank=1,
        capability_score=0.84,
        confidence=0.86,
        ci95=ConfidenceInterval(low=0.80, high=0.88),
        methodology_version=PUBLIC_METHODOLOGY_VERSION,
        trust_tier="standardized",
        freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
        evidence_count=1840,
        score_components={
            "capability": 0.84,
            "evidence": 0.91,
            "freshness": 0.87,
        },
    )


def sample_ranking_group() -> RankingGroup:
    return RankingGroup(
        group_key="mcp_server",
        entity_type="mcp_server",
        ranked=(sample_ranked_entity(),),
        group_rationale="ranked within mcp_server only; no cross-kind score comparison",
    )


def sample_entity_ref() -> EntityRef:
    return EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")


def sample_exclusion() -> Exclusion:
    return Exclusion(
        subject=sample_entity_ref(),
        reason="unknown_cost",
        detail="cost is unknown for this public fixture",
    )


def sample_evidence_item() -> EvidenceItem:
    return EvidenceItem(
        evidence_id="ev_public_trace_01",
        subject=sample_entity_ref(),
        kind="trace",
        source="public-fixture",
        observed_at=PUBLIC_GENERATED_AT,
        summary="public search demo returned a fresh cited result",
        score=0.8754321,
        metadata={"latency_ms": 1200},
    )


def sample_result_row() -> ResultRow:
    return ResultRow(
        entity_id="tool:public-search-demo",
        entity_kind="tool_server",
        benchmark_id="bench_public_search_freshness",
        benchmark_version="2026-06-25",
        harness="public-fixture-harness",
        harness_version="2026-06-25.1",
        is_self_reported=False,
        n_items=40,
        ci95=ConfidenceInterval(low=0.80, high=0.88),
        score_raw=0.8754321,
        score_unit="pass_rate",
        date_run="2026-06-25",
        model_version="public-search-demo@2026-06-25",
        provenance={
            "source": "public-fixture",
            "raw_snapshot_uri": "https://example.com/evalrank/public-search-demo/raw.json",
        },
        source_url="https://example.com/evalrank/public-search-demo",
        attribution_string="Synthetic public fixture",
        flags={
            "saturated": False,
            "contaminated": False,
            "judge_model_dependent": False,
            "scaffold_nonstandard": False,
        },
        verification_state="verified",
    )


def sample_evidence_set() -> EvidenceSet:
    return EvidenceSet(
        request_id="req_public_fixture_01",
        use_case=PUBLIC_USE_CASE_ID,
        evidence_items=(sample_evidence_item(),),
        generated_at=PUBLIC_GENERATED_AT,
    )


def sample_evaluation_request() -> EvaluationRequest:
    return EvaluationRequest(
        request_id="req_public_fixture_01",
        use_case=PUBLIC_USE_CASE_ID,
        entity_types=("mcp_server",),
        requested_at=PUBLIC_GENERATED_AT,
        constraints={"requires_citations": True},
    )


def sample_candidate_set() -> CandidateSet:
    return CandidateSet(
        request_id="req_public_fixture_01",
        use_case=PUBLIC_USE_CASE_ID,
        candidates=(sample_entity_ref(),),
        generated_at=PUBLIC_GENERATED_AT,
    )


def sample_stage_candidate() -> StageCandidate:
    return StageCandidate(
        candidate_id=sample_capability_fingerprint_input().fingerprint(),
        entity=sample_entity_ref(),
        fused_score=0.0327864,
        rrf_components={"lexical_rank": 1, "semantic_rank": 2, "graph_rank": None},
        retrieval_arms=("lexical", "semantic"),
        use_case=PUBLIC_USE_CASE_ID,
    )


def sample_recommendation() -> Recommendation:
    return Recommendation.single_scale(
        request_id="req_public_fixture_01",
        use_case=PUBLIC_USE_CASE_ID,
        methodology_version=PUBLIC_METHODOLOGY_VERSION,
        ranked=[sample_ranked_entity()],
        generated_at=PUBLIC_GENERATED_AT,
        depth_rationale="one public demo candidate clears the evidence floor",
        the_call=TheCall.recommend(
            confidence=0.86,
            reason="one public demo candidate clears the evidence floor",
        ),
    )


def sample_public_fixture(kind: str) -> dict:
    if kind == "candidate-set":
        return sample_candidate_set().to_dict()
    if kind == "evidence":
        return sample_evidence_item().to_dict()
    if kind == "evidence-set":
        return sample_evidence_set().to_dict()
    if kind == "exclusion":
        return sample_exclusion().to_dict()
    if kind == "fingerprint":
        return sample_capability_fingerprint_input().to_dict()
    if kind == "raw-entry":
        return sample_raw_entry().to_dict()
    if kind == "recommendation":
        return sample_recommendation().to_dict()
    if kind == "ranking-group":
        return sample_ranking_group().to_dict()
    if kind == "result-row":
        return sample_result_row().to_dict()
    if kind == "request":
        return sample_evaluation_request().to_dict()
    if kind == "stage-candidate":
        return sample_stage_candidate().to_dict()
    if kind == "use-cases":
        return sample_use_case_catalog().to_dict()
    raise ValueError(f"fixture kind must be one of: {', '.join(PUBLIC_FIXTURE_KINDS)}")
