import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from evalrank_core import (
    AdapterMetadataV1,
    Abstention,
    AvailabilityFactV1,
    CacheWriteRateV1,
    CacheWriteUsageV1,
    CapabilityFingerprintInput,
    CandidateSet,
    ConfigurationPassportV1,
    ContextFactV1,
    ContinuousMetricV1,
    COMPARABILITY_MODES,
    ConfidenceInterval,
    EntityRef,
    EvaluatedConfigurationV1,
    EvaluationToOfferLinkV1,
    EVIDENCE_KINDS,
    Exclusion,
    EvidenceItem,
    EvidenceSet,
    EvaluationRequest,
    FRESHNESS_STATUSES,
    Freshness,
    IntervalUncertaintyV1,
    MAX_SAFE_INTEGER,
    ObservationV1,
    PairwisePreferenceMetricV1,
    PassAtKMetricV1,
    PricingScheduleFactV1,
    PROBLEM_CODES,
    ProblemDetails,
    ProportionMetricV1,
    PublicationSnapshotRefV1,
    RankOnlyMetricV1,
    RawEntry,
    Recommendation,
    RankedEntity,
    RankingGroup,
    RankingGroupSnapshotRefV1,
    RunProvenanceV1,
    PUBLIC_FIXTURE_KINDS,
    ScoringStage,
    ScoringStageCatalog,
    ServingOfferV1,
    SourceArtifactV1,
    SnapshotSetDescriptorV1,
    StandardErrorUncertaintyV1,
    StageCandidate,
    THE_CALL_DECISIONS,
    TheCall,
    TrialPolicyV1,
    TRUST_TIERS,
    USE_CASE_ENTITY_KINDS,
    USE_CASE_RANK_POLICIES,
    UseCase,
    UseCaseCatalog,
    UnknownUncertaintyV1,
    UsageProfileV1,
    DecisionEvidenceV1,
    DecisionExclusionV1,
    DecisionFreshnessV1,
    DecisionQueryV1,
    DecisionReasonV1,
    DecisionReceiptV1,
    DecisionSelectionV1,
    DecisionSensitivityV1,
    aggregation_input_document,
    bootstrap_seed_document,
    canonical_json,
    derive_aggregation_input_digest,
    derive_bootstrap_seed,
    monthly_cost_microusd,
    restricted_jcs,
    sha256_hex,
    verify_leaderboard_snapshot_set,
    verify_leaderboard_semantics,
    verify_entity_detail_semantics,
    verify_compare_result_semantics,
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_entity_ref,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_observation,
    sample_problem_details,
    sample_public_fixture,
    sample_ranked_entity,
    sample_ranking_group,
    sample_raw_entry,
    sample_recommendation,
    sample_scoring_stage_catalog,
    sample_stage_candidate,
    sample_use_case_catalog,
)

__version__ = "0.0.0"


class EvalRankApiError(Exception):
    def __init__(self, *, status: int, problem: ProblemDetails, retry_after: int | None = None) -> None:
        self.status = status
        self.problem = problem
        self.retry_after = retry_after
        super().__init__(f"EvalRank API error {status}: {problem.title}")


