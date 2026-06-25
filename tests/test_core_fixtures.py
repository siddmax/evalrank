import sys
import unittest
from pathlib import Path


CORE_SRC = Path(__file__).resolve().parents[1] / "packages" / "core" / "src"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.fixtures import (  # noqa: E402
    PUBLIC_METHODOLOGY_VERSION,
    sample_ranked_entity,
    sample_recommendation,
)


class CoreFixtureTests(unittest.TestCase):
    def test_sample_ranked_entity_is_public_contract_payload(self):
        row = sample_ranked_entity()
        payload = row.to_dict()

        self.assertEqual("tool:public-search-demo", payload["id"])
        self.assertEqual(PUBLIC_METHODOLOGY_VERSION, payload["methodology_version"])
        self.assertEqual(["capability", "evidence", "freshness"], sorted(payload["score_components"]))

    def test_sample_recommendation_is_usable_and_stable(self):
        rec = sample_recommendation()
        payload = rec.to_dict()

        self.assertTrue(rec.result_usable)
        self.assertEqual("req_public_fixture_01", payload["request_id"])
        self.assertEqual("single-scale", payload["comparability"])
        self.assertEqual([sample_ranked_entity().to_dict()], payload["ranked"])
        self.assertEqual(sample_recommendation().recommendation_id, rec.recommendation_id)


if __name__ == "__main__":
    unittest.main()
