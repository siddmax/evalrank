from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, ClassVar


TRUST_TIERS = {"verified", "standardized", "self-reported", "tracking-only"}
FRESHNESS_STATUSES = {"fresh", "stale", "recalibrating"}
COMPARABILITY_MODES = {"single-scale", "kind-grouped"}
EVIDENCE_KINDS = {"attestation", "benchmark", "documentation", "runtime-observation", "trace"}
_METHODOLOGY_VERSION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*\.([a-z0-9]+-)*[a-z0-9]+$")


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
class Recommendation:
    object: ClassVar[str] = "recommendation"

    request_id: str
    use_case: str
    methodology_version: str
    generated_at: str
    comparability: str
    ranked: list[RankedEntity]
    groups: list[dict[str, Any]] | None
    shortlist_depth: int
    depth_rationale: str
    degraded: bool = False
    served_from: str = "base"
    base_snapshot_lag_ms: int = 0
    the_call: dict[str, Any] | None = None
    exclusions: list[dict[str, Any]] = field(default_factory=list)

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
        if self.shortlist_depth < 0:
            raise ValueError("shortlist_depth must be >= 0")
        for row in self.ranked:
            if row.methodology_version != self.methodology_version:
                raise ValueError("ranked rows must carry the envelope methodology_version")

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
        exclusions: list[dict[str, Any]] | None = None,
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
            the_call={"abstention_reason": reason},
        )

    @property
    def recommendation_id(self) -> str:
        encoded = json.dumps(self._content_addressed_payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()[:24]
        return f"rec_{digest}"

    @property
    def result_usable(self) -> bool:
        return bool(self.ranked or self.groups) and not (self.the_call or {}).get("abstention_reason")

    def to_dict(self) -> dict[str, Any]:
        payload = self._payload()
        payload["recommendation_id"] = self.recommendation_id
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
            "groups": self.groups,
            "the_call": self.the_call,
            "exclusions": self.exclusions,
        }

    def _content_addressed_payload(self) -> dict[str, Any]:
        return self._payload()


def _require_unit_interval(name: str, value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")


def _require_methodology_version(value: str) -> None:
    if not isinstance(value, str) or not _METHODOLOGY_VERSION_RE.fullmatch(value):
        raise ValueError("methodology_version must match YYYY-MM-DD.SEQ.slug")


def _round_score(value: float) -> float:
    return round(value, 6)
