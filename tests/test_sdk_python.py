import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_SRC = REPO_ROOT / "packages" / "sdk-python" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(SDK_SRC))

from evalrank_core.contracts import CapabilityFingerprintInput as CoreCapabilityFingerprintInput  # noqa: E402
from evalrank_core.contracts import EvidenceItem as CoreEvidenceItem  # noqa: E402
from evalrank_core.contracts import EvaluationRequest as CoreEvaluationRequest  # noqa: E402
from evalrank_core.contracts import RawEntry as CoreRawEntry  # noqa: E402
from evalrank_core.contracts import TheCall as CoreTheCall  # noqa: E402
from evalrank_sdk import (  # noqa: E402
    CapabilityFingerprintInput,
    EvaluationRequest,
    EvidenceItem,
    RawEntry,
    TheCall,
    sample_capability_fingerprint_input,
    sample_evidence_item,
    sample_evaluation_request,
    sample_raw_entry,
)


class PythonSdkTests(unittest.TestCase):
    def test_sdk_re_exports_core_capability_fingerprint_contracts(self):
        fingerprint_input = sample_capability_fingerprint_input()

        self.assertIs(CapabilityFingerprintInput, CoreCapabilityFingerprintInput)
        self.assertIsInstance(fingerprint_input, CoreCapabilityFingerprintInput)
        self.assertEqual(64, len(fingerprint_input.to_dict()["capability_fingerprint"]))

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

    def test_sdk_re_exports_core_raw_entry_contracts(self):
        entry = sample_raw_entry()

        self.assertIs(RawEntry, CoreRawEntry)
        self.assertIsInstance(entry, CoreRawEntry)
        self.assertEqual("raw_entry", entry.to_dict()["object"])

    def test_sdk_re_exports_core_the_call_contract(self):
        self.assertIs(TheCall, CoreTheCall)
        self.assertEqual("recommend", TheCall.recommend(confidence=0.86, reason="clear top set").decision)


if __name__ == "__main__":
    unittest.main()
