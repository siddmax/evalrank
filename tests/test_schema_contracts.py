import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SCHEMAS = REPO_ROOT / "schemas"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    CapabilityFingerprintInput,
    COMPARABILITY_MODES,
    ConfidenceInterval,
    EVIDENCE_KINDS,
    FRESHNESS_STATUSES,
    Freshness,
    Recommendation,
    RankedEntity,
    RESULT_ENTITY_KINDS,
    RESULT_FLAG_KEYS,
    RESULT_VERIFICATION_STATES,
    THE_CALL_DECISIONS,
    TRUST_TIERS,
)
from evalrank_core.fixtures import (  # noqa: E402
    sample_candidate_set,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_raw_entry,
    sample_result_row,
    sample_stage_candidate,
)


METHODOLOGY_VERSION_PATTERN = r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*\.([a-z0-9]+-)*[a-z0-9]+$"
PROBLEM_CODES = [
    "rate_limited",
    "upstream_timeout",
    "validation",
    "not_found",
    "methodology_stale",
    "internal",
    "unauthorized",
    "forbidden",
]


class SchemaContractTests(unittest.TestCase):
    def test_public_schema_files_cover_core_payload_keys(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        recommendation_schema = _schema("recommendation.schema.json")
        exclusion_schema = _schema("exclusion.schema.json")
        evidence_schema = _schema("evidence-item.schema.json")
        evidence_set_schema = _schema("evidence-set.schema.json")
        stage_candidate_schema = _schema("stage-candidate.schema.json")
        request_schema = _schema("evaluation-request.schema.json")
        candidate_set_schema = _schema("candidate-set.schema.json")
        fingerprint_schema = _schema("capability-fingerprint.schema.json")
        raw_entry_schema = _schema("raw-entry.schema.json")
        result_row_schema = _schema("result-row.schema.json")

        ranked_payload = _row().to_dict()
        recommendation_payload = Recommendation.single_scale(
            request_id="req_01",
            use_case="function-calling",
            methodology_version="2026-06-25.1.public-fixture-v1",
            ranked=[_row()],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        ).to_dict()

        self.assertEqual(set(ranked_payload), set(ranked_schema["properties"]))
        self.assertLessEqual(set(ranked_schema["required"]), set(ranked_payload))
        self.assertEqual(set(recommendation_payload), set(recommendation_schema["properties"]))
        self.assertLessEqual(set(recommendation_schema["required"]), set(recommendation_payload))
        exclusion_payload = sample_exclusion().to_dict()
        self.assertEqual(set(exclusion_payload), set(exclusion_schema["properties"]))
        self.assertLessEqual(set(exclusion_schema["required"]), set(exclusion_payload))
        evidence_payload = sample_evidence_item().to_dict()
        self.assertEqual(set(evidence_payload), set(evidence_schema["properties"]))
        self.assertLessEqual(set(evidence_schema["required"]), set(evidence_payload))
        evidence_set_payload = sample_evidence_set().to_dict()
        self.assertEqual(set(evidence_set_payload), set(evidence_set_schema["properties"]))
        self.assertLessEqual(set(evidence_set_schema["required"]), set(evidence_set_payload))
        stage_candidate_payload = sample_stage_candidate().to_dict()
        self.assertEqual(set(stage_candidate_payload), set(stage_candidate_schema["properties"]))
        self.assertLessEqual(set(stage_candidate_schema["required"]), set(stage_candidate_payload))
        request_payload = sample_evaluation_request().to_dict()
        self.assertEqual(set(request_payload), set(request_schema["properties"]))
        self.assertLessEqual(set(request_schema["required"]), set(request_payload))
        candidate_set_payload = sample_candidate_set().to_dict()
        self.assertEqual(set(candidate_set_payload), set(candidate_set_schema["properties"]))
        self.assertLessEqual(set(candidate_set_schema["required"]), set(candidate_set_payload))
        fingerprint_payload = _fingerprint_input().to_dict()
        self.assertEqual(set(fingerprint_payload), set(fingerprint_schema["properties"]))
        self.assertLessEqual(set(fingerprint_schema["required"]), set(fingerprint_payload))
        raw_entry_payload = sample_raw_entry().to_dict()
        self.assertEqual(set(raw_entry_payload), set(raw_entry_schema["properties"]))
        self.assertLessEqual(set(raw_entry_schema["required"]), set(raw_entry_payload))
        result_row_payload = sample_result_row().to_dict()
        self.assertEqual(set(result_row_payload), set(result_row_schema["properties"]))
        self.assertLessEqual(set(result_row_schema["required"]), set(result_row_payload))

    def test_schemas_are_draft_2020_12_objects(self):
        for filename in (
            "ranked-entity.schema.json",
            "recommendation.schema.json",
            "exclusion.schema.json",
            "evidence-item.schema.json",
            "evidence-set.schema.json",
            "stage-candidate.schema.json",
            "evaluation-request.schema.json",
            "candidate-set.schema.json",
            "capability-fingerprint.schema.json",
            "raw-entry.schema.json",
            "result-row.schema.json",
            "problem.schema.json",
        ):
            schema = _schema(filename)

            self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
            self.assertTrue(schema["$id"].endswith(filename))
            self.assertEqual("object", schema["type"])
            if filename == "problem.schema.json":
                self.assertTrue(schema["additionalProperties"])
            else:
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
        self.assertEqual(
            THE_CALL_DECISIONS,
            set(recommendation_schema["properties"]["the_call"]["properties"]["decision"]["enum"]),
        )
        evidence_schema = _schema("evidence-item.schema.json")
        self.assertEqual(EVIDENCE_KINDS, set(evidence_schema["properties"]["kind"]["enum"]))
        result_row_schema = _schema("result-row.schema.json")
        self.assertEqual(RESULT_ENTITY_KINDS, set(result_row_schema["properties"]["entity_kind"]["enum"]))
        self.assertEqual(
            RESULT_VERIFICATION_STATES,
            set(result_row_schema["properties"]["verification_state"]["enum"]),
        )

    def test_methodology_version_schema_pattern_matches_pinned_format(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertEqual(METHODOLOGY_VERSION_PATTERN, ranked_schema["properties"]["methodology_version"]["pattern"])
        self.assertEqual(
            METHODOLOGY_VERSION_PATTERN,
            recommendation_schema["properties"]["methodology_version"]["pattern"],
        )

    def test_recommendation_join_aliases_share_id_pattern(self):
        recommendation_schema = _schema("recommendation.schema.json")
        rec_id_pattern = recommendation_schema["properties"]["recommendation_id"]["pattern"]

        self.assertEqual(rec_id_pattern, recommendation_schema["properties"]["recommend_id"]["pattern"])
        self.assertEqual(rec_id_pattern, recommendation_schema["properties"]["search_run_id"]["pattern"])
        self.assertIn("recommend_id", recommendation_schema["required"])
        self.assertIn("search_run_id", recommendation_schema["required"])

    def test_raw_entry_schema_requires_declared_capability_shape_content(self):
        raw_entry_schema = _schema("raw-entry.schema.json")

        self.assertEqual(1, raw_entry_schema["properties"]["declared_capability_shape"]["minProperties"])

    def test_recommendation_schema_pins_the_call_shape(self):
        recommendation_schema = _schema("recommendation.schema.json")
        the_call = recommendation_schema["properties"]["the_call"]

        self.assertEqual(["object", "null"], the_call["type"])
        self.assertFalse(the_call["additionalProperties"])
        self.assertEqual(
            {"decision", "confidence", "reason", "abstention_reason"},
            set(the_call["required"]),
        )
        self.assertEqual(["number", "null"], the_call["properties"]["confidence"]["type"])
        self.assertEqual(0, the_call["properties"]["confidence"]["minimum"])
        self.assertEqual(1, the_call["properties"]["confidence"]["maximum"])

    def test_recommendation_schema_reuses_exclusion_schema(self):
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertEqual("exclusion.schema.json", recommendation_schema["properties"]["exclusions"]["items"]["$ref"])

    def test_exclusion_schema_pins_public_reason_shape(self):
        exclusion_schema = _schema("exclusion.schema.json")

        self.assertEqual({"subject", "reason", "detail"}, set(exclusion_schema["required"]))
        self.assertEqual(
            {"entity_type", "id"},
            set(exclusion_schema["properties"]["subject"]["required"]),
        )
        self.assertFalse(exclusion_schema["properties"]["subject"]["additionalProperties"])
        self.assertEqual("string", exclusion_schema["properties"]["reason"]["type"])
        self.assertEqual(1, exclusion_schema["properties"]["reason"]["minLength"])
        self.assertEqual("string", exclusion_schema["properties"]["detail"]["type"])
        self.assertEqual(1, exclusion_schema["properties"]["detail"]["minLength"])

    def test_problem_schema_pins_rfc_9457_shape(self):
        problem_schema = _schema("problem.schema.json")

        self.assertTrue(problem_schema["additionalProperties"])
        self.assertEqual({"type", "title", "status", "detail"}, set(problem_schema["required"]))
        self.assertEqual("string", problem_schema["properties"]["type"]["type"])
        self.assertEqual("uri-reference", problem_schema["properties"]["type"]["format"])
        self.assertEqual("string", problem_schema["properties"]["title"]["type"])
        self.assertEqual("integer", problem_schema["properties"]["status"]["type"])
        self.assertEqual(400, problem_schema["properties"]["status"]["minimum"])
        self.assertEqual(599, problem_schema["properties"]["status"]["maximum"])
        self.assertEqual("string", problem_schema["properties"]["detail"]["type"])
        self.assertEqual("uri-reference", problem_schema["properties"]["instance"]["format"])

    def test_problem_schema_pins_evalrank_error_extensions(self):
        problem_schema = _schema("problem.schema.json")
        properties = problem_schema["properties"]

        self.assertEqual(PROBLEM_CODES, properties["code"]["enum"])
        self.assertEqual("boolean", properties["retriable"]["type"])
        self.assertEqual("integer", properties["retry_after"]["type"])
        self.assertEqual(0, properties["retry_after"]["minimum"])
        self.assertEqual("string", properties["field"]["type"])
        self.assertEqual(1, properties["field"]["minLength"])
        self.assertEqual("string", properties["request_id"]["type"])
        self.assertEqual(1, properties["request_id"]["minLength"])
        self.assertEqual("string", properties["doc_url"]["type"])
        self.assertEqual("uri-reference", properties["doc_url"]["format"])
        self.assertEqual(1, properties["doc_url"]["minLength"])

    def test_candidate_set_schema_pins_public_candidate_refs(self):
        candidate_set_schema = _schema("candidate-set.schema.json")

        self.assertEqual(
            {"object", "request_id", "use_case", "candidates", "generated_at"},
            set(candidate_set_schema["required"]),
        )
        self.assertEqual("candidate_set", candidate_set_schema["properties"]["object"]["const"])
        candidates = candidate_set_schema["properties"]["candidates"]
        self.assertEqual("array", candidates["type"])
        self.assertEqual(1, candidates["minItems"])
        self.assertTrue(candidates["uniqueItems"])
        candidate = candidates["items"]
        self.assertFalse(candidate["additionalProperties"])
        self.assertEqual({"entity_type", "id"}, set(candidate["required"]))

    def test_evidence_set_schema_reuses_evidence_item_schema(self):
        evidence_set_schema = _schema("evidence-set.schema.json")

        self.assertEqual(
            {"object", "request_id", "use_case", "evidence_items", "generated_at"},
            set(evidence_set_schema["required"]),
        )
        self.assertEqual("evidence_set", evidence_set_schema["properties"]["object"]["const"])
        evidence_items = evidence_set_schema["properties"]["evidence_items"]
        self.assertEqual("array", evidence_items["type"])
        self.assertTrue(evidence_items["uniqueItems"])
        self.assertNotIn("minItems", evidence_items)
        self.assertEqual("evidence-item.schema.json", evidence_items["items"]["$ref"])

    def test_result_row_schema_pins_public_provenance_envelope(self):
        result_row_schema = _schema("result-row.schema.json")

        self.assertEqual("result_row", result_row_schema["properties"]["object"]["const"])
        self.assertEqual(
            {
                "object",
                "entity_id",
                "entity_kind",
                "benchmark_id",
                "benchmark_version",
                "harness",
                "harness_version",
                "is_self_reported",
                "n_items",
                "ci95",
                "score_raw",
                "score_unit",
                "date_run",
                "model_version",
                "provenance",
                "source_url",
                "attribution_string",
                "flags",
                "verification_state",
            },
            set(result_row_schema["required"]),
        )
        flags = result_row_schema["properties"]["flags"]
        self.assertFalse(flags["additionalProperties"])
        self.assertEqual(set(RESULT_FLAG_KEYS), set(flags["required"]))
        for key in RESULT_FLAG_KEYS:
            self.assertEqual("boolean", flags["properties"][key]["type"])
        self.assertEqual(0, result_row_schema["properties"]["n_items"]["minimum"])
        self.assertEqual("uri-reference", result_row_schema["properties"]["source_url"]["format"])

    def test_stage_candidate_schema_pins_stage_one_boundary(self):
        stage_candidate_schema = _schema("stage-candidate.schema.json")

        self.assertEqual(
            {"object", "candidate_id", "entity", "fused_score", "rrf_components", "retrieval_provenance"},
            set(stage_candidate_schema["required"]),
        )
        self.assertEqual("stage_candidate", stage_candidate_schema["properties"]["object"]["const"])
        self.assertEqual("^[a-f0-9]{64}$", stage_candidate_schema["properties"]["candidate_id"]["pattern"])
        self.assertFalse(stage_candidate_schema["properties"]["entity"]["additionalProperties"])
        rrf = stage_candidate_schema["properties"]["rrf_components"]
        self.assertEqual({"lexical_rank", "semantic_rank", "graph_rank"}, set(rrf["required"]))
        self.assertFalse(rrf["additionalProperties"])
        self.assertEqual(["integer", "null"], rrf["properties"]["graph_rank"]["type"])
        provenance = stage_candidate_schema["properties"]["retrieval_provenance"]
        self.assertEqual({"arms", "use_case"}, set(provenance["required"]))
        self.assertTrue(provenance["properties"]["arms"]["uniqueItems"])


def _schema(filename: str) -> dict:
    return json.loads((SCHEMAS / filename).read_text(encoding="utf-8"))


def _fingerprint_input() -> CapabilityFingerprintInput:
    return CapabilityFingerprintInput(
        id_scheme="reverse_dns",
        canonical_id="io.evalrank.public-search-demo",
        entity_kind="mcp_server",
        declared_capability_shape={
            "tool_names": ["search"],
            "param_schemas": {"search": {"type": "object"}},
            "declared_scopes": ["web.search"],
            "commit_sha": "abc123",
        },
    )


def _row() -> RankedEntity:
    return RankedEntity(
        entity_type="mcp_server",
        entity_id="tool:exa-search-mcp",
        rank=1,
        capability_score=0.84,
        confidence=0.86,
        ci95=ConfidenceInterval(low=0.80, high=0.88),
        methodology_version="2026-06-25.1.public-fixture-v1",
        trust_tier="standardized",
        freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
        evidence_count=1840,
    )


if __name__ == "__main__":
    unittest.main()
