from __future__ import annotations

import json
from typing import Any

from evalrank_core.fixtures import (
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_exclusion,
    sample_evidence_item,
    sample_evidence_set,
    sample_evaluation_request,
    sample_raw_entry,
    sample_recommendation,
    sample_result_row,
    sample_stage_candidate,
)


__version__ = "0.0.0"
FIXTURE_TOOL_NAME = "evalrank.fixture"


def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": FIXTURE_TOOL_NAME,
            "description": "Return a deterministic public EvalRank fixture payload.",
            "inputSchema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["kind"],
                "properties": {
                    "kind": {
                        "type": "string",
                        "enum": [
                            "candidate-set",
                            "evidence",
                            "evidence-set",
                            "exclusion",
                            "fingerprint",
                            "raw-entry",
                            "recommendation",
                            "result-row",
                            "request",
                            "stage-candidate",
                        ],
                    }
                },
            },
        }
    ]


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    if name != FIXTURE_TOOL_NAME:
        raise ValueError(f"unknown tool: {name}")

    arguments = arguments or {}
    payload = _fixture_payload(arguments.get("kind"))
    return {
        "isError": False,
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, sort_keys=True, separators=(",", ":")),
            }
        ],
    }


def _fixture_payload(kind: Any) -> dict[str, Any]:
    if kind == "evidence":
        return sample_evidence_item().to_dict()
    if kind == "evidence-set":
        return sample_evidence_set().to_dict()
    if kind == "exclusion":
        return sample_exclusion().to_dict()
    if kind == "candidate-set":
        return sample_candidate_set().to_dict()
    if kind == "fingerprint":
        return sample_capability_fingerprint_input().to_dict()
    if kind == "raw-entry":
        return sample_raw_entry().to_dict()
    if kind == "recommendation":
        return sample_recommendation().to_dict()
    if kind == "result-row":
        return sample_result_row().to_dict()
    if kind == "request":
        return sample_evaluation_request().to_dict()
    if kind == "stage-candidate":
        return sample_stage_candidate().to_dict()
    raise ValueError(
        "fixture kind must be 'candidate-set', 'evidence', 'evidence-set', "
        "'exclusion', 'fingerprint', 'raw-entry', 'recommendation', 'request', "
        "'result-row', or 'stage-candidate'"
    )


__all__ = ["FIXTURE_TOOL_NAME", "call_tool", "list_tools", "__version__"]
