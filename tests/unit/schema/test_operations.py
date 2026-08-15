import pytest
from pydantic import ValidationError

from fortresslab.schema.operations import (
    EngineeringCapabilities,
    EvaluationSettings,
    MovementCapabilities,
    WeaponEnvelope,
)


def test_movement_capability_rejects_vertical_ground_slope() -> None:
    with pytest.raises(ValidationError):
        MovementCapabilities(
            max_slope_deg=90,
            minimum_corridor_width_m=1,
            maximum_wading_depth_m=1,
        )


def test_disabled_bridging_requires_zero_span() -> None:
    with pytest.raises(ValidationError, match="must be zero"):
        EngineeringCapabilities(
            can_bridge=False,
            maximum_bridge_span_m=5,
            can_fill_ditch=True,
            can_breach_wall=True,
            abstract_breach_capacity=1,
        )


def test_enabled_bridging_requires_positive_span() -> None:
    with pytest.raises(ValidationError, match="must be positive"):
        EngineeringCapabilities(
            can_bridge=True,
            maximum_bridge_span_m=0,
            can_fill_ditch=True,
            can_breach_wall=True,
            abstract_breach_capacity=1,
        )


def test_disabled_breaching_requires_zero_capacity() -> None:
    with pytest.raises(ValidationError, match="must be zero"):
        EngineeringCapabilities(
            can_bridge=False,
            maximum_bridge_span_m=0,
            can_fill_ditch=True,
            can_breach_wall=False,
            abstract_breach_capacity=1,
        )


def test_enabled_breaching_requires_positive_capacity() -> None:
    with pytest.raises(ValidationError, match="must be positive"):
        EngineeringCapabilities(
            can_bridge=False,
            maximum_bridge_span_m=0,
            can_fill_ditch=True,
            can_breach_wall=True,
            abstract_breach_capacity=0,
        )


def test_weapon_envelope_requires_ordered_ranges() -> None:
    with pytest.raises(ValidationError, match="minimum_range_m"):
        WeaponEnvelope(
            minimum_range_m=100,
            maximum_range_m=100,
            facing_deg=0,
            horizontal_arc_deg=90,
        )


def test_evaluation_seed_rejects_negative_values() -> None:
    with pytest.raises(ValidationError):
        EvaluationSettings(seed=-1)


def test_evaluation_seed_accepts_unsigned_64_bit_maximum() -> None:
    assert EvaluationSettings(seed=2**64 - 1).seed == 2**64 - 1


def test_evaluation_seed_rejects_values_above_unsigned_64_bit() -> None:
    with pytest.raises(ValidationError):
        EvaluationSettings(seed=2**64)
