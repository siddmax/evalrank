import hashlib
import sys
import unittest
from dataclasses import replace
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    CandidateSet,
    EntityRef,
    EvaluationRequest,
    EvidenceItem,
    EvidenceSet,
    Exclusion,
    StageCandidate,
)
from evalrank_core.decision_contracts import (  # noqa: E402
    ContinuousMetricV1,
    IntervalUncertaintyV1,
    ObservationV1,
    ProportionMetricV1,
    RunInputArtifactV1,
    RunProvenanceV1,
    UnknownUncertaintyV1,
)
from evalrank_core.fixtures import PUBLIC_GENERATED_AT, PUBLIC_METHODOLOGY_VERSION  # noqa: E402
import evalrank_core.materializer as materializer_module  # noqa: E402
from evalrank_core.materializer import materialize_recommendation  # noqa: E402


REQUEST_ID = "req_materializer_public_01"
USE_CASE = "web-browsing"


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _entity(entity_id: str) -> EntityRef:
    return EntityRef(
        entity_type="model_configuration",
        entity_id=f"config_{_fingerprint(entity_id)}",
    )


def _stage(entity: EntityRef, fused_score: float, *, lexical_rank: int) -> StageCandidate:
    return StageCandidate(
        candidate_id=_fingerprint(entity.entity_id),
        entity=entity,
        fused_score=fused_score,
        rrf_components={"lexical_rank": lexical_rank, "semantic_rank": lexical_rank + 1, "graph_rank": None},
        retrieval_arms=("lexical", "semantic"),
        use_case=USE_CASE,
    )


def _evidence(entity: EntityRef, index: int, *, score: float = 0.8) -> EvidenceItem:
    return EvidenceItem(
        evidence_id=f"ev_public_materializer_{index}",
        subject=entity,
        kind="benchmark",
        source="public-fixture",
        observed_at=PUBLIC_GENERATED_AT,
        summary=f"public evidence row for {entity.entity_id}",
        score=score,
        metadata={"fixture": True},
    )


def _observation(
    entity: EntityRef,
    score: float,
    *,
    date_run: str = "2026-06-25",
    metric: object | None = None,
    uncertainty: object | None = None,
) -> ObservationV1:
    value = format(score, ".6g")
    low = format(max(0.0, score - 0.04), ".6g")
    high = format(min(1.0, score + 0.04), ".6g")
    short_id = entity.entity_id.removeprefix("config_")[:16]
    return ObservationV1(
        observation_id=f"obs_{short_id}",
        evaluated_configuration_id=entity.entity_id,
        metric=metric or ProportionMetricV1(value=value, numerator=None, denominator=None),
        uncertainty=uncertainty
        or IntervalUncertaintyV1(
            low=low,
            high=high,
            confidence_level="0.95",
            method="reported",
        ),
        provenance=RunProvenanceV1(
            run_id="run_public_materializer_01",
            benchmark_family_id="public-materializer-family",
            feed_id="public-materializer-feed",
            source_artifacts=(
                RunInputArtifactV1(
                    role="primary",
                    source_artifact_id=f"artifact_{'a' * 64}",
                ),
            ),
            parser_id="public-materializer-parser",
            parser_version="1",
            started_at=f"{date_run}T00:00:00Z",
            completed_at=f"{date_run}T00:00:01Z",
            harness_version="2026-06-25.1",
        ),
    )


