# FortressLab Physics Engine Consumer Targets

**Status:** Consumer-requirements baseline for review

**Date:** 2026-08-16

**Consumer:** FortressLab

**Purpose:** Portable input to the plan for a separate, general-purpose physics engine

**Source requirements:** [FortressLab Full Game Concept Pitch v2](2026-08-15-fortresslab-full-game-concept-pitch-v2.md)
and [FortressLab POC Design](2026-08-15-fortresslab-poc-design.md)

## 1. Intent

This document lists the physical properties, behaviours, interfaces, and use
cases that FortressLab needs from an external physics engine. It deliberately
does not prescribe solver architecture, programming language, middleware,
rendering technology, or whether a target is implemented analytically,
numerically, or through a validated hybrid.

The external engine may serve other games. FortressLab remains the acceptance
client for every target in this document: a feature earns inclusion here only
when it enables a named FortressLab use case.

The governing requirement is:

> A plausible fortification strategy must succeed or fail because of the
> simulated physical world, not because a bespoke action or exception was
> scripted for that strategy.

## 2. Delivery tiers

| Tier | Meaning |
|---|---|
| F0 — Foundation | Required by any credible FortressLab integration |
| C1 — Core | Required by construction validation, engineering overlays, or the static adversarial evaluator |
| D2 — Dynamic | Required by the live dynamic-siege extension |
| A3 — Advanced | Required by the deepest full-vision consequence systems |

A target assigned to a later tier is not optional within that tier. Tiers state
when FortressLab needs a capability, not its importance to the eventual vision.
In the matrices below, UC-xx abbreviates FL-UC-xx, ranges are inclusive, and
All means every use case in Section 4.

## 3. Authority and system boundary

### 3.1 The physics engine owns

- Authoritative physical state: geometry, mass, motion, contact, support,
  loading, damage, material condition, fluids, heat, and terrain deformation.
- Physically possible state transitions and explicit failure when a requested
  state or action cannot be resolved.
- Stable physical identifiers, snapshots, event output, and replay inputs.
- Queryable measurements and model results with units, assumptions, numerical
  tolerances, and provenance.

### 3.2 FortressLab owns

- Player construction intent and authoring tools.
- Historical data, equipment definitions, uncertainty, and scenario rules.
- Attacker and defender planning, doctrine, perception, reports, and orders.
- Abstract personnel, labour, health, morale, logistics, and casualties.
- Defensive findings, courses of action, composite judgements, and presentation.

The physics engine supplies hazards, loads, access-changing geometry, and
environmental exposure. FortressLab decides what those outputs mean to an
abstract formation or commander.

### 3.3 Shared integration contract

- FortressLab-authored objects retain stable identity when compiled into engine
  representations.
- Fractured, detached, burned, eroded, or otherwise transformed descendants
  retain lineage back to their source object and causal event.
- Rendering is never authoritative. Headless execution and rendered execution
  consume the same physical state.
- Runtime AI and LLM components may request actions or interpret evidence, but
  may never invent authoritative physical outcomes.

## 4. FortressLab use-case catalogue

### FL-UC-01 — Construction feasibility

Compile a terrain and fortification design and determine whether it can stand
under self-weight, permanent loads, static earth and water loads, declared
normal occupancy, and mechanism preload. Return either a viable initial state or
an evidence-rich failed-build result. A failed design remains readable; it does
not receive a valid defensive evaluation.

### FL-UC-02 — Engineering overlays

Query foundation pressure, settlement risk, compression, tension, shear,
thrust, support dependencies, mechanism loads, safety margins, and predicted
failure regions without requiring the player to calculate them manually.

### FL-UC-03 — Engineered mechanisms

Operate and damage drawbridges, doors, portcullises, locks, winches, hinges,
ropes, chains, pulleys, gears, counterweights, brakes, guides, and latches.
Outcomes follow surviving load and power paths: a bridge can drop, twist, jam,
remain partly suspended, or become impossible to operate.

### FL-UC-04 — Projectile and impact response

Resolve trajectories, incidence, collision, impulse, penetration, deflection,
fracture, spall, splinters, local damage, and collapse initiation for arrows,
stones, bolts, artillery, rams, and comparable siege loads.

### FL-UC-05 — Progressive failure and debris

Redistribute loads after local damage, permit partial and progressive collapse,
generate persistent debris, and expose the new geometry to access, cover,
visibility, logistics, and later physical interactions.

### FL-UC-06 — Terrain engineering and undermining

Excavate ditches, grade roads, build embankments, place fill, tunnel, mine
foundations, undermine walls, create ramps, and alter terrain only through
physically accountable operations.

### FL-UC-07 — Hydrology and contamination transport

Model rainfall, rivers, ditches, dams, culverts, drainage, cisterns, compartment
flooding, saturation, erosion, scour, river diversion, and passive contaminant
transport. FortressLab owns toxicology and health consequences.

### FL-UC-08 — Fire, heat, and smoke

