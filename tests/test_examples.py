import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublicExampleTests(unittest.TestCase):
    def test_public_fixture_example_prints_current_public_fixture_surface(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "examples" / "public_fixture.py")],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(
            [
                "candidate_set",
                "evidence",
                "evidence_set",
                "exclusion",
                "problem",
                "raw_entry",
                "recommendation",
                "request",
                "result_row",
                "scoring_stages",
                "stage_candidate",
                "use_cases",
            ],
            sorted(payload),
        )
        self.assertEqual("recommendation", payload["recommendation"]["object"])
        self.assertEqual("web-browsing", payload["request"]["use_case"])
        self.assertEqual("web-browsing", payload["recommendation"]["use_case"])
        self.assertEqual("candidate_set", payload["candidate_set"]["object"])
        self.assertEqual("stage_candidate", payload["stage_candidate"]["object"])
        self.assertEqual("evidence_set", payload["evidence_set"]["object"])
        self.assertEqual("result_row", payload["result_row"]["object"])
        self.assertEqual("scoring_stage_catalog", payload["scoring_stages"]["object"])
        self.assertEqual("raw_entry", payload["raw_entry"]["object"])
        self.assertEqual("use_case_catalog", payload["use_cases"]["object"])
        self.assertEqual("unknown_cost", payload["exclusion"]["reason"])
        self.assertEqual("ev_public_trace_01", payload["evidence"]["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["evidence"]["subject"]["id"])
        self.assertEqual("validation", payload["problem"]["code"])

    def test_public_fixture_readme_lists_current_output_keys(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "examples" / "public_fixture.py")],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        readme = (REPO_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        for key in sorted(payload):
            with self.subTest(key=key):
                self.assertIn(f"`{key}`", readme)

    def test_public_fixture_readme_lists_nested_contract_refs(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "examples" / "public_fixture.py")],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        readme = (REPO_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        self.assertIn("abstention", payload["recommendation"])
        self.assertIn("the_call", payload["recommendation"])
        output_contracts = {
            contract
            for stage in payload["scoring_stages"]["stages"]
            for contract in stage["output_contracts"]
        }
        self.assertIn("Abstention", output_contracts)
        for ref in (
            "recommendation.abstention",
            "recommendation.the_call",
            "scoring_stages.stages[].output_contracts",
            "Abstention",
        ):
            with self.subTest(ref=ref):
                self.assertIn(f"`{ref}`", readme)


if __name__ == "__main__":
    unittest.main()
