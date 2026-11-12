"""The id of every figure in the generated file (ported from the C# ``FigureIds``).

The format is ``{homeId}.{scenarioId}.{section}.{name}`` (register line BE-11), for example
``B1.from-step-4.monthly.service-charge``. Screens and documents quote a figure by this id.
"""

from vestagraph_engine._checks import is_a
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import CostCategory


def line(home_id: str, scenario_id: str, section: str, category: CostCategory) -> str:
    """The id of a line in a section (``monthly`` or ``upfront``)."""
    return _make(home_id, scenario_id, section, category_id(category))


def total(home_id: str, scenario_id: str, section: str) -> str:
    """The id of a section's total."""
    return _make(home_id, scenario_id, section, "total")


def budget(home_id: str, scenario_id: str) -> str:
    """The id of the monthly budget check."""
    return _make(home_id, scenario_id, "monthly", "budget")


def mortgage(home_id: str, scenario_id: str) -> str:
    """The id of the mortgage as a whole."""
    _check_text(home_id, scenario_id)
    return f"{home_id}.{scenario_id}.mortgage"


def mortgage_loan(home_id: str, scenario_id: str) -> str:
    """The id of the amount borrowed."""
    return _make(home_id, scenario_id, "mortgage", "loan")


def monthly_repayment(home_id: str, scenario_id: str) -> str:
    """The id of the monthly repayment."""
    return _make(home_id, scenario_id, "mortgage", "monthly-repayment")


def change(home_id: str, scenario_id: str, category: CostCategory) -> str:
    """The id of a change to one line since the previous scenario."""
    return _make(home_id, scenario_id, "change", category_id(category))


def monthly_total_change(home_id: str, scenario_id: str) -> str:
    """The id of the change to the monthly total since the previous scenario."""
    return _make(home_id, scenario_id, "change", "monthly-total")


def _check_text(*parts: object) -> None:
    if not all(is_a(part, str) for part in parts):
        message = "A figure id is built from text parts (str)."
        raise TypeError(message)


def _make(home_id: str, scenario_id: str, section: str, name: str) -> str:
    _check_text(home_id, scenario_id, section, name)
    return f"{home_id}.{scenario_id}.{section}.{name}"