Ignite and spread fire through available fuel and ventilation, transport heat
and smoke, weaken materials and mechanisms, permit suppression, and preserve
burned or heated state. FortressLab owns human exposure consequences.

### FL-UC-09 — Mobile siege engines

Represent rams, siege towers, trebuchets, mantlets, mobile bridges, and similar
machines as physical units. Their geometry, mass, mechanisms, stability,
traction, route width, bogging, emplacement, damage, obstruction, and debris
must affect the siege. Crews remain abstract.

### FL-UC-10 — Repair, shoring, clearing, and demolition

Apply repairs or temporary supports only when geometry, access, tools, material,
labour input, and time permit them. Clear, move, reuse, or deliberately demolish
physical material while conserving the relevant state.

### FL-UC-11 — Long-duration and hybrid simulation

Advance quiet periods of a siege efficiently while activating detailed
simulation around impacts, mechanisms, fire fronts, fluids, unstable
structures, earthworks, and settling debris. Fidelity changes must not erase
gameplay-relevant consequences.

### FL-UC-12 — Forensic evidence and replay

Record why every important physical state changed. Permit timeline scrubbing,
causal backtracking, ground-truth inspection, save and resume, reproducible
reruns, and visual overlays derived from the same authoritative state.

### FL-UC-13 — Controlled experiments and historical scenarios

Fork a canonical state, change one declared input, run comparisons and sweeps,
and expose sensitivity or numerical instability. Historical inputs may be
uncertain; results must not be forced toward a recorded outcome.

### FL-UC-14 — Abstract-personnel physical interface

Accept aggregate occupancy, carried load, operating force, labour, and formation
footprint where needed. Return hazards, blocked volumes, required effort, safe
capacity, and exposure fields without simulating individual human or animal
bodies.

## 5. Foundational engine properties

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-FND-001 | F0 | SI units and explicit coordinate frames | Every persisted quantity declares units; conversions occur only at typed boundaries | All |
| FL-PHY-FND-002 | F0 | Authoritative headless state | The same scenario runs without a renderer and produces the same physical findings as a rendered run | All |
| FL-PHY-FND-003 | F0 | Stable object and subcomponent identity | Queries and events resolve back to authored IDs; transformed pieces retain ancestry | UC-02, 05, 12 |
| FL-PHY-FND-004 | F0 | Versioned state serialization | Snapshots declare schema, engine, solver, and material-model versions and reject incompatible loads explicitly | UC-12, 13 |
| FL-PHY-FND-005 | F0 | Reproducible authoritative mode | Identical build, platform contract, initial state, configuration, and seed reproduce the same journal and checkpoints | UC-12, 13 |
| FL-PHY-FND-006 | F0 | Bounded cross-platform variation | Cross-platform differences remain inside declared tolerances or are reported as incompatible, never silently treated as identical | UC-12, 13 |
| FL-PHY-FND-007 | F0 | Controlled stochasticity | Every stochastic physical choice is seeded, versioned, and attributable to a named model | UC-05, 08, 13 |
| FL-PHY-FND-008 | F0 | Explicit fixed-step and multirate time | The run records time policy; changing it triggers convergence evidence rather than hidden behavioural drift | UC-04, 08, 11 |
| FL-PHY-FND-009 | F0 | Snapshot, restore, and fork | A canonical state can be resumed or copied for a controlled mutation without changing the source run | UC-10, 12, 13 |
| FL-PHY-FND-010 | F0 | Structured failure instead of silent repair | Invalid states, non-convergence, unsupported actions, and exhausted budgets return typed failures with affected IDs | All |
| FL-PHY-FND-011 | F0 | Data-driven validated content | Materials, components, and mechanisms can be extended through versioned bounded data without arbitrary code controlling outcomes | UC-03, 09, 13 |
| FL-PHY-FND-012 | F0 | Numerical accounting | Constraint, conservation, penetration, fracture, and coupling residuals are observable and compared with configured tolerances | UC-04, 05, 07, 12 |
| FL-PHY-FND-013 | F0 | Batch and instrumentation support | Headless runs expose timing, active regions, solver work, memory, warnings, and convergence statistics | UC-11, 13 |

