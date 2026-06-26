from __future__ import annotations

import json
from typing import Any

from evalrank_core.fixtures import (
    PUBLIC_FIXTURE_KINDS,
    sample_public_fixture,
)
from evalrank_sdk import EvalRankApiError, EvalRankClient


__version__ = "0.0.0"
FIXTURE_TOOL_NAME = "evalrank.fixture"
RECOMMEND_TOOL_NAME = "evalrank.recommend"


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
        },
        {
            "name": RECOMMEND_TOOL_NAME,
            "description": "Call the public EvalRank recommendation API.",
            "inputSchema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["base_url", "request"],
                "properties": {
                    "base_url": {
                        "type": "string",
                    },
                    "request": {
                        "type": "object",
                    },
                },
            },
        },
    ]


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    if arguments is None:
        arguments = {}
    if not isinstance(arguments, dict):
        raise ValueError("arguments must be an object")
    if name == FIXTURE_TOOL_NAME:
        return _text_result(sample_public_fixture(arguments.get("kind")))
    if name == RECOMMEND_TOOL_NAME:
        return _recommend(arguments)
    raise ValueError(f"unknown tool: {name}")


def _recommend(arguments: dict[str, Any]) -> dict[str, Any]:
    base_url = arguments.get("base_url")
    request = arguments.get("request")
    if not isinstance(base_url, str) or not base_url:
        raise ValueError("base_url is required")
    if not isinstance(request, dict):
        raise ValueError("request must be an object")
    try:
        return _text_result(EvalRankClient(base_url).recommend(request))
    except EvalRankApiError as exc:
        return _text_result(exc.problem, is_error=True)


def _text_result(payload: dict[str, Any], *, is_error: bool = False) -> dict[str, Any]:
    return {
        "isError": is_error,
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, sort_keys=True, separators=(",", ":")),
            }
        ],
    }


__all__ = ["FIXTURE_TOOL_NAME", "RECOMMEND_TOOL_NAME", "call_tool", "list_tools", "__version__"]
