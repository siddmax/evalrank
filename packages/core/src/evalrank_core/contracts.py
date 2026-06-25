from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from typing import Any, ClassVar


TRUST_TIERS = {"verified", "standardized", "self-reported", "tracking-only"}
FRESHNESS_STATUSES = {"fresh", "stale", "recalibrating"}
COMPARABILITY_MODES = {"single-scale", "kind-grouped"}
EVIDENCE_KINDS = {"attestation", "benchmark", "documentation", "runtime-observation", "trace"}
RESULT_ENTITY_KINDS = {"model", "tool_server", "agent"}
RESULT_VERIFICATION_STATES = {"verified", "provisional"}
RESULT_FLAG_KEYS = ("saturated", "contaminated", "judge_model_dependent", "scaffold_nonstandard")
THE_CALL_DECISIONS = {"recommend", "abstain"}
USE_CASE_ENTITY_KINDS = {"model", "tool", "agent"}
USE_CASE_RANK_POLICIES = {"ranked", "veto_overlay"}
_FINGERPRINT_RE = re.compile(r"^[a-f0-9]{64}$")
_METHODOLOGY_VERSION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*\.([a-z0-9]+-)*[a-z0-9]+$")
_RRF_COMPONENT_KEYS = ("lexical_rank", "semantic_rank", "graph_rank")


@dataclass(frozen=True)
class ConfidenceInterval:
    low: float
    high: float

    def __post_init__(self) -> None:
        _require_unit_interval("ci95.low", self.low)
        _require_unit_interval("ci95.high", self.high)
        if self.low > self.high:
            raise ValueError("ci95.low must be <= ci95.high")

    def to_list(self) -> list[float]:
        return [_round_score(self.low), _round_score(self.high)]


@dataclass(frozen=True)
class Freshness:
    status: str
    last_eval: str
    next_refresh: str

    def __post_init__(self) -> None:
        if self.status not in FRESHNESS_STATUSES:
            raise ValueError(f"freshness.status must be one of {sorted(FRESHNESS_STATUSES)}")
        if not self.last_eval:
            raise ValueError("freshness.last_eval is required")
        if not self.next_refresh:
            raise ValueError("freshness.next_refresh is required")

    def to_dict(self) -> dict[str, str]:
        return {
            "last_eval": self.last_eval,
            "next_refresh": self.next_refresh,
            "status": self.status,
        }


@dataclass(frozen=True)
class CapabilityFingerprintInput:
    object: ClassVar[str] = "capability_fingerprint"

    id_scheme: str
    canonical_id: str
    entity_kind: str
    declared_capability_shape: dict[str, Any]

    def __post_init__(self) -> None:
        if not self.id_scheme:
            raise ValueError("id_scheme is required")
        if not self.canonical_id:
            raise ValueError("canonical_id is required")
        if not self.entity_kind:
            raise ValueError("entity_kind is required")
        if not isinstance(self.declared_capability_shape, dict) or not self.declared_capability_shape:
            raise ValueError("declared_capability_shape is required")
        _require_string_keys("declared_capability_shape", self.declared_capability_shape)
        _normalize_json_object("declared_capability_shape", self.declared_capability_shape)

    def fingerprint(self) -> str:
        encoded = json.dumps(self._hash_input(), sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            **self._hash_input(),
            "capability_fingerprint": self.fingerprint(),
        }

    def _hash_input(self) -> dict[str, Any]:
        return {
            "id_scheme": self.id_scheme,
            "canonical_id": self.canonical_id,
            "entity_kind": self.entity_kind,
            "declared_capability_shape": _normalize_json_object(
                "declared_capability_shape", self.declared_capability_shape
            ),
        }