## 6. Geometry, contact, and spatial-query targets

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-GEO-001 | F0 | Preserve exact authored geometry | Curves, diagonals, narrow gaps, thickness, openings, and mechanism placement do not change meaning with grid resolution | UC-01 to 06 |
| FL-PHY-GEO-002 | F0 | Traceable solver representations | Every collision, reduced, or discretised representation maps back to source geometry and records approximation error | UC-02, 12 |
| FL-PHY-GEO-003 | F0 | Robust multiscale collision | Large terrain and fortress geometry coexist with thin ropes, chains, hinges, cracks, and projectiles without scale-dependent tunnelling | UC-03, 04, 09 |
| FL-PHY-GEO-004 | D2 | Continuous collision detection | Fast projectiles and rapidly moving mechanism parts cannot pass through valid targets between steps | UC-03, 04, 09 |
| FL-PHY-GEO-005 | F0 | Rich contact records | Contacts expose points, normals, penetration or separation, relative motion, impulse, friction state, materials, and source IDs | UC-02 to 10 |
| FL-PHY-GEO-006 | C1 | Terrain-conforming construction | Foundations, walls, roads, ditches, and bridges resolve against continuous terrain rather than a cosmetic height mesh | UC-01, 02, 06 |
| FL-PHY-GEO-007 | C1 | Physical topology validation | Gaps, intersections, unsupported spans, disconnected joints, invalid openings, and ambiguous containment produce actionable findings | UC-01, 03 |
| FL-PHY-GEO-008 | D2 | Persistent topology mutation | Breaches, excavation, collapse, erosion, and repairs alter later collision and query results without replacing the object with a generic state flag | UC-05 to 10 |
| FL-PHY-GEO-009 | F0 | Unified spatial queries | Point, ray, ordered chain, swept corridor, overlap, area, volume, and nearest-surface queries work against current authoritative state | UC-02, 04 to 09 |
| FL-PHY-GEO-010 | F0 | Declared geometric tolerances | Near-coincident and near-degenerate cases are resolved deterministically or rejected with a tolerance-specific failure | UC-01, 12, 13 |

## 7. Structures, foundations, and load paths

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-STR-001 | C1 | Quasi-static construction solve | A design can be checked for equilibrium and baseline viability without running an artificial settling animation | UC-01, 02 |
| FL-PHY-STR-002 | C1 | Complete baseline load case | Self-weight, permanent components, mechanism preload, static earth and water pressure, and declared normal occupancy are included | UC-01 |
| FL-PHY-STR-003 | C1 | Inspectable support and load-path graph | Loads can be traced from roofs, floors, walls, arches, mechanisms, and engines through supports into the ground | UC-02, 05, 10 |
| FL-PHY-STR-004 | C1 | Compression, tension, shear, bending, torsion, and thrust | Overlays and failure checks distinguish the governing action instead of collapsing it into durability | UC-01, 02, 05 |
| FL-PHY-STR-005 | C1 | Masonry-relevant behaviour | Weak tension, mortar interfaces, layered walls, rubble cores, arches, vaults, buttresses, and compression-dominated paths are representable | UC-01, 02, 04, 05 |
| FL-PHY-STR-006 | C1 | Timber and metal structural members | Beams, floors, roofs, ties, braces, columns, fasteners, and frames transfer load and can fail independently | UC-01, 05, 08 |
| FL-PHY-STR-007 | C1 | Foundation bearing and contact | Pressure distribution, inadequate area, eccentric loading, uplift, and loss of contact are queryable | UC-01, 02, 06 |
| FL-PHY-STR-008 | C1 | Settlement and differential movement | Soil response can distort, crack, tilt, jam, or unload connected construction and mechanisms | UC-01, 03, 06, 07 |
| FL-PHY-STR-009 | C1 | Sliding, overturning, buckling, and slope instability | The engine distinguishes relevant global failure modes and reports margins and initiating conditions | UC-01, 02, 06 |
| FL-PHY-STR-010 | D2 | Load redistribution after damage | Removing or weakening a support recomputes surviving paths and can cause arrested, local, or progressive failure | UC-04, 05, 08 |
| FL-PHY-STR-011 | D2 | Partial collapse | Structures may remain damaged and usable in part; failure is not restricted to intact or destroyed states | UC-05, 10 |
| FL-PHY-STR-012 | C1 | Weak-but-standing designs remain valid | A design above the viability boundary compiles with explicit low margins rather than being rejected for poor engineering | UC-01, 02, 13 |
| FL-PHY-STR-013 | C1 | Failed-build result | A design below baseline viability returns initiating failures, dependent failures, affected geometry, assumptions, and remedies as evidence | UC-01, 12 |
| FL-PHY-STR-014 | D2 | Shoring, reinforcement, and removal | Adding temporary support or removing load changes the real load path and can arrest or initiate failure | UC-10 |
| FL-PHY-STR-015 | C1 | Predictive failure envelopes | Non-mutating queries estimate governing modes and thresholds under declared candidate loads, with uncertainty and model limits | UC-02, 13 |

