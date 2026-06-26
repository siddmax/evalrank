import json
import re
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
    PROBLEM_CODES,
    Recommendation,
    RankedEntity,
    RESULT_ENTITY_KINDS,
    RESULT_FLAG_KEYS,
    RESULT_VERIFICATION_STATES,
    THE_CALL_DECISIONS,
    TRUST_TIERS,
    USE_CASE_ENTITY_KINDS,
    USE_CASE_RANK_POLICIES,
)
from evalrank_core.fixtures import (  # noqa: E402
    sample_candidate_set,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_raw_entry,
    sample_result_row,
    sample_scoring_stage_catalog,
    sample_stage_candidate,
    sample_use_case_catalog,
)


METHODOLOGY_VERSION_PATTERN = r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*\.([a-z0-9]+-)*[a-z0-9]+$"

class SchemaContractTests(unittest.TestCase):
    def test_schema_readme_lists_public_schema_files_and_string_guards(self):
        text = (SCHEMAS / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"`([^`]*(?:\.schema\.json|openapi\.json))`", text))
        expected = {path.name for path in SCHEMAS.glob("*.schema.json")} | {"openapi.json"}

        self.assertEqual(expected, documented)
        for filename in sorted(path.name for path in SCHEMAS.glob("*.schema.json")):
            with self.subTest(filename=filename):
                self.assertIn(filename, text)
        self.assertIn("public string fields", text)
        self.assertIn("actual non-empty strings", text)

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
        scoring_stage_catalog_schema = _schema("scoring-stage-catalog.schema.json")
        use_case_catalog_schema = _schema("use-case-catalog.schema.json")

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
        scoring_stage_catalog_payload = sample_scoring_stage_catalog().to_dict()
        self.assertEqual(set(scoring_stage_catalog_payload), set(scoring_stage_catalog_schema["properties"]))
        self.assertLessEqual(set(scoring_stage_catalog_schema["required"]), set(scoring_stage_catalog_payload))
        use_case_catalog_payload = sample_use_case_catalog().to_dict()
        self.assertEqual(set(use_case_catalog_payload), set(use_case_catalog_schema["properties"]))
        self.assertLessEqual(set(use_case_catalog_schema["required"]), set(use_case_catalog_payload))

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
            "scoring-stage-catalog.schema.json",
            "use-case-catalog.schema.json",
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
        use_case_catalog_schema = _schema("use-case-catalog.schema.json")
        use_case_schema = use_case_catalog_schema["$defs"]["UseCase"]
        self.assertEqual(USE_CASE_ENTITY_KINDS, set(use_case_schema["properties"]["entity_kinds"]["items"]["enum"]))
        self.assertEqual(USE_CASE_RANK_POLICIES, set(use_case_schema["properties"]["rank_policy"]["enum"]))

    def test_ranked_entity_schema_pins_score_components_map_shape(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        score_components = ranked_schema["properties"]["score_components"]

        self.assertEqual("object", score_components["type"])
        self.assertEqual({"type": "string", "minLength": 1}, score_components["propertyNames"])
        self.assertEqual(
            {"type": "number", "minimum": 0, "maximum": 1},
            score_components["additionalProperties"],
        )

    def test_ranked_entity_schema_pins_axes_shape(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        axes = ranked_schema["properties"]["axes"]
        evidence = axes["properties"]["evidence"]

        self.assertFalse(axes["additionalProperties"])
        self.assertEqual({"evidence"}, set(axes["required"]))
        self.assertFalse(evidence["additionalProperties"])
        self.assertEqual({"n_items", "coverage"}, set(evidence["required"]))
        self.assertEqual({"type": "integer", "minimum": 0}, evidence["properties"]["n_items"])
        self.assertEqual(TRUST_TIERS, set(evidence["properties"]["coverage"]["enum"]))

    def test_ranked_entity_schema_pins_freshness_date_format(self):
        ranked_schema = _schema("ranked-entity.schema.json")
        freshness = ranked_schema["properties"]["freshness"]["properties"]

        self.assertEqual(r"^\d{4}-\d{2}-\d{2}$", freshness["last_eval"]["pattern"])
        self.assertEqual(r"^\d{4}-\d{2}-\d{2}$", freshness["next_refresh"]["pattern"])

    def test_temporal_schema_fields_pin_public_formats(self):
        timestamp_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        for filename, field_name in (
            ("raw-entry.schema.json", "fetched_at"),
            ("use-case-catalog.schema.json", "generated_at"),
            ("scoring-stage-catalog.schema.json", "generated_at"),
            ("evidence-item.schema.json", "observed_at"),
            ("evidence-set.schema.json", "generated_at"),
            ("evaluation-request.schema.json", "requested_at"),
            ("candidate-set.schema.json", "generated_at"),
            ("recommendation.schema.json", "generated_at"),
        ):
            with self.subTest(filename=filename, field_name=field_name):
                schema = _schema(filename)
                self.assertEqual(timestamp_pattern, schema["properties"][field_name]["pattern"])

        result_row_schema = _schema("result-row.schema.json")
        self.assertEqual(r"^\d{4}-\d{2}-\d{2}$", result_row_schema["properties"]["date_run"]["pattern"])

    def test_ranked_entity_schema_pins_non_empty_caveats(self):
        ranked_schema = _schema("ranked-entity.schema.json")

        self.assertEqual({"type": "string", "minLength": 1}, ranked_schema["properties"]["caveats"]["items"])

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

    def test_capability_fingerprint_schema_requires_declared_capability_shape_content(self):
        fingerprint_schema = _schema("capability-fingerprint.schema.json")

        self.assertEqual(1, fingerprint_schema["properties"]["declared_capability_shape"]["minProperties"])

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

    def test_recommendation_schema_pins_the_call_branch_shapes(self):
        recommendation_schema = _schema("recommendation.schema.json")
        the_call = recommendation_schema["properties"]["the_call"]

        self.assertIn(
            {
                "if": {"properties": {"decision": {"const": "recommend"}}, "required": ["decision"]},
                "then": {
                    "properties": {
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "abstention_reason": {"const": None},
                    }
                },
            },
            the_call["allOf"],
        )
        self.assertIn(
            {
                "if": {"properties": {"decision": {"const": "abstain"}}, "required": ["decision"]},
                "then": {
                    "properties": {
                        "confidence": {"const": None},
                        "abstention_reason": {"type": "string", "minLength": 1},
                    }
                },
            },
            the_call["allOf"],
        )

    def test_recommendation_schema_pins_abstention_shape(self):
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertIn("abstention", recommendation_schema["required"])
        abstention = recommendation_schema["properties"]["abstention"]
        self.assertEqual(["object", "null"], abstention["type"])
        self.assertFalse(abstention["additionalProperties"])
        self.assertEqual({"reason", "detail"}, set(abstention["required"]))
        self.assertEqual("string", abstention["properties"]["reason"]["type"])
        self.assertEqual(1, abstention["properties"]["reason"]["minLength"])
        self.assertEqual("string", abstention["properties"]["detail"]["type"])
        self.assertEqual(1, abstention["properties"]["detail"]["minLength"])

    def test_recommendation_schema_pins_abstention_envelope_consistency(self):
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertIn(
            {
                "if": {
                    "properties": {
                        "the_call": {
                            "type": "object",
                            "properties": {"decision": {"const": "abstain"}},
                            "required": ["decision"],
                        }
                    },
                    "required": ["the_call"],
                },
                "then": {"required": ["abstention"], "properties": {"abstention": {"type": "object"}}},
            },
            recommendation_schema["allOf"],
        )
        self.assertIn(
            {
                "if": {
                    "properties": {
                        "the_call": {
                            "type": "object",
                            "properties": {"decision": {"const": "recommend"}},
                            "required": ["decision"],
                        }
                    },
                    "required": ["the_call"],
                },
                "then": {"required": ["abstention"], "properties": {"abstention": {"const": None}}},
            },
            recommendation_schema["allOf"],
        )
        self.assertIn(
            {
                "if": {"properties": {"abstention": {"type": "object"}}, "required": ["abstention"]},
                "then": {
                    "required": ["the_call"],
                    "properties": {
                        "the_call": {
                            "type": "object",
                            "properties": {"decision": {"const": "abstain"}},
                            "required": ["decision"],
                        }
                    }
                },
            },
            recommendation_schema["allOf"],
        )

    def test_recommendation_schema_pins_abstention_as_empty_single_scale(self):
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertIn(
            {
                "if": {"properties": {"abstention": {"type": "object"}}, "required": ["abstention"]},
                "then": {
                    "properties": {
                        "comparability": {"const": "single-scale"},
                        "shortlist_depth": {"const": 0},
                        "ranked": {"maxItems": 0},
                        "groups": {"const": None},
                    }
                },
            },
            recommendation_schema["allOf"],
        )

    def test_recommendation_schema_reuses_exclusion_schema(self):
        recommendation_schema = _schema("recommendation.schema.json")

        self.assertTrue(recommendation_schema["properties"]["exclusions"]["uniqueItems"])
        self.assertEqual("exclusion.schema.json", recommendation_schema["properties"]["exclusions"]["items"]["$ref"])

    def test_recommendation_schema_pins_ranking_group_shape(self):
        recommendation_schema = _schema("recommendation.schema.json")
        group_schema = recommendation_schema["$defs"]["RankingGroup"]

        self.assertEqual("#/$defs/RankingGroup", recommendation_schema["properties"]["groups"]["items"]["$ref"])
        self.assertFalse(group_schema["additionalProperties"])
        self.assertEqual(
            {"object", "group_key", "entity_type", "ranked", "group_rationale"},
            set(group_schema["required"]),
        )
        self.assertEqual("ranking_group", group_schema["properties"]["object"]["const"])
        self.assertEqual("ranked-entity.schema.json", group_schema["properties"]["ranked"]["items"]["$ref"])
        self.assertEqual(1, group_schema["properties"]["ranked"]["minItems"])
        self.assertTrue(group_schema["properties"]["ranked"]["uniqueItems"])

    def test_recommendation_schema_pins_comparability_branch_shapes(self):
        recommendation_schema = _schema("recommendation.schema.json")
        ranked = recommendation_schema["properties"]["ranked"]

        self.assertEqual("array", ranked["type"])
        self.assertTrue(ranked["uniqueItems"])

        self.assertIn(
            {
                "if": {"properties": {"comparability": {"const": "single-scale"}}, "required": ["comparability"]},
                "then": {"properties": {"groups": {"const": None}}},
            },
            recommendation_schema["allOf"],
        )
        self.assertIn(
            {
                "if": {"properties": {"comparability": {"const": "kind-grouped"}}, "required": ["comparability"]},
                "then": {
                    "properties": {
                        "ranked": {"maxItems": 0},
                        "groups": {"type": "array", "minItems": 1},
                    }
                },
            },
            recommendation_schema["allOf"],
        )

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

    def test_scoring_stage_catalog_schema_pins_stage_shape(self):
        schema = _schema("scoring-stage-catalog.schema.json")
        stage_schema = schema["$defs"]["ScoringStage"]

        self.assertEqual("scoring_stage_catalog", schema["properties"]["object"]["const"])
        self.assertTrue(schema["properties"]["stages"]["uniqueItems"])
        self.assertEqual("ScoringStage", stage_schema["title"])
        self.assertFalse(stage_schema["additionalProperties"])
        self.assertEqual(
            {
                "id",
                "ordinal",
                "name",
                "description",
                "input_contracts",
                "output_contracts",
                "public_boundary",
            },
            set(stage_schema["required"]),
        )
        self.assertEqual(1, stage_schema["properties"]["ordinal"]["minimum"])
        self.assertEqual(1, stage_schema["properties"]["input_contracts"]["minItems"])
        self.assertTrue(stage_schema["properties"]["input_contracts"]["uniqueItems"])
        self.assertEqual(1, stage_schema["properties"]["output_contracts"]["minItems"])
        self.assertTrue(stage_schema["properties"]["output_contracts"]["uniqueItems"])

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

        self.assertEqual(PROBLEM_CODES, set(properties["code"]["enum"]))
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

    def test_evaluation_request_schema_pins_unique_entity_types(self):
        request_schema = _schema("evaluation-request.schema.json")
        entity_types = request_schema["properties"]["entity_types"]

        self.assertEqual("array", entity_types["type"])
        self.assertEqual(1, entity_types["minItems"])
        self.assertTrue(entity_types["uniqueItems"])
        self.assertEqual({"type": "string", "minLength": 1}, entity_types["items"])

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

    def test_use_case_catalog_schema_pins_public_taxonomy_shape(self):
        catalog_schema = _schema("use-case-catalog.schema.json")
        use_case_schema = catalog_schema["$defs"]["UseCase"]

        self.assertEqual("use_case_catalog", catalog_schema["properties"]["object"]["const"])
        self.assertEqual(
            {"object", "methodology_version", "generated_at", "use_cases"},
            set(catalog_schema["required"]),
        )
        self.assertEqual(1, catalog_schema["properties"]["use_cases"]["minItems"])
        self.assertTrue(catalog_schema["properties"]["use_cases"]["uniqueItems"])
        self.assertEqual("#/$defs/UseCase", catalog_schema["properties"]["use_cases"]["items"]["$ref"])
        self.assertEqual("use_case", use_case_schema["properties"]["object"]["const"])
        self.assertEqual(
            {"object", "id", "name", "definition", "entity_kinds", "rank_policy", "is_overlay"},
            set(use_case_schema["required"]),
        )
        self.assertFalse(use_case_schema["additionalProperties"])
        self.assertTrue(use_case_schema["properties"]["entity_kinds"]["uniqueItems"])
        self.assertEqual(1, use_case_schema["properties"]["entity_kinds"]["minItems"])
        self.assertEqual(
            [
                {
                    "if": {"properties": {"is_overlay": {"const": True}}, "required": ["is_overlay"]},
                    "then": {"properties": {"rank_policy": {"const": "veto_overlay"}}},
                },
                {
                    "if": {"properties": {"is_overlay": {"const": False}}, "required": ["is_overlay"]},
                    "then": {"properties": {"rank_policy": {"const": "ranked"}}},
                },
            ],
            use_case_schema["allOf"],
        )


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
