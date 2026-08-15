"""Typed runtime snapshot and run-manifest records."""

from datetime import datetime, timedelta
from typing import Literal, Self

from pydantic import AwareDatetime, Field, field_validator, model_validator

from fortresslab.schema.base import Identifier, SchemaVersion, StrictModel


class DependencyVersion(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


class RuntimeSnapshot(StrictModel):
    package_version: str = Field(min_length=1)
    python_version: str = Field(min_length=1)
    dependencies: tuple[DependencyVersion, ...]


class RunManifest(StrictModel):
    manifest_schema_version: SchemaVersion
    run_id: Identifier
    scenario_id: Identifier
    scenario_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    evaluator_settings_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    model_version: str = Field(min_length=1)
    seed: int = Field(ge=0, le=2**64 - 1)
    runtime: RuntimeSnapshot
    status: Literal["created", "completed"]
    started_at: AwareDatetime
    completed_at: AwareDatetime | None = None

    @field_validator("started_at", "completed_at")
    @classmethod
    def require_utc(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.utcoffset() != timedelta(0):
            raise ValueError("run timestamps must use UTC")
        return value

    @model_validator(mode="after")
    def validate_lifecycle(self) -> Self:
        if self.status == "created" and self.completed_at is not None:
            raise ValueError("created manifest cannot contain completed_at")
        if self.status == "completed" and self.completed_at is None:
            raise ValueError("completed manifest requires completed_at")
        if self.completed_at is not None and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        return self
