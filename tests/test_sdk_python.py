import json
import sys
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_SRC = REPO_ROOT / "packages" / "sdk-python" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(SDK_SRC))

from evalrank_core import contracts as core_contracts  # noqa: E402
from evalrank_core.contracts import CapabilityFingerprintInput as CoreCapabilityFingerprintInput  # noqa: E402
from evalrank_core.contracts import CandidateSet as CoreCandidateSet  # noqa: E402
from evalrank_core.contracts import Exclusion as CoreExclusion  # noqa: E402
from evalrank_core.contracts import EvidenceItem as CoreEvidenceItem  # noqa: E402
from evalrank_core.contracts import EvidenceSet as CoreEvidenceSet  # noqa: E402
from evalrank_core.contracts import EvaluationRequest as CoreEvaluationRequest  # noqa: E402
from evalrank_core.contracts import ProblemDetails as CoreProblemDetails  # noqa: E402
from evalrank_core.contracts import RawEntry as CoreRawEntry  # noqa: E402
from evalrank_core.contracts import RankingGroup as CoreRankingGroup  # noqa: E402
from evalrank_core.decision_contracts import ObservationV1 as CoreObservationV1  # noqa: E402
from evalrank_core.contracts import ScoringStage as CoreScoringStage  # noqa: E402
from evalrank_core.contracts import ScoringStageCatalog as CoreScoringStageCatalog  # noqa: E402
from evalrank_core.contracts import StageCandidate as CoreStageCandidate  # noqa: E402
from evalrank_core.contracts import TheCall as CoreTheCall  # noqa: E402
from evalrank_core.contracts import UseCaseCatalog as CoreUseCaseCatalog  # noqa: E402
from evalrank_core.fixtures import PUBLIC_FIXTURE_KINDS as CorePublicFixtureKinds  # noqa: E402
from evalrank_core.fixtures import sample_public_fixture as core_sample_public_fixture  # noqa: E402
from evalrank_core.fixtures import sample_problem_details as core_sample_problem_details  # noqa: E402
from evalrank_sdk import (  # noqa: E402
    CapabilityFingerprintInput,
    CandidateSet,
    EvalRankApiError,
    EvalRankClient,
    Exclusion,
    EvaluationRequest,
    EvidenceItem,
    EvidenceSet,
    ObservationV1,
    ProblemDetails,
    RawEntry,
    RankingGroup,
    ScoringStage,
    ScoringStageCatalog,
    StageCandidate,
    TheCall,
    UseCaseCatalog,
    PUBLIC_FIXTURE_KINDS,
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_observation,
    sample_public_fixture,
    sample_problem_details,
    sample_raw_entry,
    sample_recommendation,
    sample_ranking_group,
    sample_scoring_stage_catalog,
    sample_stage_candidate,
    sample_use_case_catalog,
)

def _manifest_use_cases() -> list[dict]:
    cells = json.loads((REPO_ROOT / "catalog" / "manifest.json").read_text(encoding="utf-8"))["cells"]
    return [
        {
            "object": "use_case",
            "id": cell["cell_id"],
            "name": cell["name"],
            "definition": cell["definition"],
            "entity_kinds": cell["entity_kinds"],
            "rank_policy": "ranked",
            "is_overlay": False,
        }
        for cell in cells
    ]


