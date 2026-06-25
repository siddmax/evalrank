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

    return parser


__all__ = ["main"]
