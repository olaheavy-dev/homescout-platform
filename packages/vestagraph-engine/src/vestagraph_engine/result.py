"""Expected failures as values (decisions 0021, 0032).

``Result`` is for expected failures only; programming errors raise.
"""

from dataclasses import dataclass
from enum import Enum

from vestagraph_engine._checks import is_a


class ErrorCategory(Enum):
    """The four kinds of expected failure that were decided."""

    VALIDATION = "validation"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class Error:
    """What went wrong: a machine-readable code, a message for people, and a category."""

    code: str
    message: str
    category: ErrorCategory

    def __post_init__(self) -> None:
        if not is_a(self.code, str) or not self.code.strip():
            message = "An error needs a code that is not blank."
            raise ValueError(message)
        if not is_a(self.message, str) or not self.message.strip():
            message = "An error needs a message that is not blank."
            raise ValueError(message)
        if not is_a(self.category, ErrorCategory):
            message = "An error category must be an ErrorCategory."
            raise TypeError(message)


@dataclass(frozen=True, slots=True)
class Result[T]:
    """A value or an ``Error``. Build one with ``success``, ``ok``, ``failure``."""

    _value: T | None
    _error: Error | None

    @staticmethod
    def success[V](value: V) -> Result[V]:
        """A success carrying ``value``. ``None`` is rejected; use ``ok`` for no value."""
        if value is None:
            message = "A successful result needs a value; use Result.ok() for none."
            raise ValueError(message)
        return Result(value, None)

    @staticmethod
    def ok() -> Result[None]:
        """A success with no value."""
        return Result(None, None)

    @staticmethod
    def failure[V](error: Error) -> Result[V]:
        """A failure carrying ``error``."""
        if not is_a(error, Error):
            message = "A failed result needs an Error."
            raise TypeError(message)
        return Result(None, error)

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    @property
    def value(self) -> T:
        """The value. Raises ``RuntimeError`` on a failure (or on a success that has no value)."""
        if self._error is not None:
            message = "A failed result has no value."
            raise RuntimeError(message)
        if self._value is None:
            message = "This successful result carries no value."
            raise RuntimeError(message)
        return self._value

    @property
    def error(self) -> Error:
        """The error. Raises ``RuntimeError`` on a success."""
        if self._error is None:
            message = "A successful result has no error."
            raise RuntimeError(message)
        return self._error

    def to_result(self) -> Result[None]:
        """Drop the value, keeping only success or the error."""
        return Result(None, self._error)
