"""Canonical JSON serialization and content hashing."""

import hashlib
import json
import math
from collections.abc import Mapping, Sequence

from pydantic import BaseModel

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def _normalize_json(value: object) -> JsonValue:
    if isinstance(value, BaseModel):
        return _normalize_json(value.model_dump(mode="json"))
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("canonical JSON numbers must be finite")
        return 0.0 if value == 0.0 else value
    if isinstance(value, Mapping):
        normalized: dict[str, JsonValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical JSON object keys must be strings")
            normalized[key] = _normalize_json(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize_json(item) for item in value]
    raise TypeError(f"unsupported canonical JSON value: {type(value).__name__}")


def canonical_json_bytes(value: object) -> bytes:
    """Return deterministic project-canonical UTF-8 JSON bytes."""
    normalized = _normalize_json(value)
    return json.dumps(
        normalized,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def content_sha256(value: object) -> str:
    """Hash the canonical representation of a supported value."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
