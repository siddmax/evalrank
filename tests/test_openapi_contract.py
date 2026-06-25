import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = REPO_ROOT / "schemas"
OPENAPI = SCHEMAS / "openapi.json"


class OpenApiContractTests(unittest.TestCase):
    def test_public_openapi_contract_pins_recommendations_route(self):
        spec = _openapi()
        operation = spec["paths"]["/v1/recommendations"]["post"]

        self.assertEqual("3.1.1", spec["openapi"])
        self.assertEqual("evaluateRecommendation", operation["operationId"])
        self.assertEqual(["recommendations"], operation["tags"])
        self.assertTrue(operation["requestBody"]["required"])
        self.assertEqual(
            "#/components/schemas/EvaluationRequest",
            operation["requestBody"]["content"]["application/json"]["schema"]["$ref"],
        )
        self.assertEqual(
            "#/components/schemas/Recommendation",
            operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"],
        )

    def test_openapi_components_reference_existing_public_schemas(self):
        spec = _openapi()

        self.assertEqual(
            "evaluation-request.schema.json",
            spec["components"]["schemas"]["EvaluationRequest"]["$ref"],
        )
        self.assertEqual(
            "recommendation.schema.json",
            spec["components"]["schemas"]["Recommendation"]["$ref"],
        )
        for schema in spec["components"]["schemas"].values():
            ref = schema["$ref"]
            self.assertFalse(ref.startswith("#"))
            self.assertTrue((SCHEMAS / ref).is_file(), ref)

    def test_openapi_contract_stays_storage_free(self):
        spec = _openapi()

        self.assertNotIn("servers", spec)
        self.assertNotIn("security", spec)
        self.assertNotIn("securitySchemes", spec.get("components", {}))


def _openapi() -> dict:
    return json.loads(OPENAPI.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
