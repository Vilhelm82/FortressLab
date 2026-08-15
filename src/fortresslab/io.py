"""Scenario file loading and normalized validation failures."""

from pathlib import Path

from pydantic import ValidationError

from fortresslab.schema.scenario import Scenario
from fortresslab.schema.validation import ValidationIssue


class ScenarioInputError(Exception):
    def __init__(self, issues: tuple[ValidationIssue, ...]) -> None:
        super().__init__("scenario input is invalid")
        self.issues = issues


def _path_from_location(location: tuple[str | int, ...]) -> str:
    path = "$"
    for part in location:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def load_scenario(path: Path) -> Scenario:
    """Load one JSON file into the immutable scenario contract."""
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise ScenarioInputError(
            (
                ValidationIssue(
                    path="$",
                    code="file_error",
                    message=str(error),
                ),
            )
        ) from error

    try:
        return Scenario.model_validate_json(payload)
    except ValidationError as error:
        issues = tuple(
            ValidationIssue(
                path=_path_from_location(tuple(detail["loc"])),
                code=str(detail["type"]),
                message=str(detail["msg"]),
            )
            for detail in error.errors(include_url=False, include_input=False)
        )
        raise ScenarioInputError(issues) from error
