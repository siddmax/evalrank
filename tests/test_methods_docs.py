import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MethodsDocsTests(unittest.TestCase):
    def test_methods_readme_lists_public_method_notes(self):
        methods = REPO_ROOT / "methods"
        text = (methods / "README.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"- `([^`]+\.md)`", text))
        expected = {path.name for path in methods.glob("*.md") if path.name not in {"AGENTS.md", "README.md"}}

        self.assertEqual(expected, documented)

    def test_evidence_synthesis_defines_public_decision_method(self):
        text = (REPO_ROOT / "methods" / "evidence-synthesis.md").read_text(encoding="utf-8")

        for phrase in (
            "provisional aggregate",
            "native metric",
            "ranking group",
            "tie group",
            "sensitivity",
            "calibrated bootstrap superiority",
            "explorer",
            "top set",
            "single winner",
            "challenger",
            "leave-one-family-out",
        ):
            self.assertIn(phrase, text.lower())
        self.assertNotIn("posterior superiority", text.lower())

    def test_scoring_stages_note_tracks_public_catalog_and_private_boundary(self):
        text = (REPO_ROOT / "methods" / "scoring-stages.md").read_text(encoding="utf-8")

        for phrase in (
            "ScoringStageCatalog",
            "`request-normalization`",
            "`candidate-resolution`",
            "`evidence-attachment`",
            "`component-scoring`",
            "`ranking-or-abstention`",
            "`freshness-trust-labeling`",
            "private formulas",
            "held-out evals",
            "production telemetry",
        ):
            self.assertIn(phrase, text)

    def test_use_case_taxonomy_note_tracks_public_contract_and_private_boundary(self):
        text = (REPO_ROOT / "methods" / "use-case-taxonomy.md").read_text(encoding="utf-8")

        for phrase in (
            "UseCaseCatalog",
            "`id`",
            "`name`",
            "`definition`",
            "`entity_kinds`",
            "`rank_policy`",
            "`is_overlay`",
            "cross-cutting safety veto",
            "`kind-grouped`",
            "catalog/manifest.json",
            "exact ranking group",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
