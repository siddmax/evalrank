from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SRC = REPO_ROOT / "packages" / "core" / "src"
GOLDEN = REPO_ROOT / "examples" / "decision-contract-v1.golden.json"
sys.path.insert(0, str(CORE_SRC))

from evalrank_core.canonical_json import (  # noqa: E402
    MAX_SAFE_INTEGER,
    canonical_json,
    restricted_jcs,
    sha256_hex,
)


class CanonicalJsonTests(unittest.TestCase):
    def test_serializes_restricted_jcs_without_whitespace(self):
        value = {
            "z": [True, None, "line\nfeed"],
            "a": {"quote": '"', "slash": "/"},
        }

        self.assertEqual(
            '{"a":{"quote":"\\\"","slash":"/"},"z":[true,null,"line\\nfeed"]}',
            canonical_json(value),
        )
        self.assertEqual(canonical_json(value).encode("utf-8"), restricted_jcs(value))

    def test_orders_object_keys_by_utf16_code_units(self):
        # U+10000 sorts before U+E000 under RFC 8785's UTF-16 ordering.
        value = {"\ue000": 2, "\U00010000": 1}

        self.assertEqual('{"\U00010000":1,"\ue000":2}', canonical_json(value))

    def test_preserves_unicode_without_normalizing(self):
        decomposed = "e\u0301"
        composed = "\u00e9"

        self.assertNotEqual(canonical_json({"value": decomposed}), canonical_json({"value": composed}))
        self.assertIn(decomposed, canonical_json({"value": decomposed}))

    def test_rejects_values_outside_the_restricted_subset(self):
        invalid_values = (
            1.0,
            float("nan"),
            float("inf"),
            MAX_SAFE_INTEGER + 1,
            -(MAX_SAFE_INTEGER + 1),
            {1: "non-string-key"},
            {"value": "\ud800"},
            {"\udfff": "lone-surrogate-key"},
        )

        for value in invalid_values:
            with self.subTest(value=repr(value)):
                with self.assertRaises((TypeError, ValueError)):
                    canonical_json(value)

    def test_rejects_non_json_python_values(self):
        for value in ({1, 2}, (1, 2), b"bytes"):
            with self.subTest(value=repr(value)):
                with self.assertRaises(TypeError):
                    canonical_json(value)

    def test_sha256_hex_hashes_exact_canonical_bytes(self):
        self.assertEqual(
            "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
            sha256_hex({"b": 2, "a": 1}),
        )

    def test_python_matches_cross_language_golden_canonicalization(self):
        corpus = json.loads(GOLDEN.read_text(encoding="utf-8"))

        self.assertEqual(corpus["query"]["canonical"], canonical_json(corpus["query"]["input"]))
        self.assertEqual(corpus["receipt"]["body_sha256"], sha256_hex(corpus["receipt"]["body"]))

        for vector in corpus["rejection_vectors"][:2]:
            with self.subTest(vector=vector["name"]):
                with self.assertRaises((TypeError, ValueError)):
                    canonical_json(vector["value"])


if __name__ == "__main__":
    unittest.main()
