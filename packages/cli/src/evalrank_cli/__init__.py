from __future__ import annotations

import argparse
import json
import sys
from contextlib import redirect_stderr
from typing import TextIO

from evalrank_core.fixtures import (
    PUBLIC_FIXTURE_KINDS,
    sample_public_fixture,
)
from evalrank_sdk import EvalRankApiError, EvalRankClient


def main(argv: list[str] | None = None, *, stdout: TextIO | None = None, stderr: TextIO | None = None) -> int:
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    parser = _parser()

    try:
        with redirect_stderr(stderr):
            args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)

    if args.command == "fixture":
        payload = sample_public_fixture(args.kind)
        stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return 0
    if args.command == "recommend":
        try:
            client = EvalRankClient(args.base_url)
        except ValueError as exc:
            stderr.write(str(exc) + "\n")
            return 2
        try:
            payload = _read_request(args.request)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            stderr.write(f"invalid request JSON: {exc}\n")
            return 2
        try:
            recommendation = client.recommend(payload)
        except EvalRankApiError as exc:
            stderr.write(json.dumps(exc.problem, sort_keys=True, separators=(",", ":")) + "\n")
            return 1
        stdout.write(json.dumps(recommendation, sort_keys=True, separators=(",", ":")) + "\n")
        return 0

    parser.print_help(file=stderr)
    return 2


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evalrank")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fixture = subparsers.add_parser("fixture", help="write a public fixture payload")
    fixture.add_argument(
        "kind",
        choices=PUBLIC_FIXTURE_KINDS,
    )
    recommend = subparsers.add_parser("recommend", help="call the public recommendation API")
    recommend.add_argument("--base-url", required=True)
    recommend.add_argument("--request", required=True, help="EvaluationRequest JSON file, or '-' for stdin")

    return parser


def _read_request(path: str) -> dict:
    if path == "-":
        payload = json.load(sys.stdin)
    else:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("request JSON must be an object")
    return payload


__all__ = ["main"]