class PythonSdkTests(unittest.TestCase):
    def test_sdk_re_exports_monthly_schedule_pricing_contracts(self):
        import evalrank_core  # noqa: PLC0415
        import evalrank_sdk  # noqa: PLC0415

        for name in (
            "CacheWriteRateV1",
            "CacheWriteUsageV1",
            "PricingScheduleFactV1",
            "UsageProfileV1",
            "monthly_cost_microusd",
        ):
            with self.subTest(name=name):
                self.assertTrue(hasattr(evalrank_core, name))
                self.assertIs(getattr(evalrank_sdk, name), getattr(evalrank_core, name))
        self.assertFalse(hasattr(evalrank_core, "PricingFactV1"))
        self.assertFalse(hasattr(evalrank_sdk, "PricingFactV1"))

    def test_sdk_re_exports_aggregation_identity_contract(self):
        import evalrank_core  # noqa: PLC0415
        import evalrank_sdk  # noqa: PLC0415

        for name in (
            "aggregation_input_document",
            "bootstrap_seed_document",
            "derive_aggregation_input_digest",
            "derive_bootstrap_seed",
        ):
            with self.subTest(name=name):
                self.assertTrue(hasattr(evalrank_core, name))
                self.assertIs(getattr(evalrank_sdk, name), getattr(evalrank_core, name))

    def test_sdk_readme_lists_public_reexport_surface(self):
        text = (REPO_ROOT / "packages" / "sdk-python" / "README.md").read_text(encoding="utf-8")

        for name in (
            "Abstention",
            "COMPARABILITY_MODES",
            "EVIDENCE_KINDS",
            "FRESHNESS_STATUSES",
            "CapabilityFingerprintInput",
            "RawEntry",
            "EvaluationRequest",
            "CandidateSet",
            "StageCandidate",
            "EvidenceItem",
            "EvidenceSet",
            "ObservationV1",
            "UseCaseCatalog",
            "ScoringStage",
            "ScoringStageCatalog",
            "RankingGroup",
            "Exclusion",
            "TheCall",
            "TRUST_TIERS",
            "RankedEntity",
            "Recommendation",
            "ProblemDetails",
            "PROBLEM_CODES",
            "EntityRef",
            "EvalRankClient",
            "EvalRankApiError",
            "PUBLIC_FIXTURE_KINDS",
            "sample_public_fixture",
            "aggregation_input_document",
            "bootstrap_seed_document",
            "derive_aggregation_input_digest",
            "derive_bootstrap_seed",
        ):
            self.assertIn(name, text)

    def test_sdk_re_exports_public_fixture_dispatch(self):
        self.assertIs(PUBLIC_FIXTURE_KINDS, CorePublicFixtureKinds)
        self.assertIs(sample_public_fixture, core_sample_public_fixture)
        self.assertEqual("recommendation", sample_public_fixture("recommendation")["object"])

    def test_sdk_re_exports_public_problem_fixture(self):
        self.assertIs(sample_problem_details, core_sample_problem_details)
        self.assertEqual("validation", sample_problem_details().to_dict()["code"])

    def test_sdk_re_exports_public_vocabulary_constants(self):
        import evalrank_sdk  # noqa: PLC0415

        for name in (
            "COMPARABILITY_MODES",
            "EVIDENCE_KINDS",
            "FRESHNESS_STATUSES",
            "PROBLEM_CODES",
            "TRUST_TIERS",
        ):
            with self.subTest(name=name):
                self.assertIs(getattr(evalrank_sdk, name), getattr(core_contracts, name))

    def test_sdk_re_exports_core_abstention_contract(self):
        self.assertTrue(hasattr(core_contracts, "Abstention"))
        import evalrank_sdk  # noqa: PLC0415

        self.assertTrue(hasattr(evalrank_sdk, "Abstention"))
        self.assertIs(evalrank_sdk.Abstention, core_contracts.Abstention)

    def test_sdk_re_exports_core_capability_fingerprint_contracts(self):
        fingerprint_input = sample_capability_fingerprint_input()

        self.assertIs(CapabilityFingerprintInput, CoreCapabilityFingerprintInput)
        self.assertIsInstance(fingerprint_input, CoreCapabilityFingerprintInput)
        self.assertEqual(64, len(fingerprint_input.to_dict()["capability_fingerprint"]))

    def test_sdk_re_exports_core_evidence_contracts(self):
        evidence = sample_evidence_item()

        self.assertIs(EvidenceItem, CoreEvidenceItem)
        self.assertIsInstance(evidence, CoreEvidenceItem)
        self.assertRegex(evidence.to_dict()["subject"]["id"], r"^config_[0-9a-f]{64}$")

    def test_sdk_re_exports_core_request_contracts(self):
        request = sample_evaluation_request()

        self.assertIs(EvaluationRequest, CoreEvaluationRequest)
        self.assertIsInstance(request, CoreEvaluationRequest)
        self.assertEqual("web-browsing", request.to_dict()["use_case"])

    def test_sdk_re_exports_core_problem_details_contract(self):
        problem = ProblemDetails(
            type="about:blank",
            title="Validation failed",
            status=422,
            detail="request_id is required",
            code="validation",
        )

        self.assertIs(ProblemDetails, CoreProblemDetails)
        self.assertEqual("validation", problem.to_dict()["code"])

    def test_sdk_re_exports_core_candidate_set_contracts(self):
        candidate_set = sample_candidate_set()

        self.assertIs(CandidateSet, CoreCandidateSet)
        self.assertIsInstance(candidate_set, CoreCandidateSet)
        self.assertRegex(candidate_set.to_dict()["candidates"][0]["id"], r"^config_[0-9a-f]{64}$")

    def test_sdk_re_exports_core_exclusion_contracts(self):
        exclusion = sample_exclusion()

        self.assertIs(Exclusion, CoreExclusion)
        self.assertIsInstance(exclusion, CoreExclusion)
        self.assertEqual("unknown_cost", exclusion.to_dict()["reason"])

    def test_sdk_re_exports_core_evidence_set_contracts(self):
        evidence_set = sample_evidence_set()

        self.assertIs(EvidenceSet, CoreEvidenceSet)
        self.assertIsInstance(evidence_set, CoreEvidenceSet)
        self.assertEqual("ev_public_trace_01", evidence_set.to_dict()["evidence_items"][0]["evidence_id"])

    def test_sdk_re_exports_core_raw_entry_contracts(self):
        entry = sample_raw_entry()

        self.assertIs(RawEntry, CoreRawEntry)
        self.assertIsInstance(entry, CoreRawEntry)
        self.assertEqual("raw_entry", entry.to_dict()["object"])

    def test_sdk_re_exports_typed_observation_contract(self):
        observation = sample_observation()

        self.assertIs(ObservationV1, CoreObservationV1)
        self.assertIsInstance(observation, CoreObservationV1)
        self.assertEqual("observation", observation.to_dict()["object"])

    def test_sdk_re_exports_core_ranking_group_contracts(self):
        group = sample_ranking_group()

        self.assertIs(RankingGroup, CoreRankingGroup)
        self.assertIsInstance(group, CoreRankingGroup)
        self.assertEqual("ranking_group", group.to_dict()["object"])

    def test_sdk_re_exports_core_scoring_stage_catalog_contracts(self):
        catalog = sample_scoring_stage_catalog()

        self.assertIs(ScoringStage, CoreScoringStage)
        self.assertIs(ScoringStageCatalog, CoreScoringStageCatalog)
        self.assertIsInstance(catalog, CoreScoringStageCatalog)
        self.assertEqual("scoring_stage_catalog", catalog.to_dict()["object"])
        self.assertEqual(6, len(catalog.to_dict()["stages"]))

    def test_sdk_re_exports_core_stage_candidate_contracts(self):
        candidate = sample_stage_candidate()

        self.assertIs(StageCandidate, CoreStageCandidate)
        self.assertIsInstance(candidate, CoreStageCandidate)
        self.assertEqual("stage_candidate", candidate.to_dict()["object"])

    def test_sdk_re_exports_core_the_call_contract(self):
        self.assertIs(TheCall, CoreTheCall)
        self.assertEqual("recommend", TheCall.recommend(confidence=0.86, reason="clear top set").decision)

    def test_sdk_re_exports_core_use_case_catalog_contracts(self):
        catalog = sample_use_case_catalog()

        self.assertIs(UseCaseCatalog, CoreUseCaseCatalog)
        self.assertIsInstance(catalog, CoreUseCaseCatalog)
        self.assertEqual("use_case_catalog", catalog.to_dict()["object"])
        self.assertEqual(26, len(catalog.to_dict()["use_cases"]))
        self.assertEqual(
            "computational-research-reproduction",
            catalog.to_dict()["use_cases"][-1]["id"],
        )
        self.assertTrue(all(row["rank_policy"] == "ranked" for row in catalog.to_dict()["use_cases"]))
        self.assertEqual(_manifest_use_cases(), catalog.to_dict()["use_cases"])

    def test_recommend_posts_public_request_and_returns_recommendation_json(self):
        server = _SdkTestServer(response_status=200, response_body=sample_recommendation().to_dict())
        try:
            response = EvalRankClient(server.base_url).recommend(sample_evaluation_request())
        finally:
            server.close()

        self.assertEqual("recommendation", response["object"])
        self.assertEqual("/v1/recommendations", server.path)
        self.assertEqual("application/json", server.headers["Content-Type"])
        self.assertEqual("application/json, application/problem+json", server.headers["Accept"])
        self.assertEqual(sample_evaluation_request().to_dict(), server.request_json)

    def test_recommend_raises_public_problem_details_error(self):
        problem = {**core_sample_problem_details().to_dict(), "status": 429}
        server = _SdkTestServer(
            response_status=429,
            response_body=problem,
            response_headers={"Content-Type": "application/problem+json", "Retry-After": "3"},
        )
        try:
            with self.assertRaises(EvalRankApiError) as raised:
                EvalRankClient(server.base_url).recommend(sample_evaluation_request())
        finally:
            server.close()

        self.assertEqual(429, raised.exception.status)
        self.assertIsInstance(raised.exception.problem, CoreProblemDetails)
        self.assertEqual(problem, raised.exception.problem.to_dict())
        self.assertEqual(3, raised.exception.retry_after)

    def test_recommend_treats_malformed_retry_after_as_absent(self):
        problem = {**core_sample_problem_details().to_dict(), "status": 429}
        server = _SdkTestServer(
            response_status=429,
            response_body=problem,
            response_headers={"Content-Type": "application/problem+json", "Retry-After": "3 seconds"},
        )
        try:
            with self.assertRaises(EvalRankApiError) as raised:
                EvalRankClient(server.base_url).recommend(sample_evaluation_request())
        finally:
            server.close()

        self.assertEqual(429, raised.exception.status)
        self.assertEqual(problem, raised.exception.problem.to_dict())
        self.assertIsNone(raised.exception.retry_after)

    def test_use_cases_gets_public_catalog_json(self):
        server = _SdkTestServer(response_status=200, response_body=sample_use_case_catalog().to_dict())
        try:
            response = EvalRankClient(server.base_url).use_cases()
        finally:
            server.close()

        self.assertEqual("use_case_catalog", response["object"])
        self.assertEqual("/v1/use-cases", server.path)
        self.assertEqual("application/json, application/problem+json", server.headers["Accept"])
        self.assertIsNone(server.request_json)

    def test_scoring_stages_gets_public_catalog_json(self):
        server = _SdkTestServer(response_status=200, response_body=sample_scoring_stage_catalog().to_dict())
        try:
            response = EvalRankClient(server.base_url).scoring_stages()
        finally:
            server.close()

        self.assertEqual("scoring_stage_catalog", response["object"])
        self.assertEqual("/v1/scoring-stages", server.path)
        self.assertEqual("application/json, application/problem+json", server.headers["Accept"])
        self.assertIsNone(server.request_json)

    def test_metadata_route_raises_public_problem_details_error(self):
        problem = {**core_sample_problem_details().to_dict(), "status": 503}
        server = _SdkTestServer(
            response_status=503,
            response_body=problem,
            response_headers={"Content-Type": "application/problem+json", "Retry-After": "5"},
        )
        try:
            with self.assertRaises(EvalRankApiError) as raised:
                EvalRankClient(server.base_url).use_cases()
        finally:
            server.close()

        self.assertEqual(503, raised.exception.status)
        self.assertEqual(problem, raised.exception.problem.to_dict())
        self.assertEqual(5, raised.exception.retry_after)

    def test_client_preserves_unknown_problem_extensions_and_rejects_malformed_known_fields(self):
        problem = {
            **core_sample_problem_details().to_dict(),
            "status": 429,
            "provider_window": {"limit": 100, "seconds": 60},
        }
        server = _SdkTestServer(response_status=429, response_body=problem)
        try:
            with self.assertRaises(EvalRankApiError) as raised:
                EvalRankClient(server.base_url).use_cases()
        finally:
            server.close()
        self.assertEqual(problem, raised.exception.problem.to_dict())

        mismatched = {**problem, "status": 503}
        server = _SdkTestServer(response_status=429, response_body=mismatched)
        try:
            with self.assertRaisesRegex(ValueError, "status does not match"):
                EvalRankClient(server.base_url).use_cases()
        finally:
            server.close()

        malformed = {**problem, "status": "429"}
        server = _SdkTestServer(response_status=429, response_body=malformed)
        try:
            with self.assertRaisesRegex(ValueError, "Problem Details"):
                EvalRankClient(server.base_url).use_cases()
        finally:
            server.close()

    def test_client_rejects_non_http_base_url(self):
        with self.assertRaisesRegex(ValueError, "base_url must be an http or https URL"):
            EvalRankClient("file:///tmp/evalrank").recommend(sample_evaluation_request())


class _SdkTestServer:
    def __init__(
        self,
        *,
        response_status: int,
        response_body: dict,
        response_headers: dict[str, str] | None = None,
    ) -> None:
        self.request_json: dict | None = None
        self.headers: dict[str, str] = {}
        self.path = ""

        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                owner.path = self.path
                owner.headers = {key: self.headers[key] for key in self.headers}
                body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
                owner.request_json = json.loads(body.decode("utf-8"))
                self._write_json()

            def do_GET(self) -> None:
                owner.path = self.path
                owner.headers = {key: self.headers[key] for key in self.headers}
                owner.request_json = None
                self._write_json()

            def _write_json(self) -> None:
                encoded = json.dumps(response_body).encode("utf-8")
                self.send_response(response_status)
                for key, value in (response_headers or {"Content-Type": "application/json"}).items():
                    self.send_header(key, value)
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, format: str, *args: object) -> None:
                return

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self._thread = Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        host, port = self._server.server_address
        self.base_url = f"http://{host}:{port}"

    def close(self) -> None:
        self._server.shutdown()
        self._thread.join(timeout=5)
        self._server.server_close()


if __name__ == "__main__":
    unittest.main()
