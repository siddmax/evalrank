from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation
from typing import Iterable

from evalrank_core.canonical_json import canonical_json
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
    StageCandidate,
    TheCall,
)
from evalrank_core.decision_contracts import (
    IntervalUncertaintyV1,
    ObservationV1,
    PassAtKMetricV1,
    ProportionMetricV1,
)


def materialize_recommendation(
    *,
    request: EvaluationRequest,
    candidate_set: CandidateSet,
    stage_candidates: tuple[StageCandidate, ...],
    evidence_set: EvidenceSet,
    observations: tuple[ObservationV1, ...] = (),
    exclusions: tuple[Exclusion, ...] = (),
    methodology_version: str,
    generated_at: str,
) -> Recommendation:
    """Emit a deterministic public recommendation from already-provided inputs.

    This reference materializer is intentionally storage-free: callers supply
    the candidate, Stage-1, evidence, observation, and exclusion rows. Private source
    lookup, DB persistence, scorer weights, calibration, and live telemetry stay
    outside this public package.
    """

    _validate_inputs(
        request=request,
        candidate_set=candidate_set,
        stage_candidates=stage_candidates,
        evidence_set=evidence_set,
        observations=observations,
        exclusions=exclusions,
    )

    candidate_keys = {_entity_key(candidate) for candidate in candidate_set.candidates}
    excluded_keys = {_entity_key(exclusion.subject) for exclusion in exclusions}
    evidence_by_key = _group_evidence(evidence_set.evidence_items)
    observations_by_key = _group_observations(observations, candidate_set.candidates)
    usable_observations_by_key = {
        key: tuple(observation for observation in values if _is_usable_observation(observation))
        for key, values in observations_by_key.items()
    }

    candidate_stages = [
        stage
        for stage in sorted(stage_candidates, key=lambda stage: (-stage.fused_score, stage.candidate_id))
        if _entity_key(stage.entity) in candidate_keys and _entity_key(stage.entity) not in excluded_keys
    ]
    expected_candidate_keys = candidate_keys - excluded_keys
    if {_entity_key(stage.entity) for stage in candidate_stages} != expected_candidate_keys:
        return _abstain(
            request=request,
            methodology_version=methodology_version,
            generated_at=generated_at,
            exclusions=exclusions,
            detail="Every non-excluded candidate must have one Stage-1 row.",
        )
    if len({stage.entity.entity_type for stage in candidate_stages}) != 1:
        return _abstain(
            request=request,
            methodology_version=methodology_version,
            generated_at=generated_at,
            exclusions=exclusions,
            detail="Candidates from different ranking-group entity types cannot share one scale.",
        )
    if any(
        len(usable_observations_by_key.get(_entity_key(stage.entity), ())) != 1
        or len(observations_by_key.get(_entity_key(stage.entity), ())) != 1
        for stage in candidate_stages
    ):
        return _abstain(
            request=request,
            methodology_version=methodology_version,
            generated_at=generated_at,
            exclusions=exclusions,
            detail=(
                "At least one candidate has incomparable, interval-free, non-95%, "
                "non-reported, or ambiguous duplicate observations."
            ),
        )
    materializable_stages = list(candidate_stages)

    if not materializable_stages:
        return _abstain(
            request=request,
            methodology_version=methodology_version,
            generated_at=generated_at,
            exclusions=exclusions,
            detail=(
                "No non-excluded candidate has a unit-interval proportion or pass-at-k "
                "observation with a reported interval for this request."
            ),
        )

    comparison_scales = {
        _comparison_scale(usable_observations_by_key[_entity_key(stage.entity)][0])
        for stage in materializable_stages
    }
    if len(comparison_scales) != 1:
        return _abstain(
            request=request,
            methodology_version=methodology_version,
            generated_at=generated_at,
            exclusions=exclusions,
            detail=(
                "The eligible observations do not share one exact benchmark feed, source artifact, "
                "parser, harness, and metric scale."
            ),
        )

    materializable_stages.sort(
        key=lambda stage: (
            -_observation_score(usable_observations_by_key[_entity_key(stage.entity)]),
            -stage.fused_score,
            stage.candidate_id,
        )
    )

    ranked = [
        _ranked_entity(
            rank=rank,
            stage=stage,
            evidence_items=evidence_by_key.get(_entity_key(stage.entity), ()),
            observations=usable_observations_by_key.get(_entity_key(stage.entity), ()),
            methodology_version=methodology_version,
            generated_at=generated_at,
        )
        for rank, stage in enumerate(materializable_stages, start=1)
    ]
    return Recommendation(
        request_id=request.request_id,
        use_case=request.use_case,
        methodology_version=methodology_version,
        generated_at=generated_at,
        comparability="single-scale",
        ranked=ranked,
        groups=None,
        shortlist_depth=len(ranked),
        depth_rationale="ranked exact same-scale reported observations; Stage-1 score broke ties only",
        degraded=True,
        served_from="materialized-cache",
        base_snapshot_lag_ms=0,
        the_call=None,
        exclusions=list(exclusions),
    )


