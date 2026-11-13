"""The step bindings for the data scenarios: the wording is the contract in docs/specs/README.md.

Each binding hands over to ``DataSteps`` (``specs_support.py``), which holds the checks and their
failure messages. A step whose wording is not here makes its scenario fail as undefined: add the
step here (with a test) rather than rewording the scenario around it.

A test module that calls ``scenarios()`` imports everything from here with ``import *``: pytest-bdd
finds step definitions and fixtures in the test module's namespace (or in a ``conftest.py``, which
its documentation also describes). The decorators register each step under a generated name
(``pytestbdd_stepdef_...``) that only a star import carries over. This layout keeps the steps
importable by the proof tests' temporary modules, which a ``conftest.py`` here would not reach.
"""

import pytest
from pytest_bdd import given, parsers, then
from specs_support import DataSteps, StoryPosition


@pytest.fixture
def story_position() -> StoryPosition:
    """One per scenario, so every scenario starts with no home or story step."""
    return StoryPosition()


@pytest.fixture
def data_steps(story_position: StoryPosition) -> DataSteps:
    return DataSteps(story_position)


@given(parsers.parse('home "{home_id}" is at story step {step:d}'))
def given_home_is_at_story_step(data_steps: DataSteps, home_id: str, step: int) -> None:
    data_steps.given_home_is_at_story_step(home_id, step)


@then(parsers.parse('figure "{figure_id}" exists'))
def then_figure_exists(data_steps: DataSteps, figure_id: str) -> None:
    data_steps.then_figure_exists(figure_id)


@then(parsers.parse('figure "{figure_id}" has status "{status}"'))
def then_figure_has_status(data_steps: DataSteps, figure_id: str, status: str) -> None:
    data_steps.then_figure_has_status(figure_id, status)


@then(parsers.parse('figure "{figure_id}" shows no amount'))
def then_figure_shows_no_amount(data_steps: DataSteps, figure_id: str) -> None:
    data_steps.then_figure_shows_no_amount(figure_id)


@then(parsers.parse('figure "{figure_id}" cites evidence "{evidence_id}"'))
def then_figure_cites_evidence(data_steps: DataSteps, figure_id: str, evidence_id: str) -> None:
    data_steps.then_figure_cites_evidence(figure_id, evidence_id)


@then(parsers.parse('the total "{total_id}" is partial with reason "{category}"'))
def then_total_is_partial_with_reason(data_steps: DataSteps, total_id: str, category: str) -> None:
    data_steps.then_total_is_partial_with_reason(total_id, category)


@then(parsers.parse('evidence "{evidence_id}" exists'))
def then_evidence_exists(data_steps: DataSteps, evidence_id: str) -> None:
    data_steps.then_evidence_exists(evidence_id)


@then(parsers.parse('area record "{record_id}" has status "{status}"'))
def then_area_record_has_status(data_steps: DataSteps, record_id: str, status: str) -> None:
    data_steps.then_area_record_has_status(record_id, status)


@then(parsers.parse('area record "{record_id}" shows no value'))
def then_area_record_shows_no_value(data_steps: DataSteps, record_id: str) -> None:
    data_steps.then_area_record_shows_no_value(record_id)


@then(parsers.parse('home "{home_id}" has coverage "{coverage}"'))
def then_home_has_coverage(data_steps: DataSteps, home_id: str, coverage: str) -> None:
    data_steps.then_home_has_coverage(home_id, coverage)
