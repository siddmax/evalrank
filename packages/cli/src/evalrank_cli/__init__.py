from __future__ import annotations

import argparse
import json
import sys
from contextlib import redirect_stderr
from typing import TextIO

from evalrank_core.fixtures import (
    sample_capability_fingerprint_input,
    sample_candidate_set,
    sample_evidence_item,
    sample_evaluation_request,
    sample_raw_entry,
    sample_recommendation,
)


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
        payload = _fixture_payload(args.kind)
        stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return 0

    parser.print_help(file=stderr)
    return 2


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evalrank")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fixture = subparsers.add_parser("fixture", help="write a public fixture payload")
    fixture.add_argument(
        "kind",
        choices=("candidate-set", "evidence", "fingerprint", "raw-entry", "recommendation", "request"),
    )

    return parser


def _fixture_payload(kind: str) -> dict:
    if kind == "evidence":
        return sample_evidence_item().to_dict()
    if kind == "candidate-set":
        return sample_candidate_set().to_dict()
    if kind == "fingerprint":
        return sample_capability_fingerprint_input().to_dict()
    if kind == "raw-entry":
        return sample_raw_entry().to_dict()
    if kind == "recommendation":
        return sample_recommendation().to_dict()
    if kind == "request":
        return sample_evaluation_request().to_dict()
    raise ValueError(f"unsupported fixture kind: {kind}")


__all__ = ["main"]
