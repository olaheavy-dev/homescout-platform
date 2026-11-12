"""Chooses which evidence each cost line uses (ported from the C# ``AssumptionSelector``).

The engine works on the chosen lines only, so this is where "which figure counts" is decided and
written down.
"""

from collections.abc import Sequence
from typing import assert_never

from vestagraph_engine import cost_lines
from vestagraph_engine._checks import INT32_MAX, is_a
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import CostCategory, Mode, Period
from vestagraph_engine.evidence import (
    EvidenceItem,
    EvidenceStatus,
    HomeFacts,
    MoneyValue,
    Nation,
    RateValue,
    YearsValue,
)
from vestagraph_engine.line_input import (
    AmountLine,
    ConflictingLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.result import Error, ErrorCategory, Result
from vestagraph_engine.selected_inputs import MortgageInputs, SelectedInputs

_WATER_RESPONSIBILITY = "water-responsibility"


def select_assumptions(facts: HomeFacts, story_step: int) -> Result[SelectedInputs]:
    """Choose the inputs for a home at a story step (steps start at 1).

    The selection rules:

    1. Context-only items are ignored, so a value shown for context (for example the cost on an
       energy certificate) never enters a total.
    2. An item is in use at step s when its ``used_from_step`` is ``None`` or at most s, and no
       item that has started by step s names it in ``supersedes``.
    3. For each category the first match in this order is used: a value of the wrong kind fails
       the selection (``input.wrong-kind``, checked before ambiguity, for ordinary lines and
       anchors alike); a money item with a value gives an amount, whatever its status in the
       snapshot (the snapshot is taken after the story ends); otherwise a conflicting item
       (including the rule 4 group) gives a conflicting line, so nothing can hide a
       disagreement; then a not-calculated item gives a not-calculated line, and an included item
       an included line (not-calculated wins, as the more cautious); then a not-applicable item
       leaves the line out; and no evidence at all gives a missing line.
    4. ``water-responsibility`` items count towards the water line, for the conflicting check
       only. This is the only link between categories, and a narrow stand-in until the data has a
       proper "who pays" field.
    5. Two in-use money items for one category cannot both be used, so the selection fails.

    An anchor input that has no usable value stops the whole selection: the asking price, the
    mortgage deposit, rate and term when buying, and the rent when renting (register line BE-16).

    Error codes (tests match the code, never the message): ``home.not-covered`` (the home is not
    in England), ``home.mode-missing`` (neither buy nor rent), ``story.step-out-of-range`` (the
    step is below 1), ``input.missing.{category}`` (an anchor input has no value),
    ``input.ambiguous.{category}`` (rule 5), ``input.wrong-period.{category}`` (the price or
    deposit is not once, or the rent is not monthly), ``input.not-positive.{category}`` (an anchor
    amount is zero or less), ``input.wrong-kind.{category}`` (a value of the wrong kind, for
    example a rate given as money).

    Raises ``TypeError`` for facts that are not ``HomeFacts`` or a step that is not an ``int``,
    and ``ValueError`` for a step above the largest 32-bit ``int`` (the C# step is an ``int``).
    """
    if not is_a(facts, HomeFacts):
        message = "select_assumptions needs HomeFacts."
        raise TypeError(message)
    if type(story_step) is not int:
        message = "select_assumptions needs a whole-number (int) story step."
        raise TypeError(message)
    if story_step > INT32_MAX:
        message = "The story step is above the largest 32-bit whole number."
        raise ValueError(message)

    home = check_home(facts)
    if home.is_failure:
        return Result.failure(home.error)
    mode = home.value

    if story_step < 1:
        return Result.failure(
            Error("story.step-out-of-range", "A story step starts at 1.", ErrorCategory.VALIDATION)
        )

    in_use = _in_use(facts.evidence, story_step)

    mortgage: MortgageInputs | None = None
    if mode == Mode.BUY:
        found = _buyer_inputs(in_use)
        if found.is_failure:
            return Result.failure(found.error)
        mortgage = found.value

    monthly: list[LineInput] = []
    for category in cost_lines.monthly_order(mode):
        if category == CostCategory.MORTGAGE_REPAYMENT:
            continue  # only the mortgage calculation can supply it
        chosen = _choose_line(in_use, category, mortgage)
        if isinstance(chosen, Error):
            return Result.failure(chosen)
        if chosen is not None:
            monthly.append(chosen)

    upfront: list[LineInput] = []
    for category in cost_lines.upfront_order(mode):
        chosen = _choose_line(in_use, category, mortgage)
        if isinstance(chosen, Error):
            return Result.failure(chosen)
        if chosen is not None:
            upfront.append(chosen)

    return Result.success(SelectedInputs(mode, mortgage, tuple(monthly), tuple(upfront)))


def check_home(facts: HomeFacts) -> Result[Mode]:
    """Check that the home is one the engine covers: in England, and either for sale or to rent.

    On success the value is the home's mode.
    """
    if facts.nation != Nation.ENGLAND:
        return Result.failure(
            Error(
                "home.not-covered",
                f"Home {facts.home_id} is not in England, which is the only nation covered so far.",
                ErrorCategory.VALIDATION,
            )
        )
    if facts.mode is None:
        return Result.failure(
            Error(
                "home.mode-missing",
                f"Home {facts.home_id} is neither for sale nor to rent in the data.",
                ErrorCategory.VALIDATION,
            )
        )
    return Result.success(facts.mode)


def _in_use(evidence: Sequence[EvidenceItem], step: int) -> list[EvidenceItem]:
    """Rules 1 and 2: the items that count at this step."""
    started = [
        item
        for item in evidence
        if not item.context_only and (item.used_from_step is None or item.used_from_step <= step)
    ]
    replaced = {item.supersedes for item in started if item.supersedes is not None}
    return [item for item in started if item.id not in replaced]


def _buyer_inputs(in_use: list[EvidenceItem]) -> Result[MortgageInputs]:
    price = _money_anchor(in_use, "asking-price", Period.ONCE)
    if price.is_failure:
        return Result.failure(price.error)
    deposit = _money_anchor(in_use, "mortgage-deposit", Period.ONCE)
    if deposit.is_failure:
        return Result.failure(deposit.error)
    rate = _anchor(in_use, "mortgage-rate", RateValue)
    if rate.is_failure:
        return Result.failure(rate.error)
    term = _anchor(in_use, "mortgage-term", YearsValue)
    if term.is_failure:
        return Result.failure(term.error)

    price_item, price_money = price.value
    deposit_item, deposit_money = deposit.value
    rate_item, rate_value = rate.value
    term_item, term_value = term.value
    return Result.success(
        MortgageInputs(
            price_money.amount,
            deposit_money.amount,
            rate_value.basis_points,
            term_value.years,
            (price_item.id, deposit_item.id, rate_item.id, term_item.id),
        )
    )


def _anchor[V](
    in_use: list[EvidenceItem], category: str, expected_kind: type[V]
) -> Result[tuple[EvidenceItem, V]]:
    """Find the one item with a value of the expected kind for an anchor input.

    Items with no value (missing, for example) do not count, so an anchor with none of them is
    missing, and an anchor with two is ambiguous (rule 5).
    """
    valued = [
        (item, item.value)
        for item in in_use
        if item.category == category and item.value is not None
    ]
    of_kind = [(item, value) for item, value in valued if isinstance(value, expected_kind)]

    # Wrong kind is reported before ambiguity, as it is for ordinary lines.
    if len(of_kind) != len(valued):
        return Result.failure(_wrong_kind(category))
    if not of_kind:
        return Result.failure(
            Error(
                f"input.missing.{category}",
                f"The {category} value is needed before a cost can be worked out.",
                ErrorCategory.VALIDATION,
            )
        )
    if len(of_kind) > 1:
        return Result.failure(_ambiguous(category))
    return Result.success(of_kind[0])


def _money_anchor(
    in_use: list[EvidenceItem], category: str, period: Period
) -> Result[tuple[EvidenceItem, MoneyValue]]:
    """An anchor input that must be a positive amount of money paid in a given period."""
    found = _anchor(in_use, category, MoneyValue)
    if found.is_failure:
        return found

    money = found.value[1]
    if money.period != period:
        return Result.failure(
            Error(
                f"input.wrong-period.{category}",
                f"The {category} amount must be given as {_period_words(period)}.",
                ErrorCategory.VALIDATION,
            )
        )
    if money.amount.value <= 0:
        return Result.failure(
            Error(
                f"input.not-positive.{category}",
                f"The {category} amount must be more than zero.",
                ErrorCategory.VALIDATION,
            )
        )
    return found


def _choose_line(
    in_use: list[EvidenceItem], category: CostCategory, mortgage: MortgageInputs | None
) -> LineInput | Error | None:
    """Rule 3 for one category, with the anchor lines (rent, and the mortgage deposit) first.

    ``None`` means the line is left out.
    """
    if category == CostCategory.MORTGAGE_DEPOSIT and mortgage is not None:
        # The deposit was already checked as an anchor input; its id is the second one.
        return AmountLine(category, mortgage.deposit, Period.ONCE, (mortgage.evidence_ids[1],))

    if category == CostCategory.RENT:
        rent = _money_anchor(in_use, "rent", Period.MONTH)
        if rent.is_failure:
            return rent.error
        rent_item, rent_money = rent.value
        return AmountLine(category, rent_money.amount, Period.MONTH, (rent_item.id,))

    name = category_id(category)
    items = [item for item in in_use if item.category == name]
    valued = [(item, item.value) for item in items if item.value is not None]
    monies = [(item, value) for item, value in valued if isinstance(value, MoneyValue)]

    if len(monies) != len(valued):
        return _wrong_kind(name)
    if len(monies) > 1:
        return _ambiguous(name)
    if monies:
        item, money = monies[0]
        return AmountLine(category, money.amount, money.period, (item.id,))

    # Rule 4: for water, the "who pays" items join the conflicting check. Conflicting comes before
    # the statuses that have no value, so an "included" or "not applicable" item cannot hide a
    # disagreement.
    if category == CostCategory.WATER:
        group = [item for item in in_use if item.category in (name, _WATER_RESPONSIBILITY)]
    else:
        group = items
    if any(item.status == EvidenceStatus.CONFLICTING for item in group):
        return ConflictingLine(category, tuple(item.id for item in group))

    not_calculated = _ids_with_status(items, EvidenceStatus.NOT_CALCULATED)
    if not_calculated:
        return NotCalculatedLine(category, not_calculated)

    included = _ids_with_status(items, EvidenceStatus.INCLUDED)
    if included:
        return IncludedLine(category, included)

    if any(item.status == EvidenceStatus.NOT_APPLICABLE for item in items):
        return None

    return MissingLine(category)


def _ids_with_status(items: list[EvidenceItem], status: EvidenceStatus) -> tuple[str, ...]:
    return tuple(item.id for item in items if item.status == status)


def _period_words(period: Period) -> str:
    match period:
        case Period.ONCE:
            return "a one-off amount"
        case Period.MONTH:
            return "a monthly amount"
        case Period.YEAR:
            return "a yearly amount"
        case _:
            assert_never(period)


def _wrong_kind(category: str) -> Error:
    return Error(
        f"input.wrong-kind.{category}",
        f"The {category} value is not the kind of value this cost needs.",
        ErrorCategory.VALIDATION,
    )


def _ambiguous(category: str) -> Error:
    return Error(
        f"input.ambiguous.{category}",
        f"There is more than one {category} value in use, so none can be chosen.",
        ErrorCategory.CONFLICT,
    )
