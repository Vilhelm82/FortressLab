from fortresslab.schema.fortifications import (
    Fortification,
    Gate,
    MaterialDefinition,
    Wall,
)
from fortresslab.schema.operations import (
    AttackerProfile,
    DefensivePosition,
    EngineeringCapabilities,
    EvaluationSettings,
    MovementCapabilities,
    Objective,
    Observer,
    WeaponEnvelope,
)
from fortresslab.schema.primitives import Point2D, Point3D
from fortresslab.schema.scenario import Scenario
from fortresslab.schema.terrain import (
    HeightField,
    SoilDefinition,
    TerrainDefinition,
)


def minimal_scenario() -> Scenario:
    terrain = TerrainDefinition(
        heightfield=HeightField(
            origin=Point2D(x_m=0, y_m=0),
            cell_spacing_m=10,
            elevations_m=((0, 0, 0), (0, 0, 0), (0, 0, 0)),
        ),
        analysis_resolution_m=1,
        soils=(
            SoilDefinition(
                id="firm_ground",
                label="Firm ground",
                foundation_quality=0.8,
                traversability_multiplier=1,
            ),
        ),
        default_soil_id="firm_ground",
    )
    structures: tuple[Fortification, ...] = (
        Wall(
            id="south_wall",
            path=(Point2D(x_m=0, y_m=0), Point2D(x_m=20, y_m=0)),
            height_m=8,
            thickness_m=2,
            material_id="stone",
            condition=1,
            wall_walk_width_m=1.5,
        ),
        Wall(
            id="east_wall",
            path=(Point2D(x_m=20, y_m=0), Point2D(x_m=20, y_m=20)),
            height_m=8,
            thickness_m=2,
            material_id="stone",
            condition=1,
            wall_walk_width_m=1.5,
        ),
        Wall(
            id="north_wall",
            path=(Point2D(x_m=20, y_m=20), Point2D(x_m=0, y_m=20)),
            height_m=8,
            thickness_m=2,
            material_id="stone",
            condition=1,
            wall_walk_width_m=1.5,
        ),
        Wall(
            id="west_wall",
            path=(Point2D(x_m=0, y_m=20), Point2D(x_m=0, y_m=0)),
            height_m=8,
            thickness_m=2,
            material_id="stone",
            condition=1,
            wall_walk_width_m=1.5,
        ),
        Gate(
            id="main_gate",
            host_wall_id="south_wall",
            centre=Point2D(x_m=10, y_m=0),
            width_m=3,
            traversal_state="closed",
            abstract_resistance=1,
        ),
    )
    return Scenario(
        schema_version="1.0.0",
        scenario_id="minimal_enclosure",
        title="Minimal enclosure",
        terrain=terrain,
        materials=(
            MaterialDefinition(
                id="stone",
                label="Generic masonry",
                abstract_resistance=1,
            ),
        ),
        structures=structures,
        objectives=(
            Objective(
                id="keep",
                location=Point3D(x_m=10, y_m=10, z_m=0),
                capture_radius_m=2,
            ),
        ),
        defensive_positions=(
            DefensivePosition(
                id="gatehouse_position",
                location=Point3D(x_m=10, y_m=2, z_m=8),
                capacity=12,
                weapon_envelope=WeaponEnvelope(
                    minimum_range_m=0,
                    maximum_range_m=100,
                    facing_deg=180,
                    horizontal_arc_deg=120,
                ),
            ),
        ),
        observers=(
            Observer(
                id="south_observer",
                location=Point3D(x_m=-10, y_m=-10, z_m=5),
                reconnaissance_quality=0.6,
            ),
        ),
        attacker=AttackerProfile(
            id="generic_attackers",
            label="Generic attackers",
            movement=MovementCapabilities(
                max_slope_deg=30,
                minimum_corridor_width_m=2,
                maximum_wading_depth_m=1,
            ),
            engineering=EngineeringCapabilities(
                can_bridge=True,
                maximum_bridge_span_m=12,
                can_fill_ditch=True,
                can_breach_wall=True,
                abstract_breach_capacity=1,
            ),
        ),
        evaluation=EvaluationSettings(seed=7),
    )
