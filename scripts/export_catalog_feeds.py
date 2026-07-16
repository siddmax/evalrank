#!/usr/bin/env python3
"""Export the public feed inventory (`catalog/feeds.json`).

The inventory is a deterministic projection of the manifest and its research
companion: one row per manifest feed, in manifest feed order, nesting the exact
manifest benchmark-family object, the exact manifest feed object, and the exact
family research object. It adds no facts of its own.

`--write` regenerates the file; `--check` fails if the committed file is stale,
missing, or hand-edited. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG = REPO_ROOT / "catalog"
MANIFEST_PATH = CATALOG / "manifest.json"
PROVENANCE_PATH = CATALOG / "research-provenance.json"
FEEDS_PATH = CATALOG / "feeds.json"

SCHEMA_REF = "../schemas/feed-inventory.schema.json"
OBJECT = "feed_inventory"
SCHEMA_VERSION = "1"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_inventory(manifest: dict, provenance: dict) -> dict:
    """Join every manifest feed to its exact family and research objects."""
    family_by_id: dict[str, dict] = {}
    for family in manifest["benchmark_families"]:
        family_id = family["benchmark_family_id"]
        if family_id in family_by_id:
            raise ValueError(f"duplicate benchmark family {family_id!r}")
        family_by_id[family_id] = family

    research_by_id: dict[str, dict] = {}
    for family in provenance["families"]:
        family_id = family["benchmark_family_id"]
        if family_id in research_by_id:
            raise ValueError(f"duplicate research family {family_id!r}")
        research_by_id[family_id] = family

    feeds = []
    for feed in manifest["feeds"]:
        family_id = feed["benchmark_family_id"]
        if family_id not in family_by_id:
            raise ValueError(
                f"feed {feed['feed_id']!r} references unknown family {family_id!r}"
            )
        if family_id not in research_by_id:
            raise ValueError(
                f"feed {feed['feed_id']!r} family {family_id!r} has no research"
            )
        feeds.append(
            {
                "benchmark_family": family_by_id[family_id],
                "feed": feed,
                "research": research_by_id[family_id],
            }
        )

    return {
        "$schema": SCHEMA_REF,
        "object": OBJECT,
        "schema_version": SCHEMA_VERSION,
        "manifest_version": manifest["manifest_version"],
        "feeds": feeds,
    }


def render(inventory: dict) -> str:
    """Pretty envelope with each feed entry compact on one physical line."""
    lines = ["{"]
    for key in ("$schema", "object", "schema_version", "manifest_version"):
        lines.append(f"  {json.dumps(key)}: {json.dumps(inventory[key])},")
    lines.append('  "feeds": [')
    entries = inventory["feeds"]
    for index, entry in enumerate(entries):
        compact = json.dumps(entry, separators=(",", ":"))
        suffix = "," if index < len(entries) - 1 else ""
        lines.append(f"    {compact}{suffix}")
    lines.append("  ]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _expected_text() -> str:
    return render(build_inventory(_load(MANIFEST_PATH), _load(PROVENANCE_PATH)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="regenerate catalog/feeds.json")
    mode.add_argument("--check", action="store_true", help="fail if the file is stale")
    args = parser.parse_args(argv)

    expected = _expected_text()

    if args.write:
        FEEDS_PATH.write_text(expected, encoding="utf-8")
        return 0

    if not FEEDS_PATH.exists():
        print(f"{FEEDS_PATH} is missing; run: python3 scripts/export_catalog_feeds.py --write", file=sys.stderr)
        return 1
    actual = FEEDS_PATH.read_text(encoding="utf-8")
    if actual != expected:
        print(
            f"{FEEDS_PATH} is stale or hand-edited; run: python3 scripts/export_catalog_feeds.py --write",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