class CoreMaterializerTests(unittest.TestCase):
    def test_comparison_scale_changes_when_only_an_auxiliary_artifact_changes(self):
        entity = _entity("model:artifact-provenance")
        primary_only = _observation(entity, 0.8)
        with_categories = replace(
            primary_only,
            provenance=replace(
                primary_only.provenance,
                source_artifacts=(
                    RunInputArtifactV1(
                        role="categories",
                        source_artifact_id=f"artifact_{'b' * 64}",
                    ),
                    *primary_only.provenance.source_artifacts,
                ),
            ),
        )

        self.assertNotEqual(
            materializer_module._comparison_scale(primary_only),
            materializer_module._comparison_scale(with_categories),
        )

    def test_materializer_emits_deterministic_cached_recommendation_from_public_inputs(self):
        alpha = _entity("model:alpha")
        beta = _entity("model:beta")
        excluded = _entity("model:excluded")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model_configuration",),
            requested_at=PUBLIC_GENERATED_AT,
        )
        candidate_set = CandidateSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            candidates=(alpha, beta, excluded),
            generated_at=PUBLIC_GENERATED_AT,
        )
        stage_candidates = (
            _stage(excluded, 1.1, lexical_rank=1),
            _stage(beta, 0.9, lexical_rank=2),
            _stage(alpha, 0.9, lexical_rank=3),
        )
        evidence_set = EvidenceSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            evidence_items=(
                _evidence(alpha, 1, score=0.81),
                _evidence(beta, 2, score=0.82),
                _evidence(excluded, 3, score=0.99),
            ),
            generated_at=PUBLIC_GENERATED_AT,
        )
        exclusions = (
            Exclusion(
                subject=excluded,
                reason="public_fixture_excluded",
                detail="excluded candidates must not be ranked",
            ),
        )

        recommendation = materialize_recommendation(
            request=request,
            candidate_set=candidate_set,
            stage_candidates=stage_candidates,
            evidence_set=evidence_set,
            observations=(_observation(alpha, 0.84), _observation(beta, 0.83)),
            exclusions=exclusions,
            methodology_version=PUBLIC_METHODOLOGY_VERSION,
            generated_at=PUBLIC_GENERATED_AT,
        )
        repeated = materialize_recommendation(
            request=request,
            candidate_set=candidate_set,
            stage_candidates=stage_candidates,
            evidence_set=evidence_set,
            observations=(_observation(alpha, 0.84), _observation(beta, 0.83)),
            exclusions=exclusions,
            methodology_version=PUBLIC_METHODOLOGY_VERSION,
            generated_at=PUBLIC_GENERATED_AT,
        )

        self.assertEqual([alpha.entity_id, beta.entity_id], [row.entity_id for row in recommendation.ranked])
        self.assertEqual("single-scale", recommendation.comparability)
        self.assertEqual("materialized-cache", recommendation.served_from)
        self.assertEqual(PUBLIC_METHODOLOGY_VERSION, recommendation.methodology_version)
        self.assertEqual(PUBLIC_GENERATED_AT, recommendation.generated_at)
        self.assertTrue(recommendation.result_usable)
        self.assertIsNone(recommendation.the_call)
        self.assertTrue(recommendation.degraded)
        self.assertEqual(recommendation.recommendation_id, repeated.recommendation_id)
        self.assertEqual([excluded], [exclusion.subject for exclusion in recommendation.exclusions])
        self.assertNotIn(excluded.entity_id, [row.entity_id for row in recommendation.ranked])
        self.assertEqual([1, 2], [row.rank for row in recommendation.ranked])
        for row in recommendation.ranked:
            self.assertEqual(PUBLIC_METHODOLOGY_VERSION, row.methodology_version)
            self.assertEqual(2, row.evidence_count)
            self.assertEqual("stale", row.freshness.status)
            self.assertIn("confidence_is_reported_interval_level", row.caveats)
            self.assertEqual(
                {"reported_observation"},
                set(row.score_components),
            )

    def test_materializer_abstains_when_public_evidence_is_empty(self):
        model = _entity("model:no-evidence")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model_configuration",),
            requested_at=PUBLIC_GENERATED_AT,
        )

        recommendation = materialize_recommendation(
            request=request,
            candidate_set=CandidateSet(
                request_id=REQUEST_ID,
                use_case=USE_CASE,
                candidates=(model,),
                generated_at=PUBLIC_GENERATED_AT,
            ),
            stage_candidates=(_stage(model, 0.4, lexical_rank=1),),
            evidence_set=EvidenceSet(
                request_id=REQUEST_ID,
                use_case=USE_CASE,
                evidence_items=(),
                generated_at=PUBLIC_GENERATED_AT,
            ),
            observations=(),
            exclusions=(),
            methodology_version=PUBLIC_METHODOLOGY_VERSION,
            generated_at=PUBLIC_GENERATED_AT,
        )

        self.assertFalse(recommendation.result_usable)
        self.assertEqual([], recommendation.ranked)
        self.assertEqual("materialized-cache", recommendation.served_from)
        self.assertEqual("abstain", recommendation.the_call.decision)
        self.assertEqual("insufficient_public_evidence", recommendation.abstention.reason)

    def test_materializer_rejects_inputs_outside_the_public_request_boundary(self):
        model = _entity("model:alpha")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model_configuration",),
            requested_at=PUBLIC_GENERATED_AT,
        )
        candidate_set = CandidateSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            candidates=(model,),
            generated_at=PUBLIC_GENERATED_AT,
        )
        evidence_set = EvidenceSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            evidence_items=(_evidence(model, 1),),
            generated_at=PUBLIC_GENERATED_AT,
        )

        with self.assertRaisesRegex(ValueError, "candidate_set.request_id"):
            materialize_recommendation(
                request=request,
                candidate_set=CandidateSet(
                    request_id="req_other",
                    use_case=USE_CASE,
                    candidates=(model,),
                    generated_at=PUBLIC_GENERATED_AT,
                ),
                stage_candidates=(_stage(model, 0.4, lexical_rank=1),),
                evidence_set=evidence_set,
                methodology_version=PUBLIC_METHODOLOGY_VERSION,
                generated_at=PUBLIC_GENERATED_AT,
            )

        with self.assertRaisesRegex(ValueError, "evidence_set.use_case"):
            materialize_recommendation(
                request=request,
                candidate_set=candidate_set,
                stage_candidates=(_stage(model, 0.4, lexical_rank=1),),
                evidence_set=EvidenceSet(
                    request_id=REQUEST_ID,
                    use_case="other-use-case",
                    evidence_items=(_evidence(model, 2),),
                    generated_at=PUBLIC_GENERATED_AT,
                ),
                methodology_version=PUBLIC_METHODOLOGY_VERSION,
                generated_at=PUBLIC_GENERATED_AT,
            )

        with self.assertRaisesRegex(ValueError, "stage_candidates"):
            materialize_recommendation(
                request=request,
                candidate_set=candidate_set,
                stage_candidates=(_stage(_entity("model:not-a-candidate"), 0.4, lexical_rank=1),),
                evidence_set=evidence_set,
                methodology_version=PUBLIC_METHODOLOGY_VERSION,
                generated_at=PUBLIC_GENERATED_AT,
            )

        with self.assertRaisesRegex(ValueError, "observations"):
            materialize_recommendation(
                request=request,
                candidate_set=candidate_set,
                stage_candidates=(_stage(model, 0.4, lexical_rank=1),),
                evidence_set=evidence_set,
                observations=(_observation(_entity("model:not-a-candidate"), 0.4),),
                methodology_version=PUBLIC_METHODOLOGY_VERSION,
                generated_at=PUBLIC_GENERATED_AT,
            )

    def test_materializer_does_not_coerce_incomparable_or_interval_free_observations(self):
        model = _entity("model:alpha")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model_configuration",),
            requested_at=PUBLIC_GENERATED_AT,
        )
        candidate_set = CandidateSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            candidates=(model,),
            generated_at=PUBLIC_GENERATED_AT,
        )
        evidence_set = EvidenceSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            evidence_items=(_evidence(model, 1),),
            generated_at=PUBLIC_GENERATED_AT,
        )
        invalid_for_unit_ranking = (
            _observation(
                model,
                0.84,
                metric=ContinuousMetricV1(value="84", unit="points", n_items=40),
                uncertainty=IntervalUncertaintyV1(
                    low="80",
                    high="88",
                    confidence_level="0.95",
                    method="reported",
                ),
            ),
            _observation(model, 0.84, uncertainty=UnknownUncertaintyV1()),
            _observation(
                model,
                0.84,
                uncertainty=IntervalUncertaintyV1(
                    low="0.8",
                    high="0.88",
                    confidence_level="0.95",
                    method="wilson",
                ),
            ),
            _observation(
                model,
                0.84,
                uncertainty=IntervalUncertaintyV1(
                    low="0.8",
                    high="0.88",
                    confidence_level="0.9",
                    method="reported",
                ),
            ),
        )

        for observation in invalid_for_unit_ranking:
            with self.subTest(metric=type(observation.metric).__name__, uncertainty=type(observation.uncertainty).__name__):
                recommendation = materialize_recommendation(
                    request=request,
                    candidate_set=candidate_set,
                    stage_candidates=(_stage(model, 0.4, lexical_rank=1),),
                    evidence_set=evidence_set,
                    observations=(observation,),
                    methodology_version=PUBLIC_METHODOLOGY_VERSION,
                    generated_at=PUBLIC_GENERATED_AT,
                )

                self.assertFalse(recommendation.result_usable)
                self.assertEqual("abstain", recommendation.the_call.decision)

    def test_materializer_abstains_on_cross_scale_or_duplicate_observations(self):
        alpha = _entity("model:alpha")
        beta = _entity("model:beta")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model_configuration",),
            requested_at=PUBLIC_GENERATED_AT,
        )
        candidate_set = CandidateSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            candidates=(alpha, beta),
            generated_at=PUBLIC_GENERATED_AT,
        )
        stages = (_stage(alpha, 0.4, lexical_rank=1), _stage(beta, 0.3, lexical_rank=2))
        evidence = EvidenceSet(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            evidence_items=(),
            generated_at=PUBLIC_GENERATED_AT,
        )
        alpha_observation = _observation(alpha, 0.84)
        beta_observation = _observation(beta, 0.83)
        other_feed = replace(
            beta_observation,
            provenance=replace(beta_observation.provenance, feed_id="different-feed"),
        )
        other_scorer = replace(
            beta_observation,
            provenance=replace(beta_observation.provenance, scorer_version="different-scorer"),
        )
        duplicate = replace(alpha_observation, observation_id="obs_alpha_second")
        mixed_entity_type = EntityRef(
            entity_type="agent_system",
            entity_id=f"config_{_fingerprint('agent:beta')}",
        )

        for observations in (
            (alpha_observation, other_feed),
            (alpha_observation, other_scorer),
            (alpha_observation, duplicate, beta_observation),
        ):
            with self.subTest(observation_count=len(observations)):
                recommendation = materialize_recommendation(
                    request=request,
                    candidate_set=candidate_set,
                    stage_candidates=stages,
                    evidence_set=evidence,
                    observations=observations,
                    methodology_version=PUBLIC_METHODOLOGY_VERSION,
                    generated_at=PUBLIC_GENERATED_AT,
                )

                self.assertFalse(recommendation.result_usable)
                self.assertEqual("abstain", recommendation.the_call.decision)

        mixed_request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model_configuration", "agent_system"),
            requested_at=PUBLIC_GENERATED_AT,
        )
        mixed_recommendation = materialize_recommendation(
            request=mixed_request,
            candidate_set=CandidateSet(
                request_id=REQUEST_ID,
                use_case=USE_CASE,
                candidates=(alpha, mixed_entity_type),
                generated_at=PUBLIC_GENERATED_AT,
            ),
            stage_candidates=(
                _stage(alpha, 0.4, lexical_rank=1),
                _stage(mixed_entity_type, 0.3, lexical_rank=2),
            ),
            evidence_set=evidence,
            observations=(alpha_observation, _observation(mixed_entity_type, 0.83)),
            methodology_version=PUBLIC_METHODOLOGY_VERSION,
            generated_at=PUBLIC_GENERATED_AT,
        )
        self.assertFalse(mixed_recommendation.result_usable)
        self.assertEqual("abstain", mixed_recommendation.the_call.decision)


if __name__ == "__main__":
    unittest.main()
