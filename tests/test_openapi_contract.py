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

    def test_public_openapi_contract_pins_use_cases_route(self):
        spec = _openapi()
        operation = spec["paths"]["/v1/use-cases"]["get"]

        self.assertEqual("listUseCases", operation["operationId"])
        self.assertEqual(["metadata"], operation["tags"])
        self.assertNotIn("requestBody", operation)
        self.assertEqual(
            "#/components/schemas/UseCaseCatalog",
            operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"],
        )
        self.assertEqual("#/components/responses/RateLimited", operation["responses"]["429"]["$ref"])
        self.assertEqual("#/components/responses/ServiceUnavailable", operation["responses"]["503"]["$ref"])

    def test_public_openapi_contract_pins_scoring_stages_route(self):
        spec = _openapi()
        operation = spec["paths"]["/v1/scoring-stages"]["get"]

        self.assertEqual("listScoringStages", operation["operationId"])
        self.assertEqual(["metadata"], operation["tags"])
        self.assertNotIn("requestBody", operation)
        self.assertEqual(
            "#/components/schemas/ScoringStageCatalog",
            operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"],
        )
        self.assertEqual("#/components/responses/RateLimited", operation["responses"]["429"]["$ref"])
        self.assertEqual("#/components/responses/ServiceUnavailable", operation["responses"]["503"]["$ref"])

    def test_public_openapi_contract_pins_grouped_read_routes(self):
        spec = _openapi()
        cases = (
            (
                "/v1/entities/{entity_type}/{slug}",
                "getEntityDetail",
                "EntityDetail",
                {"entity_type": "path", "slug": "path"},
            ),
            (
                "/v1/compare",
                "compareEntities",
                "CompareResult",
                {"use_case": "query", "entities": "query"},
            ),
            (
                "/v1/leaderboard/{use_case}",
                "getLeaderboard",
                "Leaderboard",
                {"use_case": "path"},
            ),
        )

        for path, operation_id, response_schema, expected_parameters in cases:
            with self.subTest(path=path):
                operation = spec["paths"][path]["get"]
                self.assertEqual(operation_id, operation["operationId"])
                self.assertEqual(["explorer"], operation["tags"])
                self.assertEqual(
                    f"#/components/schemas/{response_schema}",
                    operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"],
                )
                self.assertEqual(
                    expected_parameters,
                    {parameter["name"]: parameter["in"] for parameter in operation["parameters"]},
                )
                self.assertTrue(all(parameter["required"] for parameter in operation["parameters"]))
                for status, response in (
                    ("400", "BadRequest"),
                    ("404", "NotFound"),
                    ("429", "RateLimited"),
                    ("503", "ServiceUnavailable"),
                ):
                    self.assertEqual(
                        f"#/components/responses/{response}",
                        operation["responses"][status]["$ref"],
                    )

        compare_entities = spec["paths"]["/v1/compare"]["get"]["parameters"][1]
        self.assertEqual("array", compare_entities["schema"]["type"])
        self.assertEqual(2, compare_entities["schema"]["minItems"])
        self.assertEqual(4, compare_entities["schema"]["maxItems"])
        self.assertTrue(compare_entities["schema"]["uniqueItems"])
        self.assertEqual("form", compare_entities["style"])
        self.assertFalse(compare_entities["explode"])

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
        self.assertEqual(
            "use-case-catalog.schema.json",
            spec["components"]["schemas"]["UseCaseCatalog"]["$ref"],
        )
        self.assertEqual(
            "scoring-stage-catalog.schema.json",
            spec["components"]["schemas"]["ScoringStageCatalog"]["$ref"],
        )
        self.assertEqual(
            "entity-detail.schema.json",
            spec["components"]["schemas"]["EntityDetail"]["$ref"],
        )
        self.assertEqual(
            "compare-result.schema.json",
            spec["components"]["schemas"]["CompareResult"]["$ref"],
        )
        self.assertEqual(
            "leaderboard.schema.json",
            spec["components"]["schemas"]["Leaderboard"]["$ref"],
        )
        for schema in spec["components"]["schemas"].values():
            ref = schema["$ref"]
            self.assertFalse(ref.startswith("#"))
            self.assertTrue((SCHEMAS / ref).is_file(), ref)

    def test_public_openapi_contract_pins_problem_details_errors(self):
        spec = _openapi()
        responses = spec["paths"]["/v1/recommendations"]["post"]["responses"]

        self.assertEqual(
            "#/components/responses/InvalidEvaluationRequest",
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
            "#/components/responses/RecommendationNotPublished",
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
                response["content"]["application/problem+json"]["schema"]["allOf"][0]["$ref"],
            )

    def test_legacy_recommendation_unavailability_is_a_named_typed_problem(self):
        spec = _openapi()
        response = spec["components"]["responses"]["RecommendationNotPublished"]

        self.assertEqual(
            "#/components/headers/RetryAfter",
            response["headers"]["Retry-After"]["$ref"],
        )
        schema = response["content"]["application/problem+json"]["schema"]
        self.assertEqual("#/components/schemas/ProblemDetails", schema["allOf"][0]["$ref"])
        typed = schema["allOf"][1]
        self.assertEqual({"code", "retriable", "status"}, set(typed["required"]))
        self.assertEqual(
            "recommendation_not_published",
            typed["properties"]["code"]["const"],
        )
        self.assertTrue(typed["properties"]["retriable"]["const"])
        self.assertEqual(503, typed["properties"]["status"]["const"])

    def test_invalid_evaluation_request_is_a_named_typed_problem(self):
        spec = _openapi()
        response = spec["components"]["responses"]["InvalidEvaluationRequest"]
        schema = response["content"]["application/problem+json"]["schema"]

        self.assertEqual("#/components/schemas/ProblemDetails", schema["allOf"][0]["$ref"])
        typed = schema["allOf"][1]
        self.assertEqual({"code", "retriable", "status"}, set(typed["required"]))
        self.assertEqual(
            "invalid_evaluation_request",
            typed["properties"]["code"]["const"],
        )
        self.assertFalse(typed["properties"]["retriable"]["const"])
        self.assertEqual(400, typed["properties"]["status"]["const"])

    def test_unsupported_media_type_is_a_strict_invalid_request_problem(self):
        spec = _openapi()
        operation = spec["paths"]["/v1/recommendations"]["post"]
        self.assertEqual(
            "#/components/responses/UnsupportedMediaType",
            operation["responses"]["415"]["$ref"],
        )

        response = spec["components"]["responses"]["UnsupportedMediaType"]
        schema = response["content"]["application/problem+json"]["schema"]
        self.assertEqual("#/components/schemas/ProblemDetails", schema["allOf"][0]["$ref"])
        typed = schema["allOf"][1]
        self.assertEqual({"status", "code", "retriable"}, set(typed["required"]))
        self.assertEqual(415, typed["properties"]["status"]["const"])
        self.assertEqual(
            "invalid_evaluation_request", typed["properties"]["code"]["const"]
        )
        self.assertFalse(typed["properties"]["retriable"]["const"])

    def test_problem_responses_pin_http_status_code_and_retry_semantics(self):
        spec = _openapi()
        expected = {
            "BadRequest": (400, "validation", False, False),
            "NotFound": (404, "not_found", False, False),
            "ValidationError": (422, "validation", False, False),
            "RateLimited": (429, "rate_limited", True, True),
            "UpstreamTimeout": (504, "upstream_timeout", True, True),
        }

        for component, (status, code, retriable, requires_retry_after) in expected.items():
            with self.subTest(component=component):
                schema = spec["components"]["responses"][component]["content"]["application/problem+json"]["schema"]
                self.assertEqual("#/components/schemas/ProblemDetails", schema["allOf"][0]["$ref"])
                typed = schema["allOf"][1]
                self.assertEqual(status, typed["properties"]["status"]["const"])
                self.assertEqual(code, typed["properties"]["code"]["const"])
                self.assertEqual(retriable, typed["properties"]["retriable"]["const"])
                self.assertEqual(requires_retry_after, "retry_after" in typed["required"])

        service = spec["components"]["responses"]["ServiceUnavailable"]["content"]["application/problem+json"]["schema"]["allOf"][1]
        self.assertEqual(503, service["properties"]["status"]["const"])
        self.assertEqual(
            {"internal", "methodology_stale", "upstream_timeout"},
            set(service["properties"]["code"]["enum"]),
        )
        self.assertTrue(service["properties"]["retriable"]["const"])
        self.assertIn("retry_after", service["required"])

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
