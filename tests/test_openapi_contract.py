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
        self.assertEqual(
            "problem.schema.json",
            spec["components"]["schemas"]["ProblemDetails"]["$ref"],
        )
        for schema in spec["components"]["schemas"].values():
            ref = schema["$ref"]
            self.assertFalse(ref.startswith("#"))
            self.assertTrue((SCHEMAS / ref).is_file(), ref)

    def test_public_openapi_contract_pins_problem_details_errors(self):
        spec = _openapi()
        responses = spec["paths"]["/v1/recommendations"]["post"]["responses"]

        self.assertEqual(
            "#/components/responses/BadRequest",
            responses["400"]["$ref"],
        )
        self.assertEqual(
            "#/components/responses/ValidationError",
            responses["422"]["$ref"],
        )
        self.assertEqual(
            "#/components/responses/RateLimited",
            responses["429"]["$ref"],
        )
        self.assertEqual(
            "#/components/responses/ServiceUnavailable",
            responses["503"]["$ref"],
        )
        self.assertEqual(
            "#/components/responses/UpstreamTimeout",
            responses["504"]["$ref"],
        )

        for response_name in (
            "BadRequest",
            "ValidationError",
            "RateLimited",
            "ServiceUnavailable",
            "UpstreamTimeout",
        ):
            response = spec["components"]["responses"][response_name]
            self.assertEqual(
                "#/components/headers/RequestId",
                response["headers"]["X-Request-Id"]["$ref"],
            )
            self.assertEqual(
                "#/components/schemas/ProblemDetails",
                response["content"]["application/problem+json"]["schema"]["$ref"],
            )

    def test_public_openapi_contract_pins_retry_headers(self):
        spec = _openapi()
        rate_limited = spec["components"]["responses"]["RateLimited"]
        unavailable = spec["components"]["responses"]["ServiceUnavailable"]
        timeout = spec["components"]["responses"]["UpstreamTimeout"]

        self.assertEqual(
            "#/components/headers/RetryAfter",
            rate_limited["headers"]["Retry-After"]["$ref"],
        )
        self.assertEqual(
            "#/components/headers/RateLimit",
            rate_limited["headers"]["RateLimit"]["$ref"],
        )
        self.assertEqual(
            "#/components/headers/RateLimitPolicy",
            rate_limited["headers"]["RateLimit-Policy"]["$ref"],
        )
        self.assertEqual(
            "#/components/headers/RetryAfter",
            unavailable["headers"]["Retry-After"]["$ref"],
        )
        self.assertEqual(
            "#/components/headers/RetryAfter",
            timeout["headers"]["Retry-After"]["$ref"],
        )
        self.assertEqual("integer", spec["components"]["headers"]["RetryAfter"]["schema"]["type"])
        self.assertEqual("string", spec["components"]["headers"]["RateLimit"]["schema"]["type"])
        self.assertEqual("string", spec["components"]["headers"]["RateLimitPolicy"]["schema"]["type"])

    def test_openapi_contract_stays_storage_free(self):
        spec = _openapi()

        self.assertNotIn("servers", spec)
        self.assertNotIn("security", spec)
        self.assertNotIn("securitySchemes", spec.get("components", {}))


def _openapi() -> dict:
    return json.loads(OPENAPI.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
