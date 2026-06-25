import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))
CORE_README = CORE_SRC.parents[0] / "README.md"

import evalrank_core.contracts as contracts  # noqa: E402
from evalrank_core.contracts import (  # noqa: E402
    CapabilityFingerprintInput,
    CandidateSet,
    ConfidenceInterval,
    EntityRef,
    Exclusion,
    EvidenceSet,
    EvidenceItem,
    EvaluationRequest,
    Freshness,
    PROBLEM_CODES,
    ProblemDetails,
    RawEntry,
    Recommendation,
    RankedEntity,
    RankingGroup,
    ResultRow,
    ScoringStage,
    ScoringStageCatalog,
    StageCandidate,
    TheCall,
    UseCase,
    UseCaseCatalog,
)


PINNED_METHODOLOGY_VERSION = "2026-06-25.1.public-fixture-v1"
PUBLIC_CAPABILITY_FINGERPRINT = "da617b2b113a59a734acb6166c305086d9a850bac2a40c8febd6e67c7eff3e12"


class CoreContractTests(unittest.TestCase):
    def test_core_readme_lists_public_contract_surface(self):
        text = CORE_README.read_text(encoding="utf-8")

        for name in (
            "CapabilityFingerprintInput",
            "RawEntry",
            "EvaluationRequest",
            "CandidateSet",
            "StageCandidate",
            "COMPARABILITY_MODES",
            "EvidenceItem",
            "EvidenceSet",
            "EVIDENCE_KINDS",
            "FRESHNESS_STATUSES",
            "ProblemDetails",
            "PROBLEM_CODES",
            "ResultRow",
            "UseCaseCatalog",
            "ScoringStage",
            "ScoringStageCatalog",
            "RankingGroup",
            "Exclusion",
            "TheCall",
            "TRUST_TIERS",
            "RankedEntity",
            "Recommendation",
            "EntityRef",
            "PUBLIC_FIXTURE_KINDS",
            "sample_public_fixture",
        ):
            with self.subTest(name=name):
                self.assertIn(name, text)
        self.assertIn("public string fields", text)
        self.assertIn("actual non-empty strings", text)

    def test_capability_fingerprint_is_stable_over_shape_key_order(self):
        first = CapabilityFingerprintInput(
            id_scheme="reverse_dns",
            canonical_id="io.evalrank.public-search-demo",
            entity_kind="mcp_server",
            declared_capability_shape={
                "tool_names": ["search"],
                "param_schemas": {"search": {"type": "object"}},
                "declared_scopes": ["web.search"],
                "commit_sha": "abc123",
            },
        )
        same_shape_different_order = CapabilityFingerprintInput(
            id_scheme="reverse_dns",
            canonical_id="io.evalrank.public-search-demo",
            entity_kind="mcp_server",
            declared_capability_shape={
                "commit_sha": "abc123",
                "declared_scopes": ["web.search"],
                "param_schemas": {"search": {"type": "object"}},
                "tool_names": ["search"],
            },
        )

        payload = first.to_dict()

        self.assertEqual("capability_fingerprint", payload["object"])
        self.assertEqual(PUBLIC_CAPABILITY_FINGERPRINT, payload["capability_fingerprint"])
        self.assertEqual(PUBLIC_CAPABILITY_FINGERPRINT, same_shape_different_order.fingerprint())
        self.assertEqual("mcp_server", payload["entity_kind"])

    def test_problem_details_serializes_public_error_shape(self):
        problem = ProblemDetails(
            type="https://evalrank.ai/problems/rate-limited",
            title="Rate limited",
            status=429,
            detail="retry after the advertised delay",
            instance="/v1/recommendations/req_public_fixture_01",
            code="rate_limited",
            retriable=True,
            retry_after=30,
            field="request_id",
            request_id="req_public_fixture_01",
            doc_url="https://evalrank.ai/docs/errors#rate-limited",
            extensions={"quota_bucket": "public-fixture"},
        )

        self.assertEqual(
            {
                "type": "https://evalrank.ai/problems/rate-limited",
                "title": "Rate limited",
                "status": 429,
                "detail": "retry after the advertised delay",
                "instance": "/v1/recommendations/req_public_fixture_01",
                "code": "rate_limited",
                "retriable": True,
                "retry_after": 30,
                "field": "request_id",
                "request_id": "req_public_fixture_01",
                "doc_url": "https://evalrank.ai/docs/errors#rate-limited",
                "quota_bucket": "public-fixture",
            },
            problem.to_dict(),
        )

    def test_problem_details_rejects_schema_incompatible_values(self):
        valid = {
            "type": "about:blank",
            "title": "Validation failed",
            "status": 422,
            "detail": "request_id is required",
        }

        for field, value in (
            ("type", ""),
            ("title", 123),
            ("status", 200),
            ("status", True),
            ("detail", ""),
            ("code", "private_code"),
            ("retriable", "yes"),
            ("retry_after", -1),
            ("retry_after", True),
            ("field", ""),
            ("request_id", 123),
            ("doc_url", ""),
            ("extensions", {"status": "override"}),
            ("extensions", {"bad": float("nan")}),
        ):
            with self.subTest(field=field):
                with self.assertRaises((TypeError, ValueError)):
                    ProblemDetails(**{**valid, field: value})

    def test_capability_fingerprint_rejects_missing_or_non_json_shape_keys(self):
        with self.assertRaisesRegex(ValueError, "canonical_id"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="",
                entity_kind="mcp_server",
                declared_capability_shape={"tool_names": ["search"]},
            )

        with self.assertRaisesRegex(ValueError, "declared_capability_shape"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="io.evalrank.public-search-demo",
                entity_kind="mcp_server",
                declared_capability_shape={1: "not-public-json-key"},
            )

        with self.assertRaisesRegex(ValueError, "declared_capability_shape"):
            CapabilityFingerprintInput(
                id_scheme="reverse_dns",
                canonical_id="io.evalrank.public-search-demo",
                entity_kind="mcp_server",
                declared_capability_shape={"score": float("nan")},
            )

        valid = {
            "id_scheme": "reverse_dns",
            "canonical_id": "io.evalrank.public-search-demo",
            "entity_kind": "mcp_server",
            "declared_capability_shape": {"tool_names": ["search"]},
        }
        for field in ("id_scheme", "canonical_id", "entity_kind"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    CapabilityFingerprintInput(**{**valid, field: 123})

    def test_raw_entry_hash_is_stable_over_content_order_and_refetch_time(self):
        entry = RawEntry(
            source="public-fixture",
            source_id="public-fixture:search-demo:2026-06-25",
            entity_kind="mcp_server",
            canonical_id="io.evalrank.public-search-demo",
            raw_metadata={
                "display_name": "Public Search Demo",
                "homepage": "https://example.com/evalrank/public-search-demo",
            },
            declared_capability_shape={
                "tool_names": ["search"],
                "param_schemas": {"search": {"type": "object"}},
            },
            fetched_at="2026-06-25T00:00:00Z",
        )
        same_content_different_order = RawEntry(
            source="public-fixture",
            source_id="public-fixture:search-demo:2026-06-25",
            entity_kind="mcp_server",
            canonical_id="io.evalrank.public-search-demo",
            raw_metadata={
                "homepage": "https://example.com/evalrank/public-search-demo",
                "display_name": "Public Search Demo",
            },
            declared_capability_shape={
                "param_schemas": {"search": {"type": "object"}},
                "tool_names": ["search"],
            },
            fetched_at="2026-06-25T00:00:00Z",
        )
        same_content_refetched_later = RawEntry(
            source="public-fixture",
            source_id="public-fixture:search-demo:2026-06-25",
            entity_kind="mcp_server",
            canonical_id="io.evalrank.public-search-demo",
            raw_metadata={
                "display_name": "Public Search Demo",
                "homepage": "https://example.com/evalrank/public-search-demo",
            },
            declared_capability_shape={
                "tool_names": ["search"],
                "param_schemas": {"search": {"type": "object"}},
            },
            fetched_at="2026-06-26T00:00:00Z",
        )

        payload = entry.to_dict()

        self.assertEqual("raw_entry", payload["object"])
        self.assertEqual("public-fixture", payload["source"])
        self.assertEqual("io.evalrank.public-search-demo", payload["canonical_id"])
        self.assertEqual(64, len(payload["content_hash"]))
        self.assertEqual(payload["content_hash"], same_content_different_order.content_hash)
        self.assertEqual(payload["content_hash"], same_content_refetched_later.content_hash)
        self.assertEqual("2026-06-25T00:00:00Z", payload["fetched_at"])
        self.assertEqual(["display_name", "homepage"], sorted(payload["raw_metadata"]))

    def test_raw_entry_rejects_missing_or_non_json_metadata(self):
        with self.assertRaisesRegex(ValueError, "source_id"):
            RawEntry(
                source="public-fixture",
                source_id="",
                entity_kind="mcp_server",
                canonical_id="io.evalrank.public-search-demo",
                raw_metadata={"homepage": "https://example.com/evalrank/public-search-demo"},
                declared_capability_shape={"tool_names": ["search"]},
                fetched_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "raw_metadata"):
            RawEntry(
                source="public-fixture",
                source_id="public-fixture:search-demo:2026-06-25",
                entity_kind="mcp_server",
                canonical_id="io.evalrank.public-search-demo",
                raw_metadata={1: "not-public-json-key"},
                declared_capability_shape={"tool_names": ["search"]},
                fetched_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "declared_capability_shape"):
            RawEntry(
                source="public-fixture",
                source_id="public-fixture:search-demo:2026-06-25",
                entity_kind="mcp_server",
                canonical_id="io.evalrank.public-search-demo",
                raw_metadata={"homepage": "https://example.com/evalrank/public-search-demo"},
                declared_capability_shape={"score": float("nan")},
                fetched_at="2026-06-25T00:00:00Z",
            )

        valid = {
            "source": "public-fixture",
            "source_id": "public-fixture:search-demo:2026-06-25",
            "entity_kind": "mcp_server",
            "canonical_id": "io.evalrank.public-search-demo",
            "raw_metadata": {"homepage": "https://example.com/evalrank/public-search-demo"},
            "declared_capability_shape": {"tool_names": ["search"]},
            "fetched_at": "2026-06-25T00:00:00Z",
        }
        for field in ("source", "source_id", "entity_kind", "canonical_id", "fetched_at"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    RawEntry(**{**valid, field: 123})

        with self.assertRaisesRegex(ValueError, "declared_capability_shape"):
            RawEntry(
                source="public-fixture",
                source_id="public-fixture:search-demo:2026-06-25",
                entity_kind="mcp_server",
                canonical_id="io.evalrank.public-search-demo",
                raw_metadata={"homepage": "https://example.com/evalrank/public-search-demo"},
                declared_capability_shape={},
                fetched_at="2026-06-25T00:00:00Z",
            )

    def test_entity_ref_rejects_schema_incompatible_values(self):
        for kwargs in (
            {"entity_type": 123, "entity_id": "tool:public-search-demo"},
            {"entity_type": "mcp_server", "entity_id": 123},
            {"entity_type": "", "entity_id": "tool:public-search-demo"},
            {"entity_type": "mcp_server", "entity_id": ""},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "entity_"):
                    EntityRef(**kwargs)

    def test_use_case_catalog_serializes_public_taxonomy(self):
        use_case = UseCase(
            id="code-generation",
            name="Code generation",
            definition="Produce correct code from a spec or prompt",
            entity_kinds=("model", "tool", "agent"),
            rank_policy="ranked",
            is_overlay=False,
        )
        catalog = UseCaseCatalog(
            methodology_version=PINNED_METHODOLOGY_VERSION,
            generated_at="2026-06-25T00:00:00Z",
            use_cases=(use_case,),
        )

        self.assertEqual(
            {
                "object": "use_case_catalog",
                "methodology_version": PINNED_METHODOLOGY_VERSION,
                "generated_at": "2026-06-25T00:00:00Z",
                "use_cases": [
                    {
                        "object": "use_case",
                        "id": "code-generation",
                        "name": "Code generation",
                        "definition": "Produce correct code from a spec or prompt",
                        "entity_kinds": ["model", "tool", "agent"],
                        "rank_policy": "ranked",
                        "is_overlay": False,
                    }
                ],
            },
            catalog.to_dict(),
        )

    def test_scoring_stage_catalog_serializes_public_stage_vocabulary(self):
        stage = ScoringStage(
            id="candidate-resolution",
            ordinal=2,
            name="Candidate resolution",
            description="Identify public candidates for a request",
            input_contracts=("EvaluationRequest",),
            output_contracts=("CandidateSet", "StageCandidate", "Exclusion"),
            public_boundary="storage-free contract refs only",
        )
        catalog = ScoringStageCatalog(
            methodology_version=PINNED_METHODOLOGY_VERSION,
            generated_at="2026-06-25T00:00:00Z",
            stages=(stage,),
        )

        self.assertEqual(
            {
                "object": "scoring_stage_catalog",
                "methodology_version": PINNED_METHODOLOGY_VERSION,
                "generated_at": "2026-06-25T00:00:00Z",
                "stages": [
                    {
                        "id": "candidate-resolution",
                        "ordinal": 2,
                        "name": "Candidate resolution",
                        "description": "Identify public candidates for a request",
                        "input_contracts": ["EvaluationRequest"],
                        "output_contracts": ["CandidateSet", "StageCandidate", "Exclusion"],
                        "public_boundary": "storage-free contract refs only",
                    }
                ],
            },
            catalog.to_dict(),
        )

    def test_scoring_stage_catalog_rejects_invalid_public_shape(self):
        valid_stage = ScoringStage(
            id="candidate-resolution",
            ordinal=2,
            name="Candidate resolution",
            description="Identify public candidates for a request",
            input_contracts=("EvaluationRequest",),
            output_contracts=("CandidateSet",),
            public_boundary="storage-free contract refs only",
        )

        with self.assertRaisesRegex(ValueError, "ordinal"):
            ScoringStage(
                id="bad-stage",
                ordinal=0,
                name="Bad stage",
                description="Bad ordinal",
                input_contracts=("EvaluationRequest",),
                output_contracts=("CandidateSet",),
                public_boundary="storage-free contract refs only",
            )
        with self.assertRaisesRegex(ValueError, "input_contracts"):
            ScoringStage(
                id="bad-stage",
                ordinal=1,
                name="Bad stage",
                description="Bad contracts",
                input_contracts=(),
                output_contracts=("CandidateSet",),
                public_boundary="storage-free contract refs only",
            )
        with self.assertRaisesRegex(TypeError, "stages"):
            ScoringStageCatalog(
                methodology_version=PINNED_METHODOLOGY_VERSION,
                generated_at="2026-06-25T00:00:00Z",
                stages=("not-stage",),
            )
        with self.assertRaisesRegex(ValueError, "duplicate stage id"):
            ScoringStageCatalog(
                methodology_version=PINNED_METHODOLOGY_VERSION,
                generated_at="2026-06-25T00:00:00Z",
                stages=(valid_stage, valid_stage),
            )

    def test_use_case_rejects_invalid_public_shape(self):
        with self.assertRaisesRegex(ValueError, "entity_kinds"):
            UseCase(
                id="code-generation",
                name="Code generation",
                definition="Produce correct code from a spec or prompt",
                entity_kinds=("model", "private_vendor"),
                rank_policy="ranked",
                is_overlay=False,
            )

        with self.assertRaisesRegex(ValueError, "duplicate use_case id"):
            row = UseCase(
                id="code-generation",
                name="Code generation",
                definition="Produce correct code from a spec or prompt",
                entity_kinds=("model",),
                rank_policy="ranked",
                is_overlay=False,
            )
            UseCaseCatalog(
                methodology_version=PINNED_METHODOLOGY_VERSION,
                generated_at="2026-06-25T00:00:00Z",
                use_cases=(row, row),
            )

        with self.assertRaisesRegex(ValueError, "rank_policy"):
            UseCase(
                id="safety-robustness",
                name="Safety / robustness",
                definition="Resistance to harmful or manipulated operation",
                entity_kinds=("model", "tool", "agent"),
                rank_policy="ranked",
                is_overlay=True,
            )

    def test_ranked_entity_requires_score_context(self):
        row = RankedEntity(
            entity_type="mcp_server",
            entity_id="tool:exa-search-mcp",
            rank=1,
            capability_score=0.84,
            confidence=0.86,
            ci95=ConfidenceInterval(low=0.80, high=0.88),
            methodology_version=PINNED_METHODOLOGY_VERSION,
            trust_tier="standardized",
            freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
            evidence_count=1840,
        )

        payload = row.to_dict()

        self.assertEqual("tool:exa-search-mcp", payload["id"])
        self.assertEqual([0.8, 0.88], payload["ci95"])
        self.assertEqual(PINNED_METHODOLOGY_VERSION, payload["methodology_version"])
        self.assertEqual("fresh", payload["freshness"]["status"])

    def test_freshness_rejects_schema_incompatible_values(self):
        for kwargs in (
            {"status": "fresh", "last_eval": 123, "next_refresh": "2026-06-17"},
            {"status": "fresh", "last_eval": "2026-06-10", "next_refresh": 123},
            {"status": "fresh", "last_eval": "", "next_refresh": "2026-06-17"},
            {"status": "fresh", "last_eval": "2026-06-10", "next_refresh": ""},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "freshness"):
                    Freshness(**kwargs)

    def test_ranked_entity_rejects_bare_or_invalid_scores(self):
        with self.assertRaisesRegex(ValueError, "capability_score"):
            RankedEntity(
                entity_type="model_version",
                entity_id="model_version:vendor/model@1",
                rank=1,
                capability_score=1.4,
                confidence=0.5,
                ci95=ConfidenceInterval(low=0.4, high=0.6),
                methodology_version=PINNED_METHODOLOGY_VERSION,
                trust_tier="verified",
                freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
                evidence_count=10,
            )

        valid = {
            "entity_type": "model_version",
            "entity_id": "model_version:vendor/model@1",
            "rank": 1,
            "capability_score": 0.4,
            "confidence": 0.5,
            "ci95": ConfidenceInterval(low=0.4, high=0.6),
            "methodology_version": PINNED_METHODOLOGY_VERSION,
            "trust_tier": "verified",
            "freshness": Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
            "evidence_count": 10,
        }
        for components in ("not-a-map", {"": 0.5}, {1: 0.5}, {"capability": True}, {"capability": 1.2}):
            with self.subTest(components=components):
                with self.assertRaisesRegex(ValueError, "score_components"):
                    RankedEntity(**{**valid, "score_components": components})

        for overrides in (
            {"entity_type": 123},
            {"entity_id": 123},
            {"rank": True},
            {"evidence_count": True},
            {"caveats": "not-an-array"},
            {"caveats": (123,)},
        ):
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValueError):
                    RankedEntity(**{**valid, **overrides})

        with self.assertRaisesRegex(ValueError, "methodology_version"):
            RankedEntity(
                entity_type="model_version",
                entity_id="model_version:vendor/model@1",
                rank=1,
                capability_score=0.4,
                confidence=0.5,
                ci95=ConfidenceInterval(low=0.4, high=0.6),
                methodology_version="",
                trust_tier="verified",
                freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
                evidence_count=10,
            )

    def test_recommendation_enforces_ranked_or_grouped_shape(self):
        row = _row("tool:exa-search-mcp")

        rec = Recommendation.single_scale(
            request_id="req_01",
            use_case="web-browsing:fresh-news",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            ranked=[row],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="one candidate clears the evidence floor",
        )

        payload = rec.to_dict()

        self.assertEqual("recommendation", payload["object"])
        self.assertEqual("single-scale", payload["comparability"])
        self.assertIn("abstention", payload)
        self.assertIsNone(payload["abstention"])
        self.assertEqual([row.to_dict()], payload["ranked"])
        self.assertIsNone(payload["groups"])
        self.assertTrue(rec.result_usable)
        self.assertTrue(payload["recommendation_id"].startswith("rec_"))
        self.assertEqual(payload["recommendation_id"], payload["recommend_id"])
        self.assertEqual(payload["recommendation_id"], payload["search_run_id"])

    def test_recommendation_rejects_schema_incompatible_envelope_fields(self):
        valid = {
            "request_id": "req_01",
            "use_case": "web-browsing:fresh-news",
            "methodology_version": PINNED_METHODOLOGY_VERSION,
            "generated_at": "2026-06-25T00:00:00Z",
            "comparability": "single-scale",
            "ranked": [_row("tool:exa-search-mcp")],
            "groups": None,
            "shortlist_depth": 1,
            "depth_rationale": "one candidate clears the evidence floor",
        }

        invalid_values = (
            ("shortlist_depth", True),
            ("depth_rationale", ""),
            ("degraded", "false"),
            ("served_from", ""),
            ("base_snapshot_lag_ms", True),
            ("base_snapshot_lag_ms", -1),
            ("base_snapshot_lag_ms", 1.5),
        )
        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(ValueError, field):
                    Recommendation(**{**valid, field: value})

    def test_recommendation_rejects_duplicate_ranked_entities(self):
        row = _row("tool:exa-search-mcp")

        with self.assertRaisesRegex(ValueError, "duplicate ranked entity"):
            Recommendation.single_scale(
                request_id="req_01",
                use_case="web-browsing:fresh-news",
                methodology_version=PINNED_METHODOLOGY_VERSION,
                ranked=[row, row],
                generated_at="2026-06-25T00:00:00Z",
                depth_rationale="one candidate clears the evidence floor",
            )

    def test_ranking_group_serializes_within_kind_rows(self):
        row = _row("tool:exa-search-mcp")
        group = RankingGroup(
            group_key="mcp_server",
            entity_type="mcp_server",
            ranked=(row,),
            group_rationale="MCP servers are ranked only against MCP servers",
        )

        self.assertEqual(
            {
                "object": "ranking_group",
                "group_key": "mcp_server",
                "entity_type": "mcp_server",
                "ranked": [row.to_dict()],
                "group_rationale": "MCP servers are ranked only against MCP servers",
            },
            group.to_dict(),
        )

    def test_kind_grouped_recommendation_serializes_groups_not_global_ranked_rows(self):
        row = _row("tool:exa-search-mcp")
        group = RankingGroup(
            group_key="mcp_server",
            entity_type="mcp_server",
            ranked=(row,),
            group_rationale="MCP servers are ranked only against MCP servers",
        )

        rec = Recommendation.kind_grouped(
            request_id="req_01",
            use_case="mcp-tool-orchestration",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            groups=[group],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="different entity kinds are not on one score scale",
        )

        payload = rec.to_dict()

        self.assertEqual("kind-grouped", payload["comparability"])
        self.assertEqual([], payload["ranked"])
        self.assertEqual([group.to_dict()], payload["groups"])
        self.assertEqual(1, payload["shortlist_depth"])
        self.assertTrue(rec.result_usable)

    def test_ranking_group_rejects_private_or_cross_kind_shapes(self):
        row = _row("model:public-demo", entity_type="model_version")

        with self.assertRaisesRegex(ValueError, "entity_type"):
            RankingGroup(
                group_key="tool_server",
                entity_type="tool_server",
                ranked=(row,),
                group_rationale="wrong entity type",
            )

        with self.assertRaisesRegex(ValueError, "methodology_version"):
            Recommendation.kind_grouped(
                request_id="req_01",
                use_case="mcp-tool-orchestration",
                methodology_version=PINNED_METHODOLOGY_VERSION,
                groups=[
                    RankingGroup(
                        group_key="model_version",
                        entity_type="model_version",
                        ranked=(
                            _row(
                                "model:public-demo",
                                methodology_version="2026-06-25.2.public-fixture-v1",
                                entity_type="model_version",
                            ),
                        ),
                        group_rationale="different methodology",
                    )
                ],
                generated_at="2026-06-25T00:00:00Z",
                depth_rationale="different methodology should not serialize",
            )

    def test_recommendation_id_is_content_addressed(self):
        base = Recommendation.single_scale(
            request_id="req_a",
            use_case="function-calling",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )
        same_payload_new_request = Recommendation.single_scale(
            request_id="req_b",
            use_case="function-calling",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )
        changed_methodology = Recommendation.single_scale(
            request_id="req_a",
            use_case="function-calling",
            methodology_version="2026-06-25.2.public-fixture-v1",
            ranked=[_row("tool:exa-search-mcp", methodology_version="2026-06-25.2.public-fixture-v1")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="clear top set",
        )

        self.assertEqual(base.recommendation_id, same_payload_new_request.recommendation_id)
        self.assertNotEqual(base.recommendation_id, changed_methodology.recommendation_id)

    def test_the_call_serializes_public_decision_confidence(self):
        call = TheCall.recommend(confidence=0.86, reason="clear top set")
        abstain = TheCall.abstain(reason="insufficient_evidence")

        self.assertEqual(
            {
                "decision": "recommend",
                "confidence": 0.86,
                "reason": "clear top set",
                "abstention_reason": None,
            },
            call.to_dict(),
        )
        self.assertEqual(
            {
                "decision": "abstain",
                "confidence": None,
                "reason": "insufficient_evidence",
                "abstention_reason": "insufficient_evidence",
            },
            abstain.to_dict(),
        )

    def test_abstention_serializes_public_reason(self):
        self.assertTrue(hasattr(contracts, "Abstention"))

        abstention = contracts.Abstention(
            reason="insufficient_evidence",
            detail="no standardized-harness evidence; below ranking floor",
        )

        self.assertEqual(
            {
                "reason": "insufficient_evidence",
                "detail": "no standardized-harness evidence; below ranking floor",
            },
            abstention.to_dict(),
        )
        for kwargs in (
            {"reason": "", "detail": "below ranking floor"},
            {"reason": "insufficient_evidence", "detail": ""},
            {"reason": 123, "detail": "below ranking floor"},
            {"reason": "insufficient_evidence", "detail": 123},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "reason|detail"):
                    contracts.Abstention(**kwargs)

    def test_the_call_rejects_private_or_incomplete_shapes(self):
        with self.assertRaisesRegex(ValueError, "decision"):
            TheCall(decision="maybe", confidence=0.5, reason="not a public decision")

        with self.assertRaisesRegex(ValueError, "confidence"):
            TheCall(decision="recommend", confidence=None, reason="missing confidence")

        with self.assertRaisesRegex(ValueError, "confidence"):
            TheCall.recommend(confidence=1.2, reason="outside unit interval")

        with self.assertRaisesRegex(ValueError, "reason"):
            TheCall.recommend(confidence=0.5, reason="")

        for kwargs in (
            {"decision": "recommend", "confidence": 0.5, "reason": 123},
            {
                "decision": "abstain",
                "confidence": None,
                "reason": "insufficient_evidence",
                "abstention_reason": 123,
            },
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "reason"):
                    TheCall(**kwargs)

    def test_abstention_is_not_value_bearing(self):
        rec = Recommendation.abstain(
            request_id="req_01",
            use_case="mobile-codegen:flutter",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            generated_at="2026-06-25T00:00:00Z",
            reason="insufficient_evidence",
            detail="no standardized-harness evidence; below ranking floor",
        )

        self.assertFalse(rec.result_usable)
        self.assertEqual([], rec.ranked)
        self.assertEqual("abstain", rec.the_call.decision)
        payload = rec.to_dict()
        self.assertEqual("insufficient_evidence", payload["the_call"]["abstention_reason"])
        self.assertEqual(
            {
                "reason": "insufficient_evidence",
                "detail": "no standardized-harness evidence; below ranking floor",
            },
            payload["abstention"],
        )
        with self.assertRaisesRegex(ValueError, "detail"):
            Recommendation.abstain(
                request_id="req_01",
                use_case="mobile-codegen:flutter",
                methodology_version=PINNED_METHODOLOGY_VERSION,
                generated_at="2026-06-25T00:00:00Z",
                reason="insufficient_evidence",
                detail="",
            )

    def test_methodology_version_rejects_unpinned_format(self):
        with self.assertRaisesRegex(ValueError, "methodology_version"):
            _row("tool:exa-search-mcp", methodology_version="2026.06.1")

        with self.assertRaisesRegex(ValueError, "methodology_version"):
            Recommendation.single_scale(
                request_id="req_bad_version",
                use_case="function-calling",
                methodology_version="2026.06.1",
                ranked=[_row("tool:exa-search-mcp")],
                generated_at="2026-06-25T00:00:00Z",
                depth_rationale="old version format should not serialize",
            )

    def test_evidence_item_serializes_public_subject_and_score(self):
        item = EvidenceItem(
            evidence_id="ev_public_trace_01",
            subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            kind="trace",
            source="public-fixture",
            observed_at="2026-06-25T00:00:00Z",
            summary="public search demo returned a fresh cited result",
            score=0.8754321,
            metadata={"latency_ms": 1200, "region": "iad"},
        )

        payload = item.to_dict()

        self.assertEqual("ev_public_trace_01", payload["evidence_id"])
        self.assertEqual({"entity_type": "mcp_server", "id": "tool:public-search-demo"}, payload["subject"])
        self.assertEqual("trace", payload["kind"])
        self.assertEqual(0.875432, payload["score"])
        self.assertEqual(["latency_ms", "region"], sorted(payload["metadata"]))

    def test_evidence_item_rejects_invalid_kind_or_score(self):
        subject = EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")

        with self.assertRaisesRegex(ValueError, "kind"):
            EvidenceItem(
                evidence_id="ev_bad_kind",
                subject=subject,
                kind="unsupported-kind",
                source="public-fixture",
                observed_at="2026-06-25T00:00:00Z",
                summary="invalid kind",
            )

        with self.assertRaisesRegex(ValueError, "score"):
            EvidenceItem(
                evidence_id="ev_bad_score",
                subject=subject,
                kind="trace",
                source="public-fixture",
                observed_at="2026-06-25T00:00:00Z",
                summary="invalid score",
                score=1.2,
            )

        for metadata in ("not-a-map", {"nested": {1: "not-public-json-key"}}, {"value": float("nan")}):
            with self.subTest(metadata=metadata):
                with self.assertRaisesRegex(ValueError, "metadata"):
                    EvidenceItem(
                        evidence_id="ev_bad_metadata",
                        subject=subject,
                        kind="trace",
                        source="public-fixture",
                        observed_at="2026-06-25T00:00:00Z",
                        summary="invalid metadata",
                        metadata=metadata,
                    )

        valid = {
            "evidence_id": "ev_public_trace_01",
            "subject": subject,
            "kind": "trace",
            "source": "public-fixture",
            "observed_at": "2026-06-25T00:00:00Z",
            "summary": "public search demo returned a fresh cited result",
        }
        for field in ("evidence_id", "source", "observed_at", "summary"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    EvidenceItem(**{**valid, field: 123})

    def test_result_row_serializes_public_provenance_envelope(self):
        row = ResultRow(
            entity_id="tool:public-search-demo",
            entity_kind="tool_server",
            benchmark_id="bench_public_search_freshness",
            benchmark_version="2026-06-25",
            harness="public-fixture-harness",
            harness_version="2026-06-25.1",
            is_self_reported=False,
            n_items=40,
            ci95=ConfidenceInterval(low=0.80, high=0.88),
            score_raw=0.8754321,
            score_unit="pass_rate",
            date_run="2026-06-25",
            model_version="public-search-demo@2026-06-25",
            provenance={
                "raw_snapshot_uri": "https://example.com/evalrank/public-search-demo/raw.json",
                "source": "public-fixture",
            },
            source_url="https://example.com/evalrank/public-search-demo",
            attribution_string="Synthetic public fixture",
            flags={
                "saturated": False,
                "contaminated": False,
                "judge_model_dependent": False,
                "scaffold_nonstandard": False,
            },
            verification_state="verified",
        )

        payload = row.to_dict()

        self.assertEqual("result_row", payload["object"])
        self.assertEqual("tool:public-search-demo", payload["entity_id"])
        self.assertEqual("tool_server", payload["entity_kind"])
        self.assertEqual([0.8, 0.88], payload["ci95"])
        self.assertEqual(0.875432, payload["score_raw"])
        self.assertEqual(["raw_snapshot_uri", "source"], sorted(payload["provenance"]))
        self.assertEqual(
            {
                "contaminated": False,
                "judge_model_dependent": False,
                "saturated": False,
                "scaffold_nonstandard": False,
            },
            payload["flags"],
        )
        self.assertEqual("verified", payload["verification_state"])

    def test_result_row_rejects_invalid_public_shape(self):
        valid = {
            "entity_id": "tool:public-search-demo",
            "entity_kind": "tool_server",
            "benchmark_id": "bench_public_search_freshness",
            "benchmark_version": "2026-06-25",
            "harness": "public-fixture-harness",
            "harness_version": "2026-06-25.1",
            "is_self_reported": False,
            "n_items": 40,
            "ci95": ConfidenceInterval(low=0.80, high=0.88),
            "score_raw": 0.8754321,
            "score_unit": "pass_rate",
            "date_run": "2026-06-25",
            "model_version": "public-search-demo@2026-06-25",
            "provenance": {"source": "public-fixture"},
            "source_url": "https://example.com/evalrank/public-search-demo",
            "attribution_string": "Synthetic public fixture",
            "flags": {
                "saturated": False,
                "contaminated": False,
                "judge_model_dependent": False,
                "scaffold_nonstandard": False,
            },
            "verification_state": "verified",
        }

        with self.assertRaisesRegex(ValueError, "entity_kind"):
            ResultRow(**{**valid, "entity_kind": "mcp_server"})

        with self.assertRaisesRegex(ValueError, "n_items"):
            ResultRow(**{**valid, "n_items": -1})

        with self.assertRaisesRegex(ValueError, "score_raw"):
            ResultRow(**{**valid, "score_raw": float("nan")})

        with self.assertRaisesRegex(ValueError, "source_url"):
            ResultRow(**{**valid, "source_url": 123})

        with self.assertRaisesRegex(ValueError, "provenance"):
            ResultRow(**{**valid, "provenance": {1: "not-public-json-key"}})

        with self.assertRaisesRegex(ValueError, "flags"):
            ResultRow(**{**valid, "flags": ["saturated"]})

        with self.assertRaisesRegex(ValueError, "flags"):
            ResultRow(**{**valid, "flags": {"saturated": False}})

        with self.assertRaisesRegex(ValueError, "flags"):
            ResultRow(**{**valid, "flags": {**valid["flags"], "extra": False}})

        with self.assertRaisesRegex(ValueError, "flags"):
            ResultRow(**{**valid, "flags": {**valid["flags"], "saturated": "false"}})

        with self.assertRaisesRegex(ValueError, "verification_state"):
            ResultRow(**{**valid, "verification_state": "unverified"})

    def test_exclusion_serializes_public_subject_and_reason(self):
        exclusion = Exclusion(
            subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            reason="unknown_cost",
            detail="cost is unknown for this public fixture",
        )

        self.assertEqual(
            {
                "subject": {"entity_type": "mcp_server", "id": "tool:public-search-demo"},
                "reason": "unknown_cost",
                "detail": "cost is unknown for this public fixture",
            },
            exclusion.to_dict(),
        )

    def test_exclusion_rejects_invalid_public_shape(self):
        subject = EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")

        with self.assertRaisesRegex(TypeError, "subject"):
            Exclusion(subject="tool:public-search-demo", reason="unknown_cost", detail="invalid subject")

        with self.assertRaisesRegex(ValueError, "reason"):
            Exclusion(subject=subject, reason="", detail="missing reason")

        with self.assertRaisesRegex(ValueError, "reason"):
            Exclusion(subject=subject, reason=42, detail="non-string reason")

        with self.assertRaisesRegex(ValueError, "detail"):
            Exclusion(subject=subject, reason="unknown_cost", detail="")

        with self.assertRaisesRegex(ValueError, "detail"):
            Exclusion(subject=subject, reason="unknown_cost", detail=42)

    def test_recommendation_serializes_public_exclusions(self):
        exclusion = Exclusion(
            subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            reason="unknown_cost",
            detail="cost is unknown for this public fixture",
        )
        rec = Recommendation.single_scale(
            request_id="req_01",
            use_case="function-calling",
            methodology_version=PINNED_METHODOLOGY_VERSION,
            ranked=[_row("tool:exa-search-mcp")],
            generated_at="2026-06-25T00:00:00Z",
            depth_rationale="one candidate clears the evidence floor",
            exclusions=[exclusion],
        )

        self.assertEqual([exclusion.to_dict()], rec.to_dict()["exclusions"])

    def test_evidence_set_serializes_public_evidence_items(self):
        evidence = EvidenceItem(
            evidence_id="ev_public_trace_01",
            subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            kind="trace",
            source="public-fixture",
            observed_at="2026-06-25T00:00:00Z",
            summary="public search demo returned a fresh cited result",
            score=0.8754321,
            metadata={"latency_ms": 1200},
        )
        evidence_set = EvidenceSet(
            request_id="req_public_fixture_01",
            use_case="web-browsing",
            evidence_items=(evidence,),
            generated_at="2026-06-25T00:00:00Z",
        )

        payload = evidence_set.to_dict()

        self.assertEqual("evidence_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-browsing", payload["use_case"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["generated_at"])
        self.assertEqual([evidence.to_dict()], payload["evidence_items"])

    def test_evidence_set_allows_empty_and_rejects_invalid_items(self):
        empty = EvidenceSet(
            request_id="req_public_fixture_01",
            use_case="web-browsing",
            evidence_items=(),
            generated_at="2026-06-25T00:00:00Z",
        )

        self.assertEqual([], empty.to_dict()["evidence_items"])

        evidence = EvidenceItem(
            evidence_id="ev_public_trace_01",
            subject=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            kind="trace",
            source="public-fixture",
            observed_at="2026-06-25T00:00:00Z",
            summary="public search demo returned a fresh cited result",
        )

        with self.assertRaisesRegex(ValueError, "request_id"):
            EvidenceSet(
                request_id="",
                use_case="web-browsing",
                evidence_items=(evidence,),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "use_case"):
            EvidenceSet(
                request_id="req_public_fixture_01",
                use_case="",
                evidence_items=(evidence,),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(TypeError, "evidence_items"):
            EvidenceSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                evidence_items=("ev_public_trace_01",),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "duplicate"):
            EvidenceSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                evidence_items=(evidence, evidence),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "generated_at"):
            EvidenceSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                evidence_items=(evidence,),
                generated_at="",
            )

        valid = {
            "request_id": "req_public_fixture_01",
            "use_case": "web-browsing",
            "evidence_items": (evidence,),
            "generated_at": "2026-06-25T00:00:00Z",
        }
        for field in ("request_id", "use_case", "generated_at"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    EvidenceSet(**{**valid, field: 123})

    def test_stage_candidate_serializes_public_stage_one_boundary(self):
        candidate = StageCandidate(
            candidate_id=PUBLIC_CAPABILITY_FINGERPRINT,
            entity=EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),
            fused_score=0.0327864,
            rrf_components={"lexical_rank": 1, "semantic_rank": 2, "graph_rank": None},
            retrieval_arms=("semantic", "lexical"),
            use_case="web-browsing",
        )

        self.assertEqual(
            {
                "object": "stage_candidate",
                "candidate_id": PUBLIC_CAPABILITY_FINGERPRINT,
                "entity": {"entity_type": "mcp_server", "id": "tool:public-search-demo"},
                "fused_score": 0.032786,
                "rrf_components": {"lexical_rank": 1, "semantic_rank": 2, "graph_rank": None},
                "retrieval_provenance": {
                    "arms": ["lexical", "semantic"],
                    "use_case": "web-browsing",
                },
            },
            candidate.to_dict(),
        )

    def test_stage_candidate_rejects_invalid_public_shape(self):
        entity = EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")
        valid = {
            "candidate_id": PUBLIC_CAPABILITY_FINGERPRINT,
            "entity": entity,
            "fused_score": 0.032786,
            "rrf_components": {"lexical_rank": 1, "semantic_rank": 2, "graph_rank": None},
            "retrieval_arms": ("lexical", "semantic"),
            "use_case": "web-browsing",
        }

        with self.assertRaisesRegex(ValueError, "candidate_id"):
            StageCandidate(**{**valid, "candidate_id": "not-a-fingerprint"})

        with self.assertRaisesRegex(TypeError, "entity"):
            StageCandidate(**{**valid, "entity": "tool:public-search-demo"})

        with self.assertRaisesRegex(ValueError, "fused_score"):
            StageCandidate(**{**valid, "fused_score": -0.1})

        with self.assertRaisesRegex(ValueError, "rrf_components"):
            StageCandidate(**{**valid, "rrf_components": {"lexical_rank": 1}})

        with self.assertRaisesRegex(ValueError, "rrf_components"):
            StageCandidate(**{**valid, "rrf_components": ["lexical_rank", "semantic_rank", "graph_rank"]})

        with self.assertRaisesRegex(ValueError, "semantic_rank"):
            StageCandidate(
                **{
                    **valid,
                    "rrf_components": {"lexical_rank": 1, "semantic_rank": 0, "graph_rank": None},
                }
            )

        with self.assertRaisesRegex(ValueError, "retrieval_arms"):
            StageCandidate(**{**valid, "retrieval_arms": ("lexical", "lexical")})

        with self.assertRaisesRegex(ValueError, "retrieval_arms"):
            StageCandidate(**{**valid, "retrieval_arms": "semantic"})

        with self.assertRaisesRegex(ValueError, "retrieval_arms"):
            StageCandidate(**{**valid, "retrieval_arms": ("",)})

        with self.assertRaisesRegex(ValueError, "use_case"):
            StageCandidate(**{**valid, "use_case": ""})

    def test_evaluation_request_serializes_public_input_context(self):
        request = EvaluationRequest(
            request_id="req_public_fixture_01",
            use_case="web-browsing",
            entity_types=("mcp_server",),
            requested_at="2026-06-25T00:00:00Z",
            constraints={"region": "public", "requires_citations": True},
        )

        payload = request.to_dict()

        self.assertEqual("evaluation_request", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-browsing", payload["use_case"])
        self.assertEqual(["mcp_server"], payload["entity_types"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["requested_at"])
        self.assertEqual(["region", "requires_citations"], sorted(payload["constraints"]))

    def test_evaluation_request_rejects_missing_required_context(self):
        with self.assertRaisesRegex(ValueError, "request_id"):
            EvaluationRequest(
                request_id="",
                use_case="web-browsing",
                entity_types=("mcp_server",),
                requested_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "entity_types"):
            EvaluationRequest(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                entity_types=(),
                requested_at="2026-06-25T00:00:00Z",
            )

        for entity_types in ("mcp_server", (123,), ("",)):
            with self.subTest(entity_types=entity_types):
                with self.assertRaisesRegex(ValueError, "entity_types"):
                    EvaluationRequest(
                        request_id="req_public_fixture_01",
                        use_case="web-browsing",
                        entity_types=entity_types,
                        requested_at="2026-06-25T00:00:00Z",
                    )

        with self.assertRaisesRegex(ValueError, "constraints"):
            EvaluationRequest(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                entity_types=("mcp_server",),
                requested_at="2026-06-25T00:00:00Z",
                constraints={1: "not-public-json-key"},
            )

        for constraints in ("not-a-map", {"nested": {1: "not-public-json-key"}}, {"value": float("nan")}):
            with self.subTest(constraints=constraints):
                with self.assertRaisesRegex(ValueError, "constraints"):
                    EvaluationRequest(
                        request_id="req_public_fixture_01",
                        use_case="web-browsing",
                        entity_types=("mcp_server",),
                        requested_at="2026-06-25T00:00:00Z",
                        constraints=constraints,
                    )

    def test_candidate_set_serializes_public_candidate_refs(self):
        candidate_set = CandidateSet(
            request_id="req_public_fixture_01",
            use_case="web-browsing",
            candidates=(EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo"),),
            generated_at="2026-06-25T00:00:00Z",
        )

        payload = candidate_set.to_dict()

        self.assertEqual("candidate_set", payload["object"])
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("web-browsing", payload["use_case"])
        self.assertEqual("2026-06-25T00:00:00Z", payload["generated_at"])
        self.assertEqual(
            [{"entity_type": "mcp_server", "id": "tool:public-search-demo"}],
            payload["candidates"],
        )

    def test_candidate_set_rejects_invalid_or_duplicate_candidates(self):
        candidate = EntityRef(entity_type="mcp_server", entity_id="tool:public-search-demo")

        with self.assertRaisesRegex(ValueError, "request_id"):
            CandidateSet(
                request_id="",
                use_case="web-browsing",
                candidates=(candidate,),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "use_case"):
            CandidateSet(
                request_id="req_public_fixture_01",
                use_case="",
                candidates=(candidate,),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "candidates"):
            CandidateSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                candidates=(),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(TypeError, "candidates"):
            CandidateSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                candidates=("tool:public-search-demo",),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "duplicate"):
            CandidateSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                candidates=(candidate, candidate),
                generated_at="2026-06-25T00:00:00Z",
            )

        with self.assertRaisesRegex(ValueError, "generated_at"):
            CandidateSet(
                request_id="req_public_fixture_01",
                use_case="web-browsing",
                candidates=(candidate,),
                generated_at="",
            )

        valid = {
            "request_id": "req_public_fixture_01",
            "use_case": "web-browsing",
            "candidates": (candidate,),
            "generated_at": "2026-06-25T00:00:00Z",
        }
        for field in ("request_id", "use_case", "generated_at"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    CandidateSet(**{**valid, field: 123})


def _row(
    entity_id: str,
    methodology_version: str = PINNED_METHODOLOGY_VERSION,
    entity_type: str = "mcp_server",
) -> RankedEntity:
    return RankedEntity(
        entity_type=entity_type,
        entity_id=entity_id,
        rank=1,
        capability_score=0.84,
        confidence=0.86,
        ci95=ConfidenceInterval(low=0.80, high=0.88),
        methodology_version=methodology_version,
        trust_tier="standardized",
        freshness=Freshness(status="fresh", last_eval="2026-06-10", next_refresh="2026-06-17"),
        evidence_count=1840,
    )


if __name__ == "__main__":
    unittest.main()
