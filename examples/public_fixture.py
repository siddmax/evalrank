from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "sdk-python" / "src"))

from evalrank_sdk import (  # noqa: E402
    sample_capability_fingerprint_input,
    sample_observation,
    sample_problem_details,
    sample_raw_entry,
    sample_use_case_catalog,
)


def main() -> int:
    print(
        json.dumps(
            {
                "fingerprint": sample_capability_fingerprint_input().to_dict(),
                "problem": sample_problem_details().to_dict(),
                "raw_entry": sample_raw_entry().to_dict(),
                "observation": sample_observation().to_dict(),
                "use_cases": sample_use_case_catalog().to_dict(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