@dataclass(frozen=True)
class RawEntry:
    object: ClassVar[str] = "raw_entry"

    source: str
    source_id: str
    entity_kind: str
    canonical_id: str
    raw_metadata: dict[str, Any]
    declared_capability_shape: dict[str, Any]
    fetched_at: str

    def __post_init__(self) -> None:
        for name in ("source", "source_id", "entity_kind", "canonical_id", "fetched_at"):
            if not getattr(self, name):
                raise ValueError(f"{name} is required")
        if not self.declared_capability_shape:
            raise ValueError("declared_capability_shape is required")
        for name, value in (
            ("raw_metadata", self.raw_metadata),
            ("declared_capability_shape", self.declared_capability_shape),
        ):
            if not isinstance(value, dict):
                raise ValueError(f"{name} must be a JSON object")
            _require_string_keys(name, value)
            _normalize_json_object(name, value)

    @property
    def content_hash(self) -> str:
        encoded = json.dumps(self._hash_input(), sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "source": self.source,
            "source_id": self.source_id,
            "entity_kind": self.entity_kind,
            "canonical_id": self.canonical_id,
            "raw_metadata": _normalize_json_object("raw_metadata", self.raw_metadata),
            "declared_capability_shape": _normalize_json_object(
                "declared_capability_shape", self.declared_capability_shape
            ),
            "fetched_at": self.fetched_at,
            "content_hash": self.content_hash,
        }

    def _hash_input(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "source_id": self.source_id,
            "entity_kind": self.entity_kind,
            "canonical_id": self.canonical_id,
            "raw_metadata": _normalize_json_object("raw_metadata", self.raw_metadata),
            "declared_capability_shape": _normalize_json_object(
                "declared_capability_shape", self.declared_capability_shape
            ),
        }


@dataclass(frozen=True)
class EntityRef:
    entity_type: str
    entity_id: str

    def __post_init__(self) -> None:
        if not self.entity_type:
            raise ValueError("entity_type is required")
        if not self.entity_id:
            raise ValueError("entity_id is required")

    def to_dict(self) -> dict[str, str]:
        return {
            "entity_type": self.entity_type,
            "id": self.entity_id,
        }


@dataclass(frozen=True)
class UseCase:
    object: ClassVar[str] = "use_case"

    id: str
    name: str
    definition: str
    entity_kinds: tuple[str, ...]
    rank_policy: str = "ranked"
    is_overlay: bool = False

    def __post_init__(self) -> None:
        _require_nonempty_string("id", self.id)
        _require_nonempty_string("name", self.name)
        _require_nonempty_string("definition", self.definition)
        if not isinstance(self.entity_kinds, tuple) or not self.entity_kinds:
            raise ValueError("entity_kinds is required")
        if len(set(self.entity_kinds)) != len(self.entity_kinds):
            raise ValueError("entity_kinds must be unique")
        if any(kind not in USE_CASE_ENTITY_KINDS for kind in self.entity_kinds):
            raise ValueError(f"entity_kinds must be one of {sorted(USE_CASE_ENTITY_KINDS)}")
        if self.rank_policy not in USE_CASE_RANK_POLICIES:
            raise ValueError(f"rank_policy must be one of {sorted(USE_CASE_RANK_POLICIES)}")
        if not isinstance(self.is_overlay, bool):
            raise ValueError("is_overlay must be a boolean")
        if self.is_overlay and self.rank_policy != "veto_overlay":
            raise ValueError("rank_policy must be veto_overlay for overlays")
        if not self.is_overlay and self.rank_policy != "ranked":
            raise ValueError("rank_policy must be ranked for non-overlay use cases")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "id": self.id,
            "name": self.name,
            "definition": self.definition,
            "entity_kinds": list(self.entity_kinds),
            "rank_policy": self.rank_policy,
            "is_overlay": self.is_overlay,
        }


