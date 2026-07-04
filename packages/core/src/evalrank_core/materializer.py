from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from evalrank_core.contracts import (
    Abstention,
    CandidateSet,
    ConfidenceInterval,
    EntityRef,
    EvaluationRequest,
    EvidenceItem,
    EvidenceSet,
    Exclusion,
    Freshness,
    RankedEntity,
    Recommendation,
    ResultRow,
    StageCandidate,
    TheCall,
)


_RESULT_KIND_BY_ENTITY_TYPE = {
    "agent": "agent",
    "mcp_server": "tool_server",
    "model": "model",
    "tool": "tool_server",
    "tool_server": "tool_server",
}


def materialize_recommendation(
    *,
    request: EvaluationRequest,
    candidate_set: CandidateSet,
    stage_candidates: tuple[StageCandidate, ...],
    evidence_set: EvidenceSet,
    result_rows: tuple[ResultRow, ...] = (),
    exclusions: tuple[Exclusion, ...] = (),
    methodology_version: str,
    generated_at: str,
) -> Recommendation:
    """Emit a deterministic public recommendation from already-provided inputs.

    This reference materializer is intentionally storage-free: callers supply
    the candidate, Stage-1, evidence, result, and exclusion rows. Private source
    lookup, DB persistence, scorer weights, calibration, and live telemetry stay
    outside this public package.
    """

    _validate_inputs(
        request=request,
        candidate_set=candidate_set,
        stage_candidates=stage_candidates,
        evidence_set=evidence_set,
        result_rows=result_rows,
        exclusions=exclusions,
    )

    candidate_keys = {_entity_key(candidate) for candidate in candidate_set.candidates}
    excluded_keys = {_entity_key(exclusion.subject) for exclusion in exclusions}
    evidence_by_key = _group_evidence(evidence_set.evidence_items)
    result_rows_by_key = _group_result_rows(result_rows, candidate_set.candidates)

    ranked_stages = [
        stage
        for stage in sorted(stage_candidates, key=lambda stage: (-stage.fused_score, stage.candidate_id))
        if _entity_key(stage.entity) in candidate_keys and _entity_key(stage.entity) not in excluded_keys
    ]
    materializable_stages = [
        stage
        for stage in ranked_stages
        if evidence_by_key.get(_entity_key(stage.entity)) or result_rows_by_key.get(_entity_key(stage.entity))
    ]

    if not materializable_stages:
        return _abstain(
            request=request,
            methodology_version=methodology_version,
            generated_at=generated_at,
            exclusions=exclusions,
            detail="No non-excluded candidate has public evidence or result rows for this request.",
        )

    max_fused_score = max(stage.fused_score for stage in materializable_stages)
    evidence_counts = {
        _entity_key(stage.entity): len(evidence_by_key.get(_entity_key(stage.entity), ()))
        + len(result_rows_by_key.get(_entity_key(stage.entity), ()))
        for stage in materializable_stages
    }
    max_evidence_count = max(evidence_counts.values())
    ranked = [
        _ranked_entity(
            rank=rank,
            stage=stage,
            evidence_items=evidence_by_key.get(_entity_key(stage.entity), ()),
            result_rows=result_rows_by_key.get(_entity_key(stage.entity), ()),
            max_fused_score=max_fused_score,
            max_evidence_count=max_evidence_count,
            methodology_version=methodology_version,
            generated_at=generated_at,
        )
        for rank, stage in enumerate(materializable_stages, start=1)
    ]
    confidence = ranked[0].confidence

    return Recommendation(
        request_id=request.request_id,
        use_case=request.use_case,
        methodology_version=methodology_version,
        generated_at=generated_at,
        comparability="single-scale",
        ranked=ranked,
        groups=None,
        shortlist_depth=len(ranked),
        depth_rationale="public reference materializer ranked candidates by Stage-1 fused score",
        degraded=False,
        served_from="materialized-cache",
        base_snapshot_lag_ms=0,
        the_call=TheCall.recommend(
            confidence=confidence,
            reason="public evidence was sufficient to return a deterministic ranking",
        ),
        exclusions=list(exclusions),
    )


