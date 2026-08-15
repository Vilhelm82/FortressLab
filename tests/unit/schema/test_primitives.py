import pytest
from pydantic import ValidationError

from fortresslab.schema.base import StrictModel
from fortresslab.schema.primitives import Point2D, Polygon2D


class DistanceSample(StrictModel):
    distance_m: float


def test_strict_model_rejects_numeric_strings() -> None:
    with pytest.raises(ValidationError):
        DistanceSample.model_validate({"distance_m": "1.0"})


def test_strict_model_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        DistanceSample.model_validate({"distance_m": 1.0, "hint": "gate"})


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_strict_model_rejects_non_finite_numbers(value: float) -> None:
    with pytest.raises(ValidationError):
        DistanceSample(distance_m=value)


def test_validated_models_are_frozen() -> None:
    point = Point2D(x_m=1.0, y_m=2.0)
    with pytest.raises(ValidationError):
        point.x_m = 3.0


def test_polygon_requires_at_least_three_vertices() -> None:
    with pytest.raises(ValidationError):
        Polygon2D(vertices=(Point2D(x_m=0, y_m=0), Point2D(x_m=1, y_m=0)))


def test_polygon_requires_three_distinct_vertices() -> None:
    with pytest.raises(ValidationError):
        Polygon2D(
            vertices=(
                Point2D(x_m=0, y_m=0),
                Point2D(x_m=1, y_m=0),
                Point2D(x_m=0, y_m=0),
            )
        )


def test_polygon_ring_must_not_repeat_its_first_vertex() -> None:
    with pytest.raises(ValidationError):
        Polygon2D(
            vertices=(
                Point2D(x_m=0, y_m=0),
                Point2D(x_m=1, y_m=0),
                Point2D(x_m=1, y_m=1),
                Point2D(x_m=0, y_m=0),
            )
        )
