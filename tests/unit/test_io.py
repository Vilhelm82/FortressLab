from pathlib import Path

import pytest

from fortresslab.io import ScenarioInputError, load_scenario


def test_loader_reports_nested_validation_path(tmp_path: Path) -> None:
    source = tmp_path / "invalid.json"
    source.write_text(
        '{"schema_version":"1.0.0","scenario_id":"x","title":"X",'
        '"coordinate_system":"local_cartesian","linear_unit":"m",'
        '"angular_unit":"deg","terrain":{"heightfield":{'
        '"origin":{"x_m":0,"y_m":0},"cell_spacing_m":"wide",'
        '"elevations_m":[[0,0],[0,0]]}}}',
        encoding="utf-8",
    )
    with pytest.raises(ScenarioInputError) as captured:
        load_scenario(source)
    assert any(
        issue.path == "$.terrain.heightfield.cell_spacing_m"
        for issue in captured.value.issues
    )


def test_loader_reports_file_error_for_missing_path(tmp_path: Path) -> None:
    source = tmp_path / "missing.json"
    with pytest.raises(ScenarioInputError) as captured:
        load_scenario(source)
    assert captured.value.issues[0].path == "$"
    assert captured.value.issues[0].code == "file_error"
