from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "sdk-python" / "src"))

from evalrank_sdk import (  # noqa: E402
    sample_candidate_set,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_exclusion,
    sample_raw_entry,
    sample_recommendation,
    sample_result_row,
    sample_scoring_stage_catalog,
    sample_stage_candidate,
    sample_use_case_catalog,
)


def main() -> int:
    print(
        json.dumps(
            {
                "candidate_set": sample_candidate_set().to_dict(),
                "evidence": sample_evidence_item().to_dict(),
                "evidence_set": sample_evidence_set().to_dict(),
                "exclusion": sample_exclusion().to_dict(),
                "raw_entry": sample_raw_entry().to_dict(),
                "recommendation": sample_recommendation().to_dict(),
                "request": sample_evaluation_request().to_dict(),
                "result_row": sample_result_row().to_dict(),
                "scoring_stages": sample_scoring_stage_catalog().to_dict(),
                "stage_candidate": sample_stage_candidate().to_dict(),
                "use_cases": sample_use_case_catalog().to_dict(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
