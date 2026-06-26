import json
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_TS = REPO_ROOT / "packages" / "sdk-ts"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.contracts import (  # noqa: E402
    EVIDENCE_KINDS,
    RESULT_ENTITY_KINDS,
    RESULT_FLAG_KEYS,
    RESULT_VERIFICATION_STATES,
    THE_CALL_DECISIONS,
    TRUST_TIERS,
    USE_CASE_ENTITY_KINDS,
    USE_CASE_RANK_POLICIES,
)
from evalrank_core.fixtures import PUBLIC_FIXTURE_KINDS  # noqa: E402

PROBLEM_CODES = {
    "rate_limited",
    "upstream_timeout",
    "validation",
    "not_found",
    "methodology_stale",
    "internal",
    "unauthorized",
    "forbidden",
}


class TypeScriptSdkTests(unittest.TestCase):
    def test_sdk_readme_lists_public_typescript_surface(self):
        text = (SDK_TS / "README.md").read_text(encoding="utf-8")

        for name in (
            "Abstention",
            "CapabilityFingerprint",
            "RawEntry",
            "EntityRef",
            "EvaluationRequest",
            "CandidateSet",
            "StageCandidate",
            "EvidenceItem",
            "EvidenceSet",
            "ResultRow",
            "ScoringStage",
            "ScoringStageCatalog",
            "UseCase",
            "UseCaseCatalog",
            "RankingGroup",
            "Exclusion",
            "TheCall",
            "RankedEntity",
            "Recommendation",
            "ProblemDetails",
            "EvalRankClient",
            "EvalRankApiError",
            "PUBLIC_FIXTURE_KINDS",
            "PublicFixtureKind",
        ):
            self.assertIn(name, text)

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
        self.assertEqual("node --experimental-strip-types --check src/index.ts", package["scripts"]["check"])
        self.assertEqual("node --experimental-strip-types --test src/index.test.ts", package["scripts"]["test"])

    def test_public_constants_match_core_contracts(self):
        source = (SDK_TS / "src" / "index.ts").read_text(encoding="utf-8")

        self.assertEqual(TRUST_TIERS, _exported_string_array(source, "TRUST_TIERS"))
        self.assertEqual(EVIDENCE_KINDS, _exported_string_array(source, "EVIDENCE_KINDS"))
        self.assertEqual(THE_CALL_DECISIONS, _exported_string_array(source, "THE_CALL_DECISIONS"))
        self.assertEqual(PROBLEM_CODES, _exported_string_array(source, "PROBLEM_CODES"))
        self.assertEqual(RESULT_ENTITY_KINDS, _exported_string_array(source, "RESULT_ENTITY_KINDS"))
        self.assertEqual(set(RESULT_FLAG_KEYS), _exported_string_array(source, "RESULT_FLAG_KEYS"))
        self.assertEqual(
            RESULT_VERIFICATION_STATES,
            _exported_string_array(source, "RESULT_VERIFICATION_STATES"),
        )
        self.assertEqual(USE_CASE_ENTITY_KINDS, _exported_string_array(source, "USE_CASE_ENTITY_KINDS"))
        self.assertEqual(USE_CASE_RANK_POLICIES, _exported_string_array(source, "USE_CASE_RANK_POLICIES"))
        self.assertEqual(set(PUBLIC_FIXTURE_KINDS), _exported_string_array(source, "PUBLIC_FIXTURE_KINDS"))

    def test_public_interfaces_cover_schema_payloads(self):
        source = (SDK_TS / "src" / "index.ts").read_text(encoding="utf-8")

        for name in (
            "Abstention",
            "CandidateSet",
            "CapabilityFingerprint",
            "EntityRef",
            "Exclusion",
            "EvidenceSet",
            "EvaluationRequest",
            "EvidenceItem",
            "RankedEntity",
            "RankingGroup",
            "RawEntry",
            "Recommendation",
            "ResultRow",
            "ScoringStage",
            "ScoringStageCatalog",
            "StageCandidate",
            "TheCall",
            "ProblemDetails",
            "UseCase",
            "UseCaseCatalog",
        ):
            self.assertIn(f"export interface {name}", source)

        self.assertIn("export class EvalRankApiError extends Error", source)
        self.assertIn("export class EvalRankClient", source)
        self.assertIn("async recommend(request: EvaluationRequest): Promise<Recommendation>", source)
        self.assertIn("/v1/recommendations", source)

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
            "benchmark_id",
            "benchmark_version",
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
            "harness_version",
            "is_self_reported",
            "score_raw",
            "score_unit",
            "date_run",
            "model_version",
            "provenance",
            "source_url",
            "attribution_string",
            "verification_state",
            "recommendation_id",
            "group_key",
            "group_rationale",
            "recommend_id",
            "search_run_id",
            "rrf_components",
            "retrieval_provenance",
            "abstention",
            "abstention_reason",
            "retry_after",
            "request_id",
            "doc_url",
            "entity_kinds",
            "rank_policy",
            "is_overlay",
            "use_cases",
            "input_contracts",
            "output_contracts",
            "public_boundary",
            "stages",
        ):
            self.assertRegex(source, rf"\b{field}\??:")

        self.assertIn("the_call: TheCall | null;", source)
        self.assertIn("abstention: Abstention | null;", source)
        self.assertIn("exclusions: Exclusion[];", source)
        self.assertIn("groups: RankingGroup[] | null;", source)
        self.assertIn("export type ProblemCode = (typeof PROBLEM_CODES)[number];", source)
        self.assertIn("export type PublicFixtureKind = (typeof PUBLIC_FIXTURE_KINDS)[number];", source)
        self.assertIn("export type ResultEntityKind = (typeof RESULT_ENTITY_KINDS)[number];", source)
        self.assertIn("export type ResultVerificationState = (typeof RESULT_VERIFICATION_STATES)[number];", source)
        self.assertIn("export type UseCaseEntityKind = (typeof USE_CASE_ENTITY_KINDS)[number];", source)
        self.assertIn("export type UseCaseRankPolicy = (typeof USE_CASE_RANK_POLICIES)[number];", source)
        self.assertIn("code?: ProblemCode;", source)
        self.assertIn("retriable?: boolean;", source)
        self.assertIn("[key: string]: unknown;", source)
        self.assertIn("entity_kind: ResultEntityKind;", source)
        self.assertIn("verification_state: ResultVerificationState;", source)
        self.assertIn("entity_kinds: UseCaseEntityKind[];", source)
        self.assertIn("rank_policy: UseCaseRankPolicy;", source)


def _exported_string_array(source: str, name: str) -> set[str]:
    match = re.search(rf"export const {name} = \[(?P<body>.*?)\] as const;", source, re.S)
    if not match:
        raise AssertionError(f"{name} export not found")
    return set(re.findall(r'"([^"]+)"', match.group("body")))


if __name__ == "__main__":
    unittest.main()
