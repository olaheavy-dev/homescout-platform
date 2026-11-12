"""The hyphenated names used in fixture data, worked cases, error codes and generated files."""

from vestagraph_engine._checks import is_a
from vestagraph_engine.cost_types import CostCategory, LineStatus


def category_id(category: CostCategory) -> str:
    """The name of a category, for example ``service-charge``. Raises ``TypeError`` otherwise."""
    if not is_a(category, CostCategory):
        message = "category_id needs a CostCategory."
        raise TypeError(message)
    return category.value


def status_id(status: LineStatus) -> str:
    """The name of a line status, for example ``not-calculated``. Raises ``TypeError`` otherwise."""
    if not is_a(status, LineStatus):
        message = "status_id needs a LineStatus."
        raise TypeError(message)
    return status.value
