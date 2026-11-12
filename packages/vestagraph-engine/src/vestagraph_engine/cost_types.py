"""The small vocabularies of a cost line: period, mode, category and status (ported from C#)."""

from enum import Enum


class Period(Enum):
    """How often an amount is charged, as its source states it."""

    ONCE = "once"
    MONTH = "month"
    YEAR = "year"


class Mode(Enum):
    """Whether a home is being bought or rented."""

    BUY = "buy"
    RENT = "rent"


class CostCategory(Enum):
    """A kind of cost the engine can place in a monthly or upfront breakdown.

    The value is the hyphenated name used in the fixture data, the worked cases, error codes and
    the generated files.
    """

    MORTGAGE_REPAYMENT = "mortgage-repayment"
    SERVICE_CHARGE = "service-charge"
    GROUND_RENT = "ground-rent"
    COUNCIL_TAX = "council-tax"
    ENERGY = "energy"
    WATER = "water"
    BROADBAND = "broadband"
    BUILDINGS_INSURANCE = "buildings-insurance"
    MAINTENANCE = "maintenance"
    RENT = "rent"
    MORTGAGE_DEPOSIT = "mortgage-deposit"
    DEPOSIT = "deposit"
    FIRST_MONTH_RENT = "first-month-rent"
    MOVING_COSTS = "moving-costs"
    STAMP_DUTY = "stamp-duty"
    LEGAL_FEES = "legal-fees"


class LineStatus(Enum):
    """What a cost line is in a result: an amount, or the reason there is no amount."""

    CALCULATED = "calculated"
    """The engine worked out an amount."""

    INCLUDED = "included"
    """Covered by another charge (for example water in the rent). It adds nothing."""

    NOT_CALCULATED = "not-calculated"
    """This version does not work it out. It adds nothing and makes the total partial."""

    CONFLICTING = "conflicting"
    """Sources disagree and it is not settled. It adds nothing and makes the total partial."""

    MISSING = "missing"
    """There is no evidence for it. It adds nothing and makes the total partial."""