@dataclass(frozen=True)
class UseCaseCatalog:
    object: ClassVar[str] = "use_case_catalog"

    methodology_version: str
    generated_at: str
    use_cases: tuple[UseCase, ...]

    def __post_init__(self) -> None:
        _require_methodology_version(self.methodology_version)
        _require_nonempty_string("generated_at", self.generated_at)
        if not isinstance(self.use_cases, tuple) or not self.use_cases:
            raise ValueError("use_cases is required")
        seen: set[str] = set()
        for use_case in self.use_cases:
            if not isinstance(use_case, UseCase):
                raise TypeError("use_cases must contain UseCase values")
            if use_case.id in seen:
                raise ValueError("duplicate use_case id")
            seen.add(use_case.id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "methodology_version": self.methodology_version,
            "generated_at": self.generated_at,
            "use_cases": [use_case.to_dict() for use_case in self.use_cases],
        }


@dataclass(frozen=True)
class Exclusion:
    subject: EntityRef
    reason: str
    detail: str

    def __post_init__(self) -> None:
        if not isinstance(self.subject, EntityRef):
            raise TypeError("subject must be an EntityRef")
        if not isinstance(self.reason, str) or not self.reason:
            raise ValueError("reason is required")
        if not isinstance(self.detail, str) or not self.detail:
            raise ValueError("detail is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject.to_dict(),
            "reason": self.reason,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    subject: EntityRef
    kind: str
    source: str
    observed_at: str
    summary: str
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evidence_id:
            raise ValueError("evidence_id is required")
        if not isinstance(self.subject, EntityRef):
            raise TypeError("subject must be an EntityRef")
        if self.kind not in EVIDENCE_KINDS:
            raise ValueError(f"kind must be one of {sorted(EVIDENCE_KINDS)}")
        if not self.source:
            raise ValueError("source is required")
        if not self.observed_at:
            raise ValueError("observed_at is required")
        if not self.summary:
            raise ValueError("summary is required")
        if self.score is not None:
            _require_unit_interval("score", self.score)
        if any(not isinstance(key, str) for key in self.metadata):
            raise ValueError("metadata keys must be strings")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "subject": self.subject.to_dict(),
            "kind": self.kind,
            "source": self.source,
            "observed_at": self.observed_at,
            "summary": self.summary,
            "score": None if self.score is None else _round_score(self.score),
            "metadata": {key: self.metadata[key] for key in sorted(self.metadata)},
        }


@dataclass(frozen=True)
class ResultRow:
    object: ClassVar[str] = "result_row"

    entity_id: str
    entity_kind: str
    benchmark_id: str
    benchmark_version: str
    harness: str
    harness_version: str
    is_self_reported: bool
    n_items: int
    ci95: ConfidenceInterval
    score_raw: float
    score_unit: str
    date_run: str
    model_version: str
    provenance: dict[str, Any]
    source_url: str
    attribution_string: str
    flags: dict[str, bool]
    verification_state: str

    def __post_init__(self) -> None:
        for name in (
            "entity_id",
            "benchmark_id",
            "benchmark_version",
            "harness",
            "harness_version",
            "score_unit",
            "date_run",
            "model_version",
            "source_url",
            "attribution_string",
        ):
            _require_nonempty_string(name, getattr(self, name))
        if self.entity_kind not in RESULT_ENTITY_KINDS:
            raise ValueError(f"entity_kind must be one of {sorted(RESULT_ENTITY_KINDS)}")
        if not isinstance(self.is_self_reported, bool):
            raise ValueError("is_self_reported must be a boolean")
        if not isinstance(self.n_items, int) or isinstance(self.n_items, bool) or self.n_items < 0:
            raise ValueError("n_items must be an integer >= 0")
        if not isinstance(self.ci95, ConfidenceInterval):
            raise TypeError("ci95 must be a ConfidenceInterval")
        _require_finite_number("score_raw", self.score_raw)
        if not isinstance(self.provenance, dict):
            raise ValueError("provenance must be a JSON object")
        _require_string_keys("provenance", self.provenance)
        _normalize_json_object("provenance", self.provenance)
        if not isinstance(self.flags, dict):
            raise ValueError("flags must be a JSON object")
        if set(self.flags) != set(RESULT_FLAG_KEYS):
            raise ValueError(f"flags must include {', '.join(RESULT_FLAG_KEYS)}")
        for key, value in self.flags.items():
            if not isinstance(value, bool):
                raise ValueError(f"flags.{key} must be a boolean")
        if self.verification_state not in RESULT_VERIFICATION_STATES:
            raise ValueError(f"verification_state must be one of {sorted(RESULT_VERIFICATION_STATES)}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "entity_id": self.entity_id,
            "entity_kind": self.entity_kind,
            "benchmark_id": self.benchmark_id,
            "benchmark_version": self.benchmark_version,
            "harness": self.harness,
            "harness_version": self.harness_version,
            "is_self_reported": self.is_self_reported,
            "n_items": self.n_items,
            "ci95": self.ci95.to_list(),
            "score_raw": _round_score(float(self.score_raw)),
            "score_unit": self.score_unit,
            "date_run": self.date_run,
            "model_version": self.model_version,
            "provenance": _normalize_json_object("provenance", self.provenance),
            "source_url": self.source_url,
            "attribution_string": self.attribution_string,
            "flags": {key: self.flags[key] for key in RESULT_FLAG_KEYS},
            "verification_state": self.verification_state,
        }


