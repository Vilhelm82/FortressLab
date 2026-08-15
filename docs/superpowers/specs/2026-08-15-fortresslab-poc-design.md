# FortressLab POC Design

**Date:** 2026-08-15
**Status:** Approved design, pending implementation plan
**Project root:** `/mnt/fast/Work/Creative Projects/FortressLab`

## 1. Purpose

FortressLab is a headless Python research environment for evaluating defensive fortifications from terrain, geometry, accessibility, visibility, and abstract attacker capabilities. Its first proof of concept (POC) must determine whether a spatially grounded, explainable evaluator can identify meaningful strengths and weaknesses without scenario-specific scripts, animated armies, or a game engine.

The evaluator is the product under test. The construction interface, historical profiles, animated combat, and adaptive commanders will be later consumers of its evidence. The POC therefore prioritizes causal traceability, experimental control, and extensibility over presentation.

The guiding principle is **bounded causal fidelity**:

> Represent variables that materially affect fortification warfare, simplify them transparently, and ensure conclusions emerge from their interaction rather than predetermined outcomes.

The project does not claim to predict historical outcomes precisely. It distinguishes exact measurements inside the model from approximate model outputs and historically inferred inputs.

## 2. Product Identity and Long-Term Direction

The eventual game casts the player as the architect rather than a battlefield commander. The player selects terrain and designs fortifications. Autonomous attacking and defending commanders inherit the resulting structure and decide how to use or defeat it. The architecture communicates strategy indirectly through access, concealment, fields of fire, fallback routes, compartments, traps, and liabilities.

The long-term simulation will separate:

1. Authoritative physical state.
2. Direction-dependent perception.
3. Each commander's uncertain belief state.
4. Doctrine- and character-conditioned planning.
5. Formation-level execution.
6. Observation, learning, and replanning.

Historical and counterfactual scenarios will be compositions of terrain, fortification, force, equipment, doctrine, command character, knowledge, logistics, objectives, weather, and victory conditions. Equipment, knowledge, doctrine, and personality must remain independent so that, for example, modern doctrine can be tested with medieval equipment without silently granting modern weapons.

These are future requirements that shape interfaces only. They are not POC implementation scope.

## 3. POC Scope

### 3.1 Included

The POC includes:

- Synthetic terrain generation and structured scenario loading.
- Exact parametric geometry for walls, towers, gates, ditches, bridges, and protected objectives.
- Dense terrain fields, sparse local 3D spatial fields, and semantic graphs.
- Point, ray/chain, corridor, area, visibility, and connectivity queries.
- Site, approach, visibility, defensive-fire, obstacle, breach, access, compartment, capture, lodgement, and deception analyses.
- A generic attacker capability profile.
- Mechanical generation and ranking of abstract courses of action (COAs).
- Separate authoritative and perceived vulnerability assessments.
- Evidence-backed findings with units, confidence, assumptions, provenance, and geometry references.
- Deterministic single runs and seeded uncertainty experiments.
- Controlled scenario mutations, parameter sweeps, and resolution-convergence experiments.
- Machine-readable JSON results and interactive HTML analysis reports.
- Unit, integration, property-based, metamorphic, golden-scenario, and adversarial-fuzz tests.

### 3.2 Excluded

The POC excludes:

- Individual soldiers or animated formations.
- Combat resolution, casualties, fatigue, morale, or medical modelling.
- Adaptive attacker or defender commanders.
- Historical battle and commander profiles.
- Detailed projectile penetration, fracture, collapse, or debris simulation.
- Real-time execution.
- Game-engine or Unreal Engine integration.
- Production UI, art, audio, networking, or distribution.
- LLMs as runtime decision makers.

Excluded systems may not be approximated through hidden constants presented as implemented functionality.

## 4. Success Criteria

The POC succeeds when it can:

1. Identify deliberately constructed weaknesses without scenario-specific rules.
2. Explain every important finding through measurements and declared assumptions.
3. Rank controlled design variants in the expected direction.
4. Preserve catastrophic weaknesses instead of hiding them inside averages.
5. Remain stable under irrelevant transformations and change sensibly under meaningful ones.
6. Identify which uncertain inputs dominate unstable conclusions.
7. Add terrain, fortifications, materials, and attacker capabilities through schemas and registries rather than evaluator rewrites.
8. Export structured evidence suitable for future commander planners.
9. Run automated experiment batches without a graphical engine.
10. Report insufficient information or numerical instability rather than invent precision.
11. Produce equivalent corresponding results when a scenario is translated or rotated without changing its physical relationships.
12. Demonstrate resolution convergence or explicitly identify conclusions that do not converge.

