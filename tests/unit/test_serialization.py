import json

import pytest

from fortresslab.serialization import canonical_json_bytes, content_sha256


def test_canonical_json_has_hand_checked_order_and_spacing() -> None:
    payload = canonical_json_bytes({"z": 0.0, "a": [2, 1]})
    assert payload == b'{"a":[2,1],"z":0.0}'


def test_canonical_json_normalizes_negative_zero() -> None:
    assert canonical_json_bytes({"value": -0.0}) == b'{"value":0.0}'


def test_mapping_insertion_order_does_not_change_content_hash() -> None:
    assert content_sha256({"a": 1, "b": 2}) == content_sha256({"b": 2, "a": 1})


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_values_are_rejected_outside_models(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        canonical_json_bytes({"distance_m": value})


def test_non_string_mapping_keys_are_rejected() -> None:
    with pytest.raises(TypeError, match="keys must be strings"):
        canonical_json_bytes({1: "invalid"})


def test_canonical_bytes_are_valid_utf8_json() -> None:
    assert json.loads(canonical_json_bytes({"name": "Crème"})) == {"name": "Crème"}