@dataclass(frozen=True)
class EvidenceSet:
    object: ClassVar[str] = "evidence_set"

    request_id: str
    use_case: str
    evidence_items: tuple[EvidenceItem, ...]
    generated_at: str

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.use_case:
            raise ValueError("use_case is required")
        if not self.generated_at:
            raise ValueError("generated_at is required")
        seen: set[str] = set()
        for item in self.evidence_items:
            if not isinstance(item, EvidenceItem):
                raise TypeError("evidence_items must contain EvidenceItem values")
            if item.evidence_id in seen:
                raise ValueError("duplicate evidence_id")
            seen.add(item.evidence_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "request_id": self.request_id,
            "use_case": self.use_case,
            "evidence_items": [item.to_dict() for item in self.evidence_items],
            "generated_at": self.generated_at,
        }


@dataclass(frozen=True)
class EvaluationRequest:
    object: ClassVar[str] = "evaluation_request"

    request_id: str
    use_case: str
    entity_types: tuple[str, ...]
    requested_at: str
    constraints: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.use_case:
            raise ValueError("use_case is required")
        if not self.entity_types:
            raise ValueError("entity_types is required")
        if any(not entity_type for entity_type in self.entity_types):
            raise ValueError("entity_types must not contain blank values")
        if not self.requested_at:
            raise ValueError("requested_at is required")
        if any(not isinstance(key, str) for key in self.constraints):
            raise ValueError("constraints keys must be strings")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "request_id": self.request_id,
            "use_case": self.use_case,
            "entity_types": list(self.entity_types),
            "requested_at": self.requested_at,
            "constraints": {key: self.constraints[key] for key in sorted(self.constraints)},
        }


@dataclass(frozen=True)
class CandidateSet:
    object: ClassVar[str] = "candidate_set"

    request_id: str
    use_case: str
    candidates: tuple[EntityRef, ...]
    generated_at: str

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.use_case:
            raise ValueError("use_case is required")
        if not self.candidates:
            raise ValueError("candidates is required")
        if not self.generated_at:
            raise ValueError("generated_at is required")
        seen: set[tuple[str, str]] = set()
        for candidate in self.candidates:
            if not isinstance(candidate, EntityRef):
                raise TypeError("candidates must contain EntityRef values")
            key = (candidate.entity_type, candidate.entity_id)
            if key in seen:
                raise ValueError("duplicate candidate")
            seen.add(key)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "request_id": self.request_id,
            "use_case": self.use_case,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "generated_at": self.generated_at,
        }


