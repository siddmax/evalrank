import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
MCP_SRC = REPO_ROOT / "packages" / "mcp" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(MCP_SRC))

from evalrank_mcp import call_tool, list_tools  # noqa: E402


class McpFixtureTests(unittest.TestCase):
    def test_list_tools_exposes_public_fixture_tool(self):
        tools = list_tools()

        self.assertEqual(["evalrank.fixture"], [tool["name"] for tool in tools])
        self.assertEqual(["kind"], tools[0]["inputSchema"]["required"])
        self.assertEqual(["evidence", "fingerprint", "recommendation", "request"], tools[0]["inputSchema"]["properties"]["kind"]["enum"])

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

    def test_call_tool_returns_public_request_fixture_text(self):
        result = call_tool("evalrank.fixture", {"kind": "request"})

        self.assertFalse(result["isError"])
        payload = json.loads(result["content"][0]["text"])
        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])

    def test_call_tool_rejects_unknown_tool(self):
        with self.assertRaisesRegex(ValueError, "unknown tool"):
            call_tool("evalrank.unknown", {"kind": "evidence"})


if __name__ == "__main__":
    unittest.main()
