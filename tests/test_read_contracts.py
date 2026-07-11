import sys
import unittest
from copy import deepcopy
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.canonical_json import sha256_hex  # noqa: E402
from evalrank_core.read_contracts import (  # noqa: E402
    RankingGroupSnapshotRefV1,
    SnapshotSetDescriptorV1,
    verify_benchmark_health_semantics,
    verify_compare_result_semantics,
    verify_entity_detail_semantics,
    verify_leaderboard_semantics,
    verify_leaderboard_snapshot_set,
)


class BenchmarkHealthSemanticTests(unittest.TestCase):
    def test_health_status_and_nested_counts_are_derived_truthfully(self):
        payload = _benchmark_health()

        self.assertIs(payload, verify_benchmark_health_semantics(payload))

        wrong_status = deepcopy(payload)
        wrong_status["cells"][0]["status"] = "active"
        with self.assertRaisesRegex(ValueError, "status"):
            verify_benchmark_health_semantics(wrong_status)

        impossible_counts = deepcopy(payload)
        impossible_counts["cells"][0]["admitted_feed_count"] = 3
        with self.assertRaisesRegex(ValueError, "nested"):
            verify_benchmark_health_semantics(impossible_counts)

    def test_health_rejects_duplicate_cells_unknown_fields_and_unsafe_counts(self):
        duplicate = _benchmark_health()
        duplicate["cells"].append(deepcopy(duplicate["cells"][0]))
        with self.assertRaisesRegex(ValueError, "unique"):
            verify_benchmark_health_semantics(duplicate)

        unknown = _benchmark_health()
        unknown["cells"][0]["detail"] = "not public"
        with self.assertRaisesRegex(ValueError, "fields"):
            verify_benchmark_health_semantics(unknown)

        unsafe = _benchmark_health()
        unsafe["cells"][0]["candidate_feed_count"] = 2**53
        with self.assertRaisesRegex(ValueError, "safe"):
            verify_benchmark_health_semantics(unsafe)

        invalid_timestamp = _benchmark_health()
        invalid_timestamp["generated_at"] = "2026-02-30T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "generated_at"):
            verify_benchmark_health_semantics(invalid_timestamp)


def _benchmark_health() -> dict:
    return {
        "object": "benchmark_health",
        "schema_version": "1",
        "manifest_version": "2026-07-09.3",
        "generated_at": "2026-07-10T00:00:00Z",
        "cells": [
            {
                "cell_id": "code-generation",
                "status": "preview",
                "ranking_group_count": 2,
                "published_ranking_group_count": 0,
                "benchmark_family_count": 3,
                "candidate_feed_count": 4,
                "implemented_feed_count": 2,
                "admitted_feed_count": 0,
                "rank_eligible_feed_count": 0,
            }
        ],
    }


