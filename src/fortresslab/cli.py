"""FortressLab command-line boundary."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from fortresslab.io import ScenarioInputError, load_scenario
from fortresslab.schema.validation import ValidationReport
from fortresslab.serialization import canonical_json_bytes, content_sha256


def validate_path(path: Path) -> ValidationReport:
    """Return a typed validation result without raising input errors."""
    try:
        scenario = load_scenario(path)
    except ScenarioInputError as error:
        return ValidationReport(valid=False, source=str(path), issues=error.issues)
    return ValidationReport(
        valid=True,
        source=str(path),
        schema_version=scenario.schema_version,
        scenario_id=scenario.scenario_id,
        scenario_sha256=content_sha256(scenario),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fortresslab")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate a scenario JSON file")
    validate.add_argument("scenario", type=Path)
    validate.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    report = validate_path(arguments.scenario)
    if arguments.as_json:
        sys.stdout.buffer.write(canonical_json_bytes(report) + b"\n")
    elif report.valid:
        print(f"VALID {report.scenario_id} {report.scenario_sha256}")
    else:
        print(f"INVALID {report.source}")
        for issue in report.issues:
            print(f"- {issue.path}: {issue.message}")
    return 0 if report.valid else 2


def entrypoint() -> None:
    raise SystemExit(main())
