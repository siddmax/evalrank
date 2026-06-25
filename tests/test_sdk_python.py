import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
SDK_SRC = REPO_ROOT / "packages" / "sdk-python" / "src"
sys.path.insert(0, str(CORE_SRC))
sys.path.insert(0, str(SDK_SRC))

from evalrank_core.contracts import CapabilityFingerprintInput as CoreCapabilityFingerprintInput  # noqa: E402
from evalrank_core.contracts import CandidateSet as CoreCandidateSet  # noqa: E402
from evalrank_core.contracts import Exclusion as CoreExclusion  # noqa: E402
from evalrank_core.contracts import EvidenceItem as CoreEvidenceItem  # noqa: E402
from evalrank_core.contracts import EvidenceSet as CoreEvidenceSet  # noqa: E402
from evalrank_core.contracts import EvaluationRequest as CoreEvaluationRequest  # noqa: E402
from evalrank_core.contracts import RawEntry as CoreRawEntry  # noqa: E402
from evalrank_core.contracts import StageCandidate as CoreStageCandidate  # noqa: E402
from evalrank_core.contracts import TheCall as CoreTheCall  # noqa: E402
from evalrank_sdk import (  # noqa: E402
    CapabilityFingerprintInput,
    CandidateSet,
    Exclusion,
    EvaluationRequest,
    EvidenceItem,
    EvidenceSet,
    RawEntry,
    StageCandidate,
    TheCall,
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_raw_entry,
    sample_stage_candidate,
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

    def test_sdk_re_exports_core_candidate_set_contracts(self):
        candidate_set = sample_candidate_set()

        self.assertIs(CandidateSet, CoreCandidateSet)
        self.assertIsInstance(candidate_set, CoreCandidateSet)
        self.assertEqual("tool:public-search-demo", candidate_set.to_dict()["candidates"][0]["id"])

    def test_sdk_re_exports_core_exclusion_contracts(self):
        exclusion = sample_exclusion()

        self.assertIs(Exclusion, CoreExclusion)
        self.assertIsInstance(exclusion, CoreExclusion)
        self.assertEqual("unknown_cost", exclusion.to_dict()["reason"])

    def test_sdk_re_exports_core_evidence_set_contracts(self):
        evidence_set = sample_evidence_set()

        self.assertIs(EvidenceSet, CoreEvidenceSet)
        self.assertIsInstance(evidence_set, CoreEvidenceSet)
        self.assertEqual("ev_public_trace_01", evidence_set.to_dict()["evidence_items"][0]["evidence_id"])

    def test_sdk_re_exports_core_raw_entry_contracts(self):
        entry = sample_raw_entry()

        self.assertIs(RawEntry, CoreRawEntry)
        self.assertIsInstance(entry, CoreRawEntry)
        self.assertEqual("raw_entry", entry.to_dict()["object"])

    def test_sdk_re_exports_core_stage_candidate_contracts(self):
        candidate = sample_stage_candidate()

        self.assertIs(StageCandidate, CoreStageCandidate)
        self.assertIsInstance(candidate, CoreStageCandidate)
        self.assertEqual("stage_candidate", candidate.to_dict()["object"])

    def test_sdk_re_exports_core_the_call_contract(self):
        self.assertIs(TheCall, CoreTheCall)
        self.assertEqual("recommend", TheCall.recommend(confidence=0.86, reason="clear top set").decision)


if __name__ == "__main__":
    unittest.main()