def _validate_inputs(
    *,
    request: EvaluationRequest,
    candidate_set: CandidateSet,
    stage_candidates: tuple[StageCandidate, ...],
    evidence_set: EvidenceSet,
    result_rows: tuple[ResultRow, ...],
    exclusions: tuple[Exclusion, ...],
) -> None:
    if not isinstance(request, EvaluationRequest):
        raise TypeError("request must be an EvaluationRequest")
    if not isinstance(candidate_set, CandidateSet):
        raise TypeError("candidate_set must be a CandidateSet")
    if not isinstance(evidence_set, EvidenceSet):
        raise TypeError("evidence_set must be an EvidenceSet")
    if not isinstance(stage_candidates, tuple):
        raise ValueError("stage_candidates must be a tuple")
    if not isinstance(result_rows, tuple):
        raise ValueError("result_rows must be a tuple")
    if not isinstance(exclusions, tuple):
        raise ValueError("exclusions must be a tuple")
    if candidate_set.request_id != request.request_id:
        raise ValueError("candidate_set.request_id must match request.request_id")
    if candidate_set.use_case != request.use_case:
        raise ValueError("candidate_set.use_case must match request.use_case")
    if evidence_set.request_id != request.request_id:
        raise ValueError("evidence_set.request_id must match request.request_id")
    if evidence_set.use_case != request.use_case:
        raise ValueError("evidence_set.use_case must match request.use_case")

    candidate_keys = {_entity_key(candidate) for candidate in candidate_set.candidates}
    for candidate in candidate_set.candidates:
        if candidate.entity_type not in request.entity_types:
            raise ValueError("candidate_set candidates must use request entity_types")

    seen_stage_entities: set[tuple[str, str]] = set()
    seen_stage_ids: set[str] = set()
    for stage in stage_candidates:
        if not isinstance(stage, StageCandidate):
            raise TypeError("stage_candidates must contain StageCandidate values")
        if stage.use_case != request.use_case:
            raise ValueError("stage_candidates use_case must match request.use_case")
        key = _entity_key(stage.entity)
        if key not in candidate_keys:
            raise ValueError("stage_candidates must reference candidate_set candidates")
        if key in seen_stage_entities or stage.candidate_id in seen_stage_ids:
            raise ValueError("stage_candidates must be unique")
        seen_stage_entities.add(key)
        seen_stage_ids.add(stage.candidate_id)

    for evidence_item in evidence_set.evidence_items:
        if _entity_key(evidence_item.subject) not in candidate_keys:
            raise ValueError("evidence_set evidence_items must reference candidate_set candidates")

    result_keys = set(_result_keys_for_candidates(candidate_set.candidates).values())
    for result_row in result_rows:
        if not isinstance(result_row, ResultRow):
            raise TypeError("result_rows must contain ResultRow values")
        if (result_row.entity_kind, result_row.entity_id) not in result_keys:
            raise ValueError("result_rows must reference candidate_set candidates")

    for exclusion in exclusions:
        if not isinstance(exclusion, Exclusion):
            raise TypeError("exclusions must contain Exclusion values")
        if _entity_key(exclusion.subject) not in candidate_keys:
            raise ValueError("exclusions must reference candidate_set candidates")


def _ranked_entity(
    *,
    rank: int,
    stage: StageCandidate,
    evidence_items: Iterable[EvidenceItem],
    result_rows: Iterable[ResultRow],
    max_fused_score: float,
    max_evidence_count: int,
    methodology_version: str,
    generated_at: str,
) -> RankedEntity:
    evidence_items = tuple(evidence_items)
    result_rows = tuple(sorted(result_rows, key=lambda row: (row.date_run, row.benchmark_id, row.model_version)))
    evidence_count = len(evidence_items) + len(result_rows)
    stage_score = _unit_ratio(stage.fused_score, max_fused_score)
    evidence_coverage = _unit_ratio(evidence_count, max_evidence_count)
    result_score = _result_score(result_rows, evidence_items)
    confidence = _round_score((stage_score + evidence_coverage + result_score) / 3)

    return RankedEntity(
        entity_type=stage.entity.entity_type,
        entity_id=stage.entity.entity_id,
        rank=rank,
        capability_score=stage_score,
        confidence=confidence,
        ci95=_confidence_interval(confidence, result_rows),
        methodology_version=methodology_version,
        trust_tier=_trust_tier(result_rows),
        freshness=_freshness(result_rows, evidence_items, generated_at),
        evidence_count=evidence_count,
        caveats=("public_reference_materializer",),
        score_components={
            "evidence_coverage": evidence_coverage,
            "result_score": result_score,
            "stage1_fused": stage_score,
        },
    )


