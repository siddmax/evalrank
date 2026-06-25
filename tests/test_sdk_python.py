import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_SRC = REPO_ROOT / "packages" / "sdk-python" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(SDK_SRC))

from evalrank_core.contracts import EvidenceItem as CoreEvidenceItem  # noqa: E402
from evalrank_core.contracts import EvaluationRequest as CoreEvaluationRequest  # noqa: E402
from evalrank_sdk import EvaluationRequest, EvidenceItem, sample_evidence_item, sample_evaluation_request  # noqa: E402


class PythonSdkTests(unittest.TestCase):
    def test_sdk_re_exports_core_evidence_contracts(self):
        evidence = sample_evidence_item()

        self.assertIs(EvidenceItem, CoreEvidenceItem)
        self.assertIsInstance(evidence, CoreEvidenceItem)
        self.assertEqual("tool:public-search-demo", evidence.to_dict()["subject"]["id"])

    def test_sdk_re_exports_core_request_contracts(self):
        request = sample_evaluation_request()

        self.assertIs(EvaluationRequest, CoreEvaluationRequest)
        self.assertIsInstance(request, CoreEvaluationRequest)
        self.assertEqual("web-research:freshness-check", request.to_dict()["use_case"])


if __name__ == "__main__":
    unittest.main()