## 8. Materials, joints, damage, and fracture

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-MAT-001 | C1 | Physically meaningful material parameters | Density, stiffness, compression, tension, shear, friction, and failure parameters replace universal hit points | UC-01 to 06 |
| FL-PHY-MAT-002 | C1 | Layered and composite construction | Facings, rubble fill, mortar, timber reinforcement, armour, and coatings retain distinct geometry and behaviour | UC-01, 04, 05 |
| FL-PHY-MAT-003 | C1 | Material interfaces and joints | Bond, slip, separation, fasteners, keys, clamps, and connection quality can govern failure | UC-03 to 05 |
| FL-PHY-MAT-004 | D2 | Persistent damage history | Cracks, crushing, plastic deformation, loosened joints, fatigue-like accumulation, and prior impacts alter later response | UC-04, 05, 10 |
| FL-PHY-MAT-005 | D2 | Local fracture and separation | Fracture location and direction follow stress, flaws, geometry, interfaces, condition, and loading rather than a canned destruction pattern | UC-04, 05 |
| FL-PHY-MAT-006 | D2 | Rate and incidence sensitivity where material | Slow loading, repeated ramming, and high-energy impact can produce different outcomes when evidence supports the distinction | UC-04, 05 |
| FL-PHY-MAT-007 | D2 | Environmental material state | Moisture, saturation, temperature, burning, rot, corrosion, and weathering can change relevant properties persistently | UC-07, 08, 11 |
| FL-PHY-MAT-008 | F0 | Calibrated ranges and uncertainty | Material definitions can carry sourced ranges; sweeps expose outcome sensitivity rather than inventing false precision | UC-12, 13 |
| FL-PHY-MAT-009 | F0 | Model provenance | Every material outcome identifies the material record, model, parameter set, version, and state used | UC-12, 13 |

## 9. Rigid bodies and engineered mechanisms

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-MEC-001 | C1 | Static and dynamic rigid bodies | Components can participate in equilibrium, articulate, detach, fall, collide, settle, and later reactivate | UC-03, 05, 09 |
| FL-PHY-MEC-002 | C1 | General constrained assemblies | Hinges, pivots, sliders, guides, locks, latches, brakes, and limits expose forces and current state | UC-03, 09 |
| FL-PHY-MEC-003 | C1 | Ropes, cables, and chains | Tension-only members support slack, sag, routing, severance, overload, attachment failure, and entanglement where relevant | UC-03, 09 |
| FL-PHY-MEC-004 | C1 | Pulleys, gears, winches, and counterweights | Power and load transmission reflect geometry, ratio, efficiency, direction, available travel, and surviving connections | UC-03, 09 |
| FL-PHY-MEC-005 | D2 | Friction, backlash, slack, and compliance | Assemblies can slip, bounce, bind, or lose motion without bespoke jam flags | UC-03 |
| FL-PHY-MEC-006 | D2 | Breakable constraints | Overload, impact, cutting, burning, sabotage, or support movement can sever a connection and expose the resulting forces | UC-03, 04, 08 |
| FL-PHY-MEC-007 | D2 | Geometry-driven jamming and misalignment | Damaged guides, distorted frames, debris, skew, and insufficient clearance can physically prevent operation | UC-03, 05, 10 |
| FL-PHY-MEC-008 | C1 | Abstract operator interface | FortressLab can apply bounded force, torque, power, timing, coordination, and control inputs without simulating crew bodies | UC-03, 09, 14 |
| FL-PHY-MEC-009 | C1 | Operability queries | Required effort, travel, clearance, access, mechanical advantage, load, and failure margin can be queried before use | UC-02, 03, 14 |
| FL-PHY-MEC-010 | D2 | Structure-mechanism coupling | Foundation movement, frame distortion, fire, impact, and collapse alter mechanism alignment and load paths | UC-03, 05, 08 |

## 10. Projectiles, impacts, and mobile siege engines

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-SIE-001 | C1 | Queryable ballistic prediction | Candidate trajectories report time, incidence, obstruction, energy, uncertainty, and reachable target regions | UC-02, 04 |
| FL-PHY-SIE-002 | D2 | Dynamic external ballistics | Gravity, launch state, declared aerodynamic model, wind, and collision produce replayable trajectories | UC-04 |
| FL-PHY-SIE-003 | D2 | Incidence-aware impact | Normal and tangential components, target motion, local normal, materials, layers, and condition affect outcome | UC-04 |
| FL-PHY-SIE-004 | D2 | Penetration, deflection, ricochet, and arrest | Outcomes conserve or account for momentum and energy within the declared model and leave persistent target/projectile state | UC-04, 05 |
| FL-PHY-SIE-005 | D2 | Shock, spall, and secondary fragments | Local impacts can create internally hazardous fragments and trigger structural effects without requiring total penetration | UC-04, 05, 14 |
| FL-PHY-SIE-006 | D2 | Repeated and sustained contact loading | Rams, rollers, dragging, pushing, and levering accumulate physical state through repeated interactions | UC-04, 06, 09 |
| FL-PHY-SIE-007 | D2 | Physical siege-engine assemblies | Mobile engines use the same bodies, joints, materials, constraints, damage, and debris rules as fortification mechanisms | UC-09 |
| FL-PHY-SIE-008 | D2 | Ground mobility and route feasibility | Width, clearance, turning, slope, traction, rolling resistance, soil pressure, mud, obstacles, and bridging affect movement | UC-06, 09 |
| FL-PHY-SIE-009 | D2 | Stability and emplacement | Recoil, anchoring, outriggers, counterweights, slope, soft ground, and assembly state determine whether an engine can operate | UC-09 |
| FL-PHY-SIE-010 | D2 | Engine obstruction and wreckage | Disabled engines and detached components remain physical obstacles, cover, salvage, or clearance tasks | UC-05, 09, 10 |
| FL-PHY-SIE-011 | D2 | Abstract crew capacity | Crew availability changes achievable control force, rate, setup, and repair but never grants non-physical motion or output | UC-09, 14 |