def _group_evidence(evidence_items: tuple[EvidenceItem, ...]) -> dict[tuple[str, str], tuple[EvidenceItem, ...]]:
    grouped: dict[tuple[str, str], list[EvidenceItem]] = defaultdict(list)
    for item in evidence_items:
        grouped[_entity_key(item.subject)].append(item)
    return {key: tuple(sorted(items, key=lambda item: item.evidence_id)) for key, items in grouped.items()}


def _group_result_rows(
    result_rows: tuple[ResultRow, ...],
    candidates: tuple[EntityRef, ...],
) -> dict[tuple[str, str], tuple[ResultRow, ...]]:
    result_key_to_candidate_key = {
        result_key: candidate_key
        for candidate_key, result_key in _result_keys_for_candidates(candidates).items()
    }
    grouped: dict[tuple[str, str], list[ResultRow]] = defaultdict(list)
    for row in result_rows:
        grouped[result_key_to_candidate_key[(row.entity_kind, row.entity_id)]].append(row)
    return {
        key: tuple(sorted(rows, key=lambda row: (row.date_run, row.benchmark_id, row.model_version)))
        for key, rows in grouped.items()
    }


def _result_keys_for_candidates(candidates: tuple[EntityRef, ...]) -> dict[tuple[str, str], tuple[str, str]]:
    result_keys: dict[tuple[str, str], tuple[str, str]] = {}
    for candidate in candidates:
        result_keys[_entity_key(candidate)] = (_result_kind(candidate.entity_type), candidate.entity_id)
    return result_keys


def _result_kind(entity_type: str) -> str:
    return _RESULT_KIND_BY_ENTITY_TYPE.get(entity_type, entity_type)


def _entity_key(entity: EntityRef) -> tuple[str, str]:
    return (entity.entity_type, entity.entity_id)


def _result_score(result_rows: tuple[ResultRow, ...], evidence_items: tuple[EvidenceItem, ...]) -> float:
    result_scores = [_unit_value(row.score_raw) for row in result_rows]
    if result_scores:
        return _round_score(sum(result_scores) / len(result_scores))
    evidence_scores = [_unit_value(item.score) for item in evidence_items if item.score is not None]
    if evidence_scores:
        return _round_score(sum(evidence_scores) / len(evidence_scores))
    return 0.0


def _confidence_interval(confidence: float, result_rows: tuple[ResultRow, ...]) -> ConfidenceInterval:
    if result_rows:
        return ConfidenceInterval(
            low=min(row.ci95.low for row in result_rows),
            high=max(row.ci95.high for row in result_rows),
        )
    return ConfidenceInterval(
        low=max(0.0, confidence - 0.1),
        high=min(1.0, confidence + 0.1),
    )


def _trust_tier(result_rows: tuple[ResultRow, ...]) -> str:
    if not result_rows:
        return "tracking-only"
    if all(row.is_self_reported for row in result_rows):
        return "self-reported"
    if any(row.verification_state == "verified" for row in result_rows):
        return "standardized"
    return "tracking-only"


def _freshness(
    result_rows: tuple[ResultRow, ...],
    evidence_items: tuple[EvidenceItem, ...],
    generated_at: str,
) -> Freshness:
    dates = [row.date_run for row in result_rows]
    dates.extend(item.observed_at[:10] for item in evidence_items)
    generated_date = generated_at[:10]
    return Freshness(
        status="fresh",
        last_eval=max(dates) if dates else generated_date,
        next_refresh=generated_date,
    )


def _abstain(
    *,
    request: EvaluationRequest,
    methodology_version: str,
    generated_at: str,
    exclusions: tuple[Exclusion, ...],
    detail: str,
) -> Recommendation:
    reason = "insufficient_public_evidence"
    return Recommendation(
        request_id=request.request_id,
        use_case=request.use_case,
        methodology_version=methodology_version,
        generated_at=generated_at,
        comparability="single-scale",
        ranked=[],
        groups=None,
        shortlist_depth=0,
        depth_rationale=reason,
        degraded=False,
        served_from="materialized-cache",
        base_snapshot_lag_ms=0,
        the_call=TheCall.abstain(reason=reason),
        abstention=Abstention(reason=reason, detail=detail),
        exclusions=list(exclusions),
    )


def _unit_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return _round_score(_unit_value(numerator / denominator))


def _unit_value(value: float | None) -> float:
    if value is None:
        return 0.0
    return max(0.0, min(1.0, float(value)))


def _round_score(value: float) -> float:
    return round(float(value), 6)
