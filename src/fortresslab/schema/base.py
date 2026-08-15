"""Shared strict schema configuration and dimension-bearing scalar types."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

SCHEMA_VERSION = "1.0.0"

type SchemaVersion = Literal["1.0.0"]
type Identifier = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9_-]{0,63}$"),
]
type PositiveMetres = Annotated[float, Field(gt=0)]
type NonNegativeMetres = Annotated[float, Field(ge=0)]
type PositiveScalar = Annotated[float, Field(gt=0)]
type NonNegativeScalar = Annotated[float, Field(ge=0)]
type UnitInterval = Annotated[float, Field(ge=0, le=1)]
type Degrees = Annotated[float, Field(ge=0, lt=360)]


class StrictModel(BaseModel):
    """Immutable schema base that rejects coercion and undeclared state."""

    model_config = ConfigDict(
        allow_inf_nan=False,
        extra="forbid",
        frozen=True,
        strict=True,
        validate_default=True,
    )
