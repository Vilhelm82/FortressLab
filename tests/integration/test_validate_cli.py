import json
import subprocess
import sys
from pathlib import Path

SCENARIO = Path("scenarios/examples/minimal-enclosure.json")


def test_validate_cli_emits_machine_readable_success() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "fortresslab", "validate", str(SCENARIO), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert report["valid"] is True
    assert report["scenario_id"] == "minimal_enclosure"
    assert len(report["scenario_sha256"]) == 64
    assert report["issues"] == []


def test_validate_cli_returns_two_without_traceback_for_bad_json(
    tmp_path: Path,
) -> None:
    source = tmp_path / "broken.json"
    source.write_text("{", encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-m", "fortresslab", "validate", str(source), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 2
    assert "Traceback" not in completed.stderr
    assert report["valid"] is False
    assert report["issues"][0]["path"] == "$"


def test_validate_cli_human_output_is_concise() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "fortresslab", "validate", str(SCENARIO)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert completed.stdout.startswith("VALID minimal_enclosure ")
    assert completed.stderr == ""
