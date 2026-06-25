import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublicExampleTests(unittest.TestCase):
    def test_public_fixture_example_prints_recommendation_and_evidence(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "examples" / "public_fixture.py")],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual("recommendation", payload["recommendation"]["object"])
        self.assertEqual("ev_public_trace_01", payload["evidence"]["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["evidence"]["subject"]["id"])


if __name__ == "__main__":
    unittest.main()
