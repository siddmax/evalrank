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
    THE_CALL_DECISIONS,
    TRUST_TIERS,
    USE_CASE_ENTITY_KINDS,
    USE_CASE_RANK_POLICIES,
)
from evalrank_core.fixtures import PUBLIC_FIXTURE_KINDS  # noqa: E402

PROBLEM_CODES = {
    "invalid_evaluation_request",
    "recommendation_not_published",
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
    def test_legacy_result_row_vocabulary_is_deleted(self):
        source = (SDK_TS / "src" / "index.ts").read_text(encoding="utf-8")
        self.assertNotIn("ResultRow", source)
        self.assertNotIn("result-row", source)
        self.assertNotIn("RESULT_ENTITY_KINDS", source)

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
            "ObservationV1",
            "ScoringStage",
            "ScoringStageCatalog",
            "UseCase",
            "UseCaseCatalog",
            "RankingGroup",
            "Exclusion",
            "TheCall",
            "RankedEntity",
            "RecommendationCallState",
            "Recommendation",
            "ProblemDetails",
            "EvalRankClient",
            "EvalRankApiError",
            "PUBLIC_FIXTURE_KINDS",
            "PublicFixtureKind",
            "NonEmptyArray",
            "AggregationInputDocument",
            "BootstrapSeedDocument",
            "RankingGroupIdentity",
            "aggregationInputDocument",
            "bootstrapSeedDocument",
            "deriveAggregationInputDigest",
            "deriveBootstrapSeed",
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
        self.assertEqual(
            "node --experimental-strip-types --check src/index.ts && "
            "node --experimental-strip-types --check src/decision-contracts.ts && "
            "node --experimental-strip-types --check src/aggregation-identity.ts",
            package["scripts"]["check"],
        )
        self.assertEqual(
            "node --experimental-strip-types --test src/index.test.ts src/decision-contracts.test.ts",
            package["scripts"]["test"],
        )

    def test_public_constants_match_core_contracts(self):
        source = (SDK_TS / "src" / "index.ts").read_text(encoding="utf-8")
        self.assertIn('export * from "./decision-contracts.ts";', source)
        self.assertIn('export * from "./aggregation-identity.ts";', source)

        self.assertEqual(TRUST_TIERS, _exported_string_array(source, "TRUST_TIERS"))
        self.assertEqual(EVIDENCE_KINDS, _exported_string_array(source, "EVIDENCE_KINDS"))
        self.assertEqual(THE_CALL_DECISIONS, _exported_string_array(source, "THE_CALL_DECISIONS"))
        self.assertEqual(PROBLEM_CODES, _exported_string_array(source, "PROBLEM_CODES"))
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
            "ScoringStage",
            "ScoringStageCatalog",
            "StageCandidate",
            "ProblemDetails",
            "UseCaseCatalog",
        ):
            self.assertIn(f"export interface {name}", source)

        self.assertIn("export interface UseCaseBase", source)
        self.assertIn("export interface RankedUseCase extends UseCaseBase", source)
        self.assertIn("export interface OverlayUseCase extends UseCaseBase", source)
        self.assertIn("export type UseCase = RankedUseCase | OverlayUseCase;", source)
        self.assertIn("export interface RecommendCall", source)
        self.assertIn("export interface AbstainCall", source)
        self.assertIn("export type TheCall = RecommendCall | AbstainCall;", source)
        self.assertIn("export interface RecommendationBase", source)
        self.assertIn("export interface RecommendationWithoutCall", source)
        self.assertIn("export interface RecommendationWithRecommendCall", source)
        self.assertIn("export interface RecommendationWithAbstainCall", source)
        self.assertIn(
            "export type RecommendationCallState =\n"
            "  | RecommendationWithoutCall\n"
            "  | RecommendationWithRecommendCall\n"
            "  | RecommendationWithAbstainCall;",
            source,
        )
        self.assertIn("export interface EmptySingleScaleAbstentionRecommendation", source)
        self.assertIn("export interface SingleScaleRecommendationBase extends RecommendationBase", source)
        self.assertIn("export interface KindGroupedRecommendationBase extends RecommendationBase", source)
        self.assertIn(
            "export type SingleScaleRecommendation =\n"
            "  | (SingleScaleRecommendationBase & (RecommendationWithoutCall | RecommendationWithRecommendCall))\n"
            "  | EmptySingleScaleAbstentionRecommendation;",
            source,
        )
        self.assertIn(
            "export type KindGroupedRecommendation = KindGroupedRecommendationBase &\n"
            "  (RecommendationWithoutCall | RecommendationWithRecommendCall);",
            source,
        )
        self.assertIn("export type Recommendation = SingleScaleRecommendation | KindGroupedRecommendation;", source)
        self.assertIn("export class EvalRankApiError extends Error", source)
        self.assertIn("export class EvalRankClient", source)
        self.assertIn("async useCases(): Promise<UseCaseCatalog>", source)
        self.assertIn("async scoringStages(): Promise<ScoringStageCatalog>", source)
        self.assertIn("async recommend(request: EvaluationRequest): Promise<Recommendation>", source)
        self.assertIn("/v1/use-cases", source)
        self.assertIn("/v1/scoring-stages", source)
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
            "group_key",
            "group_rationale",
            "recommend_id",
            "search_run_id",
            "rrf_components",
            "retrieval_provenance",
            "abstention",
            "abstention_reason",
            "axes",
            "coverage",
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

        self.assertIn("the_call: null;", source)
        self.assertIn("the_call: RecommendCall;", source)
        self.assertIn("the_call: AbstainCall;", source)
        self.assertIn("abstention: null;", source)
        self.assertIn("abstention: Abstention;", source)
        self.assertIn("shortlist_depth: 0;", source)
        self.assertIn("ranked: [];", source)
        self.assertIn("groups: null;", source)
        self.assertIn("exclusions: Exclusion[];", source)
        self.assertIn("export type ProblemCode = (typeof PROBLEM_CODES)[number];", source)
        self.assertIn("export type PublicFixtureKind = (typeof PUBLIC_FIXTURE_KINDS)[number];", source)
        self.assertIn("export type UseCaseEntityKind = (typeof USE_CASE_ENTITY_KINDS)[number];", source)
        self.assertIn("export type UseCaseRankPolicy = (typeof USE_CASE_RANK_POLICIES)[number];", source)
        self.assertIn("export type NonEmptyArray<T> = [T, ...T[]];", source)
        self.assertIn('decision: "recommend";', source)
        self.assertIn("confidence: number;", source)
        self.assertIn("abstention_reason: null;", source)
        self.assertIn('decision: "abstain";', source)
        self.assertIn("confidence: null;", source)
        self.assertIn("abstention_reason: string;", source)
        self.assertIn('comparability: "single-scale";', source)
        self.assertIn("ranked: RankedEntity[];", source)
        self.assertIn("groups: null;", source)
        self.assertIn('comparability: "kind-grouped";', source)
        self.assertIn("ranked: [];", source)
        self.assertIn("groups: NonEmptyArray<RankingGroup>;", source)
        self.assertIn("code?: ProblemCode;", source)
        self.assertIn("retriable?: boolean;", source)
        self.assertIn("[key: string]: unknown;", source)
        self.assertIn("coverage: TrustTier;", source)
        self.assertIn("entity_types: NonEmptyArray<string>;", source)
        self.assertIn("candidates: NonEmptyArray<EntityRef>;", source)
        self.assertIn("arms: NonEmptyArray<string>;", source)
        self.assertIn("entity_kinds: NonEmptyArray<UseCaseEntityKind>;", source)
        self.assertIn("use_cases: NonEmptyArray<UseCase>;", source)
        self.assertIn("input_contracts: NonEmptyArray<string>;", source)
        self.assertIn("output_contracts: NonEmptyArray<string>;", source)
        self.assertIn("stages: NonEmptyArray<ScoringStage>;", source)
        self.assertIn("ranked: NonEmptyArray<RankedEntity>;", source)
        self.assertIn('rank_policy: "ranked";', source)
        self.assertIn("is_overlay: false;", source)
        self.assertIn('rank_policy: "veto_overlay";', source)
        self.assertIn("is_overlay: true;", source)


def _exported_string_array(source: str, name: str) -> set[str]:
    match = re.search(rf"export const {name} = \[(?P<body>.*?)\] as const;", source, re.S)
    if not match:
        raise AssertionError(f"{name} export not found")
    return set(re.findall(r'"([^"]+)"', match.group("body")))


if __name__ == "__main__":
    unittest.main()