## 11. Terrain, soil, excavation, and underground works

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-TER-001 | C1 | Spatial soil and rock properties | Bearing, shear, density, cohesion, friction, permeability, saturation, and excavation resistance vary by declared region and depth | UC-01, 02, 06 |
| FL-PHY-TER-002 | C1 | Persistent cut and fill | Excavation and placed material change terrain geometry, mass, slope, drainage, and later construction support | UC-06, 07 |
| FL-PHY-TER-003 | D2 | Tunnels, mines, and voids | Underground topology, lining, ventilation openings, support, spoil, and collapse can be represented locally in three dimensions | UC-06 |
| FL-PHY-TER-004 | C1 | Compaction and preparation | Grading, compaction, footings, drainage, and replacement material alter foundation response through declared operations | UC-01, 02, 06 |
| FL-PHY-TER-005 | D2 | Slope failure and mass movement | Cutting, loading, saturation, erosion, and excavation can trigger local slip or collapse with persistent deposits | UC-06, 07 |
| FL-PHY-TER-006 | D2 | Erosion and scour | Flow can remove and transport ground, expose foundations, breach earthworks, or deposit material elsewhere | UC-06, 07 |
| FL-PHY-TER-007 | D2 | Terrain-contact traction | Ground material, moisture, slope, normal load, and disturbance affect movement and bogging | UC-09 |
| FL-PHY-TER-008 | D2 | Earthwork interaction | Fascines, ramps, ditch fill, countermines, embankments, and spoil piles use ordinary material and topology rules | UC-05, 06, 09 |
| FL-PHY-TER-009 | F0 | Terrain-change notifications | Geometry, access, drainage, support, and query consumers receive stable, localised invalidation when terrain changes | UC-05 to 10 |

## 12. Debris and transformed geometry

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-DEB-001 | D2 | Adaptive fragmentation | Detailed fragments are created where consequences require them; distant or settled rubble may use validated aggregates | UC-04, 05, 11 |
| FL-PHY-DEB-002 | D2 | Conserved identity and mass accounting | Fragment and aggregate records account for source mass and retain source/component/event lineage | UC-05, 12 |
| FL-PHY-DEB-003 | D2 | Settling, piling, and bridging | Rubble forms persistent slopes, arches, piles, voids, and unstable surfaces according to geometry and material | UC-05, 06 |
| FL-PHY-DEB-004 | D2 | Secondary impacts and loading | Falling and settled material can strike components, load floors, crush stores, destabilise slopes, or trigger further failure | UC-05 |
| FL-PHY-DEB-005 | D2 | Gameplay-semantic physical queries | Consumers can derive blockage, clearance, cover, concealment, climbability, fill, support, and hazard from actual debris geometry | UC-05, 09, 10, 14 |
| FL-PHY-DEB-006 | D2 | Rehandling and demolition | Debris can be cleared, moved, compacted, reused, supported, or demolished through bounded physical work | UC-10, 14 |
| FL-PHY-DEB-007 | D2 | Sleep and reactivation | Settled debris becomes inexpensive but reactivates if support, loading, excavation, water, or impact changes materially | UC-10, 11 |
| FL-PHY-DEB-008 | D2 | Abstract occupancy hazard output | The engine reports occupied hazardous volumes, impulses, burial, heat, and safe-clearance state without resolving individual casualties | UC-05, 14 |

