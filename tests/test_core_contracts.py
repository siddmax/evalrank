import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    ConfidenceInterval,
    Freshness,
    Recommendation,
    RankedEntity,
)


class CoreContractTests(unittest.TestCase):
    def test_ranked_entity_requires_score_context(self):
        row = RankedEntity(
            entity_type="mcp_server",
            entity_id="tool:exa-search-mcp",
            rank=1,
            capability_score=0.84,
            confidence=0.86,
            ci95=ConfidenceInterval(low=0.80, high=0.88),
            methodology_version="2026.06.1",
            trust_tier="standardized",
            freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
            evidence_count=1840,
        )

        payload = row.to_dict()

        self.assertEqual("tool:exa-search-mcp", payload["id"])
        self.assertEqual([0.8, 0.88], payload["ci95"])
        self.assertEqual("2026.06.1", payload["methodology_version"])
        self.assertEqual("fresh", payload["freshness"]["status"])

    def test_ranked_entity_rejects_bare_or_invalid_scores(self):
        with self.assertRaisesRegex(ValueError, "capability_score"):
            RankedEntity(
                entity_type="model_version",
                entity_id="model_version:vendor/model@1",
                rank=1,
                capability_score=1.4,
                confidence=0.5,
                ci95=ConfidenceInterval(low=0.4, high=0.6),
                methodology_version="2026.06.1",
                trust_tier="verified",
                freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
                evidence_count=10,
            )

        with self.assertRaisesRegex(ValueError, "methodology_version"):
            RankedEntity(
                entity_type="model_version",
                entity_id="model_version:vendor/model@1",
                rank=1,
                capability_score=0.4,
                confidence=0.5,
                ci95=ConfidenceInterval(low=0.4, high=0.6),
                methodology_version="",
                trust_tier="verified",
                freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
                evidence_count=10,
            )

    def test_recommendation_enforces_ranked_or_grouped_shape(self):
        row = _row("tool:exa-search-mcp")

        rec = Recommendation.single_scale(
            request_id="req_01",
            use_case="web-browsing:fresh-news",
            methodology_version="2026.06.1",
            ranked=[row],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="one candidate clears the evidence floor",
        )

        payload = rec.to_dict()

        self.assertEqual("recommendation", payload["object"])
        self.assertEqual("single-scale", payload["comparability"])
        self.assertEqual([row.to_dict()], payload["ranked"])
        self.assertIsNone(payload["groups"])
        self.assertTrue(rec.result_usable)
        self.assertTrue(payload["recommendation_id"].startswith("rec_"))

    def test_recommendation_id_is_content_addressed(self):
        base = Recommendation.single_scale(
            request_id="req_a",
            use_case="function-calling",
            methodology_version="2026.06.1",
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )
        same_payload_new_request = Recommendation.single_scale(
            request_id="req_b",
            use_case="function-calling",
            methodology_version="2026.06.1",
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )
        changed_methodology = Recommendation.single_scale(
            request_id="req_a",
            use_case="function-calling",
            methodology_version="2026.06.2",
            ranked=[_row("tool:exa-search-mcp", methodology_version="2026.06.2")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )

        self.assertEqual(base.recommendation_id, same_payload_new_request.recommendation_id)
        self.assertNotEqual(base.recommendation_id, changed_methodology.recommendation_id)

    def test_abstention_is_not_value_bearing(self):
        rec = Recommendation.abstain(
            request_id="req_01",
            use_case="mobile-codegen:flutter",
            methodology_version="2026.06.1",
            generated_at="2026-06-25T00:00:00Z",
            reason="insufficient_evidence",
        )

        self.assertFalse(rec.result_usable)
        self.assertEqual([], rec.ranked)
        self.assertEqual("insufficient_evidence", rec.the_call["abstention_reason"])


def _row(entity_id: str, methodology_version: str = "2026.06.1") -> RankedEntity:
    return RankedEntity(
        entity_type="mcp_server",
        entity_id=entity_id,
        rank=1,
        capability_score=0.84,
        confidence=0.86,
        ci95=ConfidenceInterval(low=0.80, high=0.88),
        methodology_version=methodology_version,
        trust_tier="standardized",
        freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
        evidence_count=1840,
    )


if __name__ == "__main__":
    unittest.main()
