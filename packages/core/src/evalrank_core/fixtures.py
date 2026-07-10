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
    ProblemDetails,
    RawEntry,
    RankedEntity,
    Recommendation,
    RankingGroup,
    ScoringStage,
    ScoringStageCatalog,
    StageCandidate,
    TheCall,
    UseCase,
    UseCaseCatalog,
)
from evalrank_core.canonical_json import sha256_hex
from evalrank_core.decision_contracts import (
    ConfigurationPassportV1,
    EvaluatedConfigurationV1,
    IntervalUncertaintyV1,
    ObservationV1,
    ProportionMetricV1,
    RunProvenanceV1,
)


PUBLIC_METHODOLOGY_VERSION = "2026-06-25.1.public-fixture-v1"
PUBLIC_GENERATED_AT = "2026-06-25T00:00:00Z"
PUBLIC_CATALOG_METHODOLOGY_VERSION = "2026-07-09.2.catalog-manifest-v1"
PUBLIC_CATALOG_GENERATED_AT = "2026-07-09T00:00:00Z"
PUBLIC_USE_CASE_ID = "web-browsing"
PUBLIC_FIXTURE_KINDS = (
    "candidate-set",
    "evidence",
    "evidence-set",
    "exclusion",
    "fingerprint",
    "observation",
    "problem",
    "raw-entry",
    "recommendation",
    "ranking-group",
    "request",
    "scoring-stages",
    "stage-candidate",
    "use-cases",
)


