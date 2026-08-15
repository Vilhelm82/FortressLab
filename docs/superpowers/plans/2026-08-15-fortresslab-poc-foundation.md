# FortressLab POC Foundation Implementation Plan

**Status:** Completed on `main` on 2026-08-15. All nine tasks and the milestone
acceptance gate were executed; the resulting implementation is recorded in the
repository history.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable FortressLab vertical slice: an installable headless Python package that strictly validates a versioned scenario, emits a canonical immutable snapshot, and derives a reproducible run manifest.

**Architecture:** Pydantic models form a frozen, project-owned schema boundary; exact geometry algorithms remain outside this milestone. Canonical JSON and SHA-256 hashing are implemented in a dependency-free serialization module, while manifest identity excludes timestamps and other volatile execution metadata. A thin CLI consumes the same loader and schemas as Python callers.

**Tech Stack:** CPython 3.14.4 development runtime with declared support for Python 3.12–3.14; uv 0.11; Pydantic 2.13; pytest 9.1; Hypothesis 6.165; Ruff 0.16; mypy 2.3; standard-library `argparse`, `json`, `hashlib`, and `importlib.metadata`.

**Spec:** `docs/superpowers/specs/2026-08-15-fortresslab-poc-design.md`, specifically development-sequence stage 1.

## Global Constraints

- This plan implements stage 1 only: repository/package setup, strict schemas, metre-based units, canonical scenario snapshots, reproducible manifest identity, and `fortresslab validate`.
- Persisted inputs are JSON and carry `schema_version = "1.0.0"`.
- Development uses Python 3.14.4; `requires-python = ">=3.12,<3.15"` prevents claiming support outside the tested language range.
- Pydantic is the only runtime dependency in this milestone. Geometry, arrays, graphs, plotting, and game-engine packages are not introduced.
- All persisted distances are metres, elevations are metres, angles are degrees, and field names include `_m` or `_deg` where a naked number would be ambiguous.
- Models reject unknown fields, string-to-number coercion, booleans used as numbers, NaN, positive infinity, and negative infinity.
- Validated models are frozen. Mutation occurs by creating and validating a new model.
- Exact geometry remains authoritative. This milestone validates structural shape and references but does not claim self-intersection, support, visibility, breach, or reachability analysis.
- Scenario production data contains state and declared capability inputs only. It contains no expected result, fixture name, evaluator hint, or scenario-specific branch key.
- Canonical serialization is UTF-8, compact, key-sorted JSON with finite numbers and normalized negative zero. It is a project format, not a claim of full RFC 8785 conformance.
- SHA-256 content hashes cover canonical bytes. Stable run identity covers scenario hash, evaluator-settings hash, model version, and seed; timestamps do not affect it.
- Tests exercise real models, files, serialization, and CLI processes. No mocks are required in this milestone.
- Property strategies generate valid inputs by construction and use no broad `assume()` filtering.
- Every task follows red-green-refactor and ends with the complete repository test suite passing.

## Milestone Boundary

This foundation is accepted when:

1. `uv sync --all-groups` installs the locked environment.
2. A valid example scenario survives load → validate → canonical JSON → load without semantic change.
3. Canonical serialization is idempotent and independent of mapping insertion order.
4. Invalid dimensions, non-finite numbers, unknown fields, duplicate IDs, and broken cross-references fail with actionable paths.
5. Identical scenario/configuration/model/seed inputs derive the same run ID despite different timestamps.
6. Changing the scenario, evaluation settings, model version, or seed changes the run ID.
7. `fortresslab validate scenarios/examples/minimal-enclosure.json --json` exits 0 and emits a typed validation report.
8. Invalid JSON and invalid scenarios exit 2 without a traceback.
9. pytest, Hypothesis, Ruff, mypy, and wheel build all pass.

## File Map

| Path | Responsibility |
|---|---|
| `pyproject.toml` | Package metadata, dependency bounds, console script, and tool configuration |
| `uv.lock` | Fully resolved dependency environment |
| `src/fortresslab/schema/base.py` | Frozen strict base model, version constants, identifier and numeric aliases |
| `src/fortresslab/schema/primitives.py` | Schema-level points and polygon/polyline boundary checks |
| `src/fortresslab/schema/terrain.py` | Heightfield, soil, water, and terrain input definitions |
| `src/fortresslab/schema/fortifications.py` | Material and discriminated fortification input definitions |
| `src/fortresslab/schema/operations.py` | Objectives, defensive positions, observers, attacker capabilities, and evaluation settings |
| `src/fortresslab/schema/scenario.py` | Aggregate scenario model and cross-reference validation |
| `src/fortresslab/schema/manifest.py` | Typed runtime snapshot and run-manifest records |
| `src/fortresslab/schema/validation.py` | Typed CLI validation result and issue records |
| `src/fortresslab/serialization.py` | Canonical JSON normalization and SHA-256 content hashing |
| `src/fortresslab/manifest.py` | Stable run-ID derivation and explicit manifest lifecycle |
| `src/fortresslab/io.py` | File loading and validation-error normalization |
| `src/fortresslab/cli.py` | Thin `argparse` command boundary |
| `tests/factories.py` | Valid hand-authored model builders used only as test setup |
| `tests/strategies.py` | Hypothesis strategies that generate valid scenarios by construction |
| `scenarios/examples/minimal-enclosure.json` | Human-readable, valid schema-v1 example |
| `docs/model/scenario-schema-v1.md` | Units, schema contract, validation boundary, and versioning rules |

---

### Task 1: Bootstrap the installable package and locked toolchain

**Files:**
- Create: `.python-version`
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `src/fortresslab/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/unit/test_package.py`
- Generate: `uv.lock`

**Interfaces:**
- Consumes: CPython 3.14.4 and uv available on the host.
- Produces: importable `fortresslab` package exposing `__version__: str` and `MODEL_VERSION: str`.

- [x] **Step 1: Write the failing package-contract test**

```python
from fortresslab import MODEL_VERSION, __version__


def test_package_exposes_independent_package_and_model_versions() -> None:
    assert __version__ == "0.1.0"
    assert MODEL_VERSION == "poc-foundation-1"
```

This catches a missing package boundary or accidental coupling between install-package versioning and evaluator-model versioning.

- [x] **Step 2: Run the test and verify the red state**

Run: `python3 -m pytest tests/unit/test_package.py -v`

Expected: collection fails with `ModuleNotFoundError: No module named 'fortresslab'`.

- [x] **Step 3: Create the minimal package and tool configuration**

`.python-version`:

```text
3.14
```

`.gitignore`:

```gitignore
.venv/
.pytest_cache/
.hypothesis/
.mypy_cache/
.ruff_cache/
__pycache__/
*.py[cod]
*.egg-info/
build/
dist/
.worktrees/
generated/runs/
generated/reports/
```

`pyproject.toml`:

