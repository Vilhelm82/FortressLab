import pytest
from pydantic import ValidationError

from fortresslab.schema.scenario import Scenario
from tests.factories import minimal_scenario


def test_minimal_scenario_is_versioned_in_metres_and_degrees() -> None:
    scenario = minimal_scenario()
    assert scenario.schema_version == "1.0.0"
    assert scenario.linear_unit == "m"
    assert scenario.angular_unit == "deg"


def test_duplicate_scene_object_ids_are_rejected() -> None:
    scenario = minimal_scenario()
    document = scenario.model_dump(mode="python")
    document["objectives"] = (
        scenario.objectives[0].model_copy(update={"id": "main_gate"}),
    )
    with pytest.raises(ValidationError, match="duplicate scene object id: main_gate"):
        Scenario.model_validate(document)


def test_duplicate_material_ids_are_rejected() -> None:
    scenario = minimal_scenario()
    with pytest.raises(ValidationError, match="materials contains duplicate ids"):
        Scenario.model_validate(
            {
                **scenario.model_dump(mode="python"),
                "materials": (scenario.materials[0], scenario.materials[0]),
            }
        )


def test_gate_host_must_reference_a_wall() -> None:
    scenario = minimal_scenario()
    structures = tuple(
        structure.model_copy(update={"host_wall_id": "missing_wall"})
        if structure.kind == "gate"
        else structure
        for structure in scenario.structures
    )
    with pytest.raises(
        ValidationError,
        match=r"structures\[4\]\.host_wall_id is unknown: missing_wall",
    ):
        Scenario.model_validate(
            {**scenario.model_dump(mode="python"), "structures": structures}
        )


def test_material_reference_must_exist() -> None:
    scenario = minimal_scenario()
    first_wall = scenario.structures[0].model_copy(
        update={"material_id": "unobtainium"}
    )
    with pytest.raises(
        ValidationError,
        match=r"structures\[0\]\.material_id is unknown: unobtainium",
    ):
        Scenario.model_validate(
            {
                **scenario.model_dump(mode="python"),
                "structures": (first_wall, *scenario.structures[1:]),
            }
        )


def test_gate_cannot_reference_itself_as_successive_barrier() -> None:
    scenario = minimal_scenario()
    structures = tuple(
        structure.model_copy(update={"successive_barrier_ids": ("main_gate",)})
        if structure.kind == "gate"
        else structure
        for structure in scenario.structures
    )
    with pytest.raises(ValidationError, match="successive_barrier_ids"):
        Scenario.model_validate(
            {**scenario.model_dump(mode="python"), "structures": structures}
        )


def test_scenario_rejects_evaluator_hints() -> None:
    scenario = minimal_scenario()
    with pytest.raises(ValidationError, match="expected_outcome"):
        Scenario.model_validate(
            {**scenario.model_dump(mode="python"), "expected_outcome": "gate_falls"}
        )


def test_unknown_schema_version_is_rejected() -> None:
    scenario = minimal_scenario()
    with pytest.raises(ValidationError, match="schema_version"):
        Scenario.model_validate(
            {**scenario.model_dump(mode="python"), "schema_version": "2.0.0"}
        )
