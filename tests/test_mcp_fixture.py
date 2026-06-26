import json
import http.server
import re
import sys
import threading
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_SRC = REPO_ROOT / "packages" / "sdk-python" / "src"
MCP_SRC = REPO_ROOT / "packages" / "mcp" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(SDK_SRC))
sys.path.insert(0, str(MCP_SRC))

from evalrank_core.fixtures import PUBLIC_FIXTURE_KINDS  # noqa: E402
from evalrank_core.fixtures import sample_evaluation_request  # noqa: E402
from evalrank_core.fixtures import sample_recommendation  # noqa: E402
from evalrank_core.fixtures import sample_scoring_stage_catalog  # noqa: E402
from evalrank_core.fixtures import sample_use_case_catalog  # noqa: E402
from evalrank_mcp import call_tool, list_tools  # noqa: E402


class McpFixtureTests(unittest.TestCase):
    def test_mcp_readme_lists_all_public_fixture_kinds(self):
        text = (REPO_ROOT / "packages" / "mcp" / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r'"kind": "([a-z-]+)"', text))

        self.assertEqual(set(PUBLIC_FIXTURE_KINDS), documented)
        for kind in PUBLIC_FIXTURE_KINDS:
            with self.subTest(kind=kind):
                self.assertIn(f'"kind": "{kind}"', text)

    def test_mcp_readme_documents_recommend_tool(self):
        text = (REPO_ROOT / "packages" / "mcp" / "README.md").read_text(encoding="utf-8")

        self.assertIn("evalrank.recommend", text)
        self.assertIn("base_url", text)
        self.assertIn("request", text)

    def test_mcp_readme_documents_metadata_tools(self):
        text = (REPO_ROOT / "packages" / "mcp" / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r'call_tool\("(evalrank\.[a-z_]+)"', text))

        self.assertIn("evalrank.fixture", documented)
        self.assertIn("evalrank.use_cases", text)
        self.assertIn("evalrank.scoring_stages", text)
        self.assertIn("base_url", text)
        self.assertEqual(
            {"evalrank.fixture", "evalrank.recommend", "evalrank.use_cases", "evalrank.scoring_stages"},
            documented,
        )

    def test_list_tools_exposes_public_fixture_tool(self):
        tools = list_tools()

        self.assertEqual(
            ["evalrank.fixture", "evalrank.recommend", "evalrank.use_cases", "evalrank.scoring_stages"],
            [tool["name"] for tool in tools],
        )
        self.assertEqual(["kind"], tools[0]["inputSchema"]["required"])
        self.assertEqual(list(PUBLIC_FIXTURE_KINDS), tools[0]["inputSchema"]["properties"]["kind"]["enum"])
        self.assertEqual(["base_url", "request"], tools[1]["inputSchema"]["required"])
        self.assertEqual(["base_url"], tools[2]["inputSchema"]["required"])
        self.assertEqual(["base_url"], tools[3]["inputSchema"]["required"])
        request_schema = tools[1]["inputSchema"]["properties"]["request"]
        self.assertFalse(request_schema["additionalProperties"])
        self.assertEqual(
            ["object", "request_id", "use_case", "entity_types", "requested_at", "constraints"],
            request_schema["required"],
        )
        self.assertEqual("evaluation_request", request_schema["properties"]["object"]["const"])
        self.assertEqual(1, request_schema["properties"]["request_id"]["minLength"])
        self.assertEqual(1, request_schema["properties"]["use_case"]["minLength"])
        self.assertEqual(1, request_schema["properties"]["entity_types"]["minItems"])
        self.assertTrue(request_schema["properties"]["entity_types"]["uniqueItems"])
        self.assertEqual(1, request_schema["properties"]["entity_types"]["items"]["minLength"])
        self.assertEqual(
            "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
            request_schema["properties"]["requested_at"]["pattern"],
        )
        self.assertTrue(request_schema["properties"]["constraints"]["additionalProperties"])
        for tool in tools[1:]:
            with self.subTest(tool=tool["name"]):
                base_url = tool["inputSchema"]["properties"]["base_url"]
                self.assertEqual("string", base_url["type"])
                self.assertEqual(1, base_url["minLength"])
                self.assertEqual("^https?://", base_url["pattern"])

    def test_call_tool_returns_public_fingerprint_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "fingerprint"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("capability_fingerprint", payload["object"])
        self.assertEqual("io.evalrank.public-search-demo", payload["canonical_id"])

    def test_call_tool_returns_public_evidence_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "evidence"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])

    def test_call_tool_returns_public_problem_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "problem"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("https://evalrank.ai/problems/validation", payload["type"])
        self.assertEqual(422, payload["status"])
        self.assertEqual("validation", payload["code"])

    def test_call_tool_returns_public_result_row_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "result-row"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("result_row", payload["object"])
        self.assertEqual("bench_public_search_freshness", payload["benchmark_id"])
        self.assertEqual("verified", payload["verification_state"])

    def test_call_tool_returns_public_exclusion_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "exclusion"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("tool:public-search-demo", payload["subject"]["id"])
        self.assertEqual("unknown_cost", payload["reason"])

    def test_call_tool_returns_public_request_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "request"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])

    def test_call_tool_returns_public_candidate_set_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "candidate-set"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("candidate_set", payload["object"])
        self.assertEqual("tool:public-search-demo", payload["candidates"][0]["id"])

    def test_call_tool_returns_public_evidence_set_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "evidence-set"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("evidence_set", payload["object"])
        self.assertEqual("ev_public_trace_01", payload["evidence_items"][0]["evidence_id"])

    def test_call_tool_returns_public_stage_candidate_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "stage-candidate"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("stage_candidate", payload["object"])
        self.assertEqual("tool:public-search-demo", payload["entity"]["id"])

    def test_call_tool_returns_public_raw_entry_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "raw-entry"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("raw_entry", payload["object"])
        self.assertEqual("public-fixture:search-demo:2026-06-25", payload["source_id"])

    def test_call_tool_returns_public_use_cases_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "use-cases"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("use_case_catalog", payload["object"])
        self.assertEqual(22, len(payload["use_cases"]))
        self.assertEqual("safety-robustness", payload["use_cases"][-1]["id"])

    def test_call_tool_returns_public_ranking_group_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "ranking-group"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("ranking_group", payload["object"])
        self.assertEqual("mcp_server", payload["group_key"])

    def test_call_tool_returns_public_scoring_stages_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "scoring-stages"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("scoring_stage_catalog", payload["object"])
        self.assertEqual("freshness-trust-labeling", payload["stages"][-1]["id"])

    def test_call_tool_posts_public_recommendation_request(self):
        with LocalApiServer(200, sample_recommendation().to_dict()) as server:
            result = call_tool(
                "evalrank.recommend",
                {"base_url": server.base_url, "request": sample_evaluation_request().to_dict()},
            )

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("recommendation", payload["object"])
        self.assertEqual("POST", server.method)
        self.assertEqual("/v1/recommendations", server.path)
        self.assertEqual(sample_evaluation_request().to_dict(), server.request_json)
        self.assertEqual("application/json", server.headers["content-type"])
        self.assertEqual("application/json", server.headers["accept"])

    def test_call_tool_gets_public_use_case_catalog(self):
        with LocalApiServer(200, sample_use_case_catalog().to_dict()) as server:
            result = call_tool("evalrank.use_cases", {"base_url": server.base_url})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("use_case_catalog", payload["object"])
        self.assertEqual("GET", server.method)
        self.assertEqual("/v1/use-cases", server.path)
        self.assertIsNone(server.request_json)
        self.assertEqual("application/json", server.headers["accept"])

    def test_call_tool_gets_public_scoring_stage_catalog(self):
        with LocalApiServer(200, sample_scoring_stage_catalog().to_dict()) as server:
            result = call_tool("evalrank.scoring_stages", {"base_url": server.base_url})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("scoring_stage_catalog", payload["object"])
        self.assertEqual("GET", server.method)
        self.assertEqual("/v1/scoring-stages", server.path)
        self.assertIsNone(server.request_json)
        self.assertEqual("application/json", server.headers["accept"])

    def test_call_tool_returns_problem_details_as_tool_error(self):
        problem = {
            "type": "https://evalrank.ai/problems/rate-limited",
            "title": "Rate limited",
            "status": 429,
            "detail": "too many requests",
            "code": "rate_limited",
            "retriable": True,
            "retry_after": 3,
        }
        with LocalApiServer(429, problem, {"Retry-After": "3"}) as server:
            result = call_tool(
                "evalrank.recommend",
                {"base_url": server.base_url, "request": sample_evaluation_request().to_dict()},
            )

        self.assertTrue(result["isError"])
        self.assertEqual(problem, json.loads(result["content"][0]["text"]))

    def test_call_tool_returns_metadata_problem_details_as_tool_error(self):
        problem = {
            "type": "https://evalrank.ai/problems/upstream-timeout",
            "title": "Upstream timeout",
            "status": 503,
            "detail": "catalog temporarily unavailable",
            "code": "upstream_timeout",
            "retriable": True,
            "retry_after": 5,
        }
        with LocalApiServer(503, problem, {"Retry-After": "5"}) as server:
            result = call_tool("evalrank.use_cases", {"base_url": server.base_url})

        self.assertTrue(result["isError"])
        self.assertEqual("GET", server.method)
        self.assertEqual(problem, json.loads(result["content"][0]["text"]))

    def test_call_tool_rejects_invalid_recommend_arguments(self):
        with self.assertRaisesRegex(ValueError, "arguments must be an object"):
            call_tool("evalrank.recommend", [])
        with self.assertRaisesRegex(ValueError, "base_url is required"):
            call_tool("evalrank.recommend", {"request": sample_evaluation_request().to_dict()})
        with self.assertRaisesRegex(ValueError, "request must be an object"):
            call_tool("evalrank.recommend", {"base_url": "https://evalrank.example", "request": []})

    def test_call_tool_rejects_invalid_metadata_arguments(self):
        with self.assertRaisesRegex(ValueError, "base_url is required"):
            call_tool("evalrank.use_cases", {})
        with self.assertRaisesRegex(ValueError, "base_url is required"):
            call_tool("evalrank.scoring_stages", {"base_url": ""})

    def test_call_tool_rejects_unknown_tool(self):
        with self.assertRaisesRegex(ValueError, "unknown tool"):
            call_tool("evalrank.unknown", {"kind": "evidence"})


