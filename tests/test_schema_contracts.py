import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SCHEMAS = REPO_ROOT / "schemas"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    COMPARABILITY_MODES,
    ConfidenceInterval,
    EVIDENCE_KINDS,
    FRESHNESS_STATUSES,
    Freshness,
    Recommendation,
    RankedEntity,
    TRUST_TIERS,
)
from evalrank_core.fixtures import sample_evidence_item  # noqa: E402


class SchemaContractTests(unittest.TestCase):
    def test_public_schema_files_cover_core_payload_keys(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        recommendation_schema = _schema("recommendation.schema.json")
        evidence_schema = _schema("evidence-item.schema.json")

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
        evidence_payload = sample_evidence_item().to_dict()
        self.assertEqual(set(evidence_payload), set(evidence_schema["properties"]))
        self.assertLessEqual(set(evidence_schema["required"]), set(evidence_payload))

    def test_schemas_are_draft_2020_12_objects(self):
        for filename in ("ranked-entity.schema.json", "recommendation.schema.json", "evidence-item.schema.json"):
            schema = _schema(filename)

            self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
            self.assertTrue(schema["$id"].endswith(filename))
            self.assertEqual("object", schema["type"])
            self.assertFalse(schema["additionalProperties"])

    def test_schema_enums_match_core_constants(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertEqual(TRUST_TIERS, set(ranked_schema["properties"]["trust_tier"]["enum"]))
        self.assertEqual(
            FRESHNESS_STATUSES,
            set(ranked_schema["properties"]["freshness"]["properties"]["status"]["enum"]),
        )
        self.assertEqual(COMPARABILITY_MODES, set(recommendation_schema["properties"]["comparability"]["enum"]))
        evidence_schema = _schema("evidence-item.schema.json")
        self.assertEqual(EVIDENCE_KINDS, set(evidence_schema["properties"]["kind"]["enum"]))


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
