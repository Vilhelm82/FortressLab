"""Stable schema primitives exported for FortressLab consumers."""

from fortresslab.schema.base import (
    SCHEMA_VERSION,
    Degrees,
    Identifier,
    NonNegativeMetres,
    NonNegativeScalar,
    PositiveMetres,
    PositiveScalar,
    SchemaVersion,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point2D, Point3D, Polygon2D

__all__ = [
    "SCHEMA_VERSION",
    "Degrees",
    "Identifier",
    "NonNegativeMetres",
    "NonNegativeScalar",
    "Point2D",
    "Point3D",
    "Polygon2D",
    "PositiveMetres",
    "PositiveScalar",
    "SchemaVersion",
    "StrictModel",
    "UnitInterval",
]