class EvalRankClient:
    def __init__(self, base_url: str, *, timeout: float | None = None) -> None:
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an http or https URL")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def recommend(self, request: EvaluationRequest | dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(_payload_dict(request), separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")
        return self._request_json(
            "/v1/recommendations",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"},
        )

    def use_cases(self) -> dict[str, Any]:
        return self._request_json("/v1/use-cases")

    def scoring_stages(self) -> dict[str, Any]:
        return self._request_json("/v1/scoring-stages")

    def _request_json(
        self,
        path: str,
        *,
        method: str = "GET",
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        http_request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            headers={
                "Accept": "application/json, application/problem+json",
                **(headers or {}),
            },
            method=method,
        )
        try:
            with urllib.request.urlopen(http_request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                raw_problem = json.loads(exc.read().decode("utf-8"))
            finally:
                exc.close()
            try:
                problem = ProblemDetails.from_dict(raw_problem)
            except (TypeError, ValueError) as problem_error:
                raise ValueError("response contained malformed Problem Details") from problem_error
            if problem.status != exc.code:
                raise ValueError("Problem Details status does not match the HTTP response")
            raise EvalRankApiError(status=exc.code, problem=problem, retry_after=_retry_after(exc.headers)) from exc


def _payload_dict(value: EvaluationRequest | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, EvaluationRequest):
        return value.to_dict()
    if isinstance(value, dict):
        return value
    raise TypeError("request must be an EvaluationRequest or dict")


def _retry_after(headers: Any) -> int | None:
    value = headers.get("Retry-After")
    if value is None:
        return None
    text = str(value).strip()
    if not text.isdigit():
        return None
    return int(text)

__all__ = [
    "AdapterMetadataV1",
    "EvalRankApiError",
    "EvalRankClient",
    "CapabilityFingerprintInput",
    "AvailabilityFactV1",
    "CacheWriteRateV1",
    "CacheWriteUsageV1",
    "Abstention",
    "CandidateSet",
    "ConfigurationPassportV1",
    "ContextFactV1",
    "ContinuousMetricV1",
    "COMPARABILITY_MODES",
    "ConfidenceInterval",
    "EntityRef",
    "EvaluatedConfigurationV1",
    "EvaluationToOfferLinkV1",
    "EVIDENCE_KINDS",
    "Exclusion",
    "EvidenceItem",
    "EvidenceSet",
    "EvaluationRequest",
    "FRESHNESS_STATUSES",
    "Freshness",
    "IntervalUncertaintyV1",
    "MAX_SAFE_INTEGER",
    "ObservationV1",
    "PairwisePreferenceMetricV1",
    "PassAtKMetricV1",
    "PricingScheduleFactV1",
    "PROBLEM_CODES",
    "ProblemDetails",
    "ProportionMetricV1",
    "PublicationSnapshotRefV1",
    "RankOnlyMetricV1",
    "RawEntry",
    "Recommendation",
    "RankedEntity",
    "RankingGroup",
    "RankingGroupSnapshotRefV1",
    "RunProvenanceV1",
    "PUBLIC_FIXTURE_KINDS",
    "ScoringStage",
    "ScoringStageCatalog",
    "ServingOfferV1",
    "SourceArtifactV1",
    "SnapshotSetDescriptorV1",
    "StandardErrorUncertaintyV1",
    "StageCandidate",
    "THE_CALL_DECISIONS",
    "TheCall",
    "TrialPolicyV1",
    "TRUST_TIERS",
    "USE_CASE_ENTITY_KINDS",
    "USE_CASE_RANK_POLICIES",
    "UseCase",
    "UseCaseCatalog",
    "UnknownUncertaintyV1",
    "UsageProfileV1",
    "DecisionEvidenceV1",
    "DecisionExclusionV1",
    "DecisionFreshnessV1",
    "DecisionQueryV1",
    "DecisionReasonV1",
    "DecisionReceiptV1",
    "DecisionSelectionV1",
    "DecisionSensitivityV1",
    "aggregation_input_document",
    "bootstrap_seed_document",
    "canonical_json",
    "derive_aggregation_input_digest",
    "derive_bootstrap_seed",
    "monthly_cost_microusd",
    "restricted_jcs",
    "sha256_hex",
    "verify_leaderboard_snapshot_set",
    "verify_leaderboard_semantics",
    "verify_entity_detail_semantics",
    "verify_compare_result_semantics",
    "sample_capability_fingerprint_input",
    "sample_candidate_set",
    "sample_entity_ref",
    "sample_exclusion",
    "sample_evidence_item",
    "sample_evidence_set",
    "sample_evaluation_request",
    "sample_observation",
    "sample_problem_details",
    "sample_public_fixture",
    "sample_ranked_entity",
    "sample_ranking_group",
    "sample_raw_entry",
    "sample_recommendation",
    "sample_scoring_stage_catalog",
    "sample_stage_candidate",
    "sample_use_case_catalog",
    "__version__",
]
