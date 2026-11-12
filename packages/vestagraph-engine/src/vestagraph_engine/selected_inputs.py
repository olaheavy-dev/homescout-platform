"""What the assumption selector chose for one home at one story step (ported from C#)."""

from dataclasses import dataclass

from vestagraph_engine._checks import check_int32, is_a
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import Mode
from vestagraph_engine.line_input import LINE_KINDS, LineInput
from vestagraph_engine.pence import Pence


def _check_lines(lines: object, name: str) -> None:
    if type(lines) is not tuple or any(type(line) not in LINE_KINDS for line in lines):
        message = f"A selection's {name} must be a tuple of line inputs."
        raise TypeError(message)


@dataclass(frozen=True, slots=True)
class MortgageInputs:
    """The inputs of a purchase's mortgage, with the evidence they came from.

    ``deposit`` is taken from ``asking_price`` to give the loan; ``rate_basis_points`` is the
    yearly rate in whole basis points; ``evidence_ids`` are the ids of the price, deposit, rate
    and term evidence, in that order.
    """

    asking_price: Pence
    deposit: Pence
    rate_basis_points: int
    term_years: int
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not is_a(self.asking_price, Pence):
            message = "A mortgage's asking_price must be a Pence."
            raise TypeError(message)
        if not is_a(self.deposit, Pence):
            message = "A mortgage's deposit must be a Pence."
            raise TypeError(message)
        check_int32(self.rate_basis_points, "A mortgage's rate_basis_points")
        check_int32(self.term_years, "A mortgage's term_years")
        if type(self.evidence_ids) is not tuple or any(
            type(item) is not str for item in self.evidence_ids
        ):
            message = "A mortgage's evidence_ids must be a tuple of str."
            raise TypeError(message)


@dataclass(frozen=True, slots=True)
class SelectedInputs:
    """What the assumption selector chose for one home at one story step.

    ``monthly_lines`` are the monthly lines except the mortgage repayment, which only the
    mortgage calculation can supply; ``mortgage`` is set when buying.
    """

    mode: Mode
    mortgage: MortgageInputs | None
    monthly_lines: tuple[LineInput, ...]
    upfront_lines: tuple[LineInput, ...]

    def __post_init__(self) -> None:
        if not is_a(self.mode, Mode):
            message = "A selection's mode must be a Mode."
            raise TypeError(message)
        if self.mortgage is not None and not is_a(self.mortgage, MortgageInputs):
            message = "A selection's mortgage must be a MortgageInputs or None."
            raise TypeError(message)
        _check_lines(self.monthly_lines, "monthly_lines")
        _check_lines(self.upfront_lines, "upfront_lines")

    def signature(self) -> str:
        """A text that is the same for two steps exactly when they use the same evidence in the
        same way. Consecutive steps with the same signature are merged into one scenario."""
        lines = ";".join(
            f"{category_id(line.category)}:{type(line).__name__}:{','.join(line.evidence_ids)}"
            for line in (*self.monthly_lines, *self.upfront_lines)
        )
        mortgage = "-" if self.mortgage is None else ",".join(self.mortgage.evidence_ids)
        return f"{self.mode.value}|{mortgage}|{lines}"
