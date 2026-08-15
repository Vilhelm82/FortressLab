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
