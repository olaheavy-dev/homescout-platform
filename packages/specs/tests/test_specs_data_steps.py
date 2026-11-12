"""The seven data steps, one by one (ported from DataStepsTests, issue #193).

Each failing case checks the message too: the message tells an author which ID to fix.
"""

import pytest
import specs_support as data
from specs_support import DataSteps, StoryPosition

_TOTAL = "B1.from-step-1.monthly.total"
_INSURANCE = "B1.from-step-1.monthly.buildings-insurance"
_SERVICE_CHARGE = "B1.from-step-1.monthly.service-charge"


@pytest.fixture
def position() -> StoryPosition:
    story = StoryPosition()
    story.set("B1", "from-step-1")
    return story


@pytest.fixture
def steps(position: StoryPosition) -> DataSteps:
    return DataSteps(position)


def test_then_figure_exists_unknown_figure_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_exists("B1.from-step-1.monthly.nope")

    assert "B1.from-step-1.monthly.nope" in str(failure.value)


def test_then_figure_exists_figure_from_another_step_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_exists("B1.from-step-3.monthly.total")

    assert 'figures here start with "B1.from-step-1."' in str(failure.value)


def test_then_figure_exists_known_figure_passes(steps: DataSteps) -> None:
    steps.then_figure_exists(_TOTAL)


def test_then_figure_exists_before_any_given_step_accepts_any_known_figure() -> None:
    DataSteps(StoryPosition()).then_figure_exists("B1.from-step-3.monthly.total")


def test_then_figure_has_status_wrong_status_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_has_status(_INSURANCE, "calculated")

    assert _INSURANCE in str(failure.value)


def test_then_figure_has_status_part_of_the_real_status_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError):
        steps.then_figure_has_status(_INSURANCE, "miss")


def test_then_figure_has_status_correct_status_passes(steps: DataSteps) -> None:
    steps.then_figure_has_status(_INSURANCE, "missing")


def test_then_figure_has_status_total_fails_saying_it_is_a_total(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_has_status(_TOTAL, "calculated")

    assert "has no status (it is a total, not a line)" in str(failure.value)


def test_then_figure_shows_no_amount_line_with_pence_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_shows_no_amount(_SERVICE_CHARGE)

    assert "missing is never shown as zero" in str(failure.value)


def test_then_figure_shows_no_amount_line_without_amount_passes(steps: DataSteps) -> None:
    steps.then_figure_shows_no_amount(_INSURANCE)


def test_then_figure_shows_no_amount_line_with_zero_pence_fails(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    zero = {"id": _INSURANCE, "status": "calculated", "pence": 0}
    monkeypatch.setattr(data, "try_get_figure", lambda _figure_id: zero)

    with pytest.raises(AssertionError) as failure:
        steps.then_figure_shows_no_amount(_INSURANCE)

    assert "has an amount (pence)" in str(failure.value)


def test_then_figure_shows_no_amount_total_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_shows_no_amount(_TOTAL)

    assert "is not a cost line" in str(failure.value)


def test_then_figure_shows_no_amount_budget_with_budget_pence_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError):
        steps.then_figure_shows_no_amount("B1.from-step-1.monthly.budget")


def test_then_figure_cites_evidence_evidence_not_cited_by_figure_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_cites_evidence(_SERVICE_CHARGE, "B1-STAMP-DUTY")

    assert "does not cite evidence" in str(failure.value)


def test_then_figure_cites_evidence_unknown_evidence_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_figure_cites_evidence(_SERVICE_CHARGE, "NO-SUCH-EVIDENCE")

    assert "NO-SUCH-EVIDENCE" in str(failure.value)
    assert "is not in packages/fixtures/data/evidence.json" in str(failure.value)


def test_then_figure_cites_evidence_cited_evidence_passes(steps: DataSteps) -> None:
    steps.then_figure_cites_evidence(_SERVICE_CHARGE, "B1-SC-LISTING")


def test_then_total_is_partial_with_reason_reason_not_listed_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_total_is_partial_with_reason(_TOTAL, "council-tax")

    assert 'not because of "council-tax"' in str(failure.value)


def test_then_total_is_partial_with_reason_partial_flag_not_true_fails(
    steps: DataSteps, monkeypatch: pytest.MonkeyPatch
) -> None:
    odd = {
        "id": _TOTAL,
        "isPartial": "yes",
        "partialReasons": [{"category": "buildings-insurance"}],
    }
    monkeypatch.setattr(data, "try_get_figure", lambda _figure_id: odd)

    with pytest.raises(AssertionError) as failure:
        steps.then_total_is_partial_with_reason(_TOTAL, "buildings-insurance")

    assert "is not partial" in str(failure.value)


def test_then_total_is_partial_with_reason_listed_reason_passes(steps: DataSteps) -> None:
    steps.then_total_is_partial_with_reason(_TOTAL, "buildings-insurance")


def test_then_total_is_partial_with_reason_total_not_partial_fails(position: StoryPosition) -> None:
    not_partial = next(
        figure_id
        for figure_id in sorted(data.figure_ids())
        if figure_id.endswith(".total")
        and (figure := data.try_get_figure(figure_id)) is not None
        and figure.get("isPartial") is False
    )
    home_id, scenario_id = not_partial.split(".")[:2]
    position.set(home_id, scenario_id)

    with pytest.raises(AssertionError) as failure:
        DataSteps(position).then_total_is_partial_with_reason(not_partial, "buildings-insurance")

    assert "is not partial" in str(failure.value)


def test_then_evidence_exists_known_evidence_passes(steps: DataSteps) -> None:
    steps.then_evidence_exists("B1-STAMP-DUTY")


def test_then_evidence_exists_unknown_evidence_fails_naming_the_id(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.then_evidence_exists("NO-SUCH-EVIDENCE")

    assert "NO-SUCH-EVIDENCE" in str(failure.value)


def test_given_home_is_at_story_step_step_inside_range_sets_the_scenario(
    position: StoryPosition, steps: DataSteps
) -> None:
    steps.given_home_is_at_story_step("B1", 2)

    assert position.scenario_id == "from-step-1"
    assert position.figure_prefix == "B1.from-step-1."


@pytest.mark.parametrize("step", [0, 5])
def test_given_home_is_at_story_step_step_out_of_range_fails(steps: DataSteps, step: int) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.given_home_is_at_story_step("B1", step)

    assert f"at story step {step}" in str(failure.value)


def test_given_home_is_at_story_step_unknown_home_fails(steps: DataSteps) -> None:
    with pytest.raises(AssertionError) as failure:
        steps.given_home_is_at_story_step("NOPE", 1)

    assert '"NOPE"' in str(failure.value)
    assert "packages/fixtures/data/homes.json" in str(failure.value)


def test_story_position_before_any_given_step_has_no_prefix() -> None:
    assert StoryPosition().figure_prefix is None