@dataclass(frozen=True)
class StageCandidate:
    object: ClassVar[str] = "stage_candidate"

    candidate_id: str
    entity: EntityRef
    fused_score: float
    rrf_components: dict[str, int | None]
    retrieval_arms: tuple[str, ...]
    use_case: str

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not _FINGERPRINT_RE.fullmatch(self.candidate_id):
            raise ValueError("candidate_id must be a 64-character lowercase hex fingerprint")
        if not isinstance(self.entity, EntityRef):
            raise TypeError("entity must be an EntityRef")
        _require_nonnegative_finite("fused_score", self.fused_score)
        if not isinstance(self.rrf_components, dict):
            raise ValueError("rrf_components must be a JSON object")
        if set(self.rrf_components) != set(_RRF_COMPONENT_KEYS):
            raise ValueError("rrf_components must include lexical_rank, semantic_rank, and graph_rank")
        for key in _RRF_COMPONENT_KEYS:
            value = self.rrf_components[key]
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 1):
                raise ValueError(f"{key} must be null or an integer >= 1")
        if not isinstance(self.retrieval_arms, tuple) or not self.retrieval_arms:
            raise ValueError("retrieval_arms is required")
        if any(not isinstance(arm, str) or not arm for arm in self.retrieval_arms):
            raise ValueError("retrieval_arms must contain non-empty strings")
        if len(set(self.retrieval_arms)) != len(self.retrieval_arms):
            raise ValueError("retrieval_arms must be unique")
        if not isinstance(self.use_case, str) or not self.use_case:
            raise ValueError("use_case is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "candidate_id": self.candidate_id,
            "entity": self.entity.to_dict(),
            "fused_score": _round_score(float(self.fused_score)),
            "rrf_components": {key: self.rrf_components[key] for key in _RRF_COMPONENT_KEYS},
            "retrieval_provenance": {
                "arms": sorted(self.retrieval_arms),
                "use_case": self.use_case,
            },
        }


@dataclass(frozen=True)
class RankedEntity:
    entity_type: str
    entity_id: str
    rank: int
    capability_score: float
    confidence: float
    ci95: ConfidenceInterval
    methodology_version: str
    trust_tier: str
    freshness: Freshness
    evidence_count: int
    caveats: tuple[str, ...] = ()
    score_components: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.entity_type:
            raise ValueError("entity_type is required")
        if not self.entity_id:
            raise ValueError("entity_id is required")
        if self.rank < 1:
            raise ValueError("rank must be >= 1")
        _require_unit_interval("capability_score", self.capability_score)
        _require_unit_interval("confidence", self.confidence)
        _require_methodology_version(self.methodology_version)
        if self.trust_tier not in TRUST_TIERS:
            raise ValueError(f"trust_tier must be one of {sorted(TRUST_TIERS)}")
        if self.evidence_count < 0:
            raise ValueError("evidence_count must be >= 0")
        for name, value in self.score_components.items():
            _require_unit_interval(f"score_components.{name}", value)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "id": self.entity_id,
            "rank": self.rank,
            "capability_score": _round_score(self.capability_score),
            "confidence": _round_score(self.confidence),
            "ci95": self.ci95.to_list(),
            "methodology_version": self.methodology_version,
            "trust_tier": self.trust_tier,
            "score_components": {key: _round_score(value) for key, value in sorted(self.score_components.items())},
            "axes": {
                "evidence": {
                    "n_items": self.evidence_count,
                    "coverage": self.trust_tier,
                }
            },
            "freshness": self.freshness.to_dict(),
            "caveats": list(self.caveats),
        }


