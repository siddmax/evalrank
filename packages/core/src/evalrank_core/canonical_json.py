"""Restricted RFC 8785 canonical JSON for portable EvalRank identities.

EvalRank hash material deliberately excludes floating-point numbers. Decimal
measurements travel as canonical decimal strings, while counts and monetary
units use JavaScript-safe integers. This keeps Python and browser SDKs byte
identical without silently rounding evidence.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


MAX_SAFE_INTEGER = (1 << 53) - 1


def canonical_json(value: Any) -> str:
    """Return restricted-JCS text, rejecting values that cannot hash portably."""

    canonical = _canonicalize(value, path="$", in_object_key=False)
    return json.dumps(
        canonical,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )


def restricted_jcs(value: Any) -> bytes:
    """Return the exact UTF-8 bytes used by EvalRank content identities."""

    return canonical_json(value).encode("utf-8")


def sha256_hex(value: Any) -> str:
    """Hash restricted-JCS bytes as lowercase SHA-256 hexadecimal text."""

    return hashlib.sha256(restricted_jcs(value)).hexdigest()


def _canonicalize(value: Any, *, path: str, in_object_key: bool) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValueError(f"{path} must be a safe integer")
        return value
    if isinstance(value, float):
        raise TypeError(f"{path} must not be a float in restricted JCS")
    if isinstance(value, str):
        _require_valid_unicode(value, path=path)
        return value
    if isinstance(value, list):
        return [
            _canonicalize(item, path=f"{path}[{index}]", in_object_key=False)
            for index, item in enumerate(value)
        ]
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise TypeError(f"{path} object keys must be strings")
            _canonicalize(key, path=f"{path} key", in_object_key=True)
        return {
            key: _canonicalize(value[key], path=f"{path}.{key}", in_object_key=False)
            for key in sorted(value, key=_utf16_sort_key)
        }
    kind = "object key" if in_object_key else "value"
    raise TypeError(f"{path} {kind} has unsupported JSON type {type(value).__name__}")


def _utf16_sort_key(value: str) -> bytes:
    return value.encode("utf-16-be")


def _require_valid_unicode(value: str, *, path: str) -> None:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ValueError(f"{path} contains a lone surrogate")

