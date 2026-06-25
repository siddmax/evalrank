from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "core" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "sdk-python" / "src"))

from evalrank_sdk import sample_evidence_item, sample_recommendation  # noqa: E402


def main() -> int:
    print(
        json.dumps(
            {
                "evidence": sample_evidence_item().to_dict(),
                "recommendation": sample_recommendation().to_dict(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