@dataclass(frozen=True)
class TheCall:
    decision: str
    confidence: float | None
    reason: str
    abstention_reason: str | None = None

    def __post_init__(self) -> None:
        if self.decision not in THE_CALL_DECISIONS:
            raise ValueError(f"decision must be one of {sorted(THE_CALL_DECISIONS)}")
        if not self.reason:
            raise ValueError("reason is required")
        if self.decision == "recommend":
            if self.confidence is None:
                raise ValueError("confidence is required for recommend")
            if self.abstention_reason is not None:
                raise ValueError("abstention_reason must be null for recommend")
        if self.decision == "abstain":
            if self.confidence is not None:
                raise ValueError("confidence must be null for abstain")
            if not self.abstention_reason:
                raise ValueError("abstention_reason is required for abstain")
        if self.confidence is not None:
            _require_unit_interval("confidence", self.confidence)

    @classmethod
    def recommend(cls, *, confidence: float, reason: str) -> "TheCall":
        return cls(decision="recommend", confidence=confidence, reason=reason)

    @classmethod
    def abstain(cls, *, reason: str) -> "TheCall":
        return cls(
            decision="abstain",
            confidence=None,
            reason=reason,
            abstention_reason=reason,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "confidence": None if self.confidence is None else _round_score(self.confidence),
            "reason": self.reason,
            "abstention_reason": self.abstention_reason,
        }


@dataclass(frozen=True)
class RankingGroup:
    object: ClassVar[str] = "ranking_group"

    group_key: str
    entity_type: str
    ranked: tuple[RankedEntity, ...]
    group_rationale: str

    def __post_init__(self) -> None:
        _require_nonempty_string("group_key", self.group_key)
        _require_nonempty_string("entity_type", self.entity_type)
        _require_nonempty_string("group_rationale", self.group_rationale)
        if not isinstance(self.ranked, tuple) or not self.ranked:
            raise ValueError("ranked is required")
        seen: set[str] = set()
        for row in self.ranked:
            if not isinstance(row, RankedEntity):
                raise TypeError("ranked must contain RankedEntity values")
            if row.entity_type != self.entity_type:
                raise ValueError("ranked rows must match group entity_type")
            if row.entity_id in seen:
                raise ValueError("duplicate ranked entity")
            seen.add(row.entity_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "group_key": self.group_key,
            "entity_type": self.entity_type,
            "ranked": [row.to_dict() for row in self.ranked],
            "group_rationale": self.group_rationale,
        }