```toml
[build-system]
requires = ["hatchling>=1.32,<2"]
build-backend = "hatchling.build"

[project]
name = "fortresslab"
version = "0.1.0"
description = "Headless, evidence-backed fortification evaluation research environment"
readme = "README.md"
requires-python = ">=3.12,<3.15"
dependencies = [
  "pydantic>=2.13.4,<3",
]

[project.scripts]
fortresslab = "fortresslab.cli:entrypoint"

[dependency-groups]
dev = [
  "hypothesis>=6.165.9,<7",
  "mypy>=2.3.1,<3",
  "pytest>=9.1.1,<10",
  "ruff>=0.16.3,<1",
]

[tool.hatch.build.targets.wheel]
packages = ["src/fortresslab"]

[tool.pytest.ini_options]
addopts = "-ra --strict-config --strict-markers"
testpaths = ["tests"]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I", "B", "SIM", "UP", "RUF"]

[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests"]
```

`src/fortresslab/__init__.py`:

```python
"""FortressLab public package metadata."""

__version__ = "0.1.0"
MODEL_VERSION = "poc-foundation-1"

__all__ = ["MODEL_VERSION", "__version__"]
```

`tests/__init__.py` is an empty package marker so shared factories and
strategies have stable import paths under pytest and mypy.

`README.md`:

```markdown
# FortressLab

FortressLab is a headless research environment for spatially grounded,
evidence-backed evaluation of defensive fortifications.

The current milestone establishes the versioned scenario and reproducibility
contracts. Geometry and evaluator behaviour are added in subsequent milestones.

## Development

~~~bash
uv sync --all-groups
uv run pytest
uv run ruff check .
uv run mypy
~~~
```

- [x] **Step 4: Lock dependencies and verify the green state**

Run:

```bash
uv lock
uv sync --all-groups
uv run pytest tests/unit/test_package.py -v
uv run ruff check .
uv run mypy
```

Expected: one test passes; lint and type checks exit 0.

- [x] **Step 5: Commit the package foundation**

```bash
git add .python-version .gitignore pyproject.toml uv.lock README.md src/fortresslab/__init__.py tests/__init__.py tests/unit/test_package.py
git commit -m "build: bootstrap FortressLab Python package"
```

---

### Task 2: Establish strict schema primitives and unit-bearing field types

**Files:**
- Create: `src/fortresslab/schema/__init__.py`
- Create: `src/fortresslab/schema/base.py`
- Create: `src/fortresslab/schema/primitives.py`
- Create: `tests/unit/schema/test_primitives.py`

**Interfaces:**
- Consumes: Pydantic 2 strict validation.
- Produces: `StrictModel`, `Identifier`, `PositiveMetres`, `NonNegativeMetres`, `PositiveScalar`, `NonNegativeScalar`, `UnitInterval`, `Degrees`, `Point2D`, `Point3D`, and `Polygon2D`.

- [x] **Step 1: Write failing strictness and primitive tests**

```python
import pytest
from pydantic import ValidationError

from fortresslab.schema.base import StrictModel
from fortresslab.schema.primitives import Point2D, Polygon2D


class DistanceSample(StrictModel):
    distance_m: float


def test_strict_model_rejects_numeric_strings_and_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        DistanceSample.model_validate({"distance_m": "1.0"})
    with pytest.raises(ValidationError):
        DistanceSample.model_validate({"distance_m": 1.0, "hint": "gate"})


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_strict_model_rejects_non_finite_numbers(value: float) -> None:
    with pytest.raises(ValidationError):
        DistanceSample(distance_m=value)


def test_validated_models_are_frozen() -> None:
    point = Point2D(x_m=1.0, y_m=2.0)
    with pytest.raises(ValidationError):
        point.x_m = 3.0


def test_polygon_requires_three_distinct_unclosed_vertices() -> None:
    with pytest.raises(ValidationError):
        Polygon2D(vertices=(Point2D(x_m=0, y_m=0), Point2D(x_m=1, y_m=0)))
    with pytest.raises(ValidationError):
        Polygon2D(
            vertices=(
                Point2D(x_m=0, y_m=0),
                Point2D(x_m=1, y_m=0),
                Point2D(x_m=0, y_m=0),
            )
        )
```

The tests catch permissive coercion, hidden extra inputs, non-finite spatial state, mutation of validated snapshots, and degenerate polygon boundaries.

- [x] **Step 2: Run the tests and verify the red state**

Run: `uv run pytest tests/unit/schema/test_primitives.py -v`

Expected: collection fails because `fortresslab.schema` does not exist.

- [x] **Step 3: Implement the strict base and primitives**

`src/fortresslab/schema/base.py`:

```python
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

SCHEMA_VERSION = "1.0.0"
SchemaVersion: TypeAlias = Literal["1.0.0"]
Identifier: TypeAlias = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9_-]{0,63}$"),
]
PositiveMetres: TypeAlias = Annotated[float, Field(gt=0)]
NonNegativeMetres: TypeAlias = Annotated[float, Field(ge=0)]
PositiveScalar: TypeAlias = Annotated[float, Field(gt=0)]
NonNegativeScalar: TypeAlias = Annotated[float, Field(ge=0)]
UnitInterval: TypeAlias = Annotated[float, Field(ge=0, le=1)]
Degrees: TypeAlias = Annotated[float, Field(ge=0, lt=360)]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        allow_inf_nan=False,
        extra="forbid",
        frozen=True,
        strict=True,
        validate_default=True,
    )
```

`src/fortresslab/schema/primitives.py`:

```python
from pydantic import Field, field_validator

from fortresslab.schema.base import StrictModel


class Point2D(StrictModel):
    x_m: float
    y_m: float


class Point3D(StrictModel):
    x_m: float
    y_m: float
    z_m: float


class Polygon2D(StrictModel):
    vertices: tuple[Point2D, ...] = Field(min_length=3)

    @field_validator("vertices")
    @classmethod
    def require_distinct_unclosed_vertices(
        cls, vertices: tuple[Point2D, ...]
    ) -> tuple[Point2D, ...]:
        coordinates = tuple((point.x_m, point.y_m) for point in vertices)
        if len(set(coordinates)) < 3:
            raise ValueError("polygon requires at least three distinct vertices")
        if coordinates[0] == coordinates[-1]:
            raise ValueError("polygon ring must not repeat its first vertex")
        return vertices
```

`src/fortresslab/schema/__init__.py` exports only the stable names above. Do not re-export every concrete scenario type from the package root.

- [x] **Step 4: Run focused and full verification**

Run:

```bash
uv run pytest tests/unit/schema/test_primitives.py -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0.

- [x] **Step 5: Commit strict schema primitives**

```bash
git add src/fortresslab/schema tests/unit/schema/test_primitives.py
git commit -m "feat: add strict schema primitives"
```

---

### Task 3: Define terrain, soil, and water input schemas

**Files:**
- Create: `src/fortresslab/schema/terrain.py`
- Create: `tests/unit/schema/test_terrain.py`

**Interfaces:**
- Consumes: `Identifier`, `PositiveMetres`, `PositiveScalar`, `UnitInterval`, `Point2D`, and `Polygon2D`.
- Produces: `HeightField`, `SoilDefinition`, `SoilRegion`, `WaterRegion`, and `TerrainDefinition`.

- [x] **Step 1: Write failing terrain-schema tests**

```python
import pytest
from pydantic import ValidationError