A visually attractive report is useful but cannot compensate for a failed analytical criterion.

## 5. Epistemic Contract

Every value exposed by the evaluator is classified as one of:

- **Measured:** Deterministic within the declared geometry and algorithms, such as elevation, route length, incidence angle, visible area, or wall thickness.
- **Modelled:** Produced by a documented abstraction, such as approach cost, potential exposure, approximate obstacle effort, or lodgement utility.
- **Inferred:** Supplied with uncertainty because it represents incomplete knowledge, such as perceived wall thickness or reconnaissance confidence.

Every composite finding retains the classifications of its contributors. Confidence is not a cosmetic score; it identifies epistemic uncertainty, sensitivity, missing information, and numerical instability.

The POC never reports precise casualty counts, historical probabilities, or physical breach times because those models are outside scope.

## 6. Architectural Principles

### 6.1 Exact geometry is authoritative

Player-authored or scenario-authored parametric geometry remains the source of truth. Spatial grids are derived query accelerators and analytical fields. Curved, diagonal, and narrow structures must not acquire different physical meaning merely because raster resolution changes.

### 6.2 Direction is part of every relevant query

Properties including presentation angle, apparent thickness, exposure, defensive orientation, and reverse defensive value depend on query origin and direction. They are computed when queried rather than stored as universal object scores.

### 6.3 Evidence precedes scores

Independent evaluators return evidence. Composite scores are reversible views over that evidence. A user must be able to trace a fortress-level conclusion down to geometry, query results, assumptions, and formulas.

### 6.4 No scenario-specific logic

Scenarios contain state and capability inputs only. They may include expected benchmark relationships in test fixtures, but production evaluator code may not inspect scenario names, expected outcomes, or fixture identifiers.

### 6.5 Deterministic core, explicit uncertainty

Identical deterministic inputs produce identical outputs. Stochastic experiments require explicit seeds. Scenario snapshots, model versions, dependency versions, and hashes are recorded for reproducibility.

### 6.6 Isolation

Geometry, spatial indexing, graph construction, queries, perception, evaluation, COA generation, scoring, experiments, and reporting communicate through narrow typed interfaces. External libraries remain behind project-owned adapters.

## 7. System Layers

### 7.1 Scenario definition

A versioned schema defines:

- Coordinate reference and metre-based units.
- Terrain extent, heightfield, soil, water, and analysis resolution.
- Parametric fortification objects.
- Protected objectives and scenario boundaries.
- Abstract defender positions and weapon envelopes.
- Generic attacker movement and engineering capabilities.
- Observer locations and reconnaissance quality.
- Evaluation settings, uncertainty distributions, and random seed.

Canonical persisted input is JSON. Tests and experiments may construct equivalent scenarios through Python builders. Scenario snapshots are immutable after validation.

### 7.2 Authoritative geometry

The initial primitives are:

- `TerrainSurface`: continuous interpolation over a heightfield plus water and soil attributes.
- `Wall`: polyline center path, base relationship to terrain, height, thickness, material, condition, and wall-walk properties.
- `Tower`: footprint, height, material, access points, fighting-position capacity, and observation/firing surfaces.
- `Gate`: wall-hosted opening, width, traversal state, abstract resistance, and successive-barrier relationships.
- `Ditch`: swept path with width, depth, side profile, water state, and crossing constraints.
- `Bridge`: span geometry, width, access relationship, traversability, and abstract denial state.
- `Objective`: target volume or point whose reachability terminates an attack course.
- `DefensivePosition`: potential—not guaranteed—observation or firing station with abstract weapon envelope.

All objects have stable identifiers and preserve their original parameters.

### 7.3 Derived terrain field

Dense two-dimensional arrays store sampled:

- Elevation.
- Gradient and slope.
- Surface normal.
- Water classification.
- Soil or foundation class.
- Base traversability by capability class.

Resolution is configurable and recorded. The terrain field is never used to redefine exact structural geometry.

### 7.4 Sparse spatial field

Sparse fixed-size chunks are allocated only near structures, obstacles, relevant air volumes, and explicit query regions. Cells may reference:

- Occupancy class.
- Source object identifier.
- Material identifier.
- Surface normal or boundary metadata.
- Local degradation state.
- Traversability modifier.
- Cover and concealment contribution.
- Water, debris, or reserved future dynamic state.

The POC uses sparse chunk allocation rather than a globally dense three-dimensional volume. Chunk size and cell resolution are configuration values. Resolution-convergence tests determine whether derived conclusions are stable.

### 7.5 Semantic graphs

Separate graphs represent different semantics:

- **Structural graph:** support and dependency relationships.
- **Defender access graph:** internal circulation, doors, stairs, wall walks, towers, and fallback connectivity.
- **Attacker access graph:** approaches, crossings, obstacles, breach candidates, captured compartments, and objectives.
- **Compartment graph:** defensible regions, boundaries, transitions, isolation, and ownership state.

Graph nodes and edges reference exact geometry and relevant spatial regions. Directional edges are used where an element is substantially easier to traverse, defend, or reverse from one direction.

### 7.6 Spatial-query engine

The query engine provides:

- **Point query:** local terrain, structure, material, state, and graph references.
- **Directional chain query:** ordered intersections and interval properties between an origin and destination.
- **Corridor query:** swept-width path suitable for formations or siege equipment.
- **Area query:** aggregate properties over a surface or volume.
- **Visibility query:** line of sight, occlusion, visible fraction, and uncertainty inputs.
- **Connectivity query:** graph reachability under declared ownership and obstacle states.

Chain results remain ordered evidence, not a pre-aggregated scalar. Consumers decide how terrain, concealment, obstacles, and exposure affect their domain.

For a surface normal `n` and incoming unit direction `d`, incidence begins with:

`cos(theta) = abs(dot(n, -d))`

A simple geometric effective-depth view may use:

`effective_depth = thickness / max(cos(theta), epsilon)`

This is a geometric measurement only. It is not treated as a complete masonry-impact model.

### 7.7 Perception layer

Authoritative query results pass through observation rules to produce reports containing:

- Observed or estimated property.
- Estimated interval or distribution.
- Confidence.
- Detection source and vantage.
- Occlusion and concealment effects.
- Unknown or hidden attributes.

The perceived fortress is assembled exclusively from these reports. Future commanders consume perceived state; they do not query authoritative geometry directly.

The POC perception model is intentionally simple but must preserve this interface and prevent hidden-state leakage.

### 7.8 Independent analytical evaluators

Each evaluator consumes typed query and graph interfaces and emits evidence:

- Site quality.
- Observation and visibility.
- Approach accessibility.
- Potential defensive-fire coverage and dead ground.
- Obstacle and crossing effort.
- Gate and breach attractiveness.
- Internal circulation and reinforcement access.
- Compartment resilience.
- Capture liability and reverse defensive value.
- Lodgement viability and attacker resupply access.
- Actual-versus-perceived vulnerability differential.

Potential fire coverage describes what a competent defending force could use. It does not assert that future defender AI will occupy or exploit every position.

### 7.9 Course-of-action generator

The POC COA generator is a mechanical adversarial enumerator, not a commander AI. A COA contains:

1. Entry boundary or attacker origin.
2. Assembly region.
3. Approach corridor.
4. Ordered obstacle interactions.
5. Selected gate, crossing, or breach objective.
6. Abstract entry operation.
7. Resulting captured region or lodgement.
8. Subsequent path through compartments.
9. Protected objective.

Each COA carries a vector of costs and benefits:

- Distance and time proxy.
- Traversal difficulty.
- Potential defensive exposure.
- Engineering effort.
- Equipment requirements.
- Congestion.
- Uncertainty.
- Supply difficulty.
- Withdrawal difficulty.
- Capture utility.
- Positional value toward subsequent objectives.

A generic configurable utility function ranks COAs for the POC. The full vector and ranking contribution remain visible so future commander profiles can apply different preferences without recomputing geometry.

### 7.10 Evidence graph

Every evidence item includes:

- Stable identifier.
- Definition and evaluator owner.
- Value, unit, and classification.
- Confidence and sensitivity metadata.
- Assumptions and model version.
- Parent evidence identifiers.
- Geometry and graph references.
- Human-readable explanation.

Findings and summary ratings reference evidence identifiers. Explanations are generated from structured templates and data, not opaque prose generation.

