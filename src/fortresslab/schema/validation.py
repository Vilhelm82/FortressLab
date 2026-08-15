"""Typed validation reports shared by CLI and Python consumers."""

from pydantic import Field

from fortresslab.schema.base import Identifier, SchemaVersion, StrictModel


class ValidationIssue(StrictModel):
    path: str = Field(min_length=1)
    code: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ValidationReport(StrictModel):
    valid: bool
    source: str
    schema_version: SchemaVersion | None = None
    scenario_id: Identifier | None = None
    scenario_sha256: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{64}$",
    )
    issues: tuple[ValidationIssue, ...] = ()
