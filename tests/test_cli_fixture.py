import json
import re
import sys
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Thread


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
CLI_SRC = REPO_ROOT / "packages" / "cli" / "src"
SDK_SRC = REPO_ROOT / "packages" / "sdk-python" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(CLI_SRC))
sys.path.insert(0, str(SDK_SRC))

from evalrank_core.fixtures import PUBLIC_FIXTURE_KINDS  # noqa: E402
from evalrank_core.fixtures import (  # noqa: E402
    sample_evaluation_request,
    sample_problem_details,
    sample_recommendation,
    sample_scoring_stage_catalog,
    sample_use_case_catalog,
)
from evalrank_cli import main  # noqa: E402

def _manifest_use_cases() -> list[dict]:
    cells = json.loads((REPO_ROOT / "catalog" / "manifest.json").read_text(encoding="utf-8"))["cells"]
    return [
        {
            "object": "use_case",
            "id": cell["cell_id"],
            "name": cell["name"],
            "definition": cell["definition"],
            "entity_kinds": cell["entity_kinds"],
            "rank_policy": "ranked",
            "is_overlay": False,
        }
        for cell in cells
    ]


class CliFixtureTests(unittest.TestCase):
    def test_cli_readme_lists_all_public_fixture_commands(self):
        text = (REPO_ROOT / "packages" / "cli" / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"^evalrank fixture ([a-z-]+)$", text, re.M))

        self.assertEqual(set(PUBLIC_FIXTURE_KINDS), documented)
        for kind in PUBLIC_FIXTURE_KINDS:
            with self.subTest(kind=kind):
                self.assertIn(f"evalrank fixture {kind}", text)

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
        self.assertRegex(payload["subject"]["id"], r"^config_[0-9a-f]{64}$")

    def test_fixture_problem_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "problem"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("https://evalrank.ai/problems/validation", payload["type"])
        self.assertEqual(422, payload["status"])
        self.assertEqual("validation", payload["code"])

    def test_fixture_observation_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "observation"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("observation", payload["object"])
        self.assertEqual("proportion", payload["metric"]["kind"])
        self.assertEqual("reported", payload["uncertainty"]["method"])

    def test_fixture_exclusion_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "exclusion"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertRegex(payload["subject"]["id"], r"^config_[0-9a-f]{64}$")
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
        self.assertEqual(["component_configuration"], payload["entity_types"])

    def test_fixture_candidate_set_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "candidate-set"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("candidate_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertRegex(payload["candidates"][0]["id"], r"^config_[0-9a-f]{64}$")

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
        self.assertRegex(payload["entity"]["id"], r"^config_[0-9a-f]{64}$")
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
        self.assertEqual(26, len(payload["use_cases"]))
        self.assertEqual(
            "computational-research-reproduction",
            payload["use_cases"][-1]["id"],
        )
        self.assertTrue(all(row["rank_policy"] == "ranked" for row in payload["use_cases"]))
        self.assertEqual(_manifest_use_cases(), payload["use_cases"])

    def test_fixture_ranking_group_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "ranking-group"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("ranking_group", payload["object"])
        self.assertEqual("component_configuration", payload["entity_type"])

    def test_fixture_scoring_stages_writes_public_json(self):
        stdout = StringIO()

        exit_code = main(["fixture", "scoring-stages"], stdout=stdout, stderr=StringIO())

        self.assertEqual(0, exit_code)
        payload = json.loads(stdout.getvalue())
        self.assertEqual("scoring_stage_catalog", payload["object"])
        self.assertEqual("request-normalization", payload["stages"][0]["id"])

    def test_invalid_fixture_exits_nonzero(self):
        stderr = StringIO()

        exit_code = main(["fixture", "unknown"], stdout=StringIO(), stderr=stderr)

        self.assertNotEqual(0, exit_code)
        self.assertIn("invalid choice", stderr.getvalue())

    def test_cli_readme_lists_recommend_command(self):
        text = (REPO_ROOT / "packages" / "cli" / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"^evalrank (?:use-cases|scoring-stages|recommend) .*$", text, re.M))

        self.assertEqual(
            {
                "evalrank use-cases --base-url https://evalrank.example",
                "evalrank scoring-stages --base-url https://evalrank.example",
                "evalrank recommend --base-url https://evalrank.example --request request.json",
                "evalrank recommend --base-url https://evalrank.example --request -",
            },
            documented,
        )
        self.assertIn("evalrank recommend --base-url", text)

    def test_cli_readme_lists_metadata_commands(self):
        text = (REPO_ROOT / "packages" / "cli" / "README.md").read_text(encoding="utf-8")

        self.assertIn("evalrank use-cases --base-url", text)
        self.assertIn("evalrank scoring-stages --base-url", text)

    def test_use_cases_gets_public_catalog_and_writes_json(self):
        server = _CliTestServer(response_status=200, response_body=sample_use_case_catalog().to_dict())
        stdout = StringIO()
        try:
            exit_code = main(
                ["use-cases", "--base-url", server.base_url],
                stdout=stdout,
                stderr=StringIO(),
            )
        finally:
            server.close()

        self.assertEqual(0, exit_code)
        self.assertEqual("GET", server.method)
        self.assertEqual("/v1/use-cases", server.path)
        self.assertIsNone(server.request_json)
        self.assertEqual("use_case_catalog", json.loads(stdout.getvalue())["object"])

    def test_scoring_stages_gets_public_catalog_and_writes_json(self):
        server = _CliTestServer(response_status=200, response_body=sample_scoring_stage_catalog().to_dict())
        stdout = StringIO()
        try:
            exit_code = main(
                ["scoring-stages", "--base-url", server.base_url],
                stdout=stdout,
                stderr=StringIO(),
            )
        finally:
            server.close()

        self.assertEqual(0, exit_code)
        self.assertEqual("GET", server.method)
        self.assertEqual("/v1/scoring-stages", server.path)
        self.assertIsNone(server.request_json)
        self.assertEqual("scoring_stage_catalog", json.loads(stdout.getvalue())["object"])

    def test_metadata_command_writes_problem_details_to_stderr(self):
        problem = {**sample_problem_details().to_dict(), "status": 503}
        server = _CliTestServer(response_status=503, response_body=problem)
        stderr = StringIO()
        try:
            exit_code = main(
                ["use-cases", "--base-url", server.base_url],
                stdout=StringIO(),
                stderr=stderr,
            )
        finally:
            server.close()

        self.assertEqual(1, exit_code)
        self.assertEqual("GET", server.method)
        self.assertEqual(problem, json.loads(stderr.getvalue()))

    def test_metadata_command_rejects_non_http_base_url(self):
        stderr = StringIO()

        exit_code = main(
            ["use-cases", "--base-url", "file:///tmp/evalrank"],
            stdout=StringIO(),
            stderr=stderr,
        )

        self.assertEqual(2, exit_code)
        self.assertIn("base_url must be an http or https URL", stderr.getvalue())

    def test_recommend_posts_request_file_and_writes_public_json(self):
        server = _CliTestServer(response_status=200, response_body=sample_recommendation().to_dict())
        stdout = StringIO()
        try:
            with NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as request_file:
                json.dump(sample_evaluation_request().to_dict(), request_file)
                request_file.flush()
                exit_code = main(
                    ["recommend", "--base-url", server.base_url, "--request", request_file.name],
                    stdout=stdout,
                    stderr=StringIO(),
                )
        finally:
            server.close()

        self.assertEqual(0, exit_code)
        self.assertEqual("POST", server.method)
        self.assertEqual("/v1/recommendations", server.path)
        self.assertEqual(sample_evaluation_request().to_dict(), server.request_json)
        self.assertEqual("recommendation", json.loads(stdout.getvalue())["object"])

    def test_recommend_reads_request_json_from_stdin(self):
        server = _CliTestServer(response_status=200, response_body=sample_recommendation().to_dict())
        stdout = StringIO()
        original_stdin = sys.stdin
        sys.stdin = StringIO(json.dumps(sample_evaluation_request().to_dict()))
        try:
            exit_code = main(
                ["recommend", "--base-url", server.base_url, "--request", "-"],
                stdout=stdout,
                stderr=StringIO(),
            )
        finally:
            sys.stdin = original_stdin
            server.close()

        self.assertEqual(0, exit_code)
        self.assertEqual("POST", server.method)
        self.assertEqual("/v1/recommendations", server.path)
        self.assertEqual(sample_evaluation_request().to_dict(), server.request_json)
        self.assertEqual("recommendation", json.loads(stdout.getvalue())["object"])

    def test_recommend_writes_problem_details_to_stderr(self):
        problem = {**sample_problem_details().to_dict(), "status": 429}
        server = _CliTestServer(response_status=429, response_body=problem)
        stderr = StringIO()
        try:
            with NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as request_file:
                json.dump(sample_evaluation_request().to_dict(), request_file)
                request_file.flush()
                exit_code = main(
                    ["recommend", "--base-url", server.base_url, "--request", request_file.name],
                    stdout=StringIO(),
                    stderr=stderr,
                )
        finally:
            server.close()

        self.assertEqual(1, exit_code)
        self.assertEqual(problem, json.loads(stderr.getvalue()))

    def test_recommend_rejects_non_http_base_url(self):
        stderr = StringIO()

        exit_code = main(
            ["recommend", "--base-url", "file:///tmp/evalrank", "--request", "-"],
            stdout=StringIO(),
            stderr=stderr,
        )

        self.assertEqual(2, exit_code)
        self.assertIn("base_url must be an http or https URL", stderr.getvalue())

    def test_recommend_rejects_invalid_request_json_without_network_call(self):
        server = _CliTestServer(response_status=200, response_body=sample_recommendation().to_dict())
        stderr = StringIO()
        try:
            with NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as request_file:
                request_file.write("{")
                request_file.flush()
                exit_code = main(
                    ["recommend", "--base-url", server.base_url, "--request", request_file.name],
                    stdout=StringIO(),
                    stderr=stderr,
                )
        finally:
            server.close()

        self.assertEqual(2, exit_code)
        self.assertIsNone(server.request_json)
        self.assertIn("invalid request JSON", stderr.getvalue())

    def test_recommend_rejects_non_object_stdin_json_without_network_call(self):
        server = _CliTestServer(response_status=200, response_body=sample_recommendation().to_dict())
        stderr = StringIO()
        original_stdin = sys.stdin
        sys.stdin = StringIO("[]")
        try:
            exit_code = main(
                ["recommend", "--base-url", server.base_url, "--request", "-"],
                stdout=StringIO(),
                stderr=stderr,
            )
        finally:
            sys.stdin = original_stdin
            server.close()

        self.assertEqual(2, exit_code)
        self.assertIsNone(server.request_json)
        self.assertIn("request JSON must be an object", stderr.getvalue())


class _CliTestServer:
    def __init__(self, *, response_status: int, response_body: dict) -> None:
        self.request_json: dict | None = None
        self.path: str | None = None
        self.method: str | None = None

        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                owner.method = self.command
                owner.path = self.path
                body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
                owner.request_json = json.loads(body.decode("utf-8"))
                self._write_json()

            def do_GET(self) -> None:
                owner.method = self.command
                owner.path = self.path
                owner.request_json = None
                self._write_json()

            def _write_json(self) -> None:
                encoded = json.dumps(response_body).encode("utf-8")
                self.send_response(response_status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format: str, *args: object) -> None:
                return

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self._thread = Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        host, port = self._server.server_address
        self.base_url = f"http://{host}:{port}"

    def close(self) -> None:
        self._server.shutdown()
        self._thread.join(timeout=5)
        self._server.server_close()


if __name__ == "__main__":
    unittest.main()