class LocalApiServer:
    def __init__(
        self,
        response_status: int,
        response_body: dict,
        response_headers: dict[str, str] | None = None,
    ) -> None:
        self.response_status = response_status
        self.response_body = response_body
        self.response_headers = response_headers or {}
        self.path: str | None = None
        self.headers: dict[str, str] = {}
        self.method: str | None = None
        self.request_json: dict | None = None
        self._server: http.server.ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        if self._server is None:
            raise RuntimeError("server is not running")
        host, port = self._server.server_address
        return f"http://{host}:{port}"

    def __enter__(self) -> "LocalApiServer":
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                owner.method = self.command
                owner.path = self.path
                owner.headers = {key.lower(): value for key, value in self.headers.items()}
                length = int(self.headers.get("Content-Length", "0"))
                owner.request_json = json.loads(self.rfile.read(length).decode("utf-8"))
                self._write_json()

            def do_GET(self) -> None:  # noqa: N802
                owner.method = self.command
                owner.path = self.path
                owner.headers = {key.lower(): value for key, value in self.headers.items()}
                owner.request_json = None
                self._write_json()

            def _write_json(self) -> None:
                encoded = json.dumps(owner.response_body).encode("utf-8")
                self.send_response(owner.response_status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                for key, value in owner.response_headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format: str, *args: object) -> None:
                return

        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever)
        self._thread.start()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join()


if __name__ == "__main__":
    unittest.main()
