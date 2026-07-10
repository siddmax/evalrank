import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = REPO_ROOT / "schemas"
sys.path.insert(0, str(REPO_ROOT / "packages" / "core" / "src"))

from evalrank_core.contracts import (  # noqa: E402
    PROBLEM_CODES,
    USE_CASE_ENTITY_KINDS,
    USE_CASE_RANK_POLICIES,
)
from evalrank_core.fixtures import (  # noqa: E402
    sample_capability_fingerprint_input,
    sample_raw_entry,
    sample_use_case_catalog,
)


class SchemaContractTests(unittest.TestCase):
    def test_superseded_recommendation_pipeline_schemas_are_deleted(self):
        for filename in (
            "candidate-set.schema.json",
            "evaluation-request.schema.json",
            "evidence-item.schema.json",
            "evidence-set.schema.json",
            "exclusion.schema.json",
            "ranked-entity.schema.json",
            "recommendation.schema.json",
            "result-row.schema.json",
            "scoring-stage-catalog.schema.json",
            "stage-candidate.schema.json",
        ):
            self.assertFalse((SCHEMAS / filename).exists(), filename)

    def test_schema_readme_is_an_exact_inventory(self):
        text = (SCHEMAS / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"`([^`]*(?:\.schema\.json|openapi\.json))`", text))
        expected = {path.name for path in SCHEMAS.glob("*.schema.json")} | {"openapi.json"}
        self.assertEqual(expected, documented)

    def test_independent_discovery_schemas_match_fixture_keys(self):
        for filename, payload in (
            ("capability-fingerprint.schema.json", sample_capability_fingerprint_input().to_dict()),
            ("raw-entry.schema.json", sample_raw_entry().to_dict()),
            ("use-case-catalog.schema.json", sample_use_case_catalog().to_dict()),
        ):
            schema = _schema(filename)
            with self.subTest(filename=filename):
                self.assertEqual(set(payload), set(schema["properties"]))
                self.assertLessEqual(set(schema["required"]), set(payload))
                self.assertFalse(schema["additionalProperties"])

    def test_use_case_schema_matches_public_taxonomy_constants(self):
        use_case = _schema("use-case-catalog.schema.json")["$defs"]["UseCase"]
        self.assertEqual(
            USE_CASE_ENTITY_KINDS,
            set(use_case["properties"]["entity_kinds"]["items"]["enum"]),
        )
        self.assertEqual(
            USE_CASE_RANK_POLICIES,
            set(use_case["properties"]["rank_policy"]["enum"]),
        )

    def test_problem_schema_pins_rfc9457_and_public_codes(self):
        schema = _schema("problem.schema.json")
        self.assertTrue(schema["additionalProperties"])
        self.assertEqual(PROBLEM_CODES, set(schema["properties"]["code"]["enum"]))
        self.assertEqual({"type", "title", "status", "detail"}, set(schema["required"]))

    def test_every_public_schema_uses_draft_2020_12(self):
        for path in SCHEMAS.glob("*.schema.json"):
            schema = _schema(path.name)
            with self.subTest(filename=path.name):
                self.assertEqual(
                    "https://json-schema.org/draft/2020-12/schema",
                    schema["$schema"],
                )


def _schema(filename: str) -> dict:
    return json.loads((SCHEMAS / filename).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
