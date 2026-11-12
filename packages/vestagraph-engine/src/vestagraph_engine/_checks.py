"""Runtime type check shared by the engine's value types."""


def is_a(value: object, kind: type) -> bool:
    """Whether ``value`` is an instance of ``kind``.

    The engine's public functions are typed, but callers may still pass anything, so they check at
    runtime. Never use this for int: bool passes it; use ``type(x) is int``.
    Going through ``object`` keeps mypy from treating those checks as unreachable code.
    """
    return isinstance(value, kind)
