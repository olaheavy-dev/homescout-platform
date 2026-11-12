"""Figure ids follow register line BE-11: ``{homeId}.{scenarioId}.{section}.{name}``.

Screens and documents quote a figure by this id (ported from the C# FigureIds tests).
"""

from typing import Any

import pytest
from vestagraph_engine import figure_ids
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import CostCategory


def test_figure_ids_line_in_the_monthly_section_follows_the_contract_format() -> None:
    assert (
        figure_ids.line("B1", "from-step-1", "monthly", CostCategory.SERVICE_CHARGE)
        == "B1.from-step-1.monthly.service-charge"
    )


def test_figure_ids_line_in_the_upfront_section_follows_the_contract_format() -> None:
    assert (
        figure_ids.line("R1", "from-step-4", "upfront", CostCategory.FIRST_MONTH_RENT)
        == "R1.from-step-4.upfront.first-month-rent"
    )


@pytest.mark.parametrize("category", list(CostCategory))
def test_figure_ids_line_names_each_category_by_its_fixture_name(category: CostCategory) -> None:
    assert figure_ids.line("H", "s", "monthly", category) == f"H.s.monthly.{category_id(category)}"


def test_figure_ids_total_follows_the_contract_format() -> None:
    assert figure_ids.total("B1", "from-step-4", "monthly") == "B1.from-step-4.monthly.total"
    assert figure_ids.total("B1", "from-step-1", "upfront") == "B1.from-step-1.upfront.total"


def test_figure_ids_budget_follows_the_contract_format() -> None:
    assert figure_ids.budget("R1", "from-step-1") == "R1.from-step-1.monthly.budget"


def test_figure_ids_mortgage_loan_follows_the_contract_format() -> None:
    assert figure_ids.mortgage_loan("B1", "from-step-1") == "B1.from-step-1.mortgage.loan"


def test_figure_ids_change_follows_the_contract_format() -> None:
    assert (
        figure_ids.change("B1", "from-step-4", CostCategory.SERVICE_CHARGE)
        == "B1.from-step-4.change.service-charge"
    )


def test_figure_ids_monthly_total_change_follows_the_contract_format() -> None:
    assert (
        figure_ids.monthly_total_change("B1", "from-step-4")
        == "B1.from-step-4.change.monthly-total"
    )


def test_figure_ids_mortgage_as_a_whole_has_no_name_part() -> None:
    assert figure_ids.mortgage("B1", "from-step-1") == "B1.from-step-1.mortgage"


def test_figure_ids_monthly_repayment_follows_the_contract_format() -> None:
    assert (
        figure_ids.monthly_repayment("B1", "from-step-1")
        == "B1.from-step-1.mortgage.monthly-repayment"
    )


@pytest.mark.parametrize("bad", [None, 1, CostCategory.RENT])
def test_figure_ids_text_part_that_is_not_a_str_raises_type_error(bad: Any) -> None:
    with pytest.raises(TypeError):
        figure_ids.total(bad, "from-step-1", "monthly")
    with pytest.raises(TypeError):
        figure_ids.total("B1", bad, "monthly")
    with pytest.raises(TypeError):
        figure_ids.total("B1", "from-step-1", bad)
    with pytest.raises(TypeError):
        figure_ids.mortgage(bad, "from-step-1")
    with pytest.raises(TypeError):
        figure_ids.mortgage("B1", bad)


@pytest.mark.parametrize("bad", [None, "rent", 3])
def test_figure_ids_category_that_is_not_a_cost_category_raises_type_error(bad: Any) -> None:
    with pytest.raises(TypeError):
        figure_ids.line("B1", "from-step-1", "monthly", bad)
    with pytest.raises(TypeError):
        figure_ids.change("B1", "from-step-1", bad)
