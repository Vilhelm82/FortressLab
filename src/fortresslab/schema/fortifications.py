"""Parametric fortification and material input schemas."""

from typing import Annotated, Literal, Self

from pydantic import Field, field_validator, model_validator

from fortresslab.schema.base import (
    Identifier,
    NonNegativeMetres,
    PositiveMetres,
    PositiveScalar,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point2D, Polygon2D


class MaterialDefinition(StrictModel):
    id: Identifier
    label: str = Field(min_length=1, max_length=120)
    abstract_resistance: PositiveScalar
    notes: str | None = Field(default=None, max_length=1000)


class Wall(StrictModel):
    kind: Literal["wall"] = "wall"
    id: Identifier
    path: tuple[Point2D, ...] = Field(min_length=2)
    height_m: PositiveMetres
    thickness_m: PositiveMetres
    material_id: Identifier
    condition: UnitInterval
    wall_walk_width_m: NonNegativeMetres

    @field_validator("path")
    @classmethod
    def require_distinct_path_points(
        cls, path: tuple[Point2D, ...]
    ) -> tuple[Point2D, ...]:
        coordinates = tuple((point.x_m, point.y_m) for point in path)
        if len(set(coordinates)) < 2:
            raise ValueError("wall path requires at least two distinct points")
        return path


class Tower(StrictModel):
    kind: Literal["tower"] = "tower"
    id: Identifier
    footprint: Polygon2D
    height_m: PositiveMetres
    material_id: Identifier
    condition: UnitInterval
    access_points: tuple[Point2D, ...] = ()
    fighting_position_capacity: int = Field(ge=0)


class Gate(StrictModel):
    kind: Literal["gate"] = "gate"
    id: Identifier
    host_wall_id: Identifier
    centre: Point2D
    width_m: PositiveMetres
    traversal_state: Literal["open", "closed", "blocked"]
    abstract_resistance: PositiveScalar
    successive_barrier_ids: tuple[Identifier, ...] = ()


class Ditch(StrictModel):
    kind: Literal["ditch"] = "ditch"
    id: Identifier
    path: tuple[Point2D, ...] = Field(min_length=2)
    width_m: PositiveMetres
    depth_m: PositiveMetres
    side_slope_deg: float = Field(gt=0, lt=90)
    water_state: Literal["dry", "wet", "flooded"]

    @field_validator("path")
    @classmethod
    def require_distinct_path_points(
        cls, path: tuple[Point2D, ...]
    ) -> tuple[Point2D, ...]:
        coordinates = tuple((point.x_m, point.y_m) for point in path)
        if len(set(coordinates)) < 2:
            raise ValueError("ditch path requires at least two distinct points")
        return path


class Bridge(StrictModel):
    kind: Literal["bridge"] = "bridge"
    id: Identifier
    start: Point2D
    end: Point2D
    width_m: PositiveMetres
    traversability: Literal["open", "restricted", "blocked"]
    denial_state: Literal["intact", "prepared", "denied"]

    @model_validator(mode="after")
    def require_nonzero_span(self) -> Self:
        if self.start == self.end:
            raise ValueError("bridge start and end must differ")
        return self


type Fortification = Annotated[
    Wall | Tower | Gate | Ditch | Bridge,
    Field(discriminator="kind"),
]
