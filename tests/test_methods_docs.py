import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MethodsDocsTests(unittest.TestCase):
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
            "`safety-robustness`",
            "`kind-grouped`",
            "private thresholds",
            "held-out tasks",
            "benchmark outputs",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