from fortresslab.schema.primitives import Point2D, Polygon2D
from fortresslab.schema.terrain import (
    HeightField,
    SoilDefinition,
    TerrainDefinition,
)


def test_heightfield_requires_a_rectangular_two_by_two_grid() -> None:
    with pytest.raises(ValidationError, match="same number of samples"):
        HeightField(
            origin=Point2D(x_m=0, y_m=0),
            cell_spacing_m=1,
            elevations_m=((0, 0), (0,)),
        )


def test_terrain_default_soil_must_reference_declared_soil() -> None:
    heightfield = HeightField(
        origin=Point2D(x_m=0, y_m=0),
        cell_spacing_m=5,
        elevations_m=((0, 0), (0, 0)),
    )
    with pytest.raises(ValidationError, match="default_soil_id"):
        TerrainDefinition(
            heightfield=heightfield,
            analysis_resolution_m=1,
            soils=(
                SoilDefinition(
                    id="rock",
                    label="Rock",
                    foundation_quality=1,
                    traversability_multiplier=1,
                ),
            ),
            default_soil_id="mud",
        )


def test_polygon_schema_does_not_claim_self_intersection_analysis() -> None:
    bow_tie = Polygon2D(
        vertices=(
            Point2D(x_m=0, y_m=0),
            Point2D(x_m=2, y_m=2),
            Point2D(x_m=0, y_m=2),
            Point2D(x_m=2, y_m=0),
        )
    )
    assert len(bow_tie.vertices) == 4
```

The final test preserves the milestone boundary: schema shape validation must not masquerade as the exact geometry layer planned for stage 2.

- [x] **Step 2: Run the tests and verify the red state**

Run: `uv run pytest tests/unit/schema/test_terrain.py -v`

Expected: collection fails because `fortresslab.schema.terrain` does not exist.

- [x] **Step 3: Implement terrain input models and local references**

```python
from pydantic import Field, field_validator, model_validator

