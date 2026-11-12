"""Runtime type check shared by the engine's value types."""


def is_a(value: object, kind: type) -> bool:
    """Whether ``value`` is an instance of ``kind``.

    The engine's public functions are typed, but callers may still pass anything, so they check at
    runtime. Never use this for int: bool passes it; use ``type(x) is int``.
    Going through ``object`` keeps mypy from treating those checks as unreachable code.
    """
    return isinstance(value, kind)


INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1


def check_int32(value: object, name: str) -> None:
    """Check that ``value`` is a whole number that fits in a signed 32-bit integer.

    The C# engine holds these numbers (steps, years, basis points) as 32-bit ``int``, so the
    Python engine keeps the same limit. A value of another type raises ``TypeError``; a number
    out of range raises ``ValueError``. ``bool`` is rejected, as it is not a whole number here.
    """
    if type(value) is not int:
        message = f"{name} must be a whole number (int)."
        raise TypeError(message)
    if not INT32_MIN <= value <= INT32_MAX:
        message = f"{name} must fit in a signed 32-bit integer."
        raise ValueError(message)
