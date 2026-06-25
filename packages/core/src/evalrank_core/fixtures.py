from __future__ import annotations

from evalrank_core.contracts import (
    ConfidenceInterval,
    EntityRef,
    EvidenceItem,
    EvaluationRequest,
    Freshness,
    RankedEntity,
    Recommendation,
)


PUBLIC_METHODOLOGY_VERSION = "2026-06-25.1.public-fixture-v1"
PUBLIC_GENERATED_AT = "2026-06-25T00:00:00Z"


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


def sample_entity_ref() -> EntityRef:
    return EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")


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


def sample_evaluation_request() -> EvaluationRequest:
    return EvaluationRequest(
        request_id="req_public_fixture_01",
        use_case="web-research:freshness-check",
        entity_types=("mcp_server",),
        requested_at=PUBLIC_GENERATED_AT,
        constraints={"requires_citations": True},
    )


def sample_recommendation() -> Recommendation:
    return Recommendation.single_scale(
        request_id="req_public_fixture_01",
        use_case="web-research:freshness-check",
        methodology_version=PUBLIC_METHODOLOGY_VERSION,
        ranked=[sample_ranked_entity()],
        generated_at=PUBLIC_GENERATED_AT,
        depth_rationale="one public demo candidate clears the evidence floor",
    )
