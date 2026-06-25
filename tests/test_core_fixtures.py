import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.fixtures import (  # noqa: E402
    PUBLIC_METHODOLOGY_VERSION,
    PUBLIC_FIXTURE_KINDS,
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_public_fixture,
    sample_ranked_entity,
    sample_ranking_group,
    sample_raw_entry,
    sample_recommendation,
    sample_result_row,
    sample_scoring_stage_catalog,
    sample_stage_candidate,
    sample_use_case_catalog,
)


class CoreFixtureTests(unittest.TestCase):
    def test_public_fixture_kind_dispatch_covers_current_surface(self):
        self.assertEqual(
            (
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
                "scoring-stages",
                "stage-candidate",
                "use-cases",
            ),
            PUBLIC_FIXTURE_KINDS,
        )

        for kind in PUBLIC_FIXTURE_KINDS:
            with self.subTest(kind=kind):
                self.assertIsInstance(sample_public_fixture(kind), dict)
                self.assertTrue(sample_public_fixture(kind))

        with self.assertRaisesRegex(ValueError, "fixture kind"):
            sample_public_fixture("private-kind")

    def test_sample_capability_fingerprint_input_is_public_contract_payload(self):
        payload = sample_capability_fingerprint_input().to_dict()

        self.assertEqual("capability_fingerprint", payload["object"])
        self.assertEqual("io.evalrank.public-search-demo", payload["canonical_id"])
        self.assertEqual("mcp_server", payload["entity_kind"])
        self.assertEqual(64, len(payload["capability_fingerprint"]))

    def test_public_methodology_version_uses_pinned_format(self):
        self.assertEqual("2026-06-25.1.public-fixture-v1", PUBLIC_METHODOLOGY_VERSION)

    def test_sample_ranked_entity_is_public_contract_payload(self):
        row = sample_ranked_entity()
        payload = row.to_dict()

        self.assertEqual("tool:public-search-demo", payload["id"])
        self.assertEqual(PUBLIC_METHODOLOGY_VERSION, payload["methodology_version"])
        self.assertEqual(["capability", "evidence", "freshness"], sorted(payload["score_components"]))

    def test_sample_recommendation_is_usable_and_stable(self):
        rec = sample_recommendation()
        payload = rec.to_dict()

        self.assertTrue(rec.result_usable)
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("single-scale", payload["comparability"])
        self.assertEqual([sample_ranked_entity().to_dict()], payload["ranked"])
        self.assertEqual("recommend", payload["the_call"]["decision"])
        self.assertEqual(0.86, payload["the_call"]["confidence"])
        self.assertEqual(sample_recommendation().recommendation_id, rec.recommendation_id)

    def test_sample_ranking_group_is_public_contract_payload(self):
        payload = sample_ranking_group().to_dict()

        self.assertEqual("ranking_group", payload["object"])
        self.assertEqual("mcp_server", payload["group_key"])
        self.assertEqual("mcp_server", payload["entity_type"])
        self.assertEqual([sample_ranked_entity().to_dict()], payload["ranked"])
        self.assertIn("within", payload["group_rationale"])

    def test_sample_evidence_item_is_public_contract_payload(self):
        evidence = sample_evidence_item()
        payload = evidence.to_dict()

        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])
        self.assertEqual("trace", payload["kind"])
        self.assertEqual("public-fixture", payload["source"])
        self.assertEqual(["latency_ms"], sorted(payload["metadata"]))

    def test_sample_result_row_is_public_contract_payload(self):
        row = sample_result_row()
        payload = row.to_dict()

        self.assertEqual("result_row", payload["object"])
        self.assertEqual("tool:public-search-demo", payload["entity_id"])
        self.assertEqual("tool_server", payload["entity_kind"])
        self.assertEqual("bench_public_search_freshness", payload["benchmark_id"])
        self.assertEqual("pass_rate", payload["score_unit"])
        self.assertEqual("verified", payload["verification_state"])

    def test_sample_exclusion_is_public_contract_payload(self):
        exclusion = sample_exclusion()
        payload = exclusion.to_dict()

        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])
        self.assertEqual("unknown_cost", payload["reason"])
        self.assertEqual("cost is unknown for this public fixture", payload["detail"])

    def test_sample_evidence_set_is_public_contract_payload(self):
        evidence_set = sample_evidence_set()
        payload = evidence_set.to_dict()

        self.assertEqual("evidence_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-browsing", payload["use_case"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["generated_at"])
        self.assertEqual("ev_public_trace_01", payload["evidence_items"][0]["evidence_id"])

    def test_sample_evaluation_request_is_public_contract_payload(self):
        request = sample_evaluation_request()
        payload = request.to_dict()

        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-browsing", payload["use_case"])
        self.assertEqual(["mcp_server"], payload["entity_types"])

    def test_sample_request_use_case_is_in_public_catalog(self):
        catalog_ids = {row["id"] for row in sample_use_case_catalog().to_dict()["use_cases"]}

        self.assertIn(sample_evaluation_request().to_dict()["use_case"], catalog_ids)

    def test_sample_candidate_set_is_public_contract_payload(self):
        candidate_set = sample_candidate_set()
        payload = candidate_set.to_dict()

        self.assertEqual("candidate_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-browsing", payload["use_case"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["generated_at"])
        self.assertEqual([{"entity_type": "mcp_server", "id": "tool:public-search-demo"}], payload["candidates"])

    def test_sample_stage_candidate_is_public_contract_payload(self):
        candidate = sample_stage_candidate()
        payload = candidate.to_dict()

        self.assertEqual("stage_candidate", payload["object"])
        self.assertEqual(64, len(payload["candidate_id"]))
        self.assertEqual("tool:public-search-demo", payload["entity"]["id"])
        self.assertEqual(["graph_rank", "lexical_rank", "semantic_rank"], sorted(payload["rrf_components"]))
        self.assertEqual(["lexical", "semantic"], payload["retrieval_provenance"]["arms"])

    def test_sample_raw_entry_is_public_contract_payload(self):
        entry = sample_raw_entry()
        payload = entry.to_dict()

        self.assertEqual("raw_entry", payload["object"])
        self.assertEqual("public-fixture", payload["source"])
        self.assertEqual("public-fixture:search-demo:2026-06-25", payload["source_id"])
        self.assertEqual("io.evalrank.public-search-demo", payload["canonical_id"])
        self.assertEqual(["display_name", "homepage"], sorted(payload["raw_metadata"]))
        self.assertEqual(64, len(payload["content_hash"]))

    def test_sample_use_case_catalog_is_public_contract_payload(self):
        catalog = sample_use_case_catalog()
        payload = catalog.to_dict()

        self.assertEqual("use_case_catalog", payload["object"])
        self.assertEqual(PUBLIC_METHODOLOGY_VERSION, payload["methodology_version"])
        self.assertEqual(22, len(payload["use_cases"]))
        self.assertEqual(21, sum(1 for row in payload["use_cases"] if row["rank_policy"] == "ranked"))
        self.assertEqual(["safety-robustness"], [row["id"] for row in payload["use_cases"] if row["is_overlay"]])
        self.assertEqual("code-generation", payload["use_cases"][0]["id"])
        self.assertEqual(["model", "tool", "agent"], payload["use_cases"][0]["entity_kinds"])

    def test_sample_scoring_stage_catalog_is_public_contract_payload(self):
        catalog = sample_scoring_stage_catalog()
        payload = catalog.to_dict()

        self.assertEqual("scoring_stage_catalog", payload["object"])
        self.assertEqual(PUBLIC_METHODOLOGY_VERSION, payload["methodology_version"])
        self.assertEqual(6, len(payload["stages"]))
        self.assertEqual("request-normalization", payload["stages"][0]["id"])
        self.assertEqual("freshness-trust-labeling", payload["stages"][-1]["id"])
        self.assertIn("EvaluationRequest", payload["stages"][1]["input_contracts"])
        self.assertIn("Recommendation", payload["stages"][4]["output_contracts"])


if __name__ == "__main__":
    unittest.main()
