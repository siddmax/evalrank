from __future__ import annotations

import json
from typing import Any

from evalrank_core.fixtures import (
    PUBLIC_FIXTURE_KINDS,
    sample_public_fixture,
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
                        "enum": list(PUBLIC_FIXTURE_KINDS),
                    }
                },
            },
        }
    ]


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    if name != FIXTURE_TOOL_NAME:
        raise ValueError(f"unknown tool: {name}")

    arguments = arguments or {}
    payload = sample_public_fixture(arguments.get("kind"))
    return {
        "isError": False,
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, sort_keys=True, separators=(",", ":")),
            }
        ],
    }


__all__ = ["FIXTURE_TOOL_NAME", "call_tool", "list_tools", "__version__"]
