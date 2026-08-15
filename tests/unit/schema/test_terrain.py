import pytest
from pydantic import ValidationError

from fortresslab.schema.primitives import Point2D, Polygon2D
from fortresslab.schema.terrain import (
    HeightField,
    SoilDefinition,
    SoilRegion,
    TerrainDefinition,
)


def flat_heightfield() -> HeightField:
    return HeightField(
        origin=Point2D(x_m=0, y_m=0),
        cell_spacing_m=5,
        elevations_m=((0, 0), (0, 0)),
    )


def rock() -> SoilDefinition:
    return SoilDefinition(
        id="rock",
        label="Rock",
        foundation_quality=1,
        traversability_multiplier=1,
    )


def test_heightfield_requires_rectangular_rows() -> None:
    with pytest.raises(ValidationError, match="same number of samples"):
        HeightField(
            origin=Point2D(x_m=0, y_m=0),
            cell_spacing_m=1,
            elevations_m=((0, 0), (0,)),
        )


def test_heightfield_requires_two_columns() -> None:
    with pytest.raises(ValidationError, match="at least two samples"):
        HeightField(
            origin=Point2D(x_m=0, y_m=0),
            cell_spacing_m=1,
            elevations_m=((0,), (0,)),
        )


def test_terrain_default_soil_must_reference_declared_soil() -> None:
    with pytest.raises(ValidationError, match="default_soil_id"):
        TerrainDefinition(
            heightfield=flat_heightfield(),
            analysis_resolution_m=1,
            soils=(rock(),),
            default_soil_id="mud",
        )


def test_terrain_rejects_duplicate_soil_ids() -> None:
    with pytest.raises(ValidationError, match="duplicate ids"):
        TerrainDefinition(
            heightfield=flat_heightfield(),
            analysis_resolution_m=1,
            soils=(rock(), rock()),
            default_soil_id="rock",
        )


def test_soil_region_must_reference_declared_soil() -> None:
    boundary = Polygon2D(
        vertices=(
            Point2D(x_m=0, y_m=0),
            Point2D(x_m=1, y_m=0),
            Point2D(x_m=0, y_m=1),
        )
    )
    with pytest.raises(ValidationError, match=r"soil_regions\[0\]\.soil_id"):
        TerrainDefinition(
            heightfield=flat_heightfield(),
            analysis_resolution_m=1,
            soils=(rock(),),
            default_soil_id="rock",
            soil_regions=(
                SoilRegion(id="mud_patch", soil_id="mud", boundary=boundary),
            ),
        )


def test_polygon_schema_does_not_claim_self_intersection_analysis() -> None:
    bow_tie = Polygon2D(
        vertices=(
            Point2D(x_m=0, y_m=0),
            Point2D(x_m=2, y_m=2),
            Point2D(x_m=0, y_m=2),
            Point2D(x_m=2, y_m=0),
        )
    )
    assert len(bow_tie.vertices) == 4