## 13. Water, substances, fire, atmosphere, and weather

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-HYD-001 | C1 | Watershed and drainage solve | Terrain, grades, ditches, walls, roads, drains, and culverts determine collection and flow paths | UC-02, 07 |
| FL-PHY-HYD-002 | D2 | Rivers and free-surface flow | Diversion, impoundment, overtopping, breach, channel flow, and inundation respond to current terrain and structures | UC-07 |
| FL-PHY-HYD-003 | D2 | Compartment filling and openings | Water enters, leaves, equalises, and loads rooms, tunnels, cisterns, gates, and breaches through actual connections | UC-07 |
| FL-PHY-HYD-004 | D2 | Hydrostatic and hydrodynamic loading | Water pressure, buoyancy, impact, uplift, and changing load couple back into structures and mechanisms | UC-03, 05, 07 |
| FL-PHY-HYD-005 | C1 | Saturation and seepage state | Rain, groundwater, drainage, leakage, and standing water alter soil and material state at an appropriate reduced fidelity | UC-01, 06, 07 |
| FL-PHY-HYD-006 | D2 | Erosion, scour, and sediment exchange | Moving water can remove, carry, and deposit terrain or debris with accounted mass | UC-06, 07 |
| FL-PHY-HYD-007 | D2 | Passive substance transport | Concentration, advection, mixing, dilution, settling, source lineage, and sampling support poison and contamination scenarios | UC-07, 12 |
| FL-PHY-HYD-008 | F0 | Water and transported-mass accounting | Sources, sinks, storage, losses, and residuals are visible and bounded by the selected model | UC-07, 12 |
| FL-PHY-FIR-001 | D2 | Physical ignition and fuel state | Heat source, material, moisture, exposure, and available fuel govern ignition; burned mass and condition persist | UC-08 |
| FL-PHY-FIR-002 | D2 | Fire spread and ventilation coupling | Geometry, contact, openings, airflow, fuel continuity, and suppression govern propagation | UC-08 |
| FL-PHY-FIR-003 | D2 | Thermal material degradation | Heating changes strength, stiffness, joints, ropes, mechanisms, stored materials, and later structural response | UC-03, 05, 08 |
| FL-PHY-FIR-004 | D2 | Smoke and hot-gas transport | Openings, buoyancy, wind, and ventilation produce queryable concentration, temperature, and visibility fields | UC-08, 14 |
| FL-PHY-FIR-005 | D2 | Suppression and interaction with water | Water availability, delivery, access, heat, fuel, and drainage govern cooling and extinguishment | UC-07, 08, 10 |
| FL-PHY-WEA-001 | D2 | Shared weather boundary conditions | Rain, wind, temperature, snow or ice where enabled, and daylight-linked heating feed relevant physical models consistently | UC-04, 07 to 11 |
| FL-PHY-WEA-002 | D2 | Ground-state evolution | Weather changes mud, traction, saturation, drainage, erosion, and mobility rather than applying a universal movement modifier | UC-06, 07, 09 |
| FL-PHY-WEA-003 | A3 | Long-term degradation | Repeated wetting, drying, freezing, heating, rot, and corrosion may advance material state under accelerated siege time | UC-11, 13 |

## 14. Coupling and hybrid fidelity

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-CPL-001 | F0 | One authoritative physical state | Structures, mechanisms, projectiles, debris, terrain, fluids, and fire read and alter compatible shared state | All |
| FL-PHY-CPL-002 | F0 | Deterministic coupling order | Cross-system updates are explicitly scheduled, versioned, and insensitive to incidental thread ordering | UC-05, 07, 08, 12 |
| FL-PHY-CPL-003 | D2 | Impact-to-collapse chain | Projectile contact can damage material, change support, redistribute load, create debris, and alter later access without scenario scripting | UC-04, 05 |
| FL-PHY-CPL-004 | D2 | Water-ground-structure chain | Water changes saturation and erosion; ground changes support; structures settle, crack, jam, or collapse | UC-03, 05 to 07 |
| FL-PHY-CPL-005 | D2 | Fire-material-structure chain | Fire and heat change material and joint state, which changes mechanisms and structural load paths | UC-03, 05, 08 |
| FL-PHY-CPL-006 | D2 | Terrain-access-hydrology chain | Excavation, fill, debris, and collapse simultaneously change routes, flow, support, and later engineering possibilities | UC-05 to 10 |
| FL-PHY-CPL-007 | F0 | Reusable interactions, not tactic buttons | Poisoning, flooding, undermining, jamming, and ramp creation emerge from ordinary primitives and shared state | UC-03 to 10 |
| FL-PHY-HYB-001 | D2 | Deterministic region activation | Detailed simulation activates from declared physical criteria, not camera position or dramatic scripting | UC-04, 05, 07 to 11 |
| FL-PHY-HYB-002 | D2 | Reduced stable-state models | Quiescent structures, mechanisms, fluids, and debris can sleep or reduce without losing load, damage, connectivity, or hazard state | UC-11 |
| FL-PHY-HYB-003 | D2 | Conservative fidelity transitions | Activation and reduction preserve accounted mass, momentum, load, heat, fluid, topology, identity, and damage as applicable | UC-05, 07, 08, 11 |
| FL-PHY-HYB-004 | D2 | Local refinement | Critical impacts, fracture zones, fire fronts, fluid fronts, unstable supports, and settling debris can refine independently | UC-04, 05, 07, 08 |
| FL-PHY-HYB-005 | D2 | Multirate stepping and quiet-time advance | Fast impacts and slow settlement, fire, seepage, weather, and siege works coexist without globally paying the smallest time step | UC-11 |
| FL-PHY-HYB-006 | C1 | Fidelity and resolution convergence | Refinement studies expose whether a finding is stable; material conclusion changes are warnings, not silently accepted output | UC-12, 13 |
| FL-PHY-HYB-007 | D2 | Activity-scaled cost | A stable full fortress adds little dynamic work; cost is driven primarily by active physical regions and requested evidence | UC-11 |

## 15. Evidence, queries, replay, and integration

