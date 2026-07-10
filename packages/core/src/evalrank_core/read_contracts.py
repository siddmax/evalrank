"""Portable helpers for content-addressed public read snapshots."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar

from evalrank_core.canonical_json import MAX_SAFE_INTEGER, sha256_hex
from evalrank_core.decision_contracts import EvaluatedConfigurationV1


_MANIFEST_VERSION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*$")
_METHODOLOGY_VERSION_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}\.[1-9]\d*\.([a-z0-9]+-)*[a-z0-9]+$"
)
_SNAPSHOT_ID_RE = re.compile(r"^snapshot_[0-9a-f]{64}$")
_CONFIGURATION_ID_RE = re.compile(r"^config_[0-9a-f]{64}$")
_CELL_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def verify_benchmark_health_semantics(payload: Any) -> dict[str, Any]:
    """Verify closed per-cell health rows and their count-derived status."""

    if not isinstance(payload, dict):
        raise TypeError("benchmark health must be a JSON object")
    expected = {"object", "schema_version", "manifest_version", "generated_at", "cells"}
    if set(payload) != expected:
        raise ValueError("benchmark health fields are invalid")
    if payload["object"] != "benchmark_health" or payload["schema_version"] != "1":
        raise ValueError("benchmark health envelope is invalid")
    if not isinstance(payload["manifest_version"], str) or not _MANIFEST_VERSION_RE.fullmatch(
        payload["manifest_version"]
    ):
        raise ValueError("benchmark health manifest_version is invalid")
    if not isinstance(payload["generated_at"], str) or not _TIMESTAMP_RE.fullmatch(
        payload["generated_at"]
    ):
        raise ValueError("benchmark health generated_at is invalid")
    try:
        datetime.fromisoformat(payload["generated_at"].removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise ValueError("benchmark health generated_at is invalid") from error
    cells = payload["cells"]
    if not isinstance(cells, list) or not cells:
        raise ValueError("benchmark health cells must be a non-empty array")
    cell_ids: set[str] = set()
    count_fields = (
        "ranking_group_count",
        "published_ranking_group_count",
        "benchmark_family_count",
        "candidate_feed_count",
        "implemented_feed_count",
        "admitted_feed_count",
        "rank_eligible_feed_count",
    )
    row_fields = {"cell_id", "status", *count_fields}
    for row in cells:
        if not isinstance(row, dict) or set(row) != row_fields:
            raise ValueError("benchmark health cell fields are invalid")
        cell_id = row["cell_id"]
        if not isinstance(cell_id, str) or not _CELL_ID_RE.fullmatch(cell_id):
            raise ValueError("benchmark health cell_id is invalid")
        if cell_id in cell_ids:
            raise ValueError("benchmark health cell_id values must be unique")
        cell_ids.add(cell_id)
        for field in count_fields:
            value = row[field]
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
                or value > MAX_SAFE_INTEGER
            ):
                raise ValueError(f"benchmark health {field} must be a safe nonnegative integer")
        if row["published_ranking_group_count"] > row["ranking_group_count"]:
            raise ValueError("published ranking groups cannot exceed ranking groups")
        if not (
            row["rank_eligible_feed_count"]
            <= row["admitted_feed_count"]
            <= row["implemented_feed_count"]
            <= row["candidate_feed_count"]
        ):
            raise ValueError("benchmark health feed counts must be monotonically nested")
        expected_status = (
            "active"
            if row["published_ranking_group_count"] > 0
            else "preview"
            if row["implemented_feed_count"] > 0
            else "unavailable"
        )
        if row["status"] != expected_status:
            raise ValueError("benchmark health status must match publication and implementation counts")
    return payload


@dataclass(frozen=True, slots=True, kw_only=True)
class RankingGroupSnapshotRefV1:
    """One ranking group's owned publication snapshot in a snapshot set."""

    ranking_group_id: str
    publication_snapshot_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.ranking_group_id, str) or not _CELL_ID_RE.fullmatch(
            self.ranking_group_id
        ):
            raise ValueError("ranking_group_id must be a canonical manifest slug")
        if not isinstance(
            self.publication_snapshot_id, str
        ) or not _SNAPSHOT_ID_RE.fullmatch(self.publication_snapshot_id):
            raise ValueError("publication_snapshot_id must be snapshot_<sha256>")

    @property
    def utf16_sort_key(self) -> tuple[bytes, bytes]:
        return (
            self.ranking_group_id.encode("utf-16-be"),
            self.publication_snapshot_id.encode("utf-16-be"),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "ranking_group_id": self.ranking_group_id,
            "publication_snapshot_id": self.publication_snapshot_id,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "RankingGroupSnapshotRefV1":
        if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
            raise TypeError("ranking-group snapshot reference must be a JSON object")
        expected = {"ranking_group_id", "publication_snapshot_id"}
        if set(value) != expected:
            missing = expected - set(value)
            unknown = set(value) - expected
            detail = (
                "missing " + ", ".join(sorted(missing))
                if missing
                else "unknown " + ", ".join(sorted(unknown))
            )
            raise ValueError(f"ranking-group snapshot reference fields are invalid: {detail}")
        return cls(
            ranking_group_id=value["ranking_group_id"],
            publication_snapshot_id=value["publication_snapshot_id"],
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotSetDescriptorV1:
    """The float-free, portable preimage for a cell snapshot-set identity."""

    object: ClassVar[str] = "snapshot_set_descriptor"
    schema_version: ClassVar[str] = "1"

    cell_id: str
    manifest_version: str
    methodology_version: str
    ranking_group_snapshots: tuple[RankingGroupSnapshotRefV1, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.cell_id, str) or not _CELL_ID_RE.fullmatch(self.cell_id):
            raise ValueError("cell_id must be a canonical manifest slug")
        if not isinstance(self.manifest_version, str) or not _MANIFEST_VERSION_RE.fullmatch(
            self.manifest_version
        ):
            raise ValueError("manifest_version must match YYYY-MM-DD.N")
        if not isinstance(self.methodology_version, str) or not _METHODOLOGY_VERSION_RE.fullmatch(
            self.methodology_version
        ):
            raise ValueError("methodology_version must match YYYY-MM-DD.N.slug")
        if not isinstance(self.ranking_group_snapshots, tuple) or not self.ranking_group_snapshots:
            raise ValueError("ranking_group_snapshots must be a non-empty tuple")
        if any(
            not isinstance(reference, RankingGroupSnapshotRefV1)
            for reference in self.ranking_group_snapshots
        ):
            raise TypeError(
                "ranking_group_snapshots must contain RankingGroupSnapshotRefV1 values"
            )
        group_ids = [reference.ranking_group_id for reference in self.ranking_group_snapshots]
        snapshot_ids = [
            reference.publication_snapshot_id for reference in self.ranking_group_snapshots
        ]
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("ranking_group_snapshots must own unique ranking_group_id values")
        if len(set(snapshot_ids)) != len(snapshot_ids):
            raise ValueError(
                "ranking_group_snapshots must own unique publication_snapshot_id values"
            )
        object.__setattr__(
            self,
            "ranking_group_snapshots",
            tuple(
                sorted(
                    self.ranking_group_snapshots,
                    key=lambda reference: reference.utf16_sort_key,
                )
            ),
        )

    @property
    def snapshot_set_id(self) -> str:
        return f"snapshot_set_{sha256_hex(self.to_dict())}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object,
            "schema_version": self.schema_version,
            "cell_id": self.cell_id,
            "manifest_version": self.manifest_version,
            "methodology_version": self.methodology_version,
            "ranking_group_snapshots": [
                reference.to_dict() for reference in self.ranking_group_snapshots
            ],
        }

    @classmethod
    def from_dict(cls, value: Any) -> "SnapshotSetDescriptorV1":
        if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
            raise TypeError("snapshot-set descriptor must be a JSON object")
        expected = {
            "object",
            "schema_version",
            "cell_id",
            "manifest_version",
            "methodology_version",
            "ranking_group_snapshots",
        }
        if set(value) != expected:
            missing = expected - set(value)
            unknown = set(value) - expected
            detail = "missing " + ", ".join(sorted(missing)) if missing else "unknown " + ", ".join(sorted(unknown))
            raise ValueError(f"snapshot-set descriptor fields are invalid: {detail}")
        if value["object"] != cls.object or value["schema_version"] != cls.schema_version:
            raise ValueError("snapshot-set descriptor envelope is invalid")
        raw_references = value["ranking_group_snapshots"]
        if not isinstance(raw_references, list):
            raise TypeError("ranking_group_snapshots must be an array")
        references = tuple(
            RankingGroupSnapshotRefV1.from_dict(reference)
            for reference in raw_references
        )
        ordered = tuple(sorted(references, key=lambda reference: reference.utf16_sort_key))
        if references != ordered:
            raise ValueError("ranking_group_snapshots must be UTF-16 sorted on the wire")
        return cls(
            cell_id=value["cell_id"],
            manifest_version=value["manifest_version"],
            methodology_version=value["methodology_version"],
            ranking_group_snapshots=references,
        )


def verify_leaderboard_snapshot_set(payload: Any) -> SnapshotSetDescriptorV1:
    """Bind a leaderboard envelope and its exact group snapshots to its content ID."""

    if not isinstance(payload, dict):
        raise TypeError("leaderboard must be a JSON object")
    required = {
        "cell_id",
        "manifest_version",
        "methodology_version",
        "snapshot_set_id",
        "snapshot_set_descriptor",
        "ranking_groups",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"leaderboard is missing {', '.join(sorted(missing))}")
    descriptor = SnapshotSetDescriptorV1.from_dict(payload["snapshot_set_descriptor"])
    for name in ("cell_id", "manifest_version", "methodology_version"):
        if payload[name] != getattr(descriptor, name):
            raise ValueError(f"leaderboard {name} must match snapshot_set_descriptor")
    groups = payload["ranking_groups"]
    if not isinstance(groups, list) or not groups:
        raise ValueError("leaderboard ranking_groups must be a non-empty array")
    group_snapshots: list[RankingGroupSnapshotRefV1] = []
    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("every ranking group must be an object")
        try:
            group_snapshots.append(
                RankingGroupSnapshotRefV1(
                    ranking_group_id=group["ranking_group_id"],
                    publication_snapshot_id=group["publication_snapshot_id"],
                )
            )
        except KeyError as error:
            raise ValueError(
                "every ranking group must carry ranking_group_id and publication_snapshot_id"
            ) from error
    try:
        expected = SnapshotSetDescriptorV1(
            cell_id=descriptor.cell_id,
            manifest_version=descriptor.manifest_version,
            methodology_version=descriptor.methodology_version,
            ranking_group_snapshots=tuple(group_snapshots),
        ).ranking_group_snapshots
    except (TypeError, ValueError) as error:
        raise ValueError("ranking-group snapshot pairs must be one-to-one") from error
    if descriptor.ranking_group_snapshots != expected:
        raise ValueError(
            "snapshot_set_descriptor must contain the exact ranking-group snapshot pairs"
        )
    if payload["snapshot_set_id"] != descriptor.snapshot_set_id:
        raise ValueError("snapshot_set_id must hash the exact snapshot_set_descriptor")
    return descriptor


def verify_leaderboard_semantics(payload: Any) -> SnapshotSetDescriptorV1:
    """Verify keyed uniqueness, ranks, claims, and evidence-gap truth after schema validation."""

    descriptor = verify_leaderboard_snapshot_set(payload)
    group_ids: set[str] = set()
    configuration_ids: set[str] = set()
    for group in payload["ranking_groups"]:
        group_id = group.get("ranking_group_id")
        if not isinstance(group_id, str) or not group_id:
            raise ValueError("every ranking group must carry ranking_group_id")
        if group_id in group_ids:
            raise ValueError("ranking_group_id values must be unique")
        group_ids.add(group_id)
        entries = group.get("entries")
        if not isinstance(entries, list):
            raise ValueError("ranking group entries must be an array")
        _verify_rankings(entries, configuration_ids=configuration_ids, require_contiguous=True)
        has_top_set = any(entry["ranking"]["in_top_set"] for entry in entries)
        _verify_nonactive_claim(group.get("state"), has_top_set)
        eligibility = group.get("eligibility_summary")
        _verify_eligibility(
            eligibility,
            state=group.get("state"),
            entity_kind=group.get("entity_kind"),
            entry_count=len(entries),
            has_top_set=has_top_set,
        )
    return descriptor


def verify_entity_detail_semantics(payload: Any) -> SnapshotSetDescriptorV1:
    """Verify one detail projection against its snapshot and configuration identity."""

    descriptor = _verify_snapshot_reference(payload)
    projection = payload.get("entity")
    if not isinstance(projection, dict):
        raise ValueError("entity detail must carry an entity projection")
    configuration = EvaluatedConfigurationV1.from_dict(projection.get("evaluated_configuration"))
    ranking = projection.get("ranking")
    _verify_ranking(ranking)
    _verify_nonactive_claim(payload.get("state"), ranking["in_top_set"])
    _verify_eligibility_summary_state(payload.get("eligibility_summary"), payload.get("state"))
    if configuration.evaluated_configuration_id != projection["evaluated_configuration"]["evaluated_configuration_id"]:
        raise ValueError("entity detail evaluated_configuration_id is invalid")
    return descriptor


def verify_compare_result_semantics(payload: Any) -> SnapshotSetDescriptorV1:
    """Verify compare-key uniqueness and snapshot/claim consistency after schema validation."""

    descriptor = _verify_snapshot_reference(payload)
    entities = payload.get("entities")
    if not isinstance(entities, list):
        raise ValueError("compare entities must be an array")
    configuration_ids: set[str] = set()
    ranks: set[int] = set()
    for entity in entities:
        if not isinstance(entity, dict):
            raise ValueError("compare entities must be objects")
        configuration_id = entity.get("evaluated_configuration_id")
        if not isinstance(configuration_id, str) or not _CONFIGURATION_ID_RE.fullmatch(configuration_id):
            raise ValueError("compare evaluated_configuration_id has an invalid format")
        if configuration_id in configuration_ids:
            raise ValueError("compare evaluated_configuration_id values must be unique")
        configuration_ids.add(configuration_id)
        ranking = entity.get("ranking")
        _verify_ranking(ranking)
        rank = ranking["rank"]
        if rank in ranks:
            raise ValueError("compare ranks must be unique")
        ranks.add(rank)
        _verify_nonactive_claim(payload.get("state"), ranking["in_top_set"])
    _verify_eligibility_summary_state(payload.get("eligibility_summary"), payload.get("state"))
    return descriptor


def _verify_snapshot_reference(payload: Any) -> SnapshotSetDescriptorV1:
    if not isinstance(payload, dict):
        raise TypeError("public read document must be a JSON object")
    descriptor = SnapshotSetDescriptorV1.from_dict(payload.get("snapshot_set_descriptor"))
    for name in ("cell_id", "manifest_version", "methodology_version"):
        if payload.get(name) != getattr(descriptor, name):
            raise ValueError(f"{name} must match snapshot_set_descriptor")
    if payload.get("snapshot_set_id") != descriptor.snapshot_set_id:
        raise ValueError("snapshot_set_id must hash snapshot_set_descriptor")
    reference = RankingGroupSnapshotRefV1(
        ranking_group_id=payload.get("ranking_group_id"),
        publication_snapshot_id=payload.get("publication_snapshot_id"),
    )
    if reference not in descriptor.ranking_group_snapshots:
        raise ValueError(
            "ranking-group snapshot pair must belong to snapshot_set_descriptor"
        )
    return descriptor


def _verify_rankings(
    entries: list[Any],
    *,
    configuration_ids: set[str],
    require_contiguous: bool,
) -> None:
    ranks: list[int] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("leaderboard entries must be objects")
        configuration_id = entry.get("evaluated_configuration_id")
        if (
            not isinstance(configuration_id, str)
            or not _CONFIGURATION_ID_RE.fullmatch(configuration_id)
            or configuration_id in configuration_ids
        ):
            raise ValueError("evaluated_configuration_id values must be unique")
        configuration_ids.add(configuration_id)
        ranking = entry.get("ranking")
        _verify_ranking(ranking)
        ranks.append(ranking["rank"])
    if require_contiguous and ranks != list(range(1, len(entries) + 1)):
        raise ValueError("leaderboard ranks must be contiguous from 1 in array order")


def _verify_ranking(ranking: Any) -> None:
    if not isinstance(ranking, dict):
        raise ValueError("entity ranking must be an object")
    if not isinstance(ranking.get("rank"), int) or isinstance(ranking.get("rank"), bool):
        raise ValueError("entity ranking rank must be an integer")
    if not isinstance(ranking.get("in_top_set"), bool):
        raise ValueError("entity ranking in_top_set must be a boolean")
    uncertainty = ranking.get("uncertainty")
    if isinstance(uncertainty, dict) and uncertainty.get("kind") == "interval":
        try:
            lower = Decimal(str(uncertainty["lower"]))
            upper = Decimal(str(uncertainty["upper"]))
        except (InvalidOperation, KeyError, TypeError) as error:
            raise ValueError("ranking interval must contain numeric lower and upper values") from error
        if not lower.is_finite() or not upper.is_finite() or lower > upper:
            raise ValueError("ranking interval lower must be <= upper")


def _verify_eligibility(
    value: Any,
    *,
    state: Any,
    entity_kind: Any,
    entry_count: int,
    has_top_set: bool,
) -> None:
    _verify_eligibility_summary_state(value, state)
    if not isinstance(value, dict):
        raise ValueError("eligibility_summary must be an object")
    if value.get("rank_eligible_configuration_count") != entry_count:
        raise ValueError("rank_eligible_configuration_count must equal leaderboard entry count")
    gaps = set(value.get("gap_codes", ()))
    if entity_kind == "unresolved":
        if entry_count or "unresolved_identity" not in gaps:
            raise ValueError("unresolved groups must be empty and disclose unresolved_identity")
    if state == "active" and not has_top_set:
        raise ValueError("active ranking groups must publish at least one top-set member")


def _verify_eligibility_summary_state(value: Any, state: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("eligibility_summary must be an object")
    gaps = value.get("gap_codes")
    if not isinstance(gaps, list) or len(set(gaps)) != len(gaps):
        raise ValueError("eligibility gap_codes must be a unique array")
    if state == "active":
        if value.get("published_claim") != "top_set" or value.get("calibration_status") != "validated" or gaps:
            raise ValueError("active reads require a validated top_set claim with no gaps")
    else:
        if value.get("published_claim") != "explorer" or not gaps:
            raise ValueError("non-active reads require an explorer claim with explicit gaps")
    _verify_eligibility_count_gaps(value, gaps)
    if state == "quarantined" and "quarantined" not in gaps:
        raise ValueError("quarantined reads must disclose the quarantined gap")


def _verify_nonactive_claim(state: Any, in_top_set: bool) -> None:
    if state != "active" and in_top_set:
        raise ValueError("non-active reads cannot claim top-set membership")


def _verify_count_gap(
    value: dict[str, Any],
    *,
    current: str,
    required: str,
    code: str,
    gaps: set[str],
) -> None:
    current_value = value.get(current)
    required_value = value.get(required)
    if not isinstance(current_value, int) or not isinstance(required_value, int):
        raise ValueError("eligibility counts must be integers")
    if (current_value < required_value) != (code in gaps):
        raise ValueError(f"{code} gap must match eligibility counts")


def _verify_eligibility_count_gaps(value: dict[str, Any], gaps: set[str]) -> None:
    _verify_count_gap(
        value,
        current="current_independent_family_count",
        required="required_independent_family_count",
        code="insufficient_independent_families",
        gaps=gaps,
    )
    _verify_count_gap(
        value,
        current="current_overlap_count",
        required="required_overlap_count",
        code="insufficient_configuration_overlap",
        gaps=gaps,
    )
    rank_eligible_count = value.get("rank_eligible_configuration_count")
    if not isinstance(rank_eligible_count, int) or isinstance(rank_eligible_count, bool):
        raise ValueError("rank_eligible_configuration_count must be an integer")
    if (rank_eligible_count == 0) != ("no_rank_eligible_configurations" in gaps):
        raise ValueError("no_rank_eligible_configurations gap must match eligibility count")
    if (value.get("calibration_status") == "unvalidated") != ("calibration_unvalidated" in gaps):
        raise ValueError("calibration_unvalidated gap must match calibration_status")
