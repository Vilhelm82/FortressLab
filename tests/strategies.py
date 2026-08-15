from hypothesis import strategies as st

from fortresslab.schema.scenario import Scenario
from tests.factories import minimal_scenario


@st.composite
def valid_scenarios(draw: st.DrawFn) -> Scenario:
    base = minimal_scenario()
    scenario_id = draw(st.from_regex(r"[a-z][a-z0-9_]{0,20}", fullmatch=True))
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
            min_value=0.125,
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