| ID | Tier | Desired property | FortressLab acceptance signal | Uses |
|---|---|---|---|---|
| FL-PHY-EVD-001 | F0 | Typed physical event journal | Creation, motion, contact, load change, damage, fracture, flow, heat, topology change, sleep, and failure events have stable schemas | UC-12 |
| FL-PHY-EVD-002 | F0 | Causal provenance | Each consequential event references causes, inputs, affected IDs, model/version, time, location, and prior event dependencies | UC-02, 12 |
| FL-PHY-EVD-003 | F0 | Geometry-referenced evidence | Findings identify points, surfaces, volumes, paths, components, and time intervals that can be highlighted on the player's model | UC-02, 12 |
| FL-PHY-EVD-004 | F0 | Measurement/model distinction | Outputs identify direct state measurements, modelled consequences, assumptions, uncertainty, and numerical warnings separately | UC-02, 12, 13 |
| FL-PHY-EVD-005 | C1 | Non-mutating diagnostic queries | FortressLab can inspect load paths, margins, contacts, capacities, trajectories, flows, temperatures, damage, and likely failure without advancing state | UC-02, 13 |
| FL-PHY-EVD-006 | C1 | Candidate-action queries | The engine can test bounded proposed loads or physical actions on a fork and return feasibility and consequences without privileged shortcuts | UC-03, 09, 10, 13 |
| FL-PHY-EVD-007 | F0 | Explicit uncertainty and sensitivity | Parameter ranges and solver sensitivity propagate into structured intervals or scenario ensembles, not decorative confidence | UC-12, 13 |
| FL-PHY-EVD-008 | F0 | Save and exact-resume contract | A saved authoritative checkpoint resumes with matching future journal under the same declared runtime contract | UC-11, 12 |
| FL-PHY-EVD-009 | F0 | Replay independent of re-simulation | Stored checkpoints and events can reproduce the forensic presentation even when the original solver is unavailable | UC-12 |
| FL-PHY-EVD-010 | F0 | Version-aware comparison | Runs with different engine, material, schema, or solver versions are labelled non-identical and remain semantically diffable | UC-12, 13 |
| FL-PHY-EVD-011 | F0 | Local invalidation and subscriptions | FortressLab can update graphs, routes, overlays, perception, and reports from affected regions instead of rebuilding the world blindly | UC-02, 05 to 12 |
| FL-PHY-EVD-012 | F0 | Stable export boundary | Physical snapshots, queries, and events use documented versioned data contracts that do not expose private solver internals | All |
| FL-PHY-EVD-013 | D2 | Presentation event hooks | Impacts, groans, breaks, flow, fire, settling, and mechanism motion emit factual magnitude/location events for sound and visuals | UC-03 to 12 |

## 16. Validation and quality targets

| ID | Tier | Desired property | FortressLab acceptance signal |
|---|---|---|---|
| FL-PHY-VAL-001 | F0 | Analytical reference tests | Elementary motion, equilibrium, contact, constraints, beams, hydrostatics, flow, and heat cases agree with independent oracles within declared tolerance |
| FL-PHY-VAL-002 | F0 | Property and metamorphic tests | Translation, rotation, object ordering, equivalent subdivision, save/resume, and irrelevant-scene additions preserve the appropriate results |
| FL-PHY-VAL-003 | F0 | Conservation and residual budgets | Each subsystem exposes applicable mass, momentum, energy, constraint, flow, and coupling accounting, including intentional dissipation |
| FL-PHY-VAL-004 | F0 | Adversarial geometry tests | Tiny gaps, thin parts, near contacts, high aspect ratios, sharp slopes, deep stacks, large mass ratios, and fast projectiles fail explicitly or resolve robustly |
| FL-PHY-VAL-005 | C1 | Structural benchmark validation | Walls, arches, frames, foundations, spans, settlement, and overturning are tested against analytical, experimental, or published engineering references |
| FL-PHY-VAL-006 | D2 | Damage and collapse validation | Local fracture, load redistribution, partial collapse, debris, and impact are bounded against suitable experiments or higher-fidelity reference models |
| FL-PHY-VAL-007 | D2 | Fluid, fire, and terrain validation | Flow, filling, drainage, erosion, heat, smoke, and spread models publish their validity ranges and benchmark evidence |
| FL-PHY-VAL-008 | F0 | Determinism regression | Scheduled tests compare journals and checkpoints across supported execution modes and detect unintended ordering or platform drift |
| FL-PHY-VAL-009 | C1 | Resolution-convergence testing | Selected FortressLab findings are rerun at finer geometry, field, structural, debris, fluid, and time resolutions until stability or instability is demonstrated |
| FL-PHY-VAL-010 | F0 | Golden causal scenarios | Reviewed fixtures preserve structured events and evidence, not merely final positions or scores |
| FL-PHY-VAL-011 | F0 | Fail-closed authoritative output | Non-convergence, invalid parameters, unsupported scale, and exhausted compute budgets cannot produce an apparently valid physical conclusion |
| FL-PHY-VAL-012 | F0 | Performance regression evidence | Benchmark runs record runtime, memory, active-set size, solver work, event volume, and accuracy so optimisation cannot silently change causality |