### 7.11 Experiment harness

The harness supports:

- Deterministic scenario evaluation.
- Controlled single-variable mutations.
- Parameter grids and sampled sweeps.
- Seeded uncertainty ensembles.
- Resolution-convergence experiments.
- Comparative reports.
- Invariant and metamorphic assertions.
- Adversarial geometry generation within declared validity constraints.

Experiment definitions are versioned, machine-readable inputs. A run manifest records every expanded case.

### 7.12 Reporting

A run produces:

- Validated scenario snapshot.
- Manifest with hashes, versions, configuration, and seed.
- Machine-readable result JSON.
- Ranked COAs with cost-vector breakdowns.
- Findings and evidence graph.
- Warnings, unsupported assumptions, and stability flags.
- Interactive HTML terrain report with contours, fortifications, routes, visibility, exposure, vulnerability, and perceived-versus-actual overlays.

Reports must support comparison between a baseline and one or more controlled variants.

## 8. Evaluation Semantics

### 8.1 Multi-objective routes

Ordinary shortest-path routing is insufficient. Candidate paths are generated and retained across multiple objectives, including distance, gradient, traversability, concealment, defensive exposure, formation width, engineering feasibility, and supply connectivity.

Dominated paths may be discarded only when they are no better in every tracked dimension. Weighting occurs during generic COA ranking, not during physical query generation.

### 8.2 Defensive exposure

Potential exposure along a corridor accounts for:

- Visibility from defensive positions.
- Abstract weapon range and firing arc.
- Occlusion by terrain and structures.
- Elevation relationship.
- Position capacity.
- Overlapping coverage.
- Flanking or enfilading orientation.
- Dead ground.
- Defender access to the position.

The POC reports exposure proxies and coverage duration or distance. It does not convert them into casualties.

### 8.3 Obstacles and breach attractiveness

Obstacle analysis combines:

- Exact geometry.
- Attacker capability compatibility.
- Required abstract effort.
- Exposure while interacting.
- Adjacent defender coverage.
- Opening or crossing created.
- Resulting graph connectivity.
- Value and liability of the captured position.

Resistance values are configurable model parameters. They are not described as validated historical breach times.

### 8.4 Capture and lodgement

Fortifications are ownership-neutral physical opportunities. When a compartment or outer work is captured, the evaluator recomputes its value from the attacker direction.

Lodgement evaluation includes:

- Protected internal capacity.
- Attacker access and resupply path.
- Barricade or reversal opportunities.
- Observation and firing value.
- Proximity to the next defensive boundary.
- Defender counterattack routes and exposure.
- Isolation or denial possibilities.
- Cascading access consequences.

Net architectural value is not simply value while defended; capture liability is reported separately and contributes to robust assessment.

### 8.5 Deception differential

Candidate selection uses perceived evidence while authoritative assessment uses actual evidence. For a COA:

`deception_differential = actual_cost - perceived_cost`

A positive result indicates an apparently cheaper approach whose hidden properties increase actual cost. A negative result indicates an opportunity whose true weakness is underestimated by the perceived model or designer-facing summary.

The POC does not simulate commitment or trap execution. It identifies information differentials that future commander and combat systems can exploit.

### 8.6 Fortress-level findings

Primary outputs are:

- Cheapest credible COA.
- Most consequential plausible COA.
- Catastrophic single-point weaknesses.
- Robust defensive properties across COAs.
- Capture and lodgement liabilities.
- Sensitivity to attacker capabilities and model assumptions.
- Numerical and resolution stability.
- Actual-versus-perceived differences.

Any overall score is a convenience view and must link to its complete evidence and COA basis.

## 9. Initial Benchmark Family

The first synthetic benchmark uses an asymmetric terrain containing:

- A hill with multiple gradients.
- A stream and constrained crossing.
- Open and partially concealed approach sectors.
- A simple enclosure with curtain walls.
- Four towers.
- One gate.
- A ditch and bridge.
- An internal protected objective.
- Abstract defensive positions.
- Generic attacker movement and engineering capabilities.

Controlled variants include:

1. Hilltop versus low-ground placement.
2. Covered versus uncovered gate.
3. Flanking towers present versus absent.
4. Uniform wall versus one weak section.
5. Ditch width/depth and bridge-placement changes.
6. Visible versus concealed internal defence.
7. Isolated capturable outer work.
8. Good versus obstructed internal circulation.
9. Single enclosure versus layered compartments.
10. Irrelevant distant-terrain modification.
11. Rotated and translated equivalents.
12. Multiple analysis resolutions.

