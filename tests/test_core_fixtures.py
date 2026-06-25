import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.fixtures import (  # noqa: E402
    PUBLIC_METHODOLOGY_VERSION,
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_evidence_item,
    sample_evaluation_request,
    sample_ranked_entity,
    sample_raw_entry,
    sample_recommendation,
)


class CoreFixtureTests(unittest.TestCase):
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

    def test_sample_evidence_item_is_public_contract_payload(self):
        evidence = sample_evidence_item()
        payload = evidence.to_dict()

        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])
        self.assertEqual("trace", payload["kind"])
        self.assertEqual("public-fixture", payload["source"])
        self.assertEqual(["latency_ms"], sorted(payload["metadata"]))

    def test_sample_evaluation_request_is_public_contract_payload(self):
        request = sample_evaluation_request()
        payload = request.to_dict()

        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-research:freshness-check", payload["use_case"])
        self.assertEqual(["mcp_server"], payload["entity_types"])

    def test_sample_candidate_set_is_public_contract_payload(self):
        candidate_set = sample_candidate_set()
        payload = candidate_set.to_dict()

        self.assertEqual("candidate_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-research:freshness-check", payload["use_case"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["generated_at"])
        self.assertEqual([{"entity_type": "mcp_server", "id": "tool:public-search-demo"}], payload["candidates"])

    def test_sample_raw_entry_is_public_contract_payload(self):
        entry = sample_raw_entry()
        payload = entry.to_dict()

        self.assertEqual("raw_entry", payload["object"])
        self.assertEqual("public-fixture", payload["source"])
        self.assertEqual("public-fixture:search-demo:2026-06-25", payload["source_id"])
        self.assertEqual("io.evalrank.public-search-demo", payload["canonical_id"])
        self.assertEqual(["display_name", "homepage"], sorted(payload["raw_metadata"]))
        self.assertEqual(64, len(payload["content_hash"]))


if __name__ == "__main__":
    unittest.main()