## 17. Minimum FortressLab acceptance scenarios

These scenarios are the integration proof set. Exact numerical tolerances belong
to the external engine's validation plan; each scenario must nevertheless have
an independent expected relationship, failure mode, or conservation check.

1. **Stable wall on prepared ground:** baseline construction succeeds and load
   reaches the expected foundation region.
2. **Unviable foundation:** an otherwise valid wall produces a failed-build
   result with bearing or settlement evidence rather than a generic error.
3. **Gate opening and arch:** load bypasses an opening through the intended
   supports; removing one support changes the surviving load path.
4. **Drawbridge chain severance:** identical geometry can drop, twist, jam, or
   remain partly supported according to which lifting members survive.
5. **Bridge overload by a siege engine:** the bridge may stand unloaded but
   fails or refuses the crossing under the engine's actual load.
6. **Angled projectile against layered masonry:** incidence and layers change
   penetration, deflection, damage location, and remaining structural margin.
7. **Partial tower collapse:** local damage redistributes load, produces
   persistent debris, and leaves a mixed usable and unusable structure.
8. **Undermined curtain wall:** excavation removes support and creates a causal
   ground-to-foundation-to-structure failure chain.
9. **Debris fills a ditch:** the same collapse creates obstruction in one
   direction, attacker cover, and a potentially climbable or crossable route.
10. **River diversion:** changed earthworks redirect flow, saturate or erode
    ground, flood connected spaces, and load foundations without a scripted
    flood-castle action.
11. **Timber floor fire:** ventilation and fuel control spread; heating weakens
    support and can initiate a later structural failure.
12. **Mobile siege engine on changing ground:** slope, clearance, rain, soil
    pressure, mud, emplacement, and damage alter whether the engine can move and
    operate.
13. **Repair and shoring:** a physically accessible temporary support changes
    the real load path; an inaccessible or under-capacity proposal fails with
    evidence.
14. **Quiet siege with local activation:** long inactive periods advance
    cheaply, a local event activates detail, and the transition preserves the
    relevant state.
15. **Save, replay, and fork:** a resumed run matches its source; a one-input
    fork is traceable; replay remains viewable from stored state and events.
16. **Resolution and ordering challenge:** refinement and shuffled independent
    object insertion do not change a material conclusion without an explicit
    instability warning.

## 18. Highest-priority blockers

The following targets are the minimum architectural blockers for FortressLab.
Deferring them would force later systems to bypass or replace the engine:

1. Authoritative headless state with stable IDs and versioned serialization.
2. Reproducible execution, snapshots, forks, and typed causal event journals.
3. Exact authored-geometry preservation and traceable derived representations.
4. Quasi-static construction feasibility and inspectable structural load paths.
5. Persistent material damage, topology change, and partial failure.
6. General mechanisms with breakable, load-bearing connections.
7. Terrain, foundation, and structure coupling.
8. Persistent debris that remains queryable as geometry.
9. Hybrid-fidelity transitions that conserve gameplay-relevant state.
10. Non-mutating evidence queries and explicit numerical failure.

Projectiles, mobile siege engines, fluids, fire, smoke, and advanced terrain
works then extend those foundations rather than creating parallel rules.

## 19. Explicit exclusions from the engine contract

- The engine does not choose attacker or defender strategy.
- It does not model individual soldiers, animals, civilians, or crews.
- It does not decide casualties, morale, surrender, doctrine, or historical
  plausibility.
- It does not produce a universal castle score.
- It does not grant difficulty-dependent physics or hidden information.
- It does not require a global per-brick, per-particle, or maximum-resolution
  simulation.
- It does not treat a single generic health value as a substitute for geometry,
  material state, load paths, mechanisms, or failure.
- It does not need universal chemistry. FortressLab requires transport and
  concentration of declared passive substances; health effects remain outside.
- It does not own rendering, sound, animation, or the war-room interface.
- It does not allow runtime AI or an LLM to manufacture authoritative outcomes.
- This document sets no frame-rate, entity-count, map-size, or hardware budget.
  Those numerical budgets belong to the broader engine plan and must be tested
  against the acceptance scenarios above.

## 20. Completion condition

The FortressLab physics integration is credible when:

1. Every enabled physical state change is produced by a reusable physical
   primitive or interaction.
2. Every important result can be traced through typed evidence to geometry,
   state, models, assumptions, and causes.
3. Impossible initial designs fail with explanations, while physically viable
   but poor designs remain available for adversarial evaluation.
4. Damage changes the future world—structure, mechanisms, access, terrain,
   water, fire, debris, and possible actions—rather than merely reducing a
   durability number.
5. Static analysis, live simulation, save/resume, replay, and comparative
   experiments share compatible authoritative state and identifiers.
6. Fidelity, time compression, parallelism, and optimisation cannot silently
   change a material conclusion.

That is the consumer contract FortressLab contributes to the broader engine
plan. Capabilities needed only by other games may extend the engine, but they
must not weaken these guarantees.
