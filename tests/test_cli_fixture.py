import json
import sys
import unittest
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
CLI_SRC = REPO_ROOT / "packages" / "cli" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(CLI_SRC))

from evalrank_cli import main  # noqa: E402


class CliFixtureTests(unittest.TestCase):
    def test_fixture_fingerprint_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "fingerprint"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("capability_fingerprint", payload["object"])
        self.assertEqual("io.evalrank.public-search-demo", payload["canonical_id"])

    def test_fixture_evidence_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "evidence"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])

    def test_fixture_result_row_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "result-row"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("result_row", payload["object"])
        self.assertEqual("bench_public_search_freshness", payload["benchmark_id"])
        self.assertEqual("verified", payload["verification_state"])

    def test_fixture_exclusion_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "exclusion"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])
        self.assertEqual("unknown_cost", payload["reason"])
        self.assertEqual("cost is unknown for this public fixture", payload["detail"])

    def test_fixture_recommendation_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "recommendation"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("recommendation", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])

    def test_fixture_request_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "request"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual(["mcp_server"], payload["entity_types"])

    def test_fixture_candidate_set_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "candidate-set"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("candidate_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("tool:public-search-demo", payload["candidates"][0]["id"])

    def test_fixture_evidence_set_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "evidence-set"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("evidence_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("ev_public_trace_01", payload["evidence_items"][0]["evidence_id"])

    def test_fixture_stage_candidate_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "stage-candidate"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("stage_candidate", payload["object"])
        self.assertEqual("tool:public-search-demo", payload["entity"]["id"])
        self.assertEqual(["lexical", "semantic"], payload["retrieval_provenance"]["arms"])

    def test_fixture_raw_entry_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "raw-entry"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("raw_entry", payload["object"])
        self.assertEqual("public-fixture:search-demo:2026-06-25", payload["source_id"])

    def test_fixture_use_cases_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "use-cases"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("use_case_catalog", payload["object"])
        self.assertEqual(22, len(payload["use_cases"]))
        self.assertEqual("safety-robustness", payload["use_cases"][-1]["id"])

    def test_fixture_ranking_group_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "ranking-group"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("ranking_group", payload["object"])
        self.assertEqual("mcp_server", payload["entity_type"])

    def test_invalid_fixture_exits_nonzero(self):
        stderr = StringIO()

        exit_code = main(["fixture", "unknown"], stdout=StringIO(), stderr=stderr)

        self.assertNotEqual(0, exit_code)
        self.assertIn("invalid choice", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
