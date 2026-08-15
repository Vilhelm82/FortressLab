from datetime import UTC, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from fortresslab.manifest import (
    complete_run_manifest,
    create_run_manifest,
    derive_run_id,
)
from fortresslab.schema.manifest import DependencyVersion, RuntimeSnapshot
from fortresslab.schema.scenario import Scenario
from tests.factories import minimal_scenario

RUNTIME = RuntimeSnapshot(
    package_version="0.1.0",
    python_version="3.14.4",
    dependencies=(DependencyVersion(name="pydantic", version="2.13.4"),),
)


def test_run_id_ignores_execution_timestamp() -> None:
    scenario = minimal_scenario()
    first = create_run_manifest(
        scenario, RUNTIME, datetime(2026, 8, 15, 10, tzinfo=UTC)
    )
    second = create_run_manifest(
        scenario, RUNTIME, datetime(2026, 8, 16, 10, tzinfo=UTC)
    )
    assert first.run_id == second.run_id
    assert first.started_at != second.started_at


def test_run_id_changes_when_seed_changes() -> None:
    scenario = minimal_scenario()
    changed = Scenario.model_validate(
        {
            **scenario.model_dump(mode="python"),
            "evaluation": scenario.evaluation.model_copy(update={"seed": 8}),
        }
    )
    assert derive_run_id(scenario) != derive_run_id(changed)


def test_run_id_changes_when_scenario_content_changes() -> None:
    scenario = minimal_scenario()
    changed = Scenario.model_validate(
        {**scenario.model_dump(mode="python"), "title": "Changed enclosure"}
    )
    assert derive_run_id(scenario) != derive_run_id(changed)


def test_run_id_changes_when_evaluator_settings_change() -> None:
    scenario = minimal_scenario()
    changed = Scenario.model_validate(
        {
            **scenario.model_dump(mode="python"),
            "evaluation": scenario.evaluation.model_copy(
                update={"sparse_chunk_cells": 32}
            ),
        }
    )
    assert derive_run_id(scenario) != derive_run_id(changed)


def test_run_id_changes_when_model_version_changes() -> None:
    scenario = minimal_scenario()
    assert derive_run_id(scenario, "model-a") != derive_run_id(scenario, "model-b")


def test_run_id_has_stable_identifier_shape() -> None:
    run_id = derive_run_id(minimal_scenario())
    assert run_id.startswith("run_")
    assert len(run_id) == 28


def test_completion_precedes_start_is_rejected() -> None:
    started = datetime(2026, 8, 15, 10, tzinfo=UTC)
    manifest = create_run_manifest(minimal_scenario(), RUNTIME, started)
    with pytest.raises(ValidationError, match="completed_at"):
        complete_run_manifest(manifest, started - timedelta(seconds=1))


def test_completed_manifest_records_completion() -> None:
    started = datetime(2026, 8, 15, 10, tzinfo=UTC)
    completed = started + timedelta(seconds=1)
    manifest = complete_run_manifest(
        create_run_manifest(minimal_scenario(), RUNTIME, started), completed
    )
    assert manifest.status == "completed"
    assert manifest.completed_at == completed


def test_run_timestamps_must_use_utc() -> None:
    non_utc = datetime(2026, 8, 15, 10, tzinfo=timezone(timedelta(hours=10)))
    with pytest.raises(ValidationError, match="UTC"):
        create_run_manifest(minimal_scenario(), RUNTIME, non_utc)
