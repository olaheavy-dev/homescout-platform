"""``name_scenarios_by_id`` on its own: how it reads the ID and when it refuses (issue #193)."""

from pathlib import Path
from typing import Any

import pytest
from specs_runner import name_scenarios_by_id


def _feature(tmp_path: Path, scenario_name: str) -> str:
    path = tmp_path / "naming.feature"
    path.write_text(
        f"Feature: Naming\n\n  Scenario: {scenario_name}\n    Given a step\n", encoding="utf-8"
    )
    return str(path)


def _description(tmp_path: Path, scenario_name: str) -> str:
    """What pytest-bdd puts in a scenario test's docstring: the feature file path and the name."""
    return f"{tmp_path / 'naming.feature'}: {scenario_name}"


def _test_function(description: str | None) -> Any:
    """A stand-in for a scenario test."""

    def test_scenario() -> None:
        return None

    test_scenario.__doc__ = description
    return test_scenario


def test_name_scenarios_by_id_single_digit_id_is_accepted(tmp_path: Path) -> None:
    namespace = {"test_buy": _test_function(_description(tmp_path, "BUY-3 first step"))}

    name_scenarios_by_id(namespace, _feature(tmp_path, "BUY-3 first step"))

    assert list(namespace) == ["test_BUY-3_first_step"]


def test_name_scenarios_by_id_dotted_id_is_kept_whole(tmp_path: Path) -> None:
    namespace = {"test_buy": _test_function(_description(tmp_path, "BUY-3.2 second thing"))}

    name_scenarios_by_id(namespace, _feature(tmp_path, "BUY-3.2 second thing"))

    assert list(namespace) == ["test_BUY-3.2_second_thing"]


def test_name_scenarios_by_id_id_not_at_the_start_of_the_name_fails(tmp_path: Path) -> None:
    namespace = {"test_odd": _test_function(_description(tmp_path, "unnumbered: SEE-12 x"))}

    with pytest.raises(ValueError, match="unnumbered: SEE-12 x") as failure:
        name_scenarios_by_id(namespace, _feature(tmp_path, "unnumbered: SEE-12 x"))

    assert "permanent ID" in str(failure.value)


def test_name_scenarios_by_id_test_without_a_docstring_fails(tmp_path: Path) -> None:
    namespace = {"test_plain": _test_function(None)}

    with pytest.raises(ValueError, match="test_plain"):
        name_scenarios_by_id(namespace, _feature(tmp_path, "BUY-3 first step"))


def test_name_scenarios_by_id_two_scenarios_with_one_id_fail(tmp_path: Path) -> None:
    namespace = {
        "test_a": _test_function(_description(tmp_path, "BUY-3 first step")),
        "test_b": _test_function(_description(tmp_path, "BUY-3 first step")),
    }

    with pytest.raises(ValueError, match="BUY-3"):
        name_scenarios_by_id(namespace, _feature(tmp_path, "BUY-3 first step"))
