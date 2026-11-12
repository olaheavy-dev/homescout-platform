"""The data the specifications check against (ported from SpecDataTests, issue #193)."""

import specs_support as data


def test_try_get_figure_known_figure_id_finds_it() -> None:
    figure = data.try_get_figure("B1.from-step-1.monthly.total")

    assert figure is not None
    assert figure["id"] == "B1.from-step-1.monthly.total"


def test_try_get_figure_unknown_figure_id_does_not_find_it() -> None:
    assert data.try_get_figure("B1.from-step-1.monthly.no-such-line") is None


def test_try_get_figure_wrong_case_does_not_find_it() -> None:
    assert data.try_get_figure("b1.from-step-1.monthly.total") is None


def test_evidence_ids_known_evidence_contains_it() -> None:
    assert "B1-STAMP-DUTY" in data.evidence_ids()


def test_has_scenario_from_step_step_with_no_scenario_is_false() -> None:
    assert data.has_scenario_from_step("B1", 99) is False


def test_figure_ids_generated_file_is_not_empty() -> None:
    assert data.figure_ids()


def test_has_scenario_from_step_step_inside_a_scenario_range_is_true() -> None:
    assert data.has_scenario_from_step("B1", 1) is True
    assert data.has_scenario_from_step("B1", 2) is True


def test_home_ids_known_home_contains_it_and_not_an_unknown_one() -> None:
    assert "B1" in data.home_ids()
    assert "NOPE" not in data.home_ids()


def test_try_find_scenario_step_inside_the_range_names_the_scenario() -> None:
    assert data.try_find_scenario("B1", 2) == "from-step-1"


def test_specs_directory_repository_root_is_docs_specs_with_its_readme() -> None:
    directory = data.specs_directory()

    assert directory == data.repository_root() / "docs" / "specs"
    assert (directory / "README.md").is_file()
