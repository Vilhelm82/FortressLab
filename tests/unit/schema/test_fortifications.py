import pytest
from pydantic import TypeAdapter, ValidationError

from fortresslab.schema.fortifications import (
    Bridge,
    Ditch,
    Fortification,
    Gate,
    MaterialDefinition,
    Wall,
)
from fortresslab.schema.primitives import Point2D


def test_fortification_union_selects_wall_from_kind() -> None:
    adapter: TypeAdapter[Fortification] = TypeAdapter(Fortification)
    wall = adapter.validate_python(
        {
            "kind": "wall",
            "id": "south_wall",
            "path": (
                {"x_m": 0.0, "y_m": 0.0},
                {"x_m": 20.0, "y_m": 0.0},
            ),
            "height_m": 8.0,
            "thickness_m": 2.0,
            "material_id": "stone",
            "condition": 1.0,
            "wall_walk_width_m": 1.5,
        }
    )
    assert isinstance(wall, Wall)


def test_fortification_union_rejects_unknown_kind() -> None:
    adapter: TypeAdapter[Fortification] = TypeAdapter(Fortification)
    with pytest.raises(ValidationError):
        adapter.validate_python({"kind": "moat_monster", "id": "surprise"})


def test_material_rejects_non_positive_resistance() -> None:
    with pytest.raises(ValidationError):
        MaterialDefinition(
            id="paper",
            label="Paper",
            abstract_resistance=0,
        )


def test_wall_requires_two_distinct_path_points() -> None:
    with pytest.raises(ValidationError, match="distinct"):
        Wall(
            id="wall",
            path=(Point2D(x_m=0, y_m=0), Point2D(x_m=0, y_m=0)),
            height_m=8,
            thickness_m=2,
            material_id="stone",
            condition=1,
            wall_walk_width_m=1,
        )


def test_gate_rejects_non_positive_width() -> None:
    with pytest.raises(ValidationError):
        Gate(
            id="main_gate",
            host_wall_id="south_wall",
            centre=Point2D(x_m=10, y_m=0),
            width_m=0,
            traversal_state="closed",
            abstract_resistance=1,
        )


def test_ditch_requires_two_distinct_path_points() -> None:
    with pytest.raises(ValidationError, match="distinct"):
        Ditch(
            id="ditch",
            path=(Point2D(x_m=0, y_m=0), Point2D(x_m=0, y_m=0)),
            width_m=4,
            depth_m=2,
            side_slope_deg=45,
            water_state="dry",
        )


def test_bridge_requires_nonzero_span() -> None:
    point = Point2D(x_m=1, y_m=1)
    with pytest.raises(ValidationError, match="must differ"):
        Bridge(
            id="bridge",
            start=point,
            end=point,
            width_m=3,
            traversability="open",
            denial_state="intact",
        )
