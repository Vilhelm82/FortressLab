"""Stable run identity and explicit manifest lifecycle operations."""

import platform
from datetime import datetime
from importlib.metadata import version

from fortresslab import MODEL_VERSION, __version__
from fortresslab.schema.manifest import (
    DependencyVersion,
    RunManifest,
    RuntimeSnapshot,
)
from fortresslab.schema.scenario import Scenario
from fortresslab.serialization import content_sha256


def derive_run_id(scenario: Scenario, model_version: str = MODEL_VERSION) -> str:
    """Derive identity only from behaviour-bearing, reproducible inputs."""
    identity = {
        "scenario_sha256": content_sha256(scenario),
        "evaluator_settings_sha256": content_sha256(scenario.evaluation),
        "model_version": model_version,
        "seed": scenario.evaluation.seed,
    }
    return f"run_{content_sha256(identity)[:24]}"


def create_run_manifest(
    scenario: Scenario,
    runtime: RuntimeSnapshot,
    started_at: datetime,
    model_version: str = MODEL_VERSION,
) -> RunManifest:
    """Create an immutable record for a newly started run."""
    return RunManifest(
        manifest_schema_version="1.0.0",
        run_id=derive_run_id(scenario, model_version),
        scenario_id=scenario.scenario_id,
        scenario_sha256=content_sha256(scenario),
        evaluator_settings_sha256=content_sha256(scenario.evaluation),
        model_version=model_version,
        seed=scenario.evaluation.seed,
        runtime=runtime,
        status="created",
        started_at=started_at,
    )


def complete_run_manifest(
    manifest: RunManifest, completed_at: datetime
) -> RunManifest:
    """Return a completed copy while preserving the original manifest."""
    return RunManifest.model_validate(
        {
            **manifest.model_dump(mode="python"),
            "status": "completed",
            "completed_at": completed_at,
        }
    )


def collect_runtime_snapshot() -> RuntimeSnapshot:
    """Record installed versions that can explain run-level differences."""
    dependencies = tuple(
        DependencyVersion(name=name, version=version(name)) for name in ("pydantic",)
    )
    return RuntimeSnapshot(
        package_version=__version__,
        python_version=platform.python_version(),
        dependencies=dependencies,
    )