from fortresslab.schema.base import (
    Identifier,
    PositiveMetres,
    PositiveScalar,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point2D, Polygon2D


class HeightField(StrictModel):
    origin: Point2D
    cell_spacing_m: PositiveMetres
    elevations_m: tuple[tuple[float, ...], ...] = Field(min_length=2)

    @field_validator("elevations_m")
    @classmethod
    def require_rectangular_grid(
        cls, rows: tuple[tuple[float, ...], ...]
    ) -> tuple[tuple[float, ...], ...]:
        width = len(rows[0])
        if width < 2:
            raise ValueError("heightfield rows require at least two samples")
        if any(len(row) != width for row in rows):
            raise ValueError("heightfield rows must have the same number of samples")
        return rows


class SoilDefinition(StrictModel):
    id: Identifier
    label: str = Field(min_length=1, max_length=120)
    foundation_quality: UnitInterval
    traversability_multiplier: PositiveScalar


class SoilRegion(StrictModel):
    id: Identifier
    soil_id: Identifier
    boundary: Polygon2D


class WaterRegion(StrictModel):
    id: Identifier
    boundary: Polygon2D
    surface_elevation_m: float
    nominal_depth_m: PositiveMetres


class TerrainDefinition(StrictModel):
    heightfield: HeightField
    analysis_resolution_m: PositiveMetres
    soils: tuple[SoilDefinition, ...] = Field(min_length=1)
    default_soil_id: Identifier
    soil_regions: tuple[SoilRegion, ...] = ()
    water_regions: tuple[WaterRegion, ...] = ()

    @model_validator(mode="after")
    def validate_local_references(self) -> "TerrainDefinition":
        soil_ids = [soil.id for soil in self.soils]
        if len(soil_ids) != len(set(soil_ids)):
            raise ValueError("terrain.soils contains duplicate ids")
        if self.default_soil_id not in soil_ids:
            raise ValueError("terrain.default_soil_id does not reference terrain.soils")
        for index, region in enumerate(self.soil_regions):
            if region.soil_id not in soil_ids:
                raise ValueError(
                    f"terrain.soil_regions[{index}].soil_id is unknown: {region.soil_id}"
                )
        return self
```

The dimensionless `PositiveScalar` alias prevents a semantically wrong unit
from entering `traversability_multiplier`.

- [x] **Step 4: Run focused and full verification**

Run:

```bash
uv run pytest tests/unit/schema/test_terrain.py -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0.

- [x] **Step 5: Commit terrain schemas**

```bash
git add src/fortresslab/schema/base.py src/fortresslab/schema/terrain.py tests/unit/schema/test_terrain.py
git commit -m "feat: define terrain input schema"
```

---

### Task 4: Define fortification and material input schemas

**Files:**
- Create: `src/fortresslab/schema/fortifications.py`
- Create: `tests/unit/schema/test_fortifications.py`

**Interfaces:**
- Consumes: strict scalar aliases, points, and polygons.
- Produces: `MaterialDefinition`, `Wall`, `Tower`, `Gate`, `Ditch`, `Bridge`, and discriminated `Fortification`.

- [x] **Step 1: Write failing discriminated-union and boundary tests**

```python
import pytest
from pydantic import TypeAdapter, ValidationError

from fortresslab.schema.fortifications import Fortification, Gate, Wall
from fortresslab.schema.primitives import Point2D


def test_fortification_union_selects_wall_from_kind() -> None:
    adapter = TypeAdapter(Fortification)
    wall = adapter.validate_python(
        {
            "kind": "wall",
            "id": "south_wall",
            "path": (
                {"x_m": 0.0, "y_m": 0.0},
                {"x_m": 20.0, "y_m": 0.0},
            ),
            "height_m": 8.0,
            "thickness_m": 2.0,
            "material_id": "stone",
            "condition": 1.0,
            "wall_walk_width_m": 1.5,
        }
    )
    assert isinstance(wall, Wall)


def test_wall_requires_two_distinct_path_points() -> None:
    with pytest.raises(ValidationError, match="distinct"):
        Wall(
            id="wall",
            path=(Point2D(x_m=0, y_m=0), Point2D(x_m=0, y_m=0)),
            height_m=8,
            thickness_m=2,
            material_id="stone",
            condition=1,
            wall_walk_width_m=1,
        )


def test_gate_rejects_non_positive_width() -> None:
    with pytest.raises(ValidationError):
        Gate(
            id="main_gate",
            host_wall_id="south_wall",
            centre=Point2D(x_m=10, y_m=0),
            width_m=0,
            traversal_state="closed",
            abstract_resistance=1,
        )
```

- [x] **Step 2: Run the tests and verify the red state**

Run: `uv run pytest tests/unit/schema/test_fortifications.py -v`

Expected: collection fails because `fortresslab.schema.fortifications` does not exist.

- [x] **Step 3: Implement the fortification union**

```python
from typing import Annotated, Literal, TypeAlias

from pydantic import Field, field_validator, model_validator

from fortresslab.schema.base import (
    Identifier,
    NonNegativeMetres,
    PositiveMetres,
    PositiveScalar,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point2D, Polygon2D


class MaterialDefinition(StrictModel):
    id: Identifier
    label: str = Field(min_length=1, max_length=120)
    abstract_resistance: PositiveScalar
    notes: str | None = Field(default=None, max_length=1000)


class Wall(StrictModel):
    kind: Literal["wall"] = "wall"
    id: Identifier
    path: tuple[Point2D, ...] = Field(min_length=2)
    height_m: PositiveMetres
    thickness_m: PositiveMetres
    material_id: Identifier
    condition: UnitInterval
    wall_walk_width_m: NonNegativeMetres

    @field_validator("path")
    @classmethod
    def require_distinct_path_points(
        cls, path: tuple[Point2D, ...]
    ) -> tuple[Point2D, ...]:
        coordinates = tuple((point.x_m, point.y_m) for point in path)
        if len(set(coordinates)) < 2:
            raise ValueError("wall path requires at least two distinct points")
        return path


class Tower(StrictModel):
    kind: Literal["tower"] = "tower"
    id: Identifier
    footprint: Polygon2D
    height_m: PositiveMetres
    material_id: Identifier
    condition: UnitInterval
    access_points: tuple[Point2D, ...] = ()
    fighting_position_capacity: int = Field(ge=0)


class Gate(StrictModel):
    kind: Literal["gate"] = "gate"
    id: Identifier
    host_wall_id: Identifier
    centre: Point2D
    width_m: PositiveMetres
    traversal_state: Literal["open", "closed", "blocked"]
    abstract_resistance: PositiveScalar
    successive_barrier_ids: tuple[Identifier, ...] = ()


class Ditch(StrictModel):
    kind: Literal["ditch"] = "ditch"
    id: Identifier
    path: tuple[Point2D, ...] = Field(min_length=2)
    width_m: PositiveMetres
    depth_m: PositiveMetres
    side_slope_deg: float = Field(gt=0, lt=90)
    water_state: Literal["dry", "wet", "flooded"]

    @field_validator("path")
    @classmethod
    def require_distinct_path_points(
        cls, path: tuple[Point2D, ...]
    ) -> tuple[Point2D, ...]:
        coordinates = tuple((point.x_m, point.y_m) for point in path)
        if len(set(coordinates)) < 2:
            raise ValueError("ditch path requires at least two distinct points")
        return path


class Bridge(StrictModel):
    kind: Literal["bridge"] = "bridge"
    id: Identifier
    start: Point2D
    end: Point2D
    width_m: PositiveMetres
    traversability: Literal["open", "restricted", "blocked"]
    denial_state: Literal["intact", "prepared", "denied"]

    @model_validator(mode="after")
    def require_nonzero_span(self) -> "Bridge":
        if self.start == self.end:
            raise ValueError("bridge start and end must differ")
        return self


Fortification: TypeAlias = Annotated[
    Wall | Tower | Gate | Ditch | Bridge,
    Field(discriminator="kind"),
]
```

These checks validate declared structure only; intersection and terrain
compatibility remain stage-2 geometry work.

- [x] **Step 4: Run focused and full verification**

Run:

```bash
uv run pytest tests/unit/schema/test_fortifications.py -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0.

- [x] **Step 5: Commit fortification schemas**

```bash
git add src/fortresslab/schema/fortifications.py tests/unit/schema/test_fortifications.py
git commit -m "feat: define fortification input schema"
```

---

### Task 5: Define operational inputs without simulating armies

**Files:**
- Create: `src/fortresslab/schema/operations.py`
- Create: `tests/unit/schema/test_operations.py`

**Interfaces:**
- Consumes: identifiers, strict numeric aliases, `Point3D`.
- Produces: `Objective`, `WeaponEnvelope`, `DefensivePosition`, `Observer`, `MovementCapabilities`, `EngineeringCapabilities`, `AttackerProfile`, and `EvaluationSettings`.

- [x] **Step 1: Write failing capability-boundary tests**

```python
import pytest
from pydantic import ValidationError

from fortresslab.schema.operations import (
    EngineeringCapabilities,
    EvaluationSettings,
    MovementCapabilities,
)


def test_movement_capability_rejects_vertical_ground_slope() -> None:
    with pytest.raises(ValidationError):
        MovementCapabilities(
            max_slope_deg=90,
            minimum_corridor_width_m=1,
            maximum_wading_depth_m=1,
        )


def test_engineering_capabilities_reject_impossible_bridge_combination() -> None:
    with pytest.raises(ValidationError, match="maximum_bridge_span_m"):
        EngineeringCapabilities(
            can_bridge=False,
            maximum_bridge_span_m=5,
            can_fill_ditch=True,
            can_breach_wall=True,
            abstract_breach_capacity=1,
        )


def test_evaluation_seed_is_unsigned_64_bit() -> None:
    with pytest.raises(ValidationError):
        EvaluationSettings(seed=-1)
    assert EvaluationSettings(seed=2**64 - 1).seed == 2**64 - 1
```

- [x] **Step 2: Run the tests and verify the red state**

Run: `uv run pytest tests/unit/schema/test_operations.py -v`

Expected: collection fails because `fortresslab.schema.operations` does not exist.

- [x] **Step 3: Implement operational input models**

```python
from typing import Literal

from pydantic import Field, model_validator

from fortresslab.schema.base import (
    Degrees,
    Identifier,
    NonNegativeScalar,
    NonNegativeMetres,
    PositiveMetres,
    PositiveScalar,
    StrictModel,
    UnitInterval,
)
from fortresslab.schema.primitives import Point3D


class Objective(StrictModel):
    id: Identifier
    location: Point3D
    capture_radius_m: PositiveMetres
    priority: PositiveScalar = 1.0


class WeaponEnvelope(StrictModel):
    minimum_range_m: NonNegativeMetres
    maximum_range_m: PositiveMetres
    facing_deg: Degrees
    horizontal_arc_deg: float = Field(gt=0, le=360)

    @model_validator(mode="after")
    def require_ordered_ranges(self) -> "WeaponEnvelope":
        if self.minimum_range_m >= self.maximum_range_m:
            raise ValueError("minimum_range_m must be less than maximum_range_m")
        return self


class DefensivePosition(StrictModel):
    id: Identifier
    location: Point3D
    capacity: int = Field(gt=0)
    weapon_envelope: WeaponEnvelope
    access_node_id: Identifier | None = None


class Observer(StrictModel):
    id: Identifier
    location: Point3D
    reconnaissance_quality: UnitInterval


class MovementCapabilities(StrictModel):
    max_slope_deg: float = Field(gt=0, lt=90)
    minimum_corridor_width_m: PositiveMetres
    maximum_wading_depth_m: NonNegativeMetres


class EngineeringCapabilities(StrictModel):
    can_bridge: bool
    maximum_bridge_span_m: NonNegativeMetres
    can_fill_ditch: bool
    can_breach_wall: bool
    abstract_breach_capacity: NonNegativeScalar

    @model_validator(mode="after")
    def require_compatible_bridge_capability(self) -> "EngineeringCapabilities":
        if self.can_bridge and self.maximum_bridge_span_m == 0:
            raise ValueError(
                "maximum_bridge_span_m must be positive when can_bridge is true"
            )
        if not self.can_bridge and self.maximum_bridge_span_m != 0:
            raise ValueError(
                "maximum_bridge_span_m must be zero when can_bridge is false"
            )
        if self.can_breach_wall and self.abstract_breach_capacity == 0:
            raise ValueError(
                "abstract_breach_capacity must be positive when can_breach_wall is true"
            )
        if not self.can_breach_wall and self.abstract_breach_capacity != 0:
            raise ValueError(
                "abstract_breach_capacity must be zero when can_breach_wall is false"
            )
        return self


class AttackerProfile(StrictModel):
    id: Identifier
    label: str = Field(min_length=1, max_length=120)
    movement: MovementCapabilities
    engineering: EngineeringCapabilities


class EvaluationSettings(StrictModel):
    seed: int = Field(ge=0, le=2**64 - 1)
    sparse_cell_resolution_m: PositiveMetres = 1.0
    sparse_chunk_cells: int = Field(default=16, ge=4, le=256)
    geometric_epsilon_m: PositiveMetres = 0.001
    mode: Literal["authoritative", "perceived", "both"] = "both"
```

These models describe capacities and potential defensive positions. They do not contain soldier counts, combat resolution, casualties, morale, fatigue, or commander behaviour.

- [x] **Step 4: Run focused and full verification**

Run:

```bash
uv run pytest tests/unit/schema/test_operations.py -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0.

- [x] **Step 5: Commit operational schemas**

```bash
git add src/fortresslab/schema/operations.py tests/unit/schema/test_operations.py
git commit -m "feat: define POC operational inputs"
```

---

### Task 6: Aggregate a versioned scenario and validate cross-references

**Files:**
- Create: `src/fortresslab/schema/scenario.py`
- Create: `tests/factories.py`
- Create: `tests/unit/schema/test_scenario.py`

**Interfaces:**
- Consumes: all stage-1 input models.
- Produces: `Scenario` with `Scenario.model_validate_json(payload) -> Scenario` and frozen, validated cross-references.

- [x] **Step 1: Create a valid test factory and failing cross-reference tests**

`tests/factories.py`:

```python
from fortresslab.schema.fortifications import Gate, MaterialDefinition, Wall
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
    structures = (
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
```

`tests/unit/schema/test_scenario.py`:

```python
import pytest
from pydantic import ValidationError

from fortresslab.schema.scenario import Scenario
from tests.factories import minimal_scenario


def test_minimal_scenario_is_frozen_and_versioned() -> None:
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
        match=r"structures\\[4\\]\\.host_wall_id is unknown: missing_wall",
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
        match=r"structures\\[0\\]\\.material_id is unknown: unobtainium",
    ):
        Scenario.model_validate(
            {
                **scenario.model_dump(mode="python"),
                "structures": (first_wall, *scenario.structures[1:]),
            }
        )
```

The expected paths are hand-authored. The tests fail if validation disappears, points at the wrong record, or accepts scenario-authored evaluator hints.

- [x] **Step 2: Run the tests and verify the red state**

Run: `uv run pytest tests/unit/schema/test_scenario.py -v`

Expected: collection fails because `fortresslab.schema.scenario` does not exist.

- [x] **Step 3: Implement the aggregate scenario model**

```python
from typing import Literal

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
    def validate_cross_references(self) -> "Scenario":
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
            if isinstance(structure, (Wall, Tower)):
                if structure.material_id not in material_id_set:
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
```

Do not add containment, intersection, wall continuity, bridge connectivity, or objective reachability here. Those checks depend on exact geometry and semantic graphs and belong to their respective milestones.

- [x] **Step 4: Run focused and full verification**

Run:

```bash
uv run pytest tests/unit/schema/test_scenario.py -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0.

- [x] **Step 5: Commit the scenario aggregate**

```bash
git add src/fortresslab/schema/scenario.py tests/factories.py tests/unit/schema/test_scenario.py
git commit -m "feat: validate versioned scenarios"
```

---

### Task 7: Canonicalize and hash immutable scenario snapshots

**Files:**
- Create: `src/fortresslab/serialization.py`
- Create: `tests/strategies.py`
- Create: `tests/unit/test_serialization.py`
- Create: `tests/properties/test_scenario_roundtrip.py`

**Interfaces:**
- Consumes: a Pydantic `BaseModel` or JSON-compatible value.
- Produces: `canonical_json_bytes(value) -> bytes` and `content_sha256(value) -> str`.

- [x] **Step 1: Write failing example and property tests**

`tests/unit/test_serialization.py`:

```python
import json

import pytest

from fortresslab.serialization import canonical_json_bytes, content_sha256


def test_canonical_json_has_hand_checked_order_spacing_and_negative_zero() -> None:
    payload = canonical_json_bytes({"z": -0.0, "a": [2, 1]})
    assert payload == b'{"a":[2,1],"z":0.0}'


def test_mapping_insertion_order_does_not_change_content_hash() -> None:
    assert content_sha256({"a": 1, "b": 2}) == content_sha256({"b": 2, "a": 1})


def test_non_finite_values_are_rejected_even_outside_models() -> None:
    with pytest.raises(ValueError, match="finite"):
        canonical_json_bytes({"distance_m": float("nan")})


def test_canonical_bytes_are_valid_utf8_json() -> None:
    assert json.loads(canonical_json_bytes({"name": "Crème"})) == {"name": "Crème"}
```

`tests/properties/test_scenario_roundtrip.py`:

```python
import json

from hypothesis import given

from fortresslab.schema.scenario import Scenario
from fortresslab.serialization import canonical_json_bytes
from tests.strategies import valid_scenarios


@given(valid_scenarios())
def test_scenario_canonical_json_roundtrip_is_semantic_identity(
    scenario: Scenario,
) -> None:
    restored = Scenario.model_validate_json(canonical_json_bytes(scenario))
    assert restored == scenario


@given(valid_scenarios())
def test_canonicalization_is_idempotent(scenario: Scenario) -> None:
    first = canonical_json_bytes(scenario)
    second = canonical_json_bytes(json.loads(first))
    assert second == first
```

`tests/strategies.py`:

```python
from hypothesis import strategies as st

from fortresslab.schema.scenario import Scenario
from tests.factories import minimal_scenario


@st.composite
def valid_scenarios(draw: st.DrawFn) -> Scenario:
    base = minimal_scenario()
    scenario_id = draw(
        st.from_regex(r"[a-z][a-z0-9_]{0,20}", fullmatch=True)
    )
    title = draw(
        st.text(
            alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -",
            min_size=1,
            max_size=60,
        )
    )
    seed = draw(st.integers(min_value=0, max_value=2**64 - 1))
    resolution = draw(
        st.floats(
            min_value=0.1,
            max_value=10,
            allow_nan=False,
            allow_infinity=False,
            width=32,
        )
    )
    samples = draw(
        st.lists(
            st.floats(
                min_value=-100,
                max_value=100,
                allow_nan=False,
                allow_infinity=False,
                width=32,
            ),
            min_size=9,
            max_size=9,
        )
    )
    heightfield = base.terrain.heightfield.model_copy(
        update={
            "elevations_m": (
                tuple(samples[0:3]),
                tuple(samples[3:6]),
                tuple(samples[6:9]),
            )
        }
    )
    terrain = base.terrain.model_copy(
        update={
            "analysis_resolution_m": resolution,
            "heightfield": heightfield,
        }
    )
    evaluation = base.evaluation.model_copy(update={"seed": seed})
    return Scenario.model_validate(
        {
            **base.model_dump(mode="python"),
            "scenario_id": scenario_id,
            "title": title,
            "terrain": terrain,
            "evaluation": evaluation,
        }
    )
```

All constraints are embedded in the strategies; there is no `assume()`
filtering.

- [x] **Step 2: Run the tests and verify the red state**

Run:

```bash
uv run pytest tests/unit/test_serialization.py tests/properties/test_scenario_roundtrip.py -v
```

Expected: collection fails because `fortresslab.serialization` does not exist.

- [x] **Step 3: Implement canonical JSON and hashing**

```python
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from typing import TypeAlias

from pydantic import BaseModel

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


def _normalize_json(value: object) -> JsonValue:
    if isinstance(value, BaseModel):
        return _normalize_json(value.model_dump(mode="json"))
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("canonical JSON numbers must be finite")
        return 0.0 if value == 0.0 else value
    if isinstance(value, Mapping):
        normalized: dict[str, JsonValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical JSON object keys must be strings")
            normalized[key] = _normalize_json(item)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize_json(item) for item in value]
    raise TypeError(f"unsupported canonical JSON value: {type(value).__name__}")


def canonical_json_bytes(value: object) -> bytes:
    normalized = _normalize_json(value)
    return json.dumps(
        normalized,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def content_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
```

- [x] **Step 4: Run focused properties with statistics, then the full suite**

Run:

```bash
uv run pytest tests/unit/test_serialization.py -v
uv run pytest tests/properties/test_scenario_roundtrip.py --hypothesis-show-statistics -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0; Hypothesis reports generated examples without filtering-health warnings.

- [x] **Step 5: Commit canonical serialization**

```bash
git add src/fortresslab/serialization.py tests/strategies.py tests/unit/test_serialization.py tests/properties/test_scenario_roundtrip.py
git commit -m "feat: canonicalize scenario snapshots"
```

---

### Task 8: Derive stable run identity and explicit manifests

**Files:**
- Create: `src/fortresslab/schema/manifest.py`
- Create: `src/fortresslab/manifest.py`
- Create: `tests/unit/test_manifest.py`
- Create: `tests/integration/test_runtime_snapshot.py`

**Interfaces:**
- Consumes: `Scenario`, `RuntimeSnapshot`, UTC start/completion times.
- Produces: `derive_run_id(scenario) -> str`, `create_run_manifest(...) -> RunManifest`, `complete_run_manifest(...) -> RunManifest`, and `collect_runtime_snapshot() -> RuntimeSnapshot`.

- [x] **Step 1: Write failing run-identity and lifecycle tests**

```python
from datetime import UTC, datetime, timedelta

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
    assert derive_run_id(scenario, "model-a") != derive_run_id(
        scenario, "model-b"
    )


def test_completion_precedes_start_is_rejected() -> None:
    started = datetime(2026, 8, 15, 10, tzinfo=UTC)
    manifest = create_run_manifest(minimal_scenario(), RUNTIME, started)
    with pytest.raises(ValidationError, match="completed_at"):
        complete_run_manifest(manifest, started - timedelta(seconds=1))
```

- [x] **Step 2: Run the tests and verify the red state**

Run: `uv run pytest tests/unit/test_manifest.py -v`

Expected: collection fails because the manifest modules do not exist.

- [x] **Step 3: Implement typed manifests and pure identity derivation**

`src/fortresslab/schema/manifest.py`:

```python
from datetime import datetime, timedelta
from typing import Literal

from pydantic import AwareDatetime, Field, field_validator, model_validator

from fortresslab.schema.base import Identifier, SchemaVersion, StrictModel


class DependencyVersion(StrictModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


class RuntimeSnapshot(StrictModel):
    package_version: str = Field(min_length=1)
    python_version: str = Field(min_length=1)
    dependencies: tuple[DependencyVersion, ...]


class RunManifest(StrictModel):
    manifest_schema_version: SchemaVersion
    run_id: Identifier
    scenario_id: Identifier
    scenario_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    evaluator_settings_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    model_version: str = Field(min_length=1)
    seed: int = Field(ge=0, le=2**64 - 1)
    runtime: RuntimeSnapshot
    status: Literal["created", "completed"]
    started_at: AwareDatetime
    completed_at: AwareDatetime | None = None

    @field_validator("started_at", "completed_at")
    @classmethod
    def require_utc(
        cls, value: datetime | None
    ) -> datetime | None:
        if value is not None and value.utcoffset() != timedelta(0):
            raise ValueError("run timestamps must use UTC")
        return value

    @model_validator(mode="after")
    def validate_lifecycle(self) -> "RunManifest":
        if self.status == "created" and self.completed_at is not None:
            raise ValueError("created manifest cannot contain completed_at")
        if self.status == "completed" and self.completed_at is None:
            raise ValueError("completed manifest requires completed_at")
        if self.completed_at is not None and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        return self
```

`src/fortresslab/manifest.py`:

```python
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
    return RunManifest.model_validate(
        {
            **manifest.model_dump(mode="python"),
            "status": "completed",
            "completed_at": completed_at,
        }
    )


def collect_runtime_snapshot() -> RuntimeSnapshot:
    dependencies = tuple(
        DependencyVersion(name=name, version=version(name))
        for name in ("pydantic",)
    )
    return RuntimeSnapshot(
        package_version=__version__,
        python_version=platform.python_version(),
        dependencies=dependencies,
    )
```

`run_id` matches the identifier grammar because it starts with `run_` and contains lowercase hexadecimal. Runtime package versions are evidence, not identity inputs; model version is the behaviour-bearing identity input.

- [x] **Step 4: Test the real runtime adapter and full suite**

`tests/integration/test_runtime_snapshot.py`:

```python
import platform

from fortresslab import __version__
from fortresslab.manifest import collect_runtime_snapshot


def test_runtime_snapshot_reads_installed_versions() -> None:
    snapshot = collect_runtime_snapshot()
    assert snapshot.package_version == __version__
    assert snapshot.python_version == platform.python_version()
    assert snapshot.dependencies[0].name == "pydantic"
    assert snapshot.dependencies[0].version
```

This test uses the real installed package metadata; it does not mock the
runtime adapter.

Run:

```bash
uv run pytest tests/unit/test_manifest.py tests/integration/test_runtime_snapshot.py -v
uv run pytest
uv run ruff check .
uv run mypy
```

Expected: all commands exit 0.

- [x] **Step 5: Commit reproducible manifests**

```bash
git add src/fortresslab/schema/manifest.py src/fortresslab/manifest.py tests/unit/test_manifest.py tests/integration/test_runtime_snapshot.py
git commit -m "feat: derive reproducible run manifests"
```

---

### Task 9: Ship the validation CLI, example scenario, and schema documentation

**Files:**
- Create: `src/fortresslab/schema/validation.py`
- Create: `src/fortresslab/io.py`
- Create: `src/fortresslab/cli.py`
- Create: `src/fortresslab/__main__.py`
- Create: `tests/unit/test_io.py`
- Create: `tests/integration/test_validate_cli.py`
- Create: `scenarios/examples/minimal-enclosure.json`
- Create: `docs/model/scenario-schema-v1.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: filesystem path to a JSON document.
- Produces: `load_scenario(path) -> Scenario`, `validate_path(path) -> ValidationReport`, console command `fortresslab validate PATH [--json]`, exit 0 for valid and exit 2 for invalid/unreadable input.

- [x] **Step 1: Write failing loader and real-process CLI tests**

`tests/unit/test_io.py`:

```python
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
```

`tests/integration/test_validate_cli.py` invokes the real module:

```python
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
```

- [x] **Step 2: Run the tests and verify the red state**

Run:

```bash
uv run pytest tests/unit/test_io.py tests/integration/test_validate_cli.py -v
```

Expected: collection fails because `fortresslab.io` and the example scenario do not exist.

- [x] **Step 3: Implement typed input errors and validation reports**

`src/fortresslab/schema/validation.py`:

```python
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
        default=None, pattern=r"^[0-9a-f]{64}$"
    )
    issues: tuple[ValidationIssue, ...] = ()
```

`src/fortresslab/io.py`:

```python
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
```

- [x] **Step 4: Implement the thin CLI boundary**

`src/fortresslab/cli.py`:

```python
import argparse
import sys
from pathlib import Path
from typing import Sequence

from fortresslab.io import ScenarioInputError, load_scenario
from fortresslab.schema.validation import ValidationReport
from fortresslab.serialization import canonical_json_bytes, content_sha256


def validate_path(path: Path) -> ValidationReport:
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
```

`src/fortresslab/__main__.py`:

```python
from fortresslab.cli import entrypoint

entrypoint()
```

- [x] **Step 5: Add the example and user-facing schema contract**

`scenarios/examples/minimal-enclosure.json`:

```json
{
  "schema_version": "1.0.0",
  "scenario_id": "minimal_enclosure",
  "title": "Minimal enclosure",
  "coordinate_system": "local_cartesian",
  "linear_unit": "m",
  "angular_unit": "deg",
  "terrain": {
    "heightfield": {
      "origin": {"x_m": 0.0, "y_m": 0.0},
      "cell_spacing_m": 10.0,
      "elevations_m": [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
      ]
    },
    "analysis_resolution_m": 1.0,
    "soils": [
      {
        "id": "firm_ground",
        "label": "Firm ground",
        "foundation_quality": 0.8,
        "traversability_multiplier": 1.0
      }
    ],
    "default_soil_id": "firm_ground",
    "soil_regions": [],
    "water_regions": []
  },
  "materials": [
    {
      "id": "stone",
      "label": "Generic masonry",
      "abstract_resistance": 1.0,
      "notes": null
    }
  ],
  "structures": [
    {
      "kind": "wall",
      "id": "south_wall",
      "path": [{"x_m": 0.0, "y_m": 0.0}, {"x_m": 20.0, "y_m": 0.0}],
      "height_m": 8.0,
      "thickness_m": 2.0,
      "material_id": "stone",
      "condition": 1.0,
      "wall_walk_width_m": 1.5
    },
    {
      "kind": "wall",
      "id": "east_wall",
      "path": [{"x_m": 20.0, "y_m": 0.0}, {"x_m": 20.0, "y_m": 20.0}],
      "height_m": 8.0,
      "thickness_m": 2.0,
      "material_id": "stone",
      "condition": 1.0,
      "wall_walk_width_m": 1.5
    },
    {
      "kind": "wall",
      "id": "north_wall",
      "path": [{"x_m": 20.0, "y_m": 20.0}, {"x_m": 0.0, "y_m": 20.0}],
      "height_m": 8.0,
      "thickness_m": 2.0,
      "material_id": "stone",
      "condition": 1.0,
      "wall_walk_width_m": 1.5
    },
    {
      "kind": "wall",
      "id": "west_wall",
      "path": [{"x_m": 0.0, "y_m": 20.0}, {"x_m": 0.0, "y_m": 0.0}],
      "height_m": 8.0,
      "thickness_m": 2.0,
      "material_id": "stone",
      "condition": 1.0,
      "wall_walk_width_m": 1.5
    },
    {
      "kind": "gate",
      "id": "main_gate",
      "host_wall_id": "south_wall",
      "centre": {"x_m": 10.0, "y_m": 0.0},
      "width_m": 3.0,
      "traversal_state": "closed",
      "abstract_resistance": 1.0,
      "successive_barrier_ids": []
    }
  ],
  "objectives": [
    {
      "id": "keep",
      "location": {"x_m": 10.0, "y_m": 10.0, "z_m": 0.0},
      "capture_radius_m": 2.0,
      "priority": 1.0
    }
  ],
  "defensive_positions": [
    {
      "id": "gatehouse_position",
      "location": {"x_m": 10.0, "y_m": 2.0, "z_m": 8.0},
      "capacity": 12,
      "weapon_envelope": {
        "minimum_range_m": 0.0,
        "maximum_range_m": 100.0,
        "facing_deg": 180.0,
        "horizontal_arc_deg": 120.0
      },
      "access_node_id": null
    }
  ],
  "observers": [
    {
      "id": "south_observer",
      "location": {"x_m": -10.0, "y_m": -10.0, "z_m": 5.0},
      "reconnaissance_quality": 0.6
    }
  ],
  "attacker": {
    "id": "generic_attackers",
    "label": "Generic attackers",
    "movement": {
      "max_slope_deg": 30.0,
      "minimum_corridor_width_m": 2.0,
      "maximum_wading_depth_m": 1.0
    },
    "engineering": {
      "can_bridge": true,
      "maximum_bridge_span_m": 12.0,
      "can_fill_ditch": true,
      "can_breach_wall": true,
      "abstract_breach_capacity": 1.0
    }
  },
  "evaluation": {
    "seed": 7,
    "sparse_cell_resolution_m": 1.0,
    "sparse_chunk_cells": 16,
    "geometric_epsilon_m": 0.001,
    "mode": "both"
  }
}
```

`docs/model/scenario-schema-v1.md`:

```markdown
# FortressLab Scenario Schema v1

## 1. Version and compatibility

Every scenario declares `schema_version`. This milestone accepts exactly
`1.0.0` and rejects unknown versions. Backward-compatible additions require a
documented schema revision; incompatible meaning changes require a new major
schema version.

Package version and model version are independent. Package `0.1.0` distributes
model `poc-foundation-1`, but neither value substitutes for the persisted
scenario version.

## 2. Coordinates and units

Version 1 uses a local right-handed Cartesian frame. `x_m` and `y_m` identify
horizontal metres; `z_m` and elevations identify vertical metres. Distances use
`_m` and angles use `_deg`. `linear_unit` must be `m` and `angular_unit` must be
`deg`.

## 3. Top-level contract

`Scenario` owns identity, units, terrain, materials, fortifications, protected
objectives, potential defensive positions, observers, one generic attacker
profile, and evaluation settings. Models are frozen after validation and reject
undeclared fields.

## 4. Stable identifiers

Identifiers match `^[a-z][a-z0-9_-]{0,63}$`. Material IDs are unique within the
material registry. Structure, objective, defensive-position, and observer IDs
share one scene-object namespace. A scenario ID and attacker-profile ID identify
their respective records and do not enter the scene-object namespace.

## 5. Terrain and heightfields

A heightfield has an origin, positive cell spacing, and at least two rows with
at least two finite samples per row. Every row has equal width. Terrain declares
at least one soil and a valid default-soil reference. Soil-region references
must resolve locally. Water boundaries use schema polygons and positive nominal
depth.

## 6. Fortifications

`kind` discriminates `wall`, `tower`, `gate`, `ditch`, and `bridge` records.
Walls and ditches require at least two distinct path points; polygon footprints
require at least three distinct unclosed vertices; bridges require distinct end
points. Wall and tower material references must resolve. A gate host must resolve
to a wall, and its successive barriers must resolve to other structures.

## 7. Operational inputs and exclusions

Defensive positions describe possible capacity and weapon envelopes, not actual
occupation or fire. The attacker profile separates movement and engineering
capabilities. Evaluation settings contain an explicit unsigned 64-bit seed,
resolution parameters, numerical tolerance, and requested authoritative or
perceived mode.

This schema contains no individual soldiers, combat resolution, casualties,
fatigue, morale, adaptive commanders, historical profiles, or runtime LLM
decisions.

## 8. Canonical snapshots and hashes

After validation, FortressLab serializes the complete model as compact UTF-8
JSON with sorted object keys, finite numbers, and negative zero normalized to
zero. SHA-256 is computed over those bytes. Mapping insertion order cannot
change the hash.

## 9. What validation proves

Validation proves schema version, type strictness, finite numeric state,
dimension bounds, identifier grammar, collection shape, local reference
integrity, and declared capability consistency. Errors identify their JSON path
where available.

## 10. What validation does not prove

Schema validation does not prove polygon simplicity, wall continuity, gate-wall
intersection, terrain compatibility, structural support, bridge connectivity,
visibility, access, objective reachability, breach feasibility, or defensive
quality. Those claims require the exact-geometry, graph, query, and evaluator
milestones. Accepting a scenario means it is structurally eligible for those
analyses—not that its fortress is physically sound or defensible.
```

Update `README.md` with:

```bash
uv run fortresslab validate scenarios/examples/minimal-enclosure.json
uv run fortresslab validate scenarios/examples/minimal-enclosure.json --json
```

- [x] **Step 6: Verify the focused tests and full milestone acceptance**

Run:

```bash
uv run pytest tests/unit/test_io.py tests/integration/test_validate_cli.py -v
uv run pytest --hypothesis-seed=0
uv run ruff check .
uv run mypy
uv build
uv run fortresslab validate scenarios/examples/minimal-enclosure.json --json
```

Expected:

- all tests pass with no Hypothesis health-check warnings;
- Ruff and mypy exit 0;
- source distribution and wheel are created under `dist/`;
- the CLI exits 0 and emits one JSON object with `valid: true`, `scenario_id: "minimal_enclosure"`, a 64-character lowercase SHA-256 value, and an empty `issues` list.

- [x] **Step 7: Commit the completed stage-1 vertical slice**

```bash
git add README.md docs/model scenarios/examples src/fortresslab tests
git commit -m "feat: ship scenario validation foundation"
```

---

## Plan Self-Review

### Spec coverage

| Stage-1 requirement | Planned evidence |
|---|---|
| Repository and installable package | Task 1 wheel/package setup |
| Locked environment | Task 1 `uv.lock` and `uv sync --all-groups` |
| Strict schemas and metre-based units | Tasks 2–6 |
| Stable IDs and actionable reference failures | Tasks 2 and 6 |
| Immutable validated snapshots | Tasks 2 and 7 |
| Deterministic canonical serialization and hashes | Task 7 |
| Explicit seed and evaluator configuration | Task 5 |
| Reproducible run manifest | Task 8 |
| Structured scenario loading | Task 9 |
| Public `validate` command | Task 9 |
| Unit, integration, and property tests | Tasks 1–9 |
| Documentation of claims and boundaries | Task 9 |

### Deliberately deferred to named design stages

- Exact terrain interpolation and fortification geometry: stage 2.
- Dense terrain fields, sparse 3D chunks, and semantic graphs: stage 3.
- Point, chain, visibility, corridor, and connectivity queries: stage 4.
- Evidence graph and explanation templates: stage 5.
- Analytical evaluators, perception, COAs, experiments, and HTML reporting: stages 6–12.

The stage-1 schemas expose stable inputs for those layers without implementing placeholder physics or evaluator scores.

### Type and naming consistency

- `scenario_id` identifies the scenario; every scene object uses `id`.
- Persisted schema version is `1.0.0`; evaluator behaviour version is `poc-foundation-1`; install package version is `0.1.0`.
- `content_sha256` hashes canonical bytes; `derive_run_id` hashes only stable behaviour-bearing inputs.
- `ScenarioInputError.issues` and `ValidationReport.issues` both use `tuple[ValidationIssue, ...]`.
- The CLI entry point is `fortresslab.cli:entrypoint`; testable logic remains in `main(argv) -> int` and `validate_path(path) -> ValidationReport`.

### Review gate

Resolved before implementation: the user explicitly chose direct execution on
`main`. The temporary empty worktree and feature branch were removed, and all
foundation commits were made directly on `main`.
