import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    CapabilityFingerprintInput,
    ConfidenceInterval,
    EntityRef,
    EvidenceItem,
    EvaluationRequest,
    Freshness,
    Recommendation,
    RankedEntity,
)


PINNED_METHODOLOGY_VERSION = "2026-06-25.1.public-fixture-v1"
PUBLIC_CAPABILITY_FINGERPRINT = "da617b2b113a59a734acb6166c305086d9a850bac2a40c8febd6e67c7eff3e12"


class CoreContractTests(unittest.TestCase):
    def test_capability_fingerprint_is_stable_over_shape_key_order(self):
        first = CapabilityFingerprintInput(
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
        same_shape_different_order = CapabilityFingerprintInput(
            id_scheme="reverse_dns",
            canonical_id="io.evalrank.public-search-demo",
            entity_kind="mcp_server",
            declared_capability_shape={
                "commit_sha": "abc123",
                "declared_scopes": ["web.search"],
                "param_schemas": {"search": {"type": "object"}},
                "tool_names": ["search"],
            },
        )

        payload = first.to_dict()

        self.assertEqual("capability_fingerprint", payload["object"])
        self.assertEqual(PUBLIC_CAPABILITY_FINGERPRINT, payload["capability_fingerprint"])
        self.assertEqual(PUBLIC_CAPABILITY_FINGERPRINT, same_shape_different_order.fingerprint())
        self.assertEqual("mcp_server", payload["entity_kind"])

    def test_capability_fingerprint_rejects_missing_or_non_json_shape_keys(self):
        with self.assertRaisesRegex(ValueError, "canonical_id"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="",
                entity_kind="mcp_server",
                declared_capability_shape={"tool_names": ["search"]},
            )

        with self.assertRaisesRegex(ValueError, "declared_capability_shape"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="io.evalrank.public-search-demo",
                entity_kind="mcp_server",
                declared_capability_shape={1: "not-public-json-key"},
            )

        with self.assertRaisesRegex(ValueError, "declared_capability_shape"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="io.evalrank.public-search-demo",
                entity_kind="mcp_server",
                declared_capability_shape={"score": float("nan")},
            )

    def test_ranked_entity_requires_score_context(self):
        row = RankedEntity(
            entity_type="mcp_server",
            entity_id="tool:exa-search-mcp",
            rank=1,
            capability_score=0.84,
            confidence=0.86,
            ci95=ConfidenceInterval(low=0.80, high=0.88),
            methodology_version=PINNED_METHODOLOGY_VERSION,
            trust_tier="standardized",
            freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
            evidence_count=1840,
        )

        payload = row.to_dict()

        self.assertEqual("tool:exa-search-mcp", payload["id"])
        self.assertEqual([0.8, 0.88], payload["ci95"])
        self.assertEqual(PINNED_METHODOLOGY_VERSION, payload["methodology_version"])
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
                methodology_version=PINNED_METHODOLOGY_VERSION,
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
            methodology_version=PINNED_METHODOLOGY_VERSION,
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
        self.assertEqual(payload["recommendation_id"], payload["recommend_id"])
        self.assertEqual(payload["recommendation_id"], payload["search_run_id"])

    def test_recommendation_id_is_content_addressed(self):
        base = Recommendation.single_scale(
            request_id="req_a",
            use_case="function-calling",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )
        same_payload_new_request = Recommendation.single_scale(
            request_id="req_b",
            use_case="function-calling",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )
        changed_methodology = Recommendation.single_scale(
            request_id="req_a",
            use_case="function-calling",
            methodology_version="2026-06-25.2.public-fixture-v1",
            ranked=[_row("tool:exa-search-mcp", methodology_version="2026-06-25.2.public-fixture-v1")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )

        self.assertEqual(base.recommendation_id, same_payload_new_request.recommendation_id)
        self.assertNotEqual(base.recommendation_id, changed_methodology.recommendation_id)

    def test_abstention_is_not_value_bearing(self):
        rec = Recommendation.abstain(
            request_id="req_01",
            use_case="mobile-codegen:flutter",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            generated_at="2026-06-25T00:00:00Z",
            reason="insufficient_evidence",
        )

        self.assertFalse(rec.result_usable)
        self.assertEqual([], rec.ranked)
        self.assertEqual("insufficient_evidence", rec.the_call["abstention_reason"])

    def test_methodology_version_rejects_unpinned_format(self):
        with self.assertRaisesRegex(ValueError, "methodology_version"):
            _row("tool:exa-search-mcp", methodology_version="2026.06.1")

        with self.assertRaisesRegex(ValueError, "methodology_version"):
            Recommendation.single_scale(
                request_id="req_bad_version",
                use_case="function-calling",
                methodology_version="2026.06.1",
                ranked=[_row("tool:exa-search-mcp")],
                generated_at="2026-06-25T00:00:00Z",
                depth_rationale="old version format should not serialize",
            )

    def test_evidence_item_serializes_public_subject_and_score(self):
        item = EvidenceItem(
            evidence_id="ev_public_trace_01",
            subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            kind="trace",
            source="public-fixture",
            observed_at="2026-06-25T00:00:00Z",
            summary="public search demo returned a fresh cited result",
            score=0.8754321,
            metadata={"latency_ms": 1200, "region": "iad"},
        )

        payload = item.to_dict()

        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual({"entity_type": "mcp_server", "id": "tool:public-search-demo"}, payload["subject"])
        self.assertEqual("trace", payload["kind"])
        self.assertEqual(0.875432, payload["score"])
        self.assertEqual(["latency_ms", "region"], sorted(payload["metadata"]))

    def test_evidence_item_rejects_invalid_kind_or_score(self):
        subject = EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")

        with self.assertRaisesRegex(ValueError, "kind"):
            EvidenceItem(
                evidence_id="ev_bad_kind",
                subject=subject,
                kind="unsupported-kind",
                source="public-fixture",
                observed_at="2026-06-25T00:00:00Z",
                summary="invalid kind",
            )

        with self.assertRaisesRegex(ValueError, "score"):
            EvidenceItem(
                evidence_id="ev_bad_score",
                subject=subject,
                kind="trace",
                source="public-fixture",
                observed_at="2026-06-25T00:00:00Z",
                summary="invalid score",
                score=1.2,
            )

    def test_evaluation_request_serializes_public_input_context(self):
        request = EvaluationRequest(
            request_id="req_public_fixture_01",
            use_case="web-research:freshness-check",
            entity_types=("mcp_server",),
            requested_at="2026-06-25T00:00:00Z",
            constraints={"region": "public", "requires_citations": True},
        )

        payload = request.to_dict()

        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-research:freshness-check", payload["use_case"])
        self.assertEqual(["mcp_server"], payload["entity_types"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["requested_at"])
        self.assertEqual(["region", "requires_citations"], sorted(payload["constraints"]))

    def test_evaluation_request_rejects_missing_required_context(self):
        with self.assertRaisesRegex(ValueError, "request_id"):
            EvaluationRequest(
                request_id="",
                use_case="web-research:freshness-check",
                entity_types=("mcp_server",),
                requested_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "entity_types"):
            EvaluationRequest(
                request_id="req_public_fixture_01",
                use_case="web-research:freshness-check",
                entity_types=(),
                requested_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "constraints"):
            EvaluationRequest(
                request_id="req_public_fixture_01",
                use_case="web-research:freshness-check",
                entity_types=("mcp_server",),
                requested_at="2026-06-25T00:00:00Z",
                constraints={1: "not-public-json-key"},
            )


def _row(entity_id: str, methodology_version: str = PINNED_METHODOLOGY_VERSION) -> RankedEntity:
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
