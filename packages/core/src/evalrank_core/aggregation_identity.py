"""Portable identities for one immutable EvalRank aggregation input."""

from __future__ import annotations

import re
from typing import Any

from evalrank_core.canonical_json import MAX_SAFE_INTEGER, canonical_json, sha256_hex


_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_CALIBRATION_REPORT_ID_RE = re.compile(r"^calibration_[0-9a-f]{64}$")
_OBSERVATION_ID_RE = re.compile(r"^obs_[0-9a-f]{64}$")


def aggregation_input_document(
    *,
    admission_cohort_digest: str,
    calibration_report_id: str,
    methodology_version: str,
    observation_ids: list[str],
    ranking_group: list[str],
) -> dict[str, Any]:
    """Return the exact validated restricted-JCS aggregation preimage."""

    observations = _observation_ids(observation_ids)
    group = _ranking_group(ranking_group)
    document = {
        "admission_cohort_digest": _pattern_string(
            "admission_cohort_digest",
            admission_cohort_digest,
            _DIGEST_RE,
        ),
        "calibration_report_id": _pattern_string(
            "calibration_report_id",
            calibration_report_id,
            _CALIBRATION_REPORT_ID_RE,
        ),
        "methodology_version": _nonempty_string(
            "methodology_version",
            methodology_version,
        ),
        "observation_ids": observations,
        "ranking_group": group,
    }
    canonical_json(document)
    return document


def derive_aggregation_input_digest(
    *,
    admission_cohort_digest: str,
    calibration_report_id: str,
    methodology_version: str,
    observation_ids: list[str],
    ranking_group: list[str],
) -> str:
    """Hash the exact aggregation input document as lowercase SHA-256."""

    return sha256_hex(
        aggregation_input_document(
            admission_cohort_digest=admission_cohort_digest,
            calibration_report_id=calibration_report_id,
            methodology_version=methodology_version,
            observation_ids=observation_ids,
            ranking_group=ranking_group,
        )
    )


def bootstrap_seed_document(
    aggregation_input_digest: str,
    methodology_version: str,
) -> dict[str, str]:
    """Return the exact validated restricted-JCS bootstrap-seed preimage."""

    document = {
        "aggregation_input_digest": _pattern_string(
            "aggregation_input_digest",
            aggregation_input_digest,
            _DIGEST_RE,
        ),
        "methodology_version": _nonempty_string(
            "methodology_version",
            methodology_version,
        ),
    }
    canonical_json(document)
    return document


def derive_bootstrap_seed(
    aggregation_input_digest: str,
    methodology_version: str,
) -> int:
    """Derive the portable safe-integer seed from the first SHA-256 bytes."""

    digest = sha256_hex(
        bootstrap_seed_document(aggregation_input_digest, methodology_version)
    )
    return int(digest[:16], 16) & MAX_SAFE_INTEGER


def _observation_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise TypeError("observation_ids must be an array")
    if not value:
        raise ValueError("observation_ids must be non-empty")
    observations = [
        _pattern_string("observation_ids item", item, _OBSERVATION_ID_RE)
        for item in value
    ]
    if len(observations) != len(set(observations)):
        raise ValueError("observation_ids must be unique")
    return sorted(observations)


def _ranking_group(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise TypeError("ranking_group must be an array")
    if len(value) != 4:
        raise ValueError("ranking_group must contain exactly four strings")
    return [
        _nonempty_string(f"ranking_group[{index}]", item)
        for index, item in enumerate(value)
    ]


def _pattern_string(name: str, value: Any, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if pattern.fullmatch(value) is None:
        raise ValueError(f"{name} has an invalid format")
    return value


def _nonempty_string(name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value:
        raise ValueError(f"{name} must be non-empty")
    return value


__all__ = [
    "aggregation_input_document",
    "bootstrap_seed_document",
    "derive_aggregation_input_digest",
    "derive_bootstrap_seed",
]
