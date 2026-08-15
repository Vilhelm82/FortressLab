import json

from hypothesis import example, given, settings

from fortresslab.schema.scenario import Scenario
from fortresslab.serialization import canonical_json_bytes
from tests.factories import minimal_scenario
from tests.strategies import valid_scenarios


@given(valid_scenarios())
@example(scenario=minimal_scenario())
@settings(max_examples=100)
def test_scenario_canonical_json_roundtrip_is_semantic_identity(
    scenario: Scenario,
) -> None:
    """Encoding and validating restores every declared scenario value."""
    restored = Scenario.model_validate_json(canonical_json_bytes(scenario))
    assert restored == scenario


@given(valid_scenarios())
@example(scenario=minimal_scenario())
@settings(max_examples=100)
def test_canonicalization_is_idempotent(scenario: Scenario) -> None:
    """Canonical bytes stay unchanged after a JSON parse and second encoding."""
    first = canonical_json_bytes(scenario)
    second = canonical_json_bytes(json.loads(first))
    assert second == first