class SnapshotSetDescriptorTests(unittest.TestCase):
    def test_snapshot_set_id_hashes_one_float_free_sorted_descriptor(self):
        first = SnapshotSetDescriptorV1(
            cell_id="code-generation",
            manifest_version="2026-07-09.2",
            methodology_version="2026-07-09.2.truth-kernel-v1",
            ranking_group_snapshots=(
                RankingGroupSnapshotRefV1(
                    ranking_group_id="rg-b",
                    evidence_snapshot_id=f"snapshot_{'b' * 64}",
                ),
                RankingGroupSnapshotRefV1(
                    ranking_group_id="rg-a",
                    evidence_snapshot_id=f"explorer_{'a' * 64}",
                ),
            ),
        )
        reordered = SnapshotSetDescriptorV1(
            cell_id=first.cell_id,
            manifest_version=first.manifest_version,
            methodology_version=first.methodology_version,
            ranking_group_snapshots=tuple(reversed(first.ranking_group_snapshots)),
        )

        self.assertEqual(first.to_dict(), reordered.to_dict())
        self.assertEqual(
            f"snapshot_set_{sha256_hex(first.to_dict())}",
            first.snapshot_set_id,
        )
        self.assertEqual(first.snapshot_set_id, reordered.snapshot_set_id)

    def test_wire_descriptor_must_be_closed_and_already_sorted(self):
        descriptor = SnapshotSetDescriptorV1(
            cell_id="code-generation",
            manifest_version="2026-07-09.2",
            methodology_version="2026-07-09.2.truth-kernel-v1",
            ranking_group_snapshots=(
                RankingGroupSnapshotRefV1(
                    ranking_group_id="rg-a",
                    evidence_snapshot_id=f"explorer_{'a' * 64}",
                ),
                RankingGroupSnapshotRefV1(
                    ranking_group_id="rg-b",
                    evidence_snapshot_id=f"snapshot_{'b' * 64}",
                ),
            ),
        )
        self.assertEqual(descriptor, SnapshotSetDescriptorV1.from_dict(descriptor.to_dict()))

        unsorted = descriptor.to_dict()
        unsorted["ranking_group_snapshots"].reverse()
        with self.assertRaisesRegex(ValueError, "sorted"):
            SnapshotSetDescriptorV1.from_dict(unsorted)

        open_pair = descriptor.to_dict()
        open_pair["ranking_group_snapshots"][0]["generated_at"] = "2026-07-09T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "unknown"):
            SnapshotSetDescriptorV1.from_dict(open_pair)

        unknown = {**descriptor.to_dict(), "generated_at": "2026-07-09T00:00:00Z"}
        with self.assertRaisesRegex(ValueError, "unknown"):
            SnapshotSetDescriptorV1.from_dict(unknown)

        invalid_cell = {**descriptor.to_dict(), "cell_id": "Not a slug"}
        with self.assertRaisesRegex(ValueError, "canonical manifest slug"):
            SnapshotSetDescriptorV1.from_dict(invalid_cell)

        legacy_pair = descriptor.to_dict()
        pair = legacy_pair["ranking_group_snapshots"][0]
        pair["publication_snapshot_id"] = pair.pop("evidence_snapshot_id")
        with self.assertRaisesRegex(ValueError, "fields are invalid"):
            SnapshotSetDescriptorV1.from_dict(legacy_pair)

    def test_leaderboard_verifier_binds_envelope_and_exact_group_snapshots(self):
        descriptor = SnapshotSetDescriptorV1(
            cell_id="code-generation",
            manifest_version="2026-07-09.2",
            methodology_version="2026-07-09.2.truth-kernel-v1",
            ranking_group_snapshots=(
                RankingGroupSnapshotRefV1(
                    ranking_group_id="rg-a",
                    evidence_snapshot_id=f"explorer_{'a' * 64}",
                ),
                RankingGroupSnapshotRefV1(
                    ranking_group_id="rg-b",
                    evidence_snapshot_id=f"snapshot_{'b' * 64}",
                ),
            ),
        )
        leaderboard = {
            **{
                key: value
                for key, value in descriptor.to_dict().items()
                if key not in {"object", "schema_version", "ranking_group_snapshots"}
            },
            "snapshot_set_id": descriptor.snapshot_set_id,
            "snapshot_set_descriptor": descriptor.to_dict(),
            "ranking_groups": [
                snapshot.to_dict() for snapshot in descriptor.ranking_group_snapshots
            ],
        }

        self.assertEqual(descriptor, verify_leaderboard_snapshot_set(leaderboard))
        for field, value in (
            ("cell_id", "other-cell"),
            ("snapshot_set_id", f"snapshot_set_{'c' * 64}"),
        ):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    verify_leaderboard_snapshot_set({**leaderboard, field: value})

        wrong_groups = {
            **leaderboard,
            "ranking_groups": [
                {
                    "ranking_group_id": "rg-a",
                    "evidence_snapshot_id": f"explorer_{'c' * 64}",
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "exact ranking-group snapshot pairs"):
            verify_leaderboard_snapshot_set(wrong_groups)

        swapped_ownership = deepcopy(leaderboard)
        swapped_ownership["ranking_groups"][0]["evidence_snapshot_id"] = f"snapshot_{'b' * 64}"
        swapped_ownership["ranking_groups"][1]["evidence_snapshot_id"] = f"explorer_{'a' * 64}"
        with self.assertRaisesRegex(ValueError, "exact ranking-group snapshot pairs"):
            verify_leaderboard_snapshot_set(swapped_ownership)

    def test_leaderboard_semantics_reject_keyed_duplicates_bad_intervals_and_false_gaps(self):
        leaderboard = _active_leaderboard()
        verify_leaderboard_semantics(leaderboard)

        duplicate = deepcopy(leaderboard)
        second = deepcopy(duplicate["ranking_groups"][0]["entries"][0])
        second["ranking"]["rank"] = 2
        second["ranking"]["display_name"] = "Same configuration, different row"
        duplicate["ranking_groups"][0]["entries"].append(second)
        duplicate["ranking_groups"][0]["eligibility_summary"]["rank_eligible_configuration_count"] = 2
        with self.assertRaisesRegex(ValueError, "evaluated_configuration_id values must be unique"):
            verify_leaderboard_semantics(duplicate)

        bad_interval = deepcopy(leaderboard)
        bad_interval["ranking_groups"][0]["entries"][0]["ranking"]["uncertainty"] = {
            "kind": "interval",
            "level": 0.95,
            "lower": 0.9,
            "upper": 0.8,
        }
        with self.assertRaisesRegex(ValueError, "lower must be <= upper"):
            verify_leaderboard_semantics(bad_interval)

        false_gap = deepcopy(leaderboard)
        false_gap["ranking_groups"][0]["state"] = "preview"
        false_gap["ranking_groups"][0]["eligibility_summary"] = {
            **false_gap["ranking_groups"][0]["eligibility_summary"],
            "published_claim": "explorer",
            "calibration_status": "unvalidated",
            "gap_codes": ["calibration_unvalidated", "insufficient_independent_families"],
        }
        false_gap["ranking_groups"][0]["entries"][0]["ranking"]["in_top_set"] = False
        with self.assertRaisesRegex(ValueError, "insufficient_independent_families"):
            verify_leaderboard_semantics(false_gap)

        preview_top_set = deepcopy(leaderboard)
        preview_top_set["ranking_groups"][0]["state"] = "preview"
        preview_top_set["ranking_groups"][0]["eligibility_summary"] = {
            **preview_top_set["ranking_groups"][0]["eligibility_summary"],
            "published_claim": "explorer",
            "calibration_status": "unvalidated",
            "gap_codes": ["calibration_unvalidated"],
        }
        with self.assertRaisesRegex(ValueError, "non-active reads cannot claim top-set"):
            verify_leaderboard_semantics(preview_top_set)

    def test_compare_semantics_reject_same_configuration_with_different_rows(self):
        leaderboard = _active_leaderboard()
        group = leaderboard["ranking_groups"][0]
        first = deepcopy(group["entries"][0])
        second = deepcopy(first)
        second["evaluated_configuration_id"] = f"config_{'d' * 64}"
        second["ranking"]["rank"] = 2
        compare = {
            "cell_id": leaderboard["cell_id"],
            "manifest_version": leaderboard["manifest_version"],
            "methodology_version": leaderboard["methodology_version"],
            "snapshot_set_id": leaderboard["snapshot_set_id"],
            "snapshot_set_descriptor": leaderboard["snapshot_set_descriptor"],
            "ranking_group_id": group["ranking_group_id"],
            "evidence_snapshot_id": group["evidence_snapshot_id"],
            "state": "active",
            "eligibility_summary": group["eligibility_summary"],
            "entities": [first, second],
        }
        verify_compare_result_semantics(compare)

        duplicate = deepcopy(compare)
        duplicate["entities"][1]["evaluated_configuration_id"] = duplicate["entities"][0]["evaluated_configuration_id"]
        with self.assertRaisesRegex(ValueError, "evaluated_configuration_id values must be unique"):
            verify_compare_result_semantics(duplicate)

    def test_entity_and_compare_bind_the_outer_ranking_group_snapshot_pair(self):
        leaderboard = _active_leaderboard()
        group = leaderboard["ranking_groups"][0]
        entry = deepcopy(group["entries"][0])
        evaluated_configuration = {
            "object": "evaluated_configuration",
            "schema_version": "1",
            "evaluated_configuration_id": entry["evaluated_configuration_id"],
            "passport": {
                "object": "configuration_passport",
                "schema_version": "1",
                "entity_kind": "model_configuration",
                "canonical_name": "Example",
                "revision": "1",
                "interaction_policy": "direct_prompt",
                "configuration_passport_class": "model-configuration-v1",
                "harness": None,
                "scaffold": None,
                "tools": [],
                "quantization": None,
                "system_prompt_policy": None,
                "environment": None,
            },
        }
        # Replace the fixture ID with the passport's actual content-addressed identity.
        evaluated_configuration["evaluated_configuration_id"] = (
            f"config_{sha256_hex(evaluated_configuration['passport'])}"
        )
        entry["evaluated_configuration_id"] = evaluated_configuration["evaluated_configuration_id"]
        common = {
            "cell_id": leaderboard["cell_id"],
            "manifest_version": leaderboard["manifest_version"],
            "methodology_version": leaderboard["methodology_version"],
            "snapshot_set_id": leaderboard["snapshot_set_id"],
            "snapshot_set_descriptor": leaderboard["snapshot_set_descriptor"],
            "ranking_group_id": group["ranking_group_id"],
            "evidence_snapshot_id": group["evidence_snapshot_id"],
            "state": "active",
            "eligibility_summary": group["eligibility_summary"],
        }
        entity = {
            **common,
            "entity": {
                "evaluated_configuration": evaluated_configuration,
                "ranking": entry["ranking"],
            },
        }
        compare = {**common, "entities": [entry]}
        verify_entity_detail_semantics(entity)
        verify_compare_result_semantics(compare)

        for document, verifier in (
            (entity, verify_entity_detail_semantics),
            (compare, verify_compare_result_semantics),
        ):
            with self.subTest(verifier=verifier.__name__):
                wrong_group = {**document, "ranking_group_id": "rg-other"}
                with self.assertRaisesRegex(ValueError, "ranking-group snapshot pair"):
                    verifier(wrong_group)


def _active_leaderboard() -> dict:
    snapshot_id = f"snapshot_{'a' * 64}"
    ranking_group_id = "rg-code-generation-model"
    descriptor = SnapshotSetDescriptorV1(
        cell_id="code-generation",
        manifest_version="2026-07-09.2",
        methodology_version="2026-07-09.2.truth-kernel-v1",
        ranking_group_snapshots=(
            RankingGroupSnapshotRefV1(
                ranking_group_id=ranking_group_id,
                evidence_snapshot_id=snapshot_id,
            ),
        ),
    )
    return {
        "cell_id": descriptor.cell_id,
        "manifest_version": descriptor.manifest_version,
        "methodology_version": descriptor.methodology_version,
        "snapshot_set_id": descriptor.snapshot_set_id,
        "snapshot_set_descriptor": descriptor.to_dict(),
        "ranking_groups": [
            {
                "ranking_group_id": ranking_group_id,
                "entity_kind": "model_configuration",
                "state": "active",
                "evidence_snapshot_id": snapshot_id,
                "eligibility_summary": {
                    "published_claim": "top_set",
                    "rank_eligible_configuration_count": 1,
                    "current_independent_family_count": 3,
                    "required_independent_family_count": 3,
                    "current_overlap_count": 2,
                    "required_overlap_count": 2,
                    "calibration_status": "validated",
                    "gap_codes": [],
                },
                "entries": [
                    {
                        "evaluated_configuration_id": f"config_{'c' * 64}",
                        "ranking": {
                            "rank": 1,
                            "display_name": "Example",
                            "capability_score": 0.8,
                            "uncertainty": {
                                "kind": "interval",
                                "level": 0.95,
                                "lower": 0.75,
                                "upper": 0.85,
                            },
                            "in_top_set": True,
                        },
                    }
                ],
                "explorer_views": [],
            }
        ],
    }


if __name__ == "__main__":
    unittest.main()