Expected relationships belong to test specifications, not scenario production data.

## 10. Test Strategy

### 10.1 Unit tests

Unit tests cover interpolation, slopes, normals, intersections, incidence, swept corridors, visibility, sparse chunks, graph construction, reachability, evidence provenance, and schema validation.

### 10.2 Property-based tests

Generated valid inputs test invariants including:

- Validated scenario and result models survive serialize/deserialize round trips without semantic change.
- Canonical serialization and normalization are idempotent.
- Increasing abstract wall resistance cannot reduce its local breach effort when all else is fixed.
- Increasing ditch width or depth cannot reduce an otherwise identical crossing effort.
- Removing a traversable edge cannot make the same graph route shorter.
- Adding an occluder cannot increase direct geometric visibility through that occluder.
- Ordered chain intersections remain ordered by distance.
- Query results reference valid source objects.
- Every published finding has a complete, acyclic provenance path to source measurements or declared model inputs.
- Deterministic evaluations repeat exactly for the same scenario and seed.

These properties apply to isolated subsystems. Fortress-level results may legitimately be non-monotonic because changing one feature can redirect an attacker toward a more damaging alternative.

Property generators construct valid terrain, geometry, graphs, and scenarios by enforcing domain constraints during generation. Invalid-input strategies begin with valid cases and apply one identifiable violating mutation. Both families explicitly include minimum dimensions, near-tolerance geometry, disconnected networks, sharp slopes, empty optional collections, and maximal supported extents. Tests avoid excessive input filtering so minimized failures remain meaningful scenarios.

Properties are stated independently of implementation algorithms. A test may use an intentionally simpler reference oracle for small inputs, but it may not merely reproduce the production calculation.

### 10.3 Metamorphic tests

- Translation preserves corresponding measurements.
- Rotation preserves corresponding measurements after direction transformation.
- Identifier renaming does not change results.
- Adding irrelevant distant empty terrain does not alter local findings.
- Equivalent scenario serialization order does not change results.

### 10.4 Golden micro-scenarios

Small fixtures isolate gate flanking, dead ground, weak curtains, protected approaches, isolated towers, compartment failure, and captured outer works. Golden results contain structured evidence, not only final scores.

### 10.5 Controlled mutations and sensitivity

Each benchmark mutation changes one declared input. Comparative reports must identify both the changed conclusion and the causal evidence responsible. Sweeps identify thresholds, unstable rankings, and dominant assumptions.

### 10.6 Adversarial fuzzing

Valid and deliberately invalid geometry generators test tiny gaps, nearly coincident surfaces, sharp turns, extreme slopes, zero-area features, overlapping structures, unsupported spans, and disconnected access networks. Invalid inputs must fail during validation with actionable paths and messages.

### 10.7 Later subagent red/blue testing

After deterministic validation, isolated development-time agents may act as:

- Blue design team.
- Red attack-analysis team with perception-limited inputs.
- White-cell deterministic evaluator.
- Audit role for information leakage and model exploits.

Agents generate hypotheses and scenarios; they never determine authoritative physical outcomes. Discovered weaknesses become permanent reproducible fixtures. This phase is explicitly outside the initial implementation milestone.

## 11. Resolution and Numerical Stability

No spatial resolution is declared universally correct. Each run records terrain and sparse-field resolutions. Convergence experiments repeat evaluations at multiple resolutions and compare:

- Route topology.
- Visibility and exposure measures.
- Ranked breach candidates.
- COA ranking.
- Fortress-level findings.

Material changes trigger a numerical-instability warning. Exact geometry remains available for resolving critical intersections where raster sampling is insufficient.

Tolerance values are named configuration parameters with units and documented purpose. They may not be scattered as unexplained literals.

## 12. Error Handling

Validation rejects or explicitly reports:

- Invalid or self-intersecting geometry.
- Disconnected wall paths where continuity is required.
- Unsupported or terrain-incompatible structures.
- Gates that do not intersect their host walls.
- Bridges connecting no traversable regions.
- Contradictory material definitions.
- Invalid dimensions or units.
- Impossible capability combinations.
- Missing or unreachable protected objectives.
- Unknown schema or model versions.

