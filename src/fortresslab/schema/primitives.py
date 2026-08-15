"""Coordinate primitives with structural, not geometric, validation."""

from pydantic import Field, field_validator

from fortresslab.schema.base import StrictModel


class Point2D(StrictModel):
    x_m: float
    y_m: float


class Point3D(StrictModel):
    x_m: float
    y_m: float
    z_m: float


class Polygon2D(StrictModel):
    vertices: tuple[Point2D, ...] = Field(min_length=3)

    @field_validator("vertices")
    @classmethod
    def require_distinct_unclosed_vertices(
        cls, vertices: tuple[Point2D, ...]
    ) -> tuple[Point2D, ...]:
        coordinates = tuple((point.x_m, point.y_m) for point in vertices)
        if len(set(coordinates)) < 3:
            raise ValueError("polygon requires at least three distinct vertices")
        if coordinates[0] == coordinates[-1]:
            raise ValueError("polygon ring must not repeat its first vertex")
        return vertices
