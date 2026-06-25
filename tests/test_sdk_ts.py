import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_TS = REPO_ROOT / "packages" / "sdk-ts"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import EVIDENCE_KINDS, THE_CALL_DECISIONS, TRUST_TIERS  # noqa: E402


class TypeScriptSdkTests(unittest.TestCase):
    def test_package_metadata_exposes_public_typescript_entrypoint(self):
        package = json.loads((SDK_TS / "package.json").read_text(encoding="utf-8"))

        self.assertEqual("@evalrank/sdk", package["name"])
        self.assertEqual("0.0.0", package["version"])
        self.assertEqual("Apache-2.0", package["license"])
        self.assertTrue(package["private"])
        self.assertEqual("module", package["type"])
        self.assertEqual("./src/index.ts", package["types"])
        self.assertEqual("./src/index.ts", package["exports"]["."]["types"])
        self.assertEqual("./src/index.ts", package["exports"]["."]["default"])

    def test_public_constants_match_core_contracts(self):
        source = (SDK_TS / "src" / "index.ts").read_text(encoding="utf-8")

        self.assertEqual(TRUST_TIERS, _exported_string_array(source, "TRUST_TIERS"))
        self.assertEqual(EVIDENCE_KINDS, _exported_string_array(source, "EVIDENCE_KINDS"))
        self.assertEqual(THE_CALL_DECISIONS, _exported_string_array(source, "THE_CALL_DECISIONS"))

    def test_public_interfaces_cover_schema_payloads(self):
        source = (SDK_TS / "src" / "index.ts").read_text(encoding="utf-8")

        for name in (
            "CandidateSet",
            "CapabilityFingerprint",
            "EntityRef",
            "Exclusion",
            "EvidenceSet",
            "EvaluationRequest",
            "EvidenceItem",
            "RankedEntity",
            "RawEntry",
            "Recommendation",
            "StageCandidate",
            "TheCall",
        ):
            self.assertIn(f"export interface {name}", source)

        for field in (
            "capability_fingerprint",
            "id_scheme",
            "canonical_id",
            "declared_capability_shape",
            "raw_metadata",
            "source_id",
            "fetched_at",
            "content_hash",
            "request_id",
            "entity_types",
            "requested_at",
            "constraints",
            "candidates",
            "detail",
            "evidence_items",
            "generated_at",
            "evidence_id",
            "subject",
            "kind",
            "source",
            "observed_at",
            "summary",
            "metadata",
            "recommendation_id",
            "recommend_id",
            "search_run_id",
            "rrf_components",
            "retrieval_provenance",
            "abstention_reason",
        ):
            self.assertRegex(source, rf"\b{field}\??:")

        self.assertIn("the_call: TheCall | null;", source)
        self.assertIn("exclusions: Exclusion[];", source)


def _exported_string_array(source: str, name: str) -> set[str]:
    match = re.search(rf"export const {name} = \[(?P<body>.*?)\] as const;", source, re.S)
    if not match:
        raise AssertionError(f"{name} export not found")
    return set(re.findall(r'"([^"]+)"', match.group("body")))


if __name__ == "__main__":
    unittest.main()