Evaluation conditions include:

- No credible attack route.
- Insufficient observation for perceived assessment.
- Unsupported interaction method.
- Resolution instability.
- Unbounded or invalid cost component.

These remain typed findings or explicit failures. They are never hidden behind arbitrary extreme scores.

## 13. Technology and Repository

### 13.1 Runtime

The reference implementation uses a currently supported Python 3 release selected during implementation after inspecting the host environment. The project is packaged through `pyproject.toml` and uses a locked dependency environment.

Expected dependency categories are:

- Numerical arrays and scientific operations.
- Exact or robust 2D geometry.
- 3D mesh/intersection utilities where justified.
- Graph algorithms.
- Typed schema validation.
- Interactive HTML plotting.
- Unit and property-based testing.

Specific libraries are selected in the implementation plan after availability and licence verification. Project-owned interfaces isolate them.

### 13.2 Repository layout

```text
FortressLab/
├── pyproject.toml
├── README.md
├── docs/
│   ├── superpowers/specs/
│   ├── model/
│   └── experiments/
├── scenarios/
│   ├── benchmarks/
│   └── examples/
├── src/fortresslab/
│   ├── schema/
│   ├── geometry/
│   ├── spatial/
│   ├── graphs/
│   ├── queries/
│   ├── perception/
│   ├── evaluators/
│   ├── courses/
│   ├── evidence/
│   ├── experiments/
│   ├── reporting/
│   └── cli.py
├── tests/
│   ├── unit/
│   ├── properties/
│   ├── scenarios/
│   └── integration/
└── generated/
    ├── runs/
    └── reports/
```

Generated outputs are ignored by version control unless explicitly promoted as benchmark evidence.

### 13.3 Command-line interface

The planned public commands are:

```text
fortresslab validate scenario.json
fortresslab evaluate scenario.json
fortresslab explain <run-id> <finding-id>
fortresslab compare baseline.json variant.json
fortresslab sweep experiment.json
fortresslab render <run-id>
```

The implementation plan may stage these commands incrementally, but their inputs and outputs follow shared schemas rather than ad hoc command-specific structures.

## 14. Reproducibility and Run Artifacts

Each run stores:

- Run identifier.
- Scenario snapshot and hash.
- Evaluator configuration and hash.
- Model and package versions.
- Dependency versions.
- Random seed.
- Start and completion timestamps.
- Findings, evidence, COAs, and warnings.
- Generated report locations.

Golden fixtures are updated only through an explicit review procedure that displays semantic differences. A changed result is never accepted solely because new output was generated.

## 15. Development Sequence

Implementation is staged so each layer proves a usable capability:

1. Repository, package, strict schemas, units, and reproducible run manifests.
2. Terrain and exact fortification primitives.
3. Derived fields, sparse chunks, and semantic graphs.
4. Point, chain, visibility, corridor, and connectivity queries.
5. Evidence graph and explanation templates.
6. Site, approach, visibility, and exposure evaluators.
7. Obstacle, gate, breach, circulation, compartment, capture, and lodgement evaluators.
8. Perception and actual-versus-perceived analysis.
9. Mechanical COA generation and vector ranking.
10. Benchmark family, comparisons, sweeps, and convergence tests.
11. Interactive HTML reporting.
12. Full stress-test run and accuracy-boundary report.

Every stage uses test-first implementation and must leave the repository passing before the next stage begins.

## 16. Deliverables

The completed POC delivers:

- Installable and documented Python package.
- Version-controlled source repository.
- Scenario, result, evidence, experiment, and report schemas.
- Exact geometry and derived spatial/graph representations.
- Unified query engine.
- Static adversarial evaluator suite.
- Perceived and authoritative assessment paths.
- Mechanical COA generator and transparent ranking.
- Automated experiment harness.
- Interactive HTML reports.
- Synthetic benchmark family.
- Comprehensive automated test suite.
- Baseline stress-test and sensitivity report.
- Documented model assumptions, limitations, and recommended next phase.

## 17. Explicit Future Boundary

The next phase may introduce abstract discrete-event attacker and defender commanders that consume POC evidence. A later phase may add animated real-time execution and historical profiles. Those phases must use the same authoritative geometry, perception, evidence, and scenario interfaces rather than bypassing them.

The POC is complete only when it provides a robust analytical foundation. It is not extended merely to demonstrate visually impressive combat.
