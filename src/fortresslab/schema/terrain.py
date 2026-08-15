"""Versioned terrain, soil, and water input schemas."""

from typing import Self

from pydantic import Field, field_validator, model_validator

from fortresslab.schema.base import (
    Identifier,
    PositiveMetres,
    PositiveScalar,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point2D, Polygon2D


class HeightField(StrictModel):
    origin: Point2D
    cell_spacing_m: PositiveMetres
    elevations_m: tuple[tuple[float, ...], ...] = Field(min_length=2)

    @field_validator("elevations_m")
    @classmethod
    def require_rectangular_grid(
        cls, rows: tuple[tuple[float, ...], ...]
    ) -> tuple[tuple[float, ...], ...]:
        width = len(rows[0])
        if width < 2:
            raise ValueError("heightfield rows require at least two samples")
        if any(len(row) != width for row in rows):
            raise ValueError("heightfield rows must have the same number of samples")
        return rows


class SoilDefinition(StrictModel):
    id: Identifier
    label: str = Field(min_length=1, max_length=120)
    foundation_quality: UnitInterval
    traversability_multiplier: PositiveScalar


class SoilRegion(StrictModel):
    id: Identifier
    soil_id: Identifier
    boundary: Polygon2D


class WaterRegion(StrictModel):
    id: Identifier
    boundary: Polygon2D
    surface_elevation_m: float
    nominal_depth_m: PositiveMetres


class TerrainDefinition(StrictModel):
    heightfield: HeightField
    analysis_resolution_m: PositiveMetres
    soils: tuple[SoilDefinition, ...] = Field(min_length=1)
    default_soil_id: Identifier
    soil_regions: tuple[SoilRegion, ...] = ()
    water_regions: tuple[WaterRegion, ...] = ()

    @model_validator(mode="after")
    def validate_local_references(self) -> Self:
        soil_ids = [soil.id for soil in self.soils]
        if len(soil_ids) != len(set(soil_ids)):
            raise ValueError("terrain.soils contains duplicate ids")
        if self.default_soil_id not in soil_ids:
            raise ValueError("terrain.default_soil_id does not reference terrain.soils")
        for index, region in enumerate(self.soil_regions):
            if region.soil_id not in soil_ids:
                raise ValueError(
                    f"terrain.soil_regions[{index}].soil_id is unknown: {region.soil_id}"
                )
        return self