def _validate_inputs(
    *,
    request: EvaluationRequest,
    candidate_set: CandidateSet,
    stage_candidates: tuple[StageCandidate, ...],
    evidence_set: EvidenceSet,
    observations: tuple[ObservationV1, ...],
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
    if not isinstance(observations, tuple):
        raise ValueError("observations must be a tuple")
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

    candidate_ids = [candidate.entity_id for candidate in candidate_set.candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate_set entity ids must be unique for observation matching")
    candidate_id_set = set(candidate_ids)
    seen_observation_ids: set[str] = set()
    for observation in observations:
        if not isinstance(observation, ObservationV1):
            raise TypeError("observations must contain ObservationV1 values")
        if observation.evaluated_configuration_id not in candidate_id_set:
            raise ValueError("observations must reference candidate_set evaluated configurations")
        if observation.observation_id in seen_observation_ids:
            raise ValueError("observations must have unique observation_id values")
        seen_observation_ids.add(observation.observation_id)

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
    observations: Iterable[ObservationV1],
    methodology_version: str,
    generated_at: str,
) -> RankedEntity:
    evidence_items = tuple(evidence_items)
    observations = tuple(sorted(observations, key=_observation_sort_key))
    evidence_count = len(evidence_items) + len(observations)
    observation_score = _observation_score(observations)
    confidence = 0.95

    return RankedEntity(
        entity_type=stage.entity.entity_type,
        entity_id=stage.entity.entity_id,
        rank=rank,
        capability_score=observation_score,
        confidence=confidence,
        ci95=_confidence_interval(observations),
        methodology_version=methodology_version,
        trust_tier="tracking-only",
        freshness=_freshness(observations, evidence_items, generated_at),
        evidence_count=evidence_count,
        caveats=("public_reference_materializer", "confidence_is_reported_interval_level"),
        score_components={
            "reported_observation": observation_score,
        },
    )


def _group_evidence(evidence_items: tuple[EvidenceItem, ...]) -> dict[tuple[str, str], tuple[EvidenceItem, ...]]:
    grouped: dict[tuple[str, str], list[EvidenceItem]] = defaultdict(list)
    for item in evidence_items:
        grouped[_entity_key(item.subject)].append(item)
    return {key: tuple(sorted(items, key=lambda item: item.evidence_id)) for key, items in grouped.items()}


def _group_observations(
    observations: tuple[ObservationV1, ...],
    candidates: tuple[EntityRef, ...],
) -> dict[tuple[str, str], tuple[ObservationV1, ...]]:
    candidate_key_by_id = {candidate.entity_id: _entity_key(candidate) for candidate in candidates}
    grouped: dict[tuple[str, str], list[ObservationV1]] = defaultdict(list)
    for observation in observations:
        grouped[candidate_key_by_id[observation.evaluated_configuration_id]].append(observation)
    return {
        key: tuple(sorted(values, key=_observation_sort_key))
        for key, values in grouped.items()
    }


def _entity_key(entity: EntityRef) -> tuple[str, str]:
    return (entity.entity_type, entity.entity_id)


def _observation_score(observations: tuple[ObservationV1, ...]) -> float:
    values = [_decimal_to_unit_float(observation.metric.value) for observation in observations]
    return _round_score(sum(values) / len(values))


def _confidence_interval(observations: tuple[ObservationV1, ...]) -> ConfidenceInterval:
    intervals = [observation.uncertainty for observation in observations]
    return ConfidenceInterval(
        low=min(_decimal_to_unit_float(interval.low) for interval in intervals),
        high=max(_decimal_to_unit_float(interval.high) for interval in intervals),
    )


def _freshness(
    observations: tuple[ObservationV1, ...],
    evidence_items: tuple[EvidenceItem, ...],
    generated_at: str,
) -> Freshness:
    dates = [observation.provenance.completed_at[:10] for observation in observations]
    dates.extend(item.observed_at[:10] for item in evidence_items)
    generated_date = generated_at[:10]
    return Freshness(
        status="stale",
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


def _is_usable_observation(observation: ObservationV1) -> bool:
    if not isinstance(observation.metric, (ProportionMetricV1, PassAtKMetricV1)):
        return False
    if not isinstance(observation.uncertainty, IntervalUncertaintyV1):
        return False
    if observation.uncertainty.method != "reported":
        return False
    try:
        value = Decimal(observation.metric.value)
        low = Decimal(observation.uncertainty.low)
        high = Decimal(observation.uncertainty.high)
        confidence_level = Decimal(observation.uncertainty.confidence_level)
    except (InvalidOperation, TypeError):
        return False
    return confidence_level == Decimal("0.95") and Decimal(0) <= low <= value <= high <= Decimal(1)


def _decimal_to_unit_float(value: str) -> float:
    parsed = Decimal(value)
    if not Decimal(0) <= parsed <= Decimal(1):
        raise ValueError("observation value must be within the unit interval")
    return float(parsed)


def _observation_sort_key(observation: ObservationV1) -> tuple[str, str, str, str]:
    provenance = observation.provenance
    return (
        provenance.completed_at,
        provenance.benchmark_family_id,
        provenance.feed_id,
        observation.observation_id,
    )


def _comparison_scale(observation: ObservationV1) -> tuple[str, ...]:
    provenance = observation.provenance
    metric = observation.metric
    metric_parameter = str(metric.k) if isinstance(metric, PassAtKMetricV1) else ""
    return (
        provenance.run_id,
        provenance.benchmark_family_id,
        provenance.feed_id,
        canonical_json([item.to_dict() for item in provenance.source_artifacts]),
        provenance.parser_id,
        provenance.parser_version,
        provenance.harness_version or "",
        provenance.environment_digest or "",
        provenance.scorer_version or "",
        "" if provenance.trial_policy is None else canonical_json(provenance.trial_policy.to_dict()),
        "" if provenance.adapter_metadata is None else canonical_json(provenance.adapter_metadata.to_dict()),
        metric.kind,
        metric_parameter,
    )


def _round_score(value: float) -> float:
    return round(float(value), 6)