@dataclass(frozen=True)
class Recommendation:
    object: ClassVar[str] = "recommendation"

    request_id: str
    use_case: str
    methodology_version: str
    generated_at: str
    comparability: str
    ranked: list[RankedEntity]
    groups: list[RankingGroup] | None
    shortlist_depth: int
    depth_rationale: str
    degraded: bool = False
    served_from: str = "base"
    base_snapshot_lag_ms: int = 0
    the_call: TheCall | None = None
    exclusions: list[Exclusion] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.use_case:
            raise ValueError("use_case is required")
        _require_methodology_version(self.methodology_version)
        if not self.generated_at:
            raise ValueError("generated_at is required")
        if self.comparability not in COMPARABILITY_MODES:
            raise ValueError("comparability must be 'single-scale' or 'kind-grouped'")
        if self.comparability == "single-scale" and self.groups is not None:
            raise ValueError("single-scale recommendations must not include groups")
        if self.comparability == "kind-grouped" and self.ranked:
            raise ValueError("kind-grouped recommendations must not include ranked rows")
        if self.comparability == "kind-grouped" and not self.groups:
            raise ValueError("kind-grouped recommendations require groups")
        if self.shortlist_depth < 0:
            raise ValueError("shortlist_depth must be >= 0")
        for row in self.ranked:
            if row.methodology_version != self.methodology_version:
                raise ValueError("ranked rows must carry the envelope methodology_version")
        for group in self.groups or []:
            if not isinstance(group, RankingGroup):
                raise TypeError("groups must contain RankingGroup values")
            for row in group.ranked:
                if row.methodology_version != self.methodology_version:
                    raise ValueError("group rows must carry the envelope methodology_version")
        for exclusion in self.exclusions:
            if not isinstance(exclusion, Exclusion):
                raise TypeError("exclusions must contain Exclusion values")

    @classmethod
    def single_scale(
        cls,
        *,
        request_id: str,
        use_case: str,
        methodology_version: str,
        ranked: list[RankedEntity],
        generated_at: str,
        depth_rationale: str,
        the_call: TheCall | None = None,
        exclusions: list[Exclusion] | None = None,
    ) -> "Recommendation":
        return cls(
            request_id=request_id,
            use_case=use_case,
            methodology_version=methodology_version,
            generated_at=generated_at,
            comparability="single-scale",
            ranked=ranked,
            groups=None,
            shortlist_depth=len(ranked),
            depth_rationale=depth_rationale,
            the_call=the_call,
            exclusions=exclusions or [],
        )

    @classmethod
    def kind_grouped(
        cls,
        *,
        request_id: str,
        use_case: str,
        methodology_version: str,
        groups: list[RankingGroup],
        generated_at: str,
        depth_rationale: str,
        the_call: TheCall | None = None,
        exclusions: list[Exclusion] | None = None,
    ) -> "Recommendation":
        return cls(
            request_id=request_id,
            use_case=use_case,
            methodology_version=methodology_version,
            generated_at=generated_at,
            comparability="kind-grouped",
            ranked=[],
            groups=groups,
            shortlist_depth=sum(len(group.ranked) for group in groups),
            depth_rationale=depth_rationale,
            the_call=the_call,
            exclusions=exclusions or [],
        )

    @classmethod
    def abstain(
        cls,
        *,
        request_id: str,
        use_case: str,
        methodology_version: str,
        generated_at: str,
        reason: str,
    ) -> "Recommendation":
        return cls(
            request_id=request_id,
            use_case=use_case,
            methodology_version=methodology_version,
            generated_at=generated_at,
            comparability="single-scale",
            ranked=[],
            groups=None,
            shortlist_depth=0,
            depth_rationale=reason,
            the_call=TheCall.abstain(reason=reason),
        )

    @property
    def recommendation_id(self) -> str:
        encoded = json.dumps(self._content_addressed_payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()[:24]
        return f"rec_{digest}"

    @property
    def result_usable(self) -> bool:
        return bool(self.ranked or self.groups) and (self.the_call is None or self.the_call.decision != "abstain")

    def to_dict(self) -> dict[str, Any]:
        payload = self._payload()
        recommendation_id = self.recommendation_id
        payload["recommendation_id"] = recommendation_id
        payload["recommend_id"] = recommendation_id
        payload["search_run_id"] = recommendation_id
        payload["request_id"] = self.request_id
        return payload

    def _payload(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "use_case": self.use_case,
            "shortlist_depth": self.shortlist_depth,
            "depth_rationale": self.depth_rationale,
            "degraded": self.degraded,
            "served_from": self.served_from,
            "base_snapshot_lag_ms": self.base_snapshot_lag_ms,
            "methodology_version": self.methodology_version,
            "generated_at": self.generated_at,
            "comparability": self.comparability,
            "ranked": [row.to_dict() for row in self.ranked],
            "groups": None if self.groups is None else [group.to_dict() for group in self.groups],
            "the_call": None if self.the_call is None else self.the_call.to_dict(),
            "exclusions": [exclusion.to_dict() for exclusion in self.exclusions],
        }

    def _content_addressed_payload(self) -> dict[str, Any]:
        return self._payload()


def _require_unit_interval(name: str, value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")


def _require_nonnegative_finite(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite number >= 0")


def _require_finite_number(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _require_nonempty_string(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} is required")


def _require_methodology_version(value: str) -> None:
    if not isinstance(value, str) or not _METHODOLOGY_VERSION_RE.fullmatch(value):
        raise ValueError("methodology_version must match YYYY-MM-DD.SEQ.slug")


def _require_string_keys(name: str, value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{name} keys must be strings")
            _require_string_keys(f"{name}.{key}", child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            _require_string_keys(name, child)


def _normalize_json_object(name: str, value: dict[str, Any]) -> dict[str, Any]:
    try:
        return json.loads(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be JSON serializable") from exc


def _round_score(value: float) -> float:
    return round(value, 6)
