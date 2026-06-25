import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SCHEMAS = REPO_ROOT / "schemas"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    ConfidenceInterval,
    Freshness,
    Recommendation,
    RankedEntity,
)


class SchemaContractTests(unittest.TestCase):
    def test_public_schema_files_cover_core_payload_keys(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        recommendation_schema = _schema("recommendation.schema.json")

        ranked_payload = _row().to_dict()
        recommendation_payload = Recommendation.single_scale(
            request_id="req_01",
            use_case="function-calling",
            methodology_version="2026.06.1",
            ranked=[_row()],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        ).to_dict()

        self.assertEqual(set(ranked_payload), set(ranked_schema["properties"]))
        self.assertLessEqual(set(ranked_schema["required"]), set(ranked_payload))
        self.assertEqual(set(recommendation_payload), set(recommendation_schema["properties"]))
        self.assertLessEqual(set(recommendation_schema["required"]), set(recommendation_payload))

    def test_schemas_are_draft_2020_12_objects(self):
        for filename in ("ranked-entity.schema.json", "recommendation.schema.json"):
            schema = _schema(filename)

            self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
            self.assertTrue(schema["$id"].endswith(filename))
            self.assertEqual("object", schema["type"])
            self.assertFalse(schema["additionalProperties"])


def _schema(filename: str) -> dict:
    return json.loads((SCHEMAS / filename).read_text(encoding="utf-8"))


def _row() -> RankedEntity:
    return RankedEntity(
        entity_type="mcp_server",
        entity_id="tool:exa-search-mcp",
        rank=1,
        capability_score=0.84,
        confidence=0.86,
        ci95=ConfidenceInterval(low=0.80, high=0.88),
        methodology_version="2026.06.1",
        trust_tier="standardized",
        freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
        evidence_count=1840,
    )


if __name__ == "__main__":
    unittest.main()