_USE_CASE_ROWS = (
    ("code-generation", "Code generation", "Produce correct code from a spec or prompt", ("model", "tool", "agent")),
    ("autonomous-swe-agent", "Autonomous SWE agent", "Complete repository-level software engineering tasks", ("model", "agent")),
    (
        "function-calling",
        "Function and tool calling",
        "Emit correct schema-valid tool calls",
        ("model", "tool", "agent"),
    ),
    ("mcp-tool-orchestration", "MCP tool orchestration", "Coordinate MCP tools to complete a task", ("model", "tool", "agent")),
    ("web-browsing", "Web browsing and navigation", "Retrieve and act on live web content", ("model", "tool", "agent")),
    ("computer-use", "Computer use", "Operate a graphical interface to complete a task", ("model", "agent")),
    ("deep-research", "Deep research", "Synthesize multiple sources with traceable citations", ("model", "tool", "agent")),
    ("customer-support", "Customer support agent", "Resolve user support issues end to end", ("model", "agent")),
    ("enterprise-crm-workflow", "Enterprise and CRM workflow", "Execute business workflows across enterprise systems", ("tool", "agent")),
    ("math-reasoning", "Mathematical reasoning", "Solve quantitative or symbolic problems", ("model",)),
    ("general-knowledge-qa", "General knowledge QA", "Answer broad knowledge questions accurately", ("model", "tool")),
    ("rag-retrieval", "RAG and retrieval", "Retrieve relevant context and ground an answer", ("model", "tool")),
    ("long-term-memory", "Long-term memory", "Persist and recall useful information across sessions", ("model", "tool", "agent")),
    ("finance", "Finance", "Perform domain-grounded financial reasoning and workflows", ("model", "tool", "agent")),
    ("legal", "Legal", "Perform domain-grounded legal reasoning and drafting", ("model", "tool", "agent")),
    ("medical", "Medical", "Perform domain-grounded clinical reasoning and question answering", ("model", "tool", "agent")),
    ("multilingual", "Multilingual", "Maintain quality across languages and translation tasks", ("model", "tool", "agent")),
    ("vision-multimodal", "Vision and multimodal", "Reason over images, audio, or video", ("model", "agent")),
    ("web-frontend-code-generation", "Web frontend code generation", "Build and iterate web interfaces from a specification", ("model", "agent")),
    ("devops-sre-terminal", "DevOps, SRE, and terminal", "Resolve infrastructure or incident tasks in a terminal", ("model", "agent")),
    ("mobile-codegen", "Mobile app code generation", "Build and iterate native or cross-platform mobile apps", ("model", "agent")),
    ("reasoning", "Reasoning", "Solve novel multi-step reasoning tasks", ("model",)),
    ("factuality", "Factuality", "Produce correct and grounded factual claims", ("model", "tool")),
    (
        "professional-deliverable-creation",
        "Professional deliverables",
        "Create review-ready professional work products from a complete brief, domain context, and reference files.",
        ("model", "agent"),
    ),
    (
        "machine-learning-engineering",
        "Machine-learning engineering",
        "Build, train, and optimize machine-learning solutions from datasets and scored task objectives.",
        ("agent",),
    ),
    (
        "computational-research-reproduction",
        "Computational research reproduction",
        "Reproduce published computational results by implementing or executing experiments from papers, code, data, and environments.",
        ("agent",),
    ),
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
    return UseCaseCatalog(
        methodology_version=PUBLIC_CATALOG_METHODOLOGY_VERSION,
        generated_at=PUBLIC_CATALOG_GENERATED_AT,
        use_cases=use_cases,
    )


_SCORING_STAGE_ROWS = (
    (
        "request-normalization",
        1,
        "Request normalization",
        "Convert a public use case into comparable entity types and constraints",
        ("EvaluationRequest",),
        ("EvaluationRequest",),
        "normalization rules only; no customer context or hosted policy",
    ),
    (
        "candidate-resolution",
        2,
        "Candidate resolution",
        "Identify public candidates that can be evaluated for the request",
        ("EvaluationRequest",),
        ("CandidateSet", "StageCandidate", "Exclusion"),
        "storage-free candidate refs only; source adapters and graph lookup stay private",
    ),
    (
        "evidence-attachment",
        3,
        "Evidence attachment",
        "Attach public evidence and ingested result provenance to candidates",
        ("CandidateSet", "StageCandidate"),
        ("EvidenceSet", "EvidenceItem", "ObservationV1"),
        "public evidence rows only; live evidence lookup and ledgers stay private",
    ),
    (
        "component-scoring",
        4,
        "Component scoring",
        "Expose named public score components on a 0-1 scale",
        ("EvidenceSet", "ObservationV1"),
        ("RankedEntity",),
        "component names and ranges only; weights, formulas, and calibration stay private",
    ),
    (
        "ranking-or-abstention",
        5,
        "Ranking or abstention",
        "Return ranked entities when evidence is sufficient or an abstention when it is not",
        ("RankedEntity", "Exclusion"),
        ("Recommendation", "TheCall", "Abstention"),
        "public decision shape only; thresholds and private confidence policy stay private",
    ),
    (
        "freshness-trust-labeling",
        6,
        "Freshness and trust labeling",
        "Attach public freshness, trust tier, caveats, and evidence counts",
        ("RankedEntity", "Recommendation"),
        ("RankedEntity", "Recommendation"),
        "labels and counts only; production telemetry and private trust policy stay private",
    ),
)


def sample_scoring_stage_catalog() -> ScoringStageCatalog:
    return ScoringStageCatalog(
        methodology_version=PUBLIC_METHODOLOGY_VERSION,
        generated_at=PUBLIC_GENERATED_AT,
        stages=tuple(
            ScoringStage(
                id=stage_id,
                ordinal=ordinal,
                name=name,
                description=description,
                input_contracts=input_contracts,
                output_contracts=output_contracts,
                public_boundary=public_boundary,
            )
            for stage_id, ordinal, name, description, input_contracts, output_contracts, public_boundary in _SCORING_STAGE_ROWS
        ),
    )


def sample_ranked_entity() -> RankedEntity:
    return RankedEntity(
        entity_type="component_configuration",
        entity_id=_sample_evaluated_configuration().evaluated_configuration_id,
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
        group_key="component_configuration",
        entity_type="component_configuration",
        ranked=(sample_ranked_entity(),),
        group_rationale="ranked within component_configuration only; no cross-kind score comparison",
    )


def sample_entity_ref() -> EntityRef:
    return EntityRef(
        entity_type="component_configuration",
        entity_id=_sample_evaluated_configuration().evaluated_configuration_id,
    )


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


def sample_problem_details() -> ProblemDetails:
    return ProblemDetails(
        type="https://evalrank.ai/problems/validation",
        title="Validation failed",
        status=422,
        detail="request_id is required",
        code="validation",
        retriable=False,
        field="request_id",
        request_id="req_public_fixture_01",
        doc_url="https://evalrank.ai/docs/errors#validation",
    )


def _sample_configuration_passport() -> ConfigurationPassportV1:
    return ConfigurationPassportV1(
        entity_kind="component_configuration",
        canonical_name="io.evalrank.public-search-demo",
        revision="2026-06-25",
        interaction_policy="retrieval",
        configuration_passport_class="component-configuration-v1",
        harness=None,
        scaffold=None,
        tools=("search",),
        quantization=None,
        system_prompt_policy=None,
        environment=None,
    )


def _sample_evaluated_configuration() -> EvaluatedConfigurationV1:
    passport = _sample_configuration_passport()
    return EvaluatedConfigurationV1(
        evaluated_configuration_id=f"config_{sha256_hex(passport.to_dict())}",
        passport=passport,
    )


def sample_observation() -> ObservationV1:
    return ObservationV1(
        observation_id="obs_public_demo_01",
        evaluated_configuration_id=_sample_evaluated_configuration().evaluated_configuration_id,
        metric=ProportionMetricV1(value="0.875", numerator=35, denominator=40),
        uncertainty=IntervalUncertaintyV1(
            low="0.8",
            high="0.88",
            confidence_level="0.95",
            method="reported",
        ),
        provenance=RunProvenanceV1(
            run_id="run_public_demo_01",
            benchmark_family_id="public-search-freshness",
            feed_id="public-search-freshness-official",
            source_artifact_id=f"artifact_{'a' * 64}",
            parser_id="public-fixture-parser",
            parser_version="1",
            started_at="2026-06-25T00:00:00Z",
            completed_at="2026-06-25T00:00:01Z",
            harness_version="2026-06-25.1",
        ),
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
        entity_types=("component_configuration",),
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
    if kind == "observation":
        return sample_observation().to_dict()
    if kind == "problem":
        return sample_problem_details().to_dict()
    if kind == "raw-entry":
        return sample_raw_entry().to_dict()
    if kind == "recommendation":
        return sample_recommendation().to_dict()
    if kind == "ranking-group":
        return sample_ranking_group().to_dict()
    if kind == "request":
        return sample_evaluation_request().to_dict()
    if kind == "scoring-stages":
        return sample_scoring_stage_catalog().to_dict()
    if kind == "stage-candidate":
        return sample_stage_candidate().to_dict()
    if kind == "use-cases":
        return sample_use_case_catalog().to_dict()
    raise ValueError(f"fixture kind must be one of: {', '.join(PUBLIC_FIXTURE_KINDS)}")
