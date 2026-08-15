"""Aggregate, versioned FortressLab scenario contract."""

from typing import Literal, Self

from pydantic import Field, model_validator

from fortresslab.schema.base import Identifier, SchemaVersion, StrictModel
from fortresslab.schema.fortifications import (
    Fortification,
    Gate,
    MaterialDefinition,
    Tower,
    Wall,
)
from fortresslab.schema.operations import (
    AttackerProfile,
    DefensivePosition,
    EvaluationSettings,
    Objective,
    Observer,
)
from fortresslab.schema.terrain import TerrainDefinition


class Scenario(StrictModel):
    schema_version: SchemaVersion
    scenario_id: Identifier
    title: str = Field(min_length=1, max_length=200)
    coordinate_system: Literal["local_cartesian"] = "local_cartesian"
    linear_unit: Literal["m"] = "m"
    angular_unit: Literal["deg"] = "deg"
    terrain: TerrainDefinition
    materials: tuple[MaterialDefinition, ...] = Field(min_length=1)
    structures: tuple[Fortification, ...] = ()
    objectives: tuple[Objective, ...] = Field(min_length=1)
    defensive_positions: tuple[DefensivePosition, ...] = ()
    observers: tuple[Observer, ...] = ()
    attacker: AttackerProfile
    evaluation: EvaluationSettings

    @model_validator(mode="after")
    def validate_cross_references(self) -> Self:
        material_ids = [material.id for material in self.materials]
        if len(material_ids) != len(set(material_ids)):
            raise ValueError("materials contains duplicate ids")

        scene_objects = (
            *self.structures,
            *self.objectives,
            *self.defensive_positions,
            *self.observers,
        )
        seen: set[str] = set()
        for item in scene_objects:
            if item.id in seen:
                raise ValueError(f"duplicate scene object id: {item.id}")
            seen.add(item.id)

        structure_by_id = {structure.id: structure for structure in self.structures}
        material_id_set = set(material_ids)
        for index, structure in enumerate(self.structures):
            if (
                isinstance(structure, (Wall, Tower))
                and structure.material_id not in material_id_set
            ):
                raise ValueError(
                    f"structures[{index}].material_id is unknown: "
                    f"{structure.material_id}"
                )
            if isinstance(structure, Gate):
                host = structure_by_id.get(structure.host_wall_id)
                if not isinstance(host, Wall):
                    raise ValueError(
                        f"structures[{index}].host_wall_id is unknown: "
                        f"{structure.host_wall_id}"
                    )
                for barrier_index, barrier_id in enumerate(
                    structure.successive_barrier_ids
                ):
                    if barrier_id == structure.id or barrier_id not in structure_by_id:
                        raise ValueError(
                            f"structures[{index}].successive_barrier_ids"
                            f"[{barrier_index}] is invalid: {barrier_id}"
                        )
        return self
