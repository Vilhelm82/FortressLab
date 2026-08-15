"""Formation-level operational inputs for static POC evaluation."""

from typing import Literal, Self

from pydantic import Field, model_validator

from fortresslab.schema.base import (
    Degrees,
    Identifier,
    NonNegativeMetres,
    NonNegativeScalar,
    PositiveMetres,
    PositiveScalar,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point3D


class Objective(StrictModel):
    id: Identifier
    location: Point3D
    capture_radius_m: PositiveMetres
    priority: PositiveScalar = 1.0


class WeaponEnvelope(StrictModel):
    minimum_range_m: NonNegativeMetres
    maximum_range_m: PositiveMetres
    facing_deg: Degrees
    horizontal_arc_deg: float = Field(gt=0, le=360)

    @model_validator(mode="after")
    def require_ordered_ranges(self) -> Self:
        if self.minimum_range_m >= self.maximum_range_m:
            raise ValueError("minimum_range_m must be less than maximum_range_m")
        return self


class DefensivePosition(StrictModel):
    id: Identifier
    location: Point3D
    capacity: int = Field(gt=0)
    weapon_envelope: WeaponEnvelope
    access_node_id: Identifier | None = None


class Observer(StrictModel):
    id: Identifier
    location: Point3D
    reconnaissance_quality: UnitInterval


class MovementCapabilities(StrictModel):
    max_slope_deg: float = Field(gt=0, lt=90)
    minimum_corridor_width_m: PositiveMetres
    maximum_wading_depth_m: NonNegativeMetres


class EngineeringCapabilities(StrictModel):
    can_bridge: bool
    maximum_bridge_span_m: NonNegativeMetres
    can_fill_ditch: bool
    can_breach_wall: bool
    abstract_breach_capacity: NonNegativeScalar

    @model_validator(mode="after")
    def require_compatible_capabilities(self) -> Self:
        if self.can_bridge and self.maximum_bridge_span_m == 0:
            raise ValueError(
                "maximum_bridge_span_m must be positive when can_bridge is true"
            )
        if not self.can_bridge and self.maximum_bridge_span_m != 0:
            raise ValueError(
                "maximum_bridge_span_m must be zero when can_bridge is false"
            )
        if self.can_breach_wall and self.abstract_breach_capacity == 0:
            raise ValueError(
                "abstract_breach_capacity must be positive when can_breach_wall is true"
            )
        if not self.can_breach_wall and self.abstract_breach_capacity != 0:
            raise ValueError(
                "abstract_breach_capacity must be zero when can_breach_wall is false"
            )
        return self


class AttackerProfile(StrictModel):
    id: Identifier
    label: str = Field(min_length=1, max_length=120)
    movement: MovementCapabilities
    engineering: EngineeringCapabilities


class EvaluationSettings(StrictModel):
    seed: int = Field(ge=0, le=2**64 - 1)
    sparse_cell_resolution_m: PositiveMetres = 1.0
    sparse_chunk_cells: int = Field(default=16, ge=4, le=256)
    geometric_epsilon_m: PositiveMetres = 0.001
    mode: Literal["authoritative", "perceived", "both"] = "both"
