import hashlib
import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    CandidateSet,
    ConfidenceInterval,
    EntityRef,
    EvaluationRequest,
    EvidenceItem,
    EvidenceSet,
    Exclusion,
    ResultRow,
    StageCandidate,
)
from evalrank_core.fixtures import PUBLIC_GENERATED_AT, PUBLIC_METHODOLOGY_VERSION  # noqa: E402
from evalrank_core.materializer import materialize_recommendation  # noqa: E402


REQUEST_ID = "req_materializer_public_01"
USE_CASE = "web-browsing"


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _entity(entity_id: str) -> EntityRef:
    return EntityRef(entity_type="model", entity_id=entity_id)


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


def _result(entity: EntityRef, score: float, *, date_run: str = "2026-06-25") -> ResultRow:
    return ResultRow(
        entity_id=entity.entity_id,
        entity_kind="model",
        benchmark_id=f"bench_{entity.entity_id.replace(':', '_')}",
        benchmark_version="2026-06-25",
        harness="public-materializer-fixture",
        harness_version="2026-06-25.1",
        is_self_reported=False,
        n_items=40,
        ci95=ConfidenceInterval(low=max(0.0, score - 0.04), high=min(1.0, score + 0.04)),
        score_raw=score,
        score_unit="pass_rate",
        date_run=date_run,
        model_version=f"{entity.entity_id}@2026-06-25",
        provenance={"source": "public-fixture"},
        source_url=f"https://example.com/evalrank/{entity.entity_id.replace(':', '-')}",
        attribution_string="Synthetic public materializer fixture",
        flags={
            "saturated": False,
            "contaminated": False,
            "judge_model_dependent": False,
            "scaffold_nonstandard": False,
        },
        verification_state="verified",
    )


class CoreMaterializerTests(unittest.TestCase):
    def test_materializer_emits_deterministic_cached_recommendation_from_public_inputs(self):
        alpha = _entity("model:alpha")
        beta = _entity("model:beta")
        excluded = _entity("model:excluded")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model",),
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
            result_rows=(_result(alpha, 0.84), _result(beta, 0.83), _result(excluded, 0.99)),
            exclusions=exclusions,
            methodology_version=PUBLIC_METHODOLOGY_VERSION,
            generated_at=PUBLIC_GENERATED_AT,
        )
        repeated = materialize_recommendation(
            request=request,
            candidate_set=candidate_set,
            stage_candidates=stage_candidates,
            evidence_set=evidence_set,
            result_rows=(_result(alpha, 0.84), _result(beta, 0.83), _result(excluded, 0.99)),
            exclusions=exclusions,
            methodology_version=PUBLIC_METHODOLOGY_VERSION,
            generated_at=PUBLIC_GENERATED_AT,
        )

        ranked_stage_candidates = [
            stage
            for stage in sorted(stage_candidates, key=lambda stage: (-stage.fused_score, stage.candidate_id))
            if stage.entity != excluded
        ]
        self.assertEqual([stage.entity.entity_id for stage in ranked_stage_candidates], [row.entity_id for row in recommendation.ranked])
        self.assertEqual("single-scale", recommendation.comparability)
        self.assertEqual("materialized-cache", recommendation.served_from)
        self.assertEqual(PUBLIC_METHODOLOGY_VERSION, recommendation.methodology_version)
        self.assertEqual(PUBLIC_GENERATED_AT, recommendation.generated_at)
        self.assertTrue(recommendation.result_usable)
        self.assertEqual("recommend", recommendation.the_call.decision)
        self.assertEqual(recommendation.recommendation_id, repeated.recommendation_id)
        self.assertEqual([excluded], [exclusion.subject for exclusion in recommendation.exclusions])
        self.assertNotIn("model:excluded", [row.entity_id for row in recommendation.ranked])
        self.assertEqual([1, 2], [row.rank for row in recommendation.ranked])
        for row in recommendation.ranked:
            self.assertEqual(PUBLIC_METHODOLOGY_VERSION, row.methodology_version)
            self.assertEqual(2, row.evidence_count)
            self.assertEqual(
                {"evidence_coverage", "result_score", "stage1_fused"},
                set(row.score_components),
            )

    def test_materializer_abstains_when_public_evidence_is_empty(self):
        model = _entity("model:no-evidence")
        request = EvaluationRequest(
            request_id=REQUEST_ID,
            use_case=USE_CASE,
            entity_types=("model",),
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
            result_rows=(),
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
            entity_types=("model",),
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

        with self.assertRaisesRegex(ValueError, "result_rows"):
            materialize_recommendation(
                request=request,
                candidate_set=candidate_set,
                stage_candidates=(_stage(model, 0.4, lexical_rank=1),),
                evidence_set=evidence_set,
                result_rows=(_result(_entity("model:not-a-candidate"), 0.4),),
                methodology_version=PUBLIC_METHODOLOGY_VERSION,
                generated_at=PUBLIC_GENERATED_AT,
            )


if __name__ == "__main__":
    unittest.main()
