"""Portable EvalRank provenance and decision contracts.

These objects are storage-free public contracts. They deliberately separate
what was evaluated from where a configuration can be bought today, and they
make every decision identity reproducible from restricted canonical JSON.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation, localcontext
from types import MappingProxyType
from typing import Any, ClassVar, Mapping
from urllib.parse import urlparse

from evalrank_core.canonical_json import MAX_SAFE_INTEGER, canonical_json, sha256_hex


_HEX_RE = re.compile(r"^[0-9a-f]{64}$")
_ARTIFACT_ID_RE = re.compile(r"^artifact_[0-9a-f]{64}$")
_CONFIGURATION_ID_RE = re.compile(r"^config_[0-9a-f]{64}$")
_OBSERVATION_ID_RE = re.compile(r"^obs_[A-Za-z0-9][A-Za-z0-9._:-]*$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_MEDIA_TYPE_RE = re.compile(r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+$")
_DECIMAL_RE = re.compile(
    r"^(?:0|[1-9]\d*)(?:\.\d*[1-9])?$|^-(?:0\.\d*[1-9]|[1-9]\d*(?:\.\d*[1-9])?)$"
)
_METHODOLOGY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*\.([a-z0-9]+-)*[a-z0-9]+$")

IDENTITY_TRIPLES = {
    ("model_configuration", "direct_prompt", "model-configuration-v1"),
    ("agent_system", "agentic", "agent-system-v1"),
    ("system_configuration", "system", "system-configuration-v1"),
    ("component_configuration", "retrieval", "component-configuration-v1"),
    ("arena_system", "crowd_pairwise", "arena-system-v1"),
}
INTERVAL_METHODS = {
    "reported",
    "bootstrap_percentile",
    "bootstrap_bca",
    "clopper_pearson",
    "wilson",
    "normal_approximation",
    "credible_interval",
}
ABSTENTION_REASONS = {
    "insufficient_comparable_evidence",
    "no_eligible_serving_offer",
    "constraints_eliminate_all_candidates",
    "evidence_stale",
    "methodology_unavailable",
}
EXCLUSION_CODES = {
    "constraints_not_met",
    "not_in_capability_top_set",
    "serving_offer_unverified",
    "evidence_stale",
    "incompatible_configuration",
}
REASON_CODES = {
    "strongest_capability_evidence",
    "within_capability_top_set",
    "lowest_verified_cost",
    "budget_constraint_met",
    "provider_constraint_match",
    "region_constraint_match",
    "context_requirement_met",
    "insufficient_evidence",
    "serving_offer_unverified",
    "budget_exceeded",
    "stale_evidence",
}
REASON_PREDICATES = {"eq", "ne", "lt", "lte", "gt", "gte", "within_top_set", "unavailable"}
REASON_AXES = {"capability", "monthly_cost", "context", "availability", "freshness", "provider", "region"}
REASON_UNITS = {
    "probability",
    "score",
    "microusd_per_month",
    "tokens",
    "status",
    "timestamp",
    "provider_id",
    "region_id",
}
CAVEAT_CODES = {
    "provider_offer_link_required",
    "limited_availability",
    "evidence_near_expiry",
    "incomplete_family_coverage",
    "cost_sensitive_to_usage",
}
SENSITIVITY_SCENARIOS = {
    "price_plus_20_percent",
    "price_minus_20_percent",
    "usage_double",
    "leave_one_family_out",
}


@dataclass(frozen=True, slots=True, kw_only=True)
class AdapterMetadataV1:
    schema_version: str
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        _require_string("schema_version", self.schema_version)
        if not isinstance(self.payload, Mapping):
            raise TypeError("payload must be a JSON object")
        plain = dict(self.payload)
        canonical_json(plain)
        object.__setattr__(self, "payload", MappingProxyType(_copy_json_object(plain)))

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "payload": _thaw_json(self.payload)}

    @classmethod
    def from_dict(cls, value: Any) -> "AdapterMetadataV1":
        payload = _closed(value, required=("schema_version", "payload"))
        return cls(schema_version=payload["schema_version"], payload=payload["payload"])


@dataclass(frozen=True, slots=True, kw_only=True)
class TrialPolicyV1:
    attempts_per_item: int
    seed_strategy: str
    seed: int | None

    def __post_init__(self) -> None:
        _require_safe_integer("attempts_per_item", self.attempts_per_item, minimum=1)
        _require_enum("seed_strategy", self.seed_strategy, {"fixed", "derived", "upstream"})
        if self.seed_strategy == "fixed":
            _require_safe_integer("seed", self.seed)
        elif self.seed is not None:
            raise ValueError("seed must be null unless seed_strategy is fixed")

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempts_per_item": self.attempts_per_item,
            "seed_strategy": self.seed_strategy,
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "TrialPolicyV1":
        payload = _closed(value, required=("attempts_per_item", "seed_strategy", "seed"))
        return cls(**payload)


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceArtifactV1:
    object: ClassVar[str] = "source_artifact"
    schema_version: ClassVar[str] = "1"

    source_artifact_id: str
    canonical_url: str
    upstream_version: str
    content_sha256: str
    byte_length: int
    media_type: str
    fetched_at: str

    def __post_init__(self) -> None:
        _require_hash("content_sha256", self.content_sha256)
        if self.source_artifact_id != f"artifact_{self.content_sha256}":
            raise ValueError("source_artifact_id must be artifact_<content_sha256>")
        _require_http_url("canonical_url", self.canonical_url)
        _require_string("upstream_version", self.upstream_version)
        _require_safe_integer("byte_length", self.byte_length, minimum=0)
        if not isinstance(self.media_type, str) or not _MEDIA_TYPE_RE.fullmatch(self.media_type):
            raise ValueError("media_type must be an RFC media type without parameters")
        _parse_timestamp("fetched_at", self.fetched_at)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "source_artifact_id": self.source_artifact_id,
            "canonical_url": self.canonical_url,
            "upstream_version": self.upstream_version,
            "content_sha256": self.content_sha256,
            "byte_length": self.byte_length,
            "media_type": self.media_type,
            "fetched_at": self.fetched_at,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "SourceArtifactV1":
        payload = _closed(
            value,
            required=(
                "object",
                "schema_version",
                "source_artifact_id",
                "canonical_url",
                "upstream_version",
                "content_sha256",
                "byte_length",
                "media_type",
                "fetched_at",
            ),
        )
        _envelope(payload, cls.object)
        return cls(**_without_envelope(payload))


@dataclass(frozen=True, slots=True, kw_only=True)
class RunProvenanceV1:
    object: ClassVar[str] = "run_provenance"
    schema_version: ClassVar[str] = "1"

    run_id: str
    benchmark_family_id: str
    feed_id: str
    source_artifact_id: str
    parser_id: str
    parser_version: str
    started_at: str
    completed_at: str
    harness_version: str | None = None
    environment_digest: str | None = None
    scorer_version: str | None = None
    trial_policy: TrialPolicyV1 | None = None
    adapter_metadata: AdapterMetadataV1 | None = None

    def __post_init__(self) -> None:
        for name in ("run_id", "benchmark_family_id", "feed_id", "parser_id", "parser_version"):
            _require_string(name, getattr(self, name))
        _require_pattern("source_artifact_id", self.source_artifact_id, _ARTIFACT_ID_RE)
        started = _parse_timestamp("started_at", self.started_at)
        completed = _parse_timestamp("completed_at", self.completed_at)
        if completed < started:
            raise ValueError("completed_at must be on or after started_at")
        for name in ("harness_version", "environment_digest", "scorer_version"):
            _require_nullable_string(name, getattr(self, name))
        if self.trial_policy is not None and not isinstance(self.trial_policy, TrialPolicyV1):
            raise TypeError("trial_policy must be TrialPolicyV1 or null")
        if self.adapter_metadata is not None and not isinstance(self.adapter_metadata, AdapterMetadataV1):
            raise TypeError("adapter_metadata must be AdapterMetadataV1 or null")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "benchmark_family_id": self.benchmark_family_id,
            "feed_id": self.feed_id,
            "source_artifact_id": self.source_artifact_id,
            "parser_id": self.parser_id,
            "parser_version": self.parser_version,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "harness_version": self.harness_version,
            "environment_digest": self.environment_digest,
            "scorer_version": self.scorer_version,
            "trial_policy": None if self.trial_policy is None else self.trial_policy.to_dict(),
            "adapter_metadata": None if self.adapter_metadata is None else self.adapter_metadata.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "RunProvenanceV1":
        raw = _mapping(value)
        if "source_artifact_id" not in raw:
            raise ValueError("missing required field: source_artifact_id")
        payload = _closed(
            raw,
            required=(
                "object",
                "schema_version",
                "run_id",
                "benchmark_family_id",
                "feed_id",
                "source_artifact_id",
                "parser_id",
                "parser_version",
                "started_at",
                "completed_at",
                "harness_version",
                "environment_digest",
                "scorer_version",
                "trial_policy",
                "adapter_metadata",
            ),
        )
        _envelope(payload, cls.object)
        values = _without_envelope(payload)
        values["trial_policy"] = (
            None if values["trial_policy"] is None else TrialPolicyV1.from_dict(values["trial_policy"])
        )
        values["adapter_metadata"] = (
            None
            if values["adapter_metadata"] is None
            else AdapterMetadataV1.from_dict(values["adapter_metadata"])
        )
        return cls(**values)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProportionMetricV1:
    kind: ClassVar[str] = "proportion"
    value: str
    numerator: int | None
    denominator: int | None

    def __post_init__(self) -> None:
        numeric = _require_decimal("value", self.value)
        _require_unit_interval("value", numeric)
        _validate_count_pair("numerator", self.numerator, "denominator", self.denominator)
        if self.numerator is not None:
            _require_rounded_ratio("value", self.value, self.numerator, self.denominator)

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "value": self.value, "numerator": self.numerator, "denominator": self.denominator}

    @classmethod
    def from_dict(cls, value: Any) -> "ProportionMetricV1":
        payload = _closed(value, required=("kind", "value", "numerator", "denominator"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


@dataclass(frozen=True, slots=True, kw_only=True)
class ContinuousMetricV1:
    kind: ClassVar[str] = "continuous"
    value: str
    unit: str
    n_items: int | None

    def __post_init__(self) -> None:
        _require_decimal("value", self.value)
        _require_string("unit", self.unit)
        _require_nullable_safe_integer("n_items", self.n_items, minimum=1)

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "value": self.value, "unit": self.unit, "n_items": self.n_items}

    @classmethod
    def from_dict(cls, value: Any) -> "ContinuousMetricV1":
        payload = _closed(value, required=("kind", "value", "unit", "n_items"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


@dataclass(frozen=True, slots=True, kw_only=True)
class PassAtKMetricV1:
    kind: ClassVar[str] = "pass_at_k"
    value: str
    k: int
    successful_items: int | None
    evaluated_items: int | None

    def __post_init__(self) -> None:
        numeric = _require_decimal("value", self.value)
        _require_unit_interval("value", numeric)
        _require_safe_integer("k", self.k, minimum=1)
        _validate_count_pair("successful_items", self.successful_items, "evaluated_items", self.evaluated_items)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "value": self.value,
            "k": self.k,
            "successful_items": self.successful_items,
            "evaluated_items": self.evaluated_items,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "PassAtKMetricV1":
        payload = _closed(value, required=("kind", "value", "k", "successful_items", "evaluated_items"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


@dataclass(frozen=True, slots=True, kw_only=True)
class PairwisePreferenceMetricV1:
    kind: ClassVar[str] = "pairwise_preference"
    value: str
    scale: str
    comparison_count: int | None

    def __post_init__(self) -> None:
        _require_decimal("value", self.value)
        _require_enum("scale", self.scale, {"probability", "elo", "margin"})
        _require_nullable_safe_integer("comparison_count", self.comparison_count, minimum=1)
        if self.scale == "probability":
            _require_unit_interval("value", Decimal(self.value))

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "value": self.value, "scale": self.scale, "comparison_count": self.comparison_count}

    @classmethod
    def from_dict(cls, value: Any) -> "PairwisePreferenceMetricV1":
        payload = _closed(value, required=("kind", "value", "scale", "comparison_count"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


@dataclass(frozen=True, slots=True, kw_only=True)
class RankOnlyMetricV1:
    kind: ClassVar[str] = "rank_only"
    rank: int
    candidate_count: int | None

    def __post_init__(self) -> None:
        _require_safe_integer("rank", self.rank, minimum=1)
        _require_nullable_safe_integer("candidate_count", self.candidate_count, minimum=1)
        if self.candidate_count is not None and self.rank > self.candidate_count:
            raise ValueError("rank must not exceed candidate_count")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "rank": self.rank, "candidate_count": self.candidate_count}

    @classmethod
    def from_dict(cls, value: Any) -> "RankOnlyMetricV1":
        payload = _closed(value, required=("kind", "rank", "candidate_count"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


MetricV1 = ProportionMetricV1 | ContinuousMetricV1 | PassAtKMetricV1 | PairwisePreferenceMetricV1 | RankOnlyMetricV1


@dataclass(frozen=True, slots=True, kw_only=True)
class UnknownUncertaintyV1:
    kind: ClassVar[str] = "unknown"

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind}

    @classmethod
    def from_dict(cls, value: Any) -> "UnknownUncertaintyV1":
        payload = _closed(value, required=("kind",))
        _kind(payload, cls.kind)
        return cls()


@dataclass(frozen=True, slots=True, kw_only=True)
class StandardErrorUncertaintyV1:
    kind: ClassVar[str] = "standard_error"
    value: str

    def __post_init__(self) -> None:
        if _require_decimal("value", self.value) < 0:
            raise ValueError("value must be nonnegative")

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "value": self.value}

    @classmethod
    def from_dict(cls, value: Any) -> "StandardErrorUncertaintyV1":
        payload = _closed(value, required=("kind", "value"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


@dataclass(frozen=True, slots=True, kw_only=True)
class IntervalUncertaintyV1:
    kind: ClassVar[str] = "interval"
    low: str
    high: str
    confidence_level: str
    method: str

    def __post_init__(self) -> None:
        low = _require_decimal("low", self.low)
        high = _require_decimal("high", self.high)
        if low > high:
            raise ValueError("low must be <= high")
        level = _require_decimal("confidence_level", self.confidence_level)
        if level <= 0 or level > 1:
            raise ValueError("confidence_level must be in (0, 1]")
        _require_enum("method", self.method, INTERVAL_METHODS)

    def to_dict(self) -> dict[str, str]:
        return {
            "kind": self.kind,
            "low": self.low,
            "high": self.high,
            "confidence_level": self.confidence_level,
            "method": self.method,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "IntervalUncertaintyV1":
        payload = _closed(value, required=("kind", "low", "high", "confidence_level", "method"))
        _kind(payload, cls.kind)
        return cls(**_without_kind(payload))


UncertaintyV1 = UnknownUncertaintyV1 | StandardErrorUncertaintyV1 | IntervalUncertaintyV1


@dataclass(frozen=True, slots=True, kw_only=True)
class ObservationV1:
    object: ClassVar[str] = "observation"
    schema_version: ClassVar[str] = "1"

    observation_id: str
    evaluated_configuration_id: str
    metric: MetricV1
    uncertainty: UncertaintyV1
    provenance: RunProvenanceV1

    def __post_init__(self) -> None:
        _require_pattern("observation_id", self.observation_id, _OBSERVATION_ID_RE)
        _require_pattern("evaluated_configuration_id", self.evaluated_configuration_id, _CONFIGURATION_ID_RE)
        if not isinstance(self.metric, (ProportionMetricV1, ContinuousMetricV1, PassAtKMetricV1, PairwisePreferenceMetricV1, RankOnlyMetricV1)):
            raise TypeError("metric must be a typed metric")
        if not isinstance(self.uncertainty, (UnknownUncertaintyV1, StandardErrorUncertaintyV1, IntervalUncertaintyV1)):
            raise TypeError("uncertainty must be a typed uncertainty")
        if not isinstance(self.provenance, RunProvenanceV1):
            raise TypeError("provenance must be RunProvenanceV1")
        if isinstance(self.metric, RankOnlyMetricV1) and not isinstance(self.uncertainty, UnknownUncertaintyV1):
            raise ValueError("rank_only observations require unknown uncertainty")
        if isinstance(self.uncertainty, IntervalUncertaintyV1) and hasattr(self.metric, "value"):
            metric_value = Decimal(self.metric.value)
            if not Decimal(self.uncertainty.low) <= metric_value <= Decimal(self.uncertainty.high):
                raise ValueError("uncertainty interval must contain metric value")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "observation_id": self.observation_id,
            "evaluated_configuration_id": self.evaluated_configuration_id,
            "metric": self.metric.to_dict(),
            "uncertainty": self.uncertainty.to_dict(),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationV1":
        payload = _closed(
            value,
            required=("object", "schema_version", "observation_id", "evaluated_configuration_id", "metric", "uncertainty", "provenance"),
        )
        _envelope(payload, cls.object)
        values = _without_envelope(payload)
        values["metric"] = _metric_from_dict(values["metric"])
        values["uncertainty"] = _uncertainty_from_dict(values["uncertainty"])
        values["provenance"] = RunProvenanceV1.from_dict(values["provenance"])
        return cls(**values)


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfigurationPassportV1:
    object: ClassVar[str] = "configuration_passport"
    schema_version: ClassVar[str] = "1"

    entity_kind: str
    canonical_name: str
    revision: str
    interaction_policy: str
    configuration_passport_class: str
    harness: str | None
    scaffold: str | None
    tools: tuple[str, ...] = ()
    quantization: str | None = None
    system_prompt_policy: str | None = None
    environment: str | None = None

    def __post_init__(self) -> None:
        _require_identity_triple(self.entity_kind, self.interaction_policy, self.configuration_passport_class)
        _require_string("canonical_name", self.canonical_name)
        _require_string("revision", self.revision)
        for name in ("harness", "scaffold", "quantization", "system_prompt_policy", "environment"):
            _require_nullable_string(name, getattr(self, name))
        if self.entity_kind == "agent_system":
            _require_string("harness", self.harness)
            _require_string("scaffold", self.scaffold)
        object.__setattr__(self, "tools", _normalize_string_set("tools", self.tools, allow_empty=True))

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "entity_kind": self.entity_kind,
            "canonical_name": self.canonical_name,
            "revision": self.revision,
            "interaction_policy": self.interaction_policy,
            "configuration_passport_class": self.configuration_passport_class,
            "harness": self.harness,
            "scaffold": self.scaffold,
            "tools": list(self.tools),
            "quantization": self.quantization,
            "system_prompt_policy": self.system_prompt_policy,
            "environment": self.environment,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "ConfigurationPassportV1":
        payload = _closed(
            value,
            required=(
                "object", "schema_version", "entity_kind", "canonical_name", "revision",
                "interaction_policy", "configuration_passport_class", "harness", "scaffold",
                "tools", "quantization", "system_prompt_policy", "environment",
            ),
        )
        _envelope(payload, cls.object)
        values = _without_envelope(payload)
        values["tools"] = _array_to_tuple("tools", values["tools"])
        return cls(**values)


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluatedConfigurationV1:
    object: ClassVar[str] = "evaluated_configuration"
    schema_version: ClassVar[str] = "1"

    evaluated_configuration_id: str
    passport: ConfigurationPassportV1

    def __post_init__(self) -> None:
        if not isinstance(self.passport, ConfigurationPassportV1):
            raise TypeError("passport must be ConfigurationPassportV1")
        expected = f"config_{sha256_hex(self.passport.to_dict())}"
        if self.evaluated_configuration_id != expected:
            raise ValueError("evaluated_configuration_id must hash the exact passport")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "evaluated_configuration_id": self.evaluated_configuration_id,
            "passport": self.passport.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "EvaluatedConfigurationV1":
        payload = _closed(value, required=("object", "schema_version", "evaluated_configuration_id", "passport"))
        _envelope(payload, cls.object)
        return cls(
            evaluated_configuration_id=payload["evaluated_configuration_id"],
            passport=ConfigurationPassportV1.from_dict(payload["passport"]),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ContextFactV1:
    context_window_tokens: int
    observed_at: str
    expires_at: str
    source_artifact_id: str

    def __post_init__(self) -> None:
        _require_safe_integer("context_window_tokens", self.context_window_tokens, minimum=1)
        _validate_dated_fact(self.observed_at, self.expires_at, self.source_artifact_id)

    def to_dict(self) -> dict[str, Any]:
        return _fact_dict(self, {"context_window_tokens": self.context_window_tokens})

    @classmethod
    def from_dict(cls, value: Any) -> "ContextFactV1":
        return cls(**_closed(value, required=("context_window_tokens", "observed_at", "expires_at", "source_artifact_id")))


@dataclass(frozen=True, slots=True, kw_only=True)
class AvailabilityFactV1:
    status: str
    observed_at: str
    expires_at: str
    source_artifact_id: str

    def __post_init__(self) -> None:
        _require_enum("status", self.status, {"available", "limited", "unavailable"})
        _validate_dated_fact(self.observed_at, self.expires_at, self.source_artifact_id)

    def to_dict(self) -> dict[str, Any]:
        return _fact_dict(self, {"status": self.status})

    @classmethod
    def from_dict(cls, value: Any) -> "AvailabilityFactV1":
        return cls(**_closed(value, required=("status", "observed_at", "expires_at", "source_artifact_id")))


@dataclass(frozen=True, slots=True, kw_only=True)
class PricingFactV1:
    input_microusd_per_million_tokens: int
    output_microusd_per_million_tokens: int
    observed_at: str
    expires_at: str
    source_artifact_id: str

    def __post_init__(self) -> None:
        _require_safe_integer("input_microusd_per_million_tokens", self.input_microusd_per_million_tokens, minimum=0)
        _require_safe_integer("output_microusd_per_million_tokens", self.output_microusd_per_million_tokens, minimum=0)
        _validate_dated_fact(self.observed_at, self.expires_at, self.source_artifact_id)

    def to_dict(self) -> dict[str, Any]:
        return _fact_dict(
            self,
            {
                "input_microusd_per_million_tokens": self.input_microusd_per_million_tokens,
                "output_microusd_per_million_tokens": self.output_microusd_per_million_tokens,
            },
        )

    @classmethod
    def from_dict(cls, value: Any) -> "PricingFactV1":
        return cls(**_closed(
            value,
            required=(
                "input_microusd_per_million_tokens", "output_microusd_per_million_tokens",
                "observed_at", "expires_at", "source_artifact_id",
            ),
        ))


@dataclass(frozen=True, slots=True, kw_only=True)
class ServingOfferV1:
    object: ClassVar[str] = "serving_offer"
    schema_version: ClassVar[str] = "1"

    serving_offer_id: str
    provider_id: str
    sku: str
    region: str
    context: ContextFactV1
    availability: AvailabilityFactV1
    pricing: PricingFactV1

    def __post_init__(self) -> None:
        for name in ("serving_offer_id", "provider_id", "sku", "region"):
            _require_string(name, getattr(self, name))
        if not self.serving_offer_id.startswith("offer_"):
            raise ValueError("serving_offer_id must start with offer_")
        if not isinstance(self.context, ContextFactV1):
            raise TypeError("context must be ContextFactV1")
        if not isinstance(self.availability, AvailabilityFactV1):
            raise TypeError("availability must be AvailabilityFactV1")
        if not isinstance(self.pricing, PricingFactV1):
            raise TypeError("pricing must be PricingFactV1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "serving_offer_id": self.serving_offer_id,
            "provider_id": self.provider_id,
            "sku": self.sku,
            "region": self.region,
            "context": self.context.to_dict(),
            "availability": self.availability.to_dict(),
            "pricing": self.pricing.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "ServingOfferV1":
        payload = _closed(value, required=("object", "schema_version", "serving_offer_id", "provider_id", "sku", "region", "context", "availability", "pricing"))
        _envelope(payload, cls.object)
        return cls(
            serving_offer_id=payload["serving_offer_id"],
            provider_id=payload["provider_id"],
            sku=payload["sku"],
            region=payload["region"],
            context=ContextFactV1.from_dict(payload["context"]),
            availability=AvailabilityFactV1.from_dict(payload["availability"]),
            pricing=PricingFactV1.from_dict(payload["pricing"]),
        )

    def is_decision_eligible(self, link: "EvaluationToOfferLinkV1", *, as_of: str) -> bool:
        instant = _parse_timestamp("as_of", as_of)
        if not isinstance(link, EvaluationToOfferLinkV1) or link.serving_offer_id != self.serving_offer_id:
            return False
        if not link.is_eligible(as_of=as_of) or self.availability.status != "available":
            return False
        return all(
            _parse_timestamp("observed_at", fact.observed_at) <= instant < _parse_timestamp("expires_at", fact.expires_at)
            for fact in (self.context, self.availability, self.pricing)
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluationToOfferLinkV1:
    object: ClassVar[str] = "evaluation_to_offer_link"
    schema_version: ClassVar[str] = "1"

    evaluation_to_offer_link_id: str
    evaluated_configuration_id: str
    serving_offer_id: str
    compatibility: str
    evidence_source_artifact_id: str
    observed_at: str
    expires_at: str
    review_state: str

    def __post_init__(self) -> None:
        _require_string("evaluation_to_offer_link_id", self.evaluation_to_offer_link_id)
        if not self.evaluation_to_offer_link_id.startswith("link_"):
            raise ValueError("evaluation_to_offer_link_id must start with link_")
        _require_pattern("evaluated_configuration_id", self.evaluated_configuration_id, _CONFIGURATION_ID_RE)
        _require_string("serving_offer_id", self.serving_offer_id)
        if not self.serving_offer_id.startswith("offer_"):
            raise ValueError("serving_offer_id must start with offer_")
        _require_enum("compatibility", self.compatibility, {"exact", "incompatible", "unresolved"})
        _require_pattern("evidence_source_artifact_id", self.evidence_source_artifact_id, _ARTIFACT_ID_RE)
        observed = _parse_timestamp("observed_at", self.observed_at)
        expires = _parse_timestamp("expires_at", self.expires_at)
        if expires <= observed:
            raise ValueError("expires_at must be after observed_at")
        _require_enum("review_state", self.review_state, {"pending", "approved", "rejected"})

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "evaluation_to_offer_link_id": self.evaluation_to_offer_link_id,
            "evaluated_configuration_id": self.evaluated_configuration_id,
            "serving_offer_id": self.serving_offer_id,
            "compatibility": self.compatibility,
            "evidence_source_artifact_id": self.evidence_source_artifact_id,
            "observed_at": self.observed_at,
            "expires_at": self.expires_at,
            "review_state": self.review_state,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "EvaluationToOfferLinkV1":
        payload = _closed(
            value,
            required=("object", "schema_version", "evaluation_to_offer_link_id", "evaluated_configuration_id", "serving_offer_id", "compatibility", "evidence_source_artifact_id", "observed_at", "expires_at", "review_state"),
        )
        _envelope(payload, cls.object)
        return cls(**_without_envelope(payload))

    def is_eligible(self, *, as_of: str) -> bool:
        instant = _parse_timestamp("as_of", as_of)
        return (
            self.compatibility == "exact"
            and self.review_state == "approved"
            and _parse_timestamp("observed_at", self.observed_at) <= instant < _parse_timestamp("expires_at", self.expires_at)
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionQueryV1:
    object: ClassVar[str] = "decision_query"
    schema_version: ClassVar[str] = "1"

    cell_id: str
    ranking_group_id: str
    entity_kind: str
    interaction_policy: str
    configuration_passport_class: str
    objective: str
    provider_ids: tuple[str, ...] | None = None
    regions: tuple[str, ...] | None = None
    minimum_context_tokens: int | None = None
    input_tokens_per_request: int | None = None
    output_tokens_per_request: int | None = None
    requests_per_month: int | None = None
    monthly_budget_microusd: int | None = None

    def __post_init__(self) -> None:
        _require_string("cell_id", self.cell_id)
        _require_string("ranking_group_id", self.ranking_group_id)
        _require_identity_triple(self.entity_kind, self.interaction_policy, self.configuration_passport_class)
        _require_enum("objective", self.objective, {"capability_top_set", "lowest_cost_within_top_set"})
        if self.provider_ids is not None:
            object.__setattr__(self, "provider_ids", _normalize_string_set("provider_ids", self.provider_ids))
        if self.regions is not None:
            object.__setattr__(self, "regions", _normalize_string_set("regions", self.regions))
        _require_nullable_safe_integer("minimum_context_tokens", self.minimum_context_tokens, minimum=1)
        _require_nullable_safe_integer("input_tokens_per_request", self.input_tokens_per_request, minimum=0)
        _require_nullable_safe_integer("output_tokens_per_request", self.output_tokens_per_request, minimum=0)
        _require_nullable_safe_integer("requests_per_month", self.requests_per_month, minimum=1)
        _require_nullable_safe_integer("monthly_budget_microusd", self.monthly_budget_microusd, minimum=0)
        usage = (self.input_tokens_per_request, self.output_tokens_per_request, self.requests_per_month)
        if any(value is not None for value in usage) and any(value is None for value in usage):
            raise ValueError("input_tokens_per_request, output_tokens_per_request, and requests_per_month must be supplied together")
        if self.objective == "lowest_cost_within_top_set" and any(value is None for value in usage):
            raise ValueError("lowest_cost_within_top_set requires input_tokens_per_request, output_tokens_per_request, and requests_per_month")
        if self.monthly_budget_microusd is not None and any(value is None for value in usage):
            raise ValueError("monthly_budget_microusd requires input_tokens_per_request, output_tokens_per_request, and requests_per_month")

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "object": self.object,
            "schema_version": self.schema_version,
            "cell_id": self.cell_id,
            "ranking_group_id": self.ranking_group_id,
            "entity_kind": self.entity_kind,
            "interaction_policy": self.interaction_policy,
            "configuration_passport_class": self.configuration_passport_class,
            "objective": self.objective,
        }
        for name in (
            "provider_ids", "regions", "minimum_context_tokens", "input_tokens_per_request",
            "output_tokens_per_request", "requests_per_month", "monthly_budget_microusd",
        ):
            value = getattr(self, name)
            if value is not None:
                payload[name] = list(value) if isinstance(value, tuple) else value
        return payload

    def canonical_json(self) -> str:
        return canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionQueryV1":
        required = (
            "object", "schema_version", "cell_id", "ranking_group_id", "entity_kind",
            "interaction_policy", "configuration_passport_class", "objective",
        )
        optional = (
            "provider_ids", "regions", "minimum_context_tokens", "input_tokens_per_request",
            "output_tokens_per_request", "requests_per_month", "monthly_budget_microusd",
        )
        payload = _closed(value, required=required, optional=optional)
        _envelope(payload, cls.object)
        for name in optional:
            if name in payload and payload[name] is None:
                raise ValueError(f"{name} must not be null; omit it instead")
        values = _without_envelope(payload)
        for name in ("provider_ids", "regions"):
            if name in values:
                values[name] = _array_to_tuple(name, values[name])
        return cls(**values)


@dataclass(frozen=True, slots=True, kw_only=True)
class PublicationSnapshotRefV1:
    publication_snapshot_id: str
    ranking_group_id: str
    manifest_version: str
    published_at: str

    def __post_init__(self) -> None:
        _require_pattern("publication_snapshot_id", self.publication_snapshot_id, re.compile(r"^snapshot_[0-9a-f]{64}$"))
        _require_string("ranking_group_id", self.ranking_group_id)
        if not isinstance(self.manifest_version, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}\.[1-9]\d*", self.manifest_version):
            raise ValueError("manifest_version must be YYYY-MM-DD.N")
        _parse_timestamp("published_at", self.published_at)

    def to_dict(self) -> dict[str, str]:
        return {
            "publication_snapshot_id": self.publication_snapshot_id,
            "ranking_group_id": self.ranking_group_id,
            "manifest_version": self.manifest_version,
            "published_at": self.published_at,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "PublicationSnapshotRefV1":
        return cls(**_closed(value, required=("publication_snapshot_id", "ranking_group_id", "manifest_version", "published_at")))


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionSelectionV1:
    evaluated_configuration_id: str
    serving_offer_id: str | None
    capability_rank: int
    estimated_monthly_cost_microusd: int | None

    def __post_init__(self) -> None:
        _require_pattern("evaluated_configuration_id", self.evaluated_configuration_id, _CONFIGURATION_ID_RE)
        _require_nullable_string("serving_offer_id", self.serving_offer_id)
        if self.serving_offer_id is not None and not self.serving_offer_id.startswith("offer_"):
            raise ValueError("serving_offer_id must start with offer_")
        _require_safe_integer("capability_rank", self.capability_rank, minimum=1)
        _require_nullable_safe_integer("estimated_monthly_cost_microusd", self.estimated_monthly_cost_microusd, minimum=0)
        if self.estimated_monthly_cost_microusd is not None and self.serving_offer_id is None:
            raise ValueError("serving_offer_id is required when estimated_monthly_cost_microusd is present")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluated_configuration_id": self.evaluated_configuration_id,
            "serving_offer_id": self.serving_offer_id,
            "capability_rank": self.capability_rank,
            "estimated_monthly_cost_microusd": self.estimated_monthly_cost_microusd,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionSelectionV1":
        return cls(**_closed(value, required=("evaluated_configuration_id", "serving_offer_id", "capability_rank", "estimated_monthly_cost_microusd")))


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionExclusionV1:
    evaluated_configuration_id: str
    code: str
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_pattern("evaluated_configuration_id", self.evaluated_configuration_id, _CONFIGURATION_ID_RE)
        _require_enum("code", self.code, EXCLUSION_CODES)
        object.__setattr__(self, "evidence_ids", _normalize_string_set("evidence_ids", self.evidence_ids))

    def to_dict(self) -> dict[str, Any]:
        return {"evaluated_configuration_id": self.evaluated_configuration_id, "code": self.code, "evidence_ids": list(self.evidence_ids)}

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionExclusionV1":
        payload = _closed(value, required=("evaluated_configuration_id", "code", "evidence_ids"))
        payload["evidence_ids"] = _array_to_tuple("evidence_ids", payload["evidence_ids"])
        return cls(**payload)


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionFreshnessV1:
    observed_at: str
    expires_at: str

    def __post_init__(self) -> None:
        observed = _parse_timestamp("observed_at", self.observed_at)
        expires = _parse_timestamp("expires_at", self.expires_at)
        if expires <= observed:
            raise ValueError("expires_at must be after observed_at")

    def to_dict(self) -> dict[str, str]:
        return {"observed_at": self.observed_at, "expires_at": self.expires_at}

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionFreshnessV1":
        return cls(**_closed(value, required=("observed_at", "expires_at")))


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionReasonV1:
    reason_type: str
    code: str
    subject_id: str
    predicate: str
    axis: str
    observed_value: str
    unit: str
    threshold: str | None
    evidence_ids: tuple[str, ...]
    freshness: DecisionFreshnessV1
    caveat_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_enum("reason_type", self.reason_type, {"best_when", "avoid_when"})
        _require_enum("code", self.code, REASON_CODES)
        _require_string("subject_id", self.subject_id)
        _require_enum("predicate", self.predicate, REASON_PREDICATES)
        _require_enum("axis", self.axis, REASON_AXES)
        _require_string("observed_value", self.observed_value)
        _require_enum("unit", self.unit, REASON_UNITS)
        _require_nullable_string("threshold", self.threshold)
        if self.unit not in {"status", "timestamp", "provider_id", "region_id"}:
            _require_decimal("observed_value", self.observed_value)
            if self.threshold is not None:
                _require_decimal("threshold", self.threshold)
        object.__setattr__(self, "evidence_ids", _normalize_string_set("evidence_ids", self.evidence_ids))
        if not isinstance(self.freshness, DecisionFreshnessV1):
            raise TypeError("freshness must be DecisionFreshnessV1")
        object.__setattr__(self, "caveat_codes", _normalize_enum_set("caveat_codes", self.caveat_codes, CAVEAT_CODES, allow_empty=True))
        expected_shape = {
            "strongest_capability_evidence": ("capability", "score", "gte"),
            "within_capability_top_set": ("capability", "score", "within_top_set"),
            "provider_constraint_match": ("provider", "provider_id", "eq"),
            "region_constraint_match": ("region", "region_id", "eq"),
            "lowest_verified_cost": ("monthly_cost", "microusd_per_month", "eq"),
            "budget_constraint_met": ("monthly_cost", "microusd_per_month", "lte"),
            "budget_exceeded": ("monthly_cost", "microusd_per_month", "gt"),
            "context_requirement_met": ("context", "tokens", "gte"),
            "insufficient_evidence": ("capability", "status", "unavailable"),
            "serving_offer_unverified": ("availability", "status", "unavailable"),
            "stale_evidence": ("freshness", "timestamp", "lt"),
        }.get(self.code)
        if expected_shape is not None and (self.axis, self.unit, self.predicate) != expected_shape:
            raise ValueError(
                f"{self.code} requires axis={expected_shape[0]}, unit={expected_shape[1]}, predicate={expected_shape[2]}"
            )
        comparison_predicates = {"eq", "ne", "lt", "lte", "gt", "gte"}
        if self.predicate in comparison_predicates and self.threshold is None:
            raise ValueError(f"{self.predicate} predicate requires threshold")
        if self.predicate in {"within_top_set", "unavailable"} and self.threshold is not None:
            raise ValueError(f"{self.predicate} predicate requires a null threshold")
        positive = {
            "strongest_capability_evidence", "within_capability_top_set", "lowest_verified_cost",
            "budget_constraint_met", "provider_constraint_match", "region_constraint_match",
            "context_requirement_met",
        }
        if (self.code in positive) != (self.reason_type == "best_when"):
            expected_type = "best_when" if self.code in positive else "avoid_when"
            raise ValueError(f"{self.code} requires reason_type={expected_type}")
        if self.unit == "timestamp":
            _parse_timestamp("observed_value", self.observed_value)
            if self.threshold is not None:
                _parse_timestamp("threshold", self.threshold)
        if self.unit == "status":
            _require_enum(
                "observed_value",
                self.observed_value,
                {"available", "limited", "unavailable", "sufficient", "insufficient", "fresh", "stale"},
            )
            if self.threshold is not None:
                _require_enum(
                    "threshold",
                    self.threshold,
                    {"available", "limited", "unavailable", "sufficient", "insufficient", "fresh", "stale"},
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reason_type": self.reason_type,
            "code": self.code,
            "subject_id": self.subject_id,
            "predicate": self.predicate,
            "axis": self.axis,
            "observed_value": self.observed_value,
            "unit": self.unit,
            "threshold": self.threshold,
            "evidence_ids": list(self.evidence_ids),
            "freshness": self.freshness.to_dict(),
            "caveat_codes": list(self.caveat_codes),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionReasonV1":
        payload = _closed(value, required=("reason_type", "code", "subject_id", "predicate", "axis", "observed_value", "unit", "threshold", "evidence_ids", "freshness", "caveat_codes"))
        payload["evidence_ids"] = _array_to_tuple("evidence_ids", payload["evidence_ids"])
        payload["caveat_codes"] = _array_to_tuple("caveat_codes", payload["caveat_codes"])
        payload["freshness"] = DecisionFreshnessV1.from_dict(payload["freshness"])
        return cls(**payload)


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionSensitivityV1:
    scenario: str
    stable: bool
    selected_configuration_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_enum("scenario", self.scenario, SENSITIVITY_SCENARIOS)
        if not isinstance(self.stable, bool):
            raise TypeError("stable must be a boolean")
        identifiers = _normalize_string_set("selected_configuration_ids", self.selected_configuration_ids, allow_empty=True)
        for identifier in identifiers:
            _require_pattern("selected_configuration_ids item", identifier, _CONFIGURATION_ID_RE)
        object.__setattr__(self, "selected_configuration_ids", identifiers)

    def to_dict(self) -> dict[str, Any]:
        return {"scenario": self.scenario, "stable": self.stable, "selected_configuration_ids": list(self.selected_configuration_ids)}

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionSensitivityV1":
        payload = _closed(value, required=("scenario", "stable", "selected_configuration_ids"))
        payload["selected_configuration_ids"] = _array_to_tuple("selected_configuration_ids", payload["selected_configuration_ids"])
        return cls(**payload)


@dataclass(frozen=True, slots=True, kw_only=True)
class ObservationEvidenceV1:
    kind: ClassVar[str] = "observation"
    evidence_id: str
    observation: ObservationV1

    def __post_init__(self) -> None:
        _require_string("evidence_id", self.evidence_id)
        if not isinstance(self.observation, ObservationV1):
            raise TypeError("observation must be ObservationV1")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "evidence_id": self.evidence_id, "observation": self.observation.to_dict()}

    @classmethod
    def from_dict(cls, value: Any) -> "ObservationEvidenceV1":
        payload = _closed(value, required=("kind", "evidence_id", "observation"))
        _kind(payload, cls.kind)
        return cls(evidence_id=payload["evidence_id"], observation=ObservationV1.from_dict(payload["observation"]))


@dataclass(frozen=True, slots=True, kw_only=True)
class ServingOfferEvidenceV1:
    kind: ClassVar[str] = "serving_offer"
    evidence_id: str
    serving_offer: ServingOfferV1

    def __post_init__(self) -> None:
        _require_string("evidence_id", self.evidence_id)
        if not isinstance(self.serving_offer, ServingOfferV1):
            raise TypeError("serving_offer must be ServingOfferV1")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "evidence_id": self.evidence_id, "serving_offer": self.serving_offer.to_dict()}

    @classmethod
    def from_dict(cls, value: Any) -> "ServingOfferEvidenceV1":
        payload = _closed(value, required=("kind", "evidence_id", "serving_offer"))
        _kind(payload, cls.kind)
        return cls(evidence_id=payload["evidence_id"], serving_offer=ServingOfferV1.from_dict(payload["serving_offer"]))


@dataclass(frozen=True, slots=True, kw_only=True)
class EvaluationToOfferLinkEvidenceV1:
    kind: ClassVar[str] = "evaluation_to_offer_link"
    evidence_id: str
    evaluation_to_offer_link: EvaluationToOfferLinkV1

    def __post_init__(self) -> None:
        _require_string("evidence_id", self.evidence_id)
        if not isinstance(self.evaluation_to_offer_link, EvaluationToOfferLinkV1):
            raise TypeError("evaluation_to_offer_link must be EvaluationToOfferLinkV1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "evidence_id": self.evidence_id,
            "evaluation_to_offer_link": self.evaluation_to_offer_link.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "EvaluationToOfferLinkEvidenceV1":
        payload = _closed(value, required=("kind", "evidence_id", "evaluation_to_offer_link"))
        _kind(payload, cls.kind)
        return cls(
            evidence_id=payload["evidence_id"],
            evaluation_to_offer_link=EvaluationToOfferLinkV1.from_dict(payload["evaluation_to_offer_link"]),
        )


DecisionEvidenceV1 = ObservationEvidenceV1 | ServingOfferEvidenceV1 | EvaluationToOfferLinkEvidenceV1


@dataclass(frozen=True, slots=True, kw_only=True)
class DecisionReceiptV1:
    object: ClassVar[str] = "decision_receipt"
    schema_version: ClassVar[str] = "1"

    receipt_id: str
    query: DecisionQueryV1
    publication_snapshot: PublicationSnapshotRefV1
    methodology_version: str
    decided_at: str
    outcome: str
    selections: tuple[DecisionSelectionV1, ...]
    exclusions: tuple[DecisionExclusionV1, ...]
    reasons: tuple[DecisionReasonV1, ...]
    sensitivity: tuple[DecisionSensitivityV1, ...]
    evidence: tuple[DecisionEvidenceV1, ...]
    freshness: DecisionFreshnessV1
    abstention_reason: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.query, DecisionQueryV1):
            raise TypeError("query must be DecisionQueryV1")
        if not isinstance(self.publication_snapshot, PublicationSnapshotRefV1):
            raise TypeError("publication_snapshot must be PublicationSnapshotRefV1")
        if self.publication_snapshot.ranking_group_id != self.query.ranking_group_id:
            raise ValueError("publication_snapshot ranking_group_id must match query")
        if not isinstance(self.methodology_version, str) or not _METHODOLOGY_RE.fullmatch(self.methodology_version):
            raise ValueError("methodology_version has an invalid public format")
        decided_at = _parse_timestamp("decided_at", self.decided_at)
        if decided_at < _parse_timestamp("published_at", self.publication_snapshot.published_at):
            raise ValueError("decided_at must be on or after publication_snapshot.published_at")
        _require_enum("outcome", self.outcome, {"top_set", "abstain"})
        object.__setattr__(self, "selections", _normalize_typed_records("selections", self.selections, DecisionSelectionV1, lambda row: (row.evaluated_configuration_id,)))
        object.__setattr__(self, "exclusions", _normalize_typed_records("exclusions", self.exclusions, DecisionExclusionV1, lambda row: (row.evaluated_configuration_id, row.code)))
        object.__setattr__(self, "reasons", _normalize_typed_records("reasons", self.reasons, DecisionReasonV1, lambda row: (row.reason_type, row.code, row.subject_id, row.axis)))
        object.__setattr__(self, "sensitivity", _normalize_typed_records("sensitivity", self.sensitivity, DecisionSensitivityV1, lambda row: row.scenario))
        evidence_types = (ObservationEvidenceV1, ServingOfferEvidenceV1, EvaluationToOfferLinkEvidenceV1)
        object.__setattr__(self, "evidence", _normalize_typed_records("evidence", self.evidence, evidence_types, lambda row: row.evidence_id))
        evidence_targets = [_evidence_target(row) for row in self.evidence]
        if len(set(evidence_targets)) != len(evidence_targets):
            raise ValueError("evidence targets must be unique")
        if not isinstance(self.freshness, DecisionFreshnessV1):
            raise TypeError("freshness must be DecisionFreshnessV1")
        if not (
            _parse_timestamp("freshness.observed_at", self.freshness.observed_at)
            <= decided_at
            < _parse_timestamp("freshness.expires_at", self.freshness.expires_at)
        ):
            raise ValueError("receipt freshness must contain decided_at")
        if self.outcome == "top_set":
            if not self.selections:
                raise ValueError("top_set outcome requires at least one selection")
            if self.abstention_reason is not None:
                raise ValueError("abstention_reason must be null for top_set")
            if not self.reasons:
                raise ValueError("top_set outcome requires reasons")
            if not self.evidence:
                raise ValueError("top_set outcome requires evidence")
        else:
            if self.selections:
                raise ValueError("abstain outcome must not contain selections")
            _require_enum("abstention_reason", self.abstention_reason, ABSTENTION_REASONS)
        if self.outcome == "top_set" and self.query.objective == "lowest_cost_within_top_set":
            for selection in self.selections:
                if selection.serving_offer_id is None:
                    raise ValueError("lowest_cost_within_top_set requires serving_offer_id for every selection")
                if selection.estimated_monthly_cost_microusd is None:
                    raise ValueError(
                        "lowest_cost_within_top_set requires estimated_monthly_cost_microusd for every selection"
                    )
                if (
                    self.query.monthly_budget_microusd is not None
                    and selection.estimated_monthly_cost_microusd > self.query.monthly_budget_microusd
                ):
                    raise ValueError("selection cost must not exceed monthly_budget_microusd")
            selected_costs = {
                selection.estimated_monthly_cost_microusd
                for selection in self.selections
            }
            if len(selected_costs) != 1:
                raise ValueError(
                    "lowest_cost_within_top_set selections must share one equal minimum cost"
                )
        selected_ids = {row.evaluated_configuration_id for row in self.selections}
        excluded_ids = {row.evaluated_configuration_id for row in self.exclusions}
        if selected_ids & excluded_ids:
            raise ValueError("a configuration cannot be both selected and excluded")
        if self.outcome == "top_set":
            leave_one_out = next(
                (row for row in self.sensitivity if row.scenario == "leave_one_family_out"),
                None,
            )
            if (
                leave_one_out is None
                or not leave_one_out.stable
                or set(leave_one_out.selected_configuration_ids) != selected_ids
            ):
                raise ValueError(
                    "every top_set requires stable leave_one_family_out sensitivity for the exact selected set"
                )
            if self.query.objective == "lowest_cost_within_top_set":
                for scenario in {"price_plus_20_percent", "price_minus_20_percent", "usage_double"}:
                    if not any(row.scenario == scenario for row in self.sensitivity):
                        raise ValueError(f"lowest_cost_within_top_set requires {scenario} sensitivity")
            for sensitivity in self.sensitivity:
                sensitivity_ids = set(sensitivity.selected_configuration_ids)
                if sensitivity.stable and sensitivity_ids != selected_ids:
                    raise ValueError("stable sensitivity must preserve the exact selected configuration set")
                if not sensitivity.stable and sensitivity_ids == selected_ids:
                    raise ValueError("unstable sensitivity must change the selected configuration set")
                known_ids = selected_ids | excluded_ids
                if not sensitivity_ids <= known_ids:
                    raise ValueError("sensitivity selected_configuration_ids must be known decision candidates")
            uncovered = {
                selection.evaluated_configuration_id
                for selection in self.selections
                if not any(
                    reason.subject_id
                    in {selection.evaluated_configuration_id, selection.serving_offer_id}
                    for reason in self.reasons
                )
            }
            if uncovered:
                raise ValueError("reasons must cover every selected configuration or serving offer")
            _validate_selected_decision_evidence(self, decided_at=decided_at)
        evidence_ids = {row.evidence_id for row in self.evidence}
        cited_ids = {
            evidence_id
            for row in (*self.exclusions, *self.reasons)
            for evidence_id in row.evidence_ids
        }
        if not cited_ids <= evidence_ids:
            raise ValueError("every cited evidence_id must be present in evidence")
        evidence_by_id = {row.evidence_id: row for row in self.evidence}
        for exclusion in self.exclusions:
            if not exclusion.evidence_ids or not all(
                _evidence_configuration_id(evidence_by_id[evidence_id])
                == exclusion.evaluated_configuration_id
                for evidence_id in exclusion.evidence_ids
                if evidence_id in evidence_by_id
            ):
                raise ValueError("exclusion evidence must concern its excluded configuration")
        expected = f"receipt_{sha256_hex(self.to_body_dict())}"
        if self.receipt_id != expected:
            raise ValueError("receipt_id must hash the full receipt body except receipt_id")

    @classmethod
    def create(
        cls,
        *,
        query: DecisionQueryV1,
        publication_snapshot: PublicationSnapshotRefV1,
        methodology_version: str,
        decided_at: str,
        outcome: str,
        selections: tuple[DecisionSelectionV1, ...],
        exclusions: tuple[DecisionExclusionV1, ...],
        reasons: tuple[DecisionReasonV1, ...],
        sensitivity: tuple[DecisionSensitivityV1, ...],
        evidence: tuple[DecisionEvidenceV1, ...],
        freshness: DecisionFreshnessV1,
        abstention_reason: str | None,
    ) -> "DecisionReceiptV1":
        values = {
            "query": query,
            "publication_snapshot": publication_snapshot,
            "methodology_version": methodology_version,
            "decided_at": decided_at,
            "outcome": outcome,
            "selections": selections,
            "exclusions": exclusions,
            "reasons": reasons,
            "sensitivity": sensitivity,
            "evidence": evidence,
            "freshness": freshness,
            "abstention_reason": abstention_reason,
        }
        body = _receipt_body_from_values(values)
        return cls(receipt_id=f"receipt_{sha256_hex(body)}", **values)

    def to_body_dict(self) -> dict[str, Any]:
        return _receipt_body_from_values({
            "query": self.query,
            "publication_snapshot": self.publication_snapshot,
            "methodology_version": self.methodology_version,
            "decided_at": self.decided_at,
            "outcome": self.outcome,
            "selections": self.selections,
            "exclusions": self.exclusions,
            "reasons": self.reasons,
            "sensitivity": self.sensitivity,
            "evidence": self.evidence,
            "freshness": self.freshness,
            "abstention_reason": self.abstention_reason,
        })

    def to_dict(self) -> dict[str, Any]:
        return {**self.to_body_dict(), "receipt_id": self.receipt_id}

    @classmethod
    def from_dict(cls, value: Any) -> "DecisionReceiptV1":
        payload = _closed(
            value,
            required=(
                "object", "schema_version", "receipt_id", "query", "publication_snapshot",
                "methodology_version", "decided_at", "outcome", "selections", "exclusions", "reasons",
                "sensitivity", "evidence", "freshness", "abstention_reason",
            ),
        )
        _envelope(payload, cls.object)
        return cls(
            receipt_id=payload["receipt_id"],
            query=DecisionQueryV1.from_dict(payload["query"]),
            publication_snapshot=PublicationSnapshotRefV1.from_dict(payload["publication_snapshot"]),
            methodology_version=payload["methodology_version"],
            decided_at=payload["decided_at"],
            outcome=payload["outcome"],
            selections=tuple(DecisionSelectionV1.from_dict(row) for row in _array("selections", payload["selections"])),
            exclusions=tuple(DecisionExclusionV1.from_dict(row) for row in _array("exclusions", payload["exclusions"])),
            reasons=tuple(DecisionReasonV1.from_dict(row) for row in _array("reasons", payload["reasons"])),
            sensitivity=tuple(DecisionSensitivityV1.from_dict(row) for row in _array("sensitivity", payload["sensitivity"])),
            evidence=tuple(_decision_evidence_from_dict(row) for row in _array("evidence", payload["evidence"])),
            freshness=DecisionFreshnessV1.from_dict(payload["freshness"]),
            abstention_reason=payload["abstention_reason"],
        )


def _receipt_body_from_values(values: Mapping[str, Any]) -> dict[str, Any]:
    selections = sorted(values["selections"], key=lambda row: _portable_sort_key((row.evaluated_configuration_id,)))
    exclusions = sorted(values["exclusions"], key=lambda row: _portable_sort_key((row.evaluated_configuration_id, row.code)))
    reasons = sorted(values["reasons"], key=lambda row: _portable_sort_key((row.reason_type, row.code, row.subject_id, row.axis)))
    sensitivity = sorted(values["sensitivity"], key=lambda row: _portable_sort_key((row.scenario,)))
    evidence = sorted(values["evidence"], key=lambda row: _portable_sort_key((row.evidence_id,)))
    return {
        "object": DecisionReceiptV1.object,
        "schema_version": DecisionReceiptV1.schema_version,
        "query": values["query"].to_dict(),
        "publication_snapshot": values["publication_snapshot"].to_dict(),
        "methodology_version": values["methodology_version"],
        "decided_at": values["decided_at"],
        "outcome": values["outcome"],
        "selections": [row.to_dict() for row in selections],
        "exclusions": [row.to_dict() for row in exclusions],
        "reasons": [row.to_dict() for row in reasons],
        "sensitivity": [row.to_dict() for row in sensitivity],
        "evidence": [row.to_dict() for row in evidence],
        "freshness": values["freshness"].to_dict(),
        "abstention_reason": values["abstention_reason"],
    }


def _decision_evidence_from_dict(value: Any) -> DecisionEvidenceV1:
    payload = _mapping(value)
    parser = {
        "observation": ObservationEvidenceV1.from_dict,
        "serving_offer": ServingOfferEvidenceV1.from_dict,
        "evaluation_to_offer_link": EvaluationToOfferLinkEvidenceV1.from_dict,
    }.get(payload.get("kind"))
    if parser is None:
        raise ValueError("evidence.kind must be observation, serving_offer, or evaluation_to_offer_link")
    return parser(payload)


def _evidence_target(evidence: DecisionEvidenceV1) -> tuple[str, ...]:
    if isinstance(evidence, ObservationEvidenceV1):
        return evidence.kind, evidence.observation.observation_id
    if isinstance(evidence, ServingOfferEvidenceV1):
        return evidence.kind, evidence.serving_offer.serving_offer_id
    link = evidence.evaluation_to_offer_link
    return evidence.kind, link.evaluated_configuration_id, link.serving_offer_id


def _evidence_configuration_id(evidence: DecisionEvidenceV1) -> str | None:
    if isinstance(evidence, ObservationEvidenceV1):
        return evidence.observation.evaluated_configuration_id
    if isinstance(evidence, EvaluationToOfferLinkEvidenceV1):
        return evidence.evaluation_to_offer_link.evaluated_configuration_id
    return None


def _validate_selected_decision_evidence(
    receipt: DecisionReceiptV1,
    *,
    decided_at: datetime,
) -> None:
    evidence_by_id = {row.evidence_id: row for row in receipt.evidence}
    for reason in receipt.reasons:
        if reason.reason_type == "best_when" and not (
            _parse_timestamp("reason.freshness.observed_at", reason.freshness.observed_at)
            <= decided_at
            < _parse_timestamp("reason.freshness.expires_at", reason.freshness.expires_at)
        ):
            raise ValueError("positive reason freshness must contain decided_at")

    for selection in receipt.selections:
        capability_reasons = [
            reason
            for reason in receipt.reasons
            if reason.subject_id == selection.evaluated_configuration_id
            and reason.code in {"strongest_capability_evidence", "within_capability_top_set"}
        ]
        if not capability_reasons or not all(
            reason.evidence_ids
            and all(
                isinstance(evidence_by_id.get(evidence_id), ObservationEvidenceV1)
                and evidence_by_id[evidence_id].observation.evaluated_configuration_id
                == selection.evaluated_configuration_id
                for evidence_id in reason.evidence_ids
            )
            for reason in capability_reasons
        ):
            raise ValueError("every selected configuration requires matching capability observation evidence")

        query = receipt.query
        offer_required = any(
            (
                selection.serving_offer_id is not None,
                query.objective == "lowest_cost_within_top_set",
                query.provider_ids is not None,
                query.regions is not None,
                query.minimum_context_tokens is not None,
                query.monthly_budget_microusd is not None,
            )
        )
        if not offer_required:
            continue
        if selection.serving_offer_id is None:
            raise ValueError("selected configuration requires serving_offer_id for applied offer constraints")
        offer_evidence = next(
            (
                row
                for row in receipt.evidence
                if isinstance(row, ServingOfferEvidenceV1)
                and row.serving_offer.serving_offer_id == selection.serving_offer_id
            ),
            None,
        )
        link_evidence = next(
            (
                row
                for row in receipt.evidence
                if isinstance(row, EvaluationToOfferLinkEvidenceV1)
                and row.evaluation_to_offer_link.evaluated_configuration_id
                == selection.evaluated_configuration_id
                and row.evaluation_to_offer_link.serving_offer_id == selection.serving_offer_id
            ),
            None,
        )
        if offer_evidence is None:
            raise ValueError("selected serving offer requires full typed serving-offer evidence")
        if link_evidence is None:
            raise ValueError("selected serving offer requires full typed offer-link evidence")
        offer = offer_evidence.serving_offer
        link = link_evidence.evaluation_to_offer_link
        if not offer.is_decision_eligible(link, as_of=receipt.decided_at):
            raise ValueError("selected offer and link must be exact, approved, available, and current at decided_at")
        if query.provider_ids is not None and offer.provider_id not in query.provider_ids:
            raise ValueError("selected offer provider must satisfy provider_ids")
        if query.regions is not None and offer.region not in query.regions:
            raise ValueError("selected offer region must satisfy regions")
        if (
            query.minimum_context_tokens is not None
            and offer.context.context_window_tokens < query.minimum_context_tokens
        ):
            raise ValueError("selected offer must satisfy minimum_context_tokens")

        computed_cost = None
        if query.input_tokens_per_request is not None:
            computed_cost = _monthly_cost_microusd(query, offer)
            if selection.estimated_monthly_cost_microusd != computed_cost:
                raise ValueError("estimated_monthly_cost_microusd must equal the computed monthly cost")
            if query.monthly_budget_microusd is not None and computed_cost > query.monthly_budget_microusd:
                raise ValueError("computed monthly cost must not exceed monthly_budget_microusd")
        elif selection.estimated_monthly_cost_microusd is not None:
            raise ValueError("estimated_monthly_cost_microusd must be null when query usage is omitted")

        required_evidence_ids = {offer_evidence.evidence_id, link_evidence.evidence_id}
        offer_observed_at = max(
            offer.context.observed_at,
            offer.availability.observed_at,
            offer.pricing.observed_at,
            link.observed_at,
        )
        offer_expires_at = min(
            offer.context.expires_at,
            offer.availability.expires_at,
            offer.pricing.expires_at,
            link.expires_at,
        )
        if query.objective == "lowest_cost_within_top_set":
            _require_offer_reason(
                receipt,
                selection,
                code="lowest_verified_cost",
                observed_value=str(computed_cost),
                threshold=str(computed_cost),
                evidence_ids=required_evidence_ids,
                observed_at=offer_observed_at,
                expires_at=offer_expires_at,
            )
        if query.monthly_budget_microusd is not None:
            _require_offer_reason(
                receipt,
                selection,
                code="budget_constraint_met",
                observed_value=str(computed_cost),
                threshold=str(query.monthly_budget_microusd),
                evidence_ids=required_evidence_ids,
                observed_at=offer_observed_at,
                expires_at=offer_expires_at,
            )
        if query.provider_ids is not None:
            _require_offer_reason(
                receipt,
                selection,
                code="provider_constraint_match",
                observed_value=offer.provider_id,
                threshold=offer.provider_id,
                evidence_ids=required_evidence_ids,
                observed_at=offer_observed_at,
                expires_at=offer_expires_at,
            )
        if query.regions is not None:
            _require_offer_reason(
                receipt,
                selection,
                code="region_constraint_match",
                observed_value=offer.region,
                threshold=offer.region,
                evidence_ids=required_evidence_ids,
                observed_at=offer_observed_at,
                expires_at=offer_expires_at,
            )
        if query.minimum_context_tokens is not None:
            _require_offer_reason(
                receipt,
                selection,
                code="context_requirement_met",
                observed_value=str(offer.context.context_window_tokens),
                threshold=str(query.minimum_context_tokens),
                evidence_ids=required_evidence_ids,
                observed_at=offer_observed_at,
                expires_at=offer_expires_at,
            )

    positive_reasons = [row for row in receipt.reasons if row.reason_type == "best_when"]
    if positive_reasons:
        expected_observed_at = max(row.freshness.observed_at for row in positive_reasons)
        expected_expires_at = min(row.freshness.expires_at for row in positive_reasons)
        if (
            receipt.freshness.observed_at != expected_observed_at
            or receipt.freshness.expires_at != expected_expires_at
        ):
            raise ValueError("receipt freshness must equal the intersection of positive reason freshness")


def _require_offer_reason(
    receipt: DecisionReceiptV1,
    selection: DecisionSelectionV1,
    *,
    code: str,
    observed_value: str,
    threshold: str,
    evidence_ids: set[str],
    observed_at: str,
    expires_at: str,
) -> None:
    reason = next(
        (
            row
            for row in receipt.reasons
            if row.code == code and row.subject_id == selection.serving_offer_id
        ),
        None,
    )
    if reason is None:
        raise ValueError(f"applied query constraint requires {code} reason")
    if reason.observed_value != observed_value or reason.threshold != threshold:
        raise ValueError(f"{code} observed_value/threshold must match the selected offer and query")
    if set(reason.evidence_ids) != evidence_ids:
        raise ValueError(f"{code} must cite exactly the matching serving-offer and offer-link evidence")
    if reason.freshness.observed_at != observed_at or reason.freshness.expires_at != expires_at:
        raise ValueError(f"{code} freshness must equal the selected offer/link validity intersection")


def _monthly_cost_microusd(query: DecisionQueryV1, offer: ServingOfferV1) -> int:
    numerator = query.requests_per_month * (
        query.input_tokens_per_request * offer.pricing.input_microusd_per_million_tokens
        + query.output_tokens_per_request * offer.pricing.output_microusd_per_million_tokens
    )
    quotient, remainder = divmod(numerator, 1_000_000)
    value = quotient + (1 if remainder else 0)
    _require_safe_integer("computed monthly cost", value, minimum=0)
    return value


def _metric_from_dict(value: Any) -> MetricV1:
    payload = _mapping(value)
    kind = payload.get("kind")
    parser = {
        "proportion": ProportionMetricV1.from_dict,
        "continuous": ContinuousMetricV1.from_dict,
        "pass_at_k": PassAtKMetricV1.from_dict,
        "pairwise_preference": PairwisePreferenceMetricV1.from_dict,
        "rank_only": RankOnlyMetricV1.from_dict,
    }.get(kind)
    if parser is None:
        raise ValueError("metric.kind must be one of the five supported metric kinds")
    return parser(payload)


def _uncertainty_from_dict(value: Any) -> UncertaintyV1:
    payload = _mapping(value)
    kind = payload.get("kind")
    parser = {
        "unknown": UnknownUncertaintyV1.from_dict,
        "standard_error": StandardErrorUncertaintyV1.from_dict,
        "interval": IntervalUncertaintyV1.from_dict,
    }.get(kind)
    if parser is None:
        raise ValueError("uncertainty.kind must be unknown, standard_error, or interval")
    return parser(payload)


def _closed(value: Any, *, required: tuple[str, ...], optional: tuple[str, ...] = ()) -> dict[str, Any]:
    payload = _mapping(value)
    missing = [name for name in required if name not in payload]
    if missing:
        raise ValueError(f"missing required field: {missing[0]}")
    unknown = set(payload) - set(required) - set(optional)
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
    return dict(payload)


def _mapping(value: Any) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError("contract value must be a JSON object")
    if any(not isinstance(key, str) for key in value):
        raise TypeError("contract object keys must be strings")
    return value


def _envelope(payload: Mapping[str, Any], object_name: str) -> None:
    if payload["object"] != object_name:
        raise ValueError(f"object must be {object_name}")
    if payload["schema_version"] != "1":
        raise ValueError("schema_version must be 1")


def _without_envelope(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in {"object", "schema_version"}}


def _kind(payload: Mapping[str, Any], expected: str) -> None:
    if payload["kind"] != expected:
        raise ValueError(f"kind must be {expected}")


def _without_kind(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "kind"}


def _require_string(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    canonical_json(value)


def _require_nullable_string(name: str, value: Any) -> None:
    if value is not None:
        _require_string(name, value)


def _require_pattern(name: str, value: Any, pattern: re.Pattern[str]) -> None:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise ValueError(f"{name} has an invalid format")


def _require_hash(name: str, value: Any) -> None:
    _require_pattern(name, value, _HEX_RE)


def _require_enum(name: str, value: Any, allowed: set[str]) -> None:
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f"{name} must be one of {sorted(allowed)}")


def _require_safe_integer(name: str, value: Any, *, minimum: int | None = None) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or abs(value) > MAX_SAFE_INTEGER:
        raise ValueError(f"{name} must be a safe integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")


def _require_nullable_safe_integer(name: str, value: Any, *, minimum: int | None = None) -> None:
    if value is not None:
        _require_safe_integer(name, value, minimum=minimum)


def _require_decimal(name: str, value: Any) -> Decimal:
    if not isinstance(value, str) or len(value) > 128 or not _DECIMAL_RE.fullmatch(value):
        raise ValueError(f"{name} must be a canonical decimal string")
    try:
        return Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} must be a canonical decimal string") from error


def _require_unit_interval(name: str, value: Decimal) -> None:
    if value < 0 or value > 1:
        raise ValueError(f"{name} must be in [0, 1]")


def _validate_count_pair(numerator_name: str, numerator: Any, denominator_name: str, denominator: Any) -> None:
    if (numerator is None) != (denominator is None):
        raise ValueError(f"{numerator_name} and {denominator_name} must both be integers or both be null")
    if numerator is None:
        return
    _require_safe_integer(numerator_name, numerator, minimum=0)
    _require_safe_integer(denominator_name, denominator, minimum=1)
    if numerator > denominator:
        raise ValueError(f"{numerator_name} must not exceed {denominator_name}")


def _parse_timestamp(name: str, value: Any) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP_RE.fullmatch(value):
        raise ValueError(f"{name} must be a UTC timestamp with second precision")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as error:
        raise ValueError(f"{name} must be a valid UTC timestamp") from error


def _require_http_url(name: str, value: Any) -> None:
    _require_string(name, value)
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password or parsed.fragment:
        raise ValueError(f"{name} must be a canonical public http(s) URL without credentials or fragment")


def _require_identity_triple(entity_kind: Any, interaction_policy: Any, passport_class: Any) -> None:
    if (entity_kind, interaction_policy, passport_class) not in IDENTITY_TRIPLES:
        raise ValueError("entity_kind, interaction_policy, and configuration_passport_class must be a resolved identity triple")


def _normalize_string_set(name: str, values: Any, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{name} must be a tuple")
    for value in values:
        _require_string(f"{name} item", value)
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must be unique")
    if not allow_empty and not values:
        raise ValueError(f"{name} must not be empty")
    return tuple(sorted(values, key=lambda value: value.encode("utf-16-be")))


def _normalize_enum_set(name: str, values: Any, allowed: set[str], *, allow_empty: bool = False) -> tuple[str, ...]:
    normalized = _normalize_string_set(name, values, allow_empty=allow_empty)
    for value in normalized:
        _require_enum(f"{name} item", value, allowed)
    return normalized


def _array(name: str, value: Any) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be an array")
    return value


def _array_to_tuple(name: str, value: Any) -> tuple[Any, ...]:
    return tuple(_array(name, value))


def _normalize_typed_records(name: str, values: Any, expected_type: type, key) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{name} must be a tuple")
    if any(not isinstance(value, expected_type) for value in values):
        raise TypeError(f"{name} contains an invalid record")
    keys = [key(value) for value in values]
    if len(set(keys)) != len(keys):
        raise ValueError(f"{name} must be unique")
    return tuple(sorted(values, key=lambda value: _portable_sort_key(key(value))))


def _validate_dated_fact(observed_at: str, expires_at: str, source_artifact_id: str) -> None:
    observed = _parse_timestamp("observed_at", observed_at)
    expires = _parse_timestamp("expires_at", expires_at)
    if expires <= observed:
        raise ValueError("expires_at must be after observed_at")
    _require_pattern("source_artifact_id", source_artifact_id, _ARTIFACT_ID_RE)


def _fact_dict(fact: Any, values: dict[str, Any]) -> dict[str, Any]:
    return {
        **values,
        "observed_at": fact.observed_at,
        "expires_at": fact.expires_at,
        "source_artifact_id": fact.source_artifact_id,
    }


def _copy_json_object(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: _copy_json_value(item) for key, item in value.items()}


def _copy_json_value(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType(_copy_json_object(value))
    if isinstance(value, list):
        return tuple(_copy_json_value(item) for item in value)
    return value


def _portable_sort_key(value: Any) -> bytes:
    parts = value if isinstance(value, tuple) else (value,)
    return canonical_json(list(parts)).encode("utf-16-be")


def _require_rounded_ratio(name: str, value: str, numerator: int, denominator: int) -> None:
    decimal_value = Decimal(value)
    scale = max(0, -decimal_value.as_tuple().exponent)
    if decimal_value * denominator != numerator and scale < 6:
        raise ValueError(
            f"{name} must use at least six fractional digits when counts are not exactly representable"
        )
    quantum = Decimal(1).scaleb(-scale)
    with localcontext() as context:
        context.prec = max(256, scale + 64)
        expected = (Decimal(numerator) / Decimal(denominator)).quantize(
            quantum,
            rounding=ROUND_HALF_EVEN,
        )
    if decimal_value != expected:
        raise ValueError(
            f"{name} must equal numerator / denominator rounded half-even to its declared decimal scale"
        )


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value
