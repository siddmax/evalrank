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
    def test_fixture_evidence_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "evidence"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])

    def test_fixture_recommendation_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "recommendation"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("recommendation", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])

    def test_invalid_fixture_exits_nonzero(self):
        stderr = StringIO()

        exit_code = main(["fixture", "unknown"], stdout=StringIO(), stderr=stderr)

        self.assertNotEqual(0, exit_code)
        self.assertIn("invalid choice", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
