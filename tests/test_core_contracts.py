import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

import evalrank_core.contracts as contracts  # noqa: E402
from evalrank_core.contracts import (  # noqa: E402
    CapabilityFingerprintInput,
    PROBLEM_CODES,
    ProblemDetails,
    RawEntry,
    UseCase,
    UseCaseCatalog,
)


class CoreContractTests(unittest.TestCase):
    def test_superseded_recommendation_pipeline_surface_is_deleted(self):
        for name in (
            "Abstention",
            "CandidateSet",
            "EntityRef",
            "EvaluationRequest",
            "EvidenceItem",
            "EvidenceSet",
            "Exclusion",
            "Freshness",
            "RankedEntity",
            "RankingGroup",
            "Recommendation",
            "ResultRow",
            "ScoringStage",
            "ScoringStageCatalog",
            "StageCandidate",
            "TheCall",
        ):
            self.assertFalse(hasattr(contracts, name), name)

    def test_capability_fingerprint_is_canonical_and_order_independent(self):
        values = {
            "id_scheme": "reverse_dns",
            "canonical_id": "io.evalrank.public-search-demo",
            "entity_kind": "mcp_server",
        }
        first = CapabilityFingerprintInput(
            **values,
            declared_capability_shape={"tools": ["search"], "commit": "abc123"},
        )
        reordered = CapabilityFingerprintInput(
            **values,
            declared_capability_shape={"commit": "abc123", "tools": ["search"]},
        )

        self.assertEqual(first.fingerprint(), reordered.fingerprint())
        self.assertRegex(first.fingerprint(), r"^[0-9a-f]{64}$")

    def test_capability_fingerprint_rejects_open_or_non_json_input(self):
        with self.assertRaisesRegex(ValueError, "canonical_id"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="",
                entity_kind="mcp_server",
                declared_capability_shape={"tools": ["search"]},
            )
        with self.assertRaisesRegex(ValueError, "JSON serializable"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="io.evalrank.public-search-demo",
                entity_kind="mcp_server",
                declared_capability_shape={"score": float("nan")},
            )

    def test_raw_entry_hash_excludes_fetch_time_but_binds_source_content(self):
        values = {
            "source": "official",
            "source_id": "release:v1",
            "entity_kind": "model",
            "canonical_id": "model-a",
            "raw_metadata": {"name": "Model A"},
            "declared_capability_shape": {"modalities": ["text"]},
        }
        first = RawEntry(**values, fetched_at="2026-07-10T00:00:00Z")
        refetched = RawEntry(**values, fetched_at="2026-07-11T00:00:00Z")
        changed = RawEntry(
            **{**values, "raw_metadata": {"name": "Model B"}},
            fetched_at="2026-07-10T00:00:00Z",
        )

        self.assertEqual(first.content_hash, refetched.content_hash)
        self.assertNotEqual(first.content_hash, changed.content_hash)

    def test_use_case_catalog_is_closed_and_pinned(self):
        row = UseCase(
            id="code-generation",
            name="Code generation",
            definition="Produce correct code",
            entity_kinds=("model", "agent"),
        )
        catalog = UseCaseCatalog(
            methodology_version="2026-07-10.1.catalog-manifest-v1",
            generated_at="2026-07-10T00:00:00Z",
            use_cases=(row,),
        )

        self.assertEqual("use_case_catalog", catalog.to_dict()["object"])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            UseCaseCatalog(
                methodology_version=catalog.methodology_version,
                generated_at=catalog.generated_at,
                use_cases=(row, row),
            )
        with self.assertRaisesRegex(ValueError, "methodology_version"):
            UseCaseCatalog(
                methodology_version="latest",
                generated_at=catalog.generated_at,
                use_cases=(row,),
            )

        self.assertEqual(catalog, UseCaseCatalog.from_dict(catalog.to_dict()))
        malformed = catalog.to_dict()
        malformed["use_cases"][0]["rank_policy"] = "anything-goes"
        with self.assertRaisesRegex(ValueError, "rank_policy"):
            UseCaseCatalog.from_dict(malformed)

        duplicate = catalog.to_dict()
        duplicate["use_cases"].append(dict(duplicate["use_cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            UseCaseCatalog.from_dict(duplicate)

    def test_problem_details_round_trips_extensions_and_rejects_private_codes(self):
        payload = {
            "type": "https://evalrank.ai/problems/rate-limited",
            "title": "Rate limited",
            "status": 429,
            "detail": "retry later",
            "code": "rate_limited",
            "retriable": True,
            "retry_after": 3,
            "quota_bucket": "public",
        }
        self.assertEqual(payload, ProblemDetails.from_dict(payload).to_dict())
        self.assertIn("validation", PROBLEM_CODES)
        with self.assertRaisesRegex(ValueError, "code"):
            ProblemDetails(
                type="about:blank",
                title="Bad",
                status=400,
                detail="bad",
                code="private_code",
            )

    def test_problem_details_matches_shared_uri_regression_vectors(self):
        vectors = json.loads(
            (REPO_ROOT / "examples" / "problem-details-uri-v1.golden.json").read_text(
                encoding="utf-8"
            )
        )
        base = {"title": "Validation", "status": 422, "detail": "invalid"}
        for value in vectors["uri_references"]["valid"]:
            ProblemDetails(type=value, **base)
        for value in vectors["uri_references"]["invalid"]:
            with self.assertRaises((TypeError, ValueError)):
                ProblemDetails(type=value, **base)


if __name__ == "__main__":
    unittest.main()
