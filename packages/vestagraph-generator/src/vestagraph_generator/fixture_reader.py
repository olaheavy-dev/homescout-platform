"""Reads the fixture data files into the engine's own types (ported from the C# ``FixtureReader``).

The files are checked against their schemas by ``make validate``. Anything this reader does not
understand is an ``InvalidDataError`` rather than a guess; a missing file is an ``OSError``.
Decimals are read as exact ``Fraction`` values (``parse_float=Fraction``, so no ``float`` is ever
made); the whole-number check is the guard that refuses them where a whole number belongs
(AGENTS rule 2). NaN and Infinity are refused, and whole numbers must fit the C# reader's 32 bits
(64 for pence).
"""

import json
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_engine import (
    EvidenceItem,
    EvidenceStatus,
    EvidenceValue,
    Mode,
    MoneyValue,
    Nation,
    OtherValue,
    Pence,
    Period,
    RateValue,
    YearsValue,
)


class InvalidDataError(ValueError):
    """A data file holds something the reader does not understand."""


@dataclass(frozen=True, slots=True)
class StoryData:
    """A story: its steps in order, and the homes it covers."""

    id: str
    steps: tuple[int, ...]
    home_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HomeData:
    """A home as the data file describes it; ``mode`` is ``None`` when the data does not say."""

    id: str
    mode: Mode | None
    nation: Nation


@dataclass(frozen=True, slots=True)
class EvidenceRow:
    """One evidence item and whom it is about."""

    subject_type: str
    subject_id: str
    item: EvidenceItem


@dataclass(frozen=True, slots=True)
class FixtureData:
    """Everything the generator reads from ``packages/fixtures/data``."""

    snapshot_date: str
    household_id: str
    home_ids: tuple[str, ...]
    stories: tuple[StoryData, ...]
    homes: tuple[HomeData, ...]
    monthly_budget: Pence
    evidence: tuple[EvidenceRow, ...]


def read_fixtures(fixtures_directory: Path) -> FixtureData:
    """Read the data files under ``fixtures_directory/data``."""
    snapshot = _object(_load(fixtures_directory, "snapshot"), "snapshot", "snapshot.json")
    household = _object(_load(fixtures_directory, "household"), "household", "household.json")
    homes = _list(_load(fixtures_directory, "homes"), "homes", "homes.json")
    evidence = _list(_load(fixtures_directory, "evidence"), "evidence", "evidence.json")

    return FixtureData(
        snapshot_date=_text(snapshot, "snapshotDate"),
        household_id=_text(snapshot, "householdId"),
        home_ids=tuple(_as_text(i, "homeIds") for i in _list(snapshot, "homeIds")),
        stories=tuple(_read_story(s) for s in _list(snapshot, "stories")),
        homes=tuple(_read_home(h) for h in homes),
        monthly_budget=_read_budget(household),
        evidence=tuple(_read_evidence(e) for e in evidence),
    )


def _refuse_constant(text: str) -> object:
    raise InvalidDataError(
        f"A data file holds {text}, which is not a number the generator accepts."
    )


def _load(fixtures_directory: Path, name: str) -> Any:
    path = fixtures_directory / "data" / f"{name}.json"
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text, parse_float=Fraction, parse_constant=_refuse_constant)
    except UnicodeDecodeError as exception:
        message = f"{path} is not valid UTF-8 text: {exception}"
        raise InvalidDataError(message) from exception
    except InvalidDataError as exception:
        message = f"{path}: {exception}"
        raise InvalidDataError(message) from exception
    except ValueError as exception:
        # Bad JSON, or a whole number with more digits than Python converts (4300).
        message = f"{path} is not valid JSON: {exception}"
        raise InvalidDataError(message) from exception


def _invalid(message: str) -> InvalidDataError:
    return InvalidDataError(message)


def _object(parent: Any, key: str, where: str) -> dict[str, Any]:
    """The object under ``key`` of a file's top-level object."""
    if not isinstance(parent, dict):
        raise _invalid(f"{where} must hold a JSON object.")
    found = parent.get(key)
    if found is None:
        raise _invalid(f"{where} has no {key}.")
    if not isinstance(found, dict):
        raise _invalid(f"{where}: {key} must be a JSON object.")
    return found


def _list(parent: Any, key: str, where: str = "A data file") -> list[Any]:
    """The list under ``key`` of an object."""
    if not isinstance(parent, dict):
        raise _invalid(f"{where} must hold a JSON object.")
    found = parent.get(key)
    if found is None:
        raise _invalid(f"A required list '{key}' is missing.")
    if not isinstance(found, list):
        raise _invalid(f"A data file has a value of the wrong type: '{key}' must be a list.")
    return found


def _node(parent: Any, what: str) -> dict[str, Any]:
    if not isinstance(parent, dict):
        raise _invalid(f"A data file has a value of the wrong type: {what} must be an object.")
    return parent


def _as_text(value: Any, key: str) -> str:
    if not isinstance(value, str):
        raise _invalid(f"A data file has a value of the wrong type: '{key}' must be text.")
    return value


def _as_whole_number(value: Any, key: str, bits: int = 32) -> int:
    # bool is a subclass of int and a decimal is read as a Fraction: neither is a whole number.
    # The range is the signed size the C# reader used (32 bits, 64 for pence).
    if type(value) is not int:
        raise _invalid(
            f"A data file has a value of the wrong type: '{key}' must be a whole number."
        )
    if not -(2 ** (bits - 1)) <= value < 2 ** (bits - 1):
        raise _invalid(f"A data file has a value out of range: '{key}' must fit in {bits} bits.")
    return value


def _text(node: dict[str, Any], key: str) -> str:
    value = node.get(key)
    if value is None:
        raise _invalid(f"A required text field '{key}' is missing.")
    return _as_text(value, key)


def _number(node: dict[str, Any], key: str, bits: int = 32) -> int:
    value = node.get(key)
    if value is None:
        raise _invalid(f"A required number field '{key}' is missing.")
    return _as_whole_number(value, key, bits)


def _enum[E: Enum](kind: type[E], text: str, what: str) -> E:
    for member in kind:
        if member.value == text:
            return member
    raise _invalid(f"Unknown {what} '{text}'.")


def _read_story(story: Any) -> StoryData:
    node = _node(story, "a story")
    return StoryData(
        id=_text(node, "id"),
        steps=tuple(_number(_node(s, "a story step"), "step") for s in _list(node, "steps")),
        home_ids=tuple(_as_text(i, "homeIds") for i in _list(node, "homeIds")),
    )


def _read_home(home: Any) -> HomeData:
    node = _node(home, "a home")
    mode_text = node.get("mode")
    mode = None if mode_text is None else _enum(Mode, _as_text(mode_text, "mode"), "mode")
    address = node.get("address")
    if address is None:
        raise _invalid("A home has no address.")
    nation = _enum(Nation, _text(_node(address, "an address"), "nation"), "nation")
    return HomeData(_text(node, "id"), mode, nation)


def _read_budget(household: dict[str, Any]) -> Pence:
    budget = household.get("monthlyBudget")
    if budget is None:
        raise _invalid("The household has no monthlyBudget.")
    node = _node(budget, "monthlyBudget")
    if _text(node, "period") != "month":
        raise _invalid("The household budget must be a monthly amount.")
    return _read_pence(node, "The household budget has no pence.")


def _read_pence(node: dict[str, Any], missing: str) -> Pence:
    if node.get("pence") is None:
        raise _invalid(missing)
    return Pence(_number(node, "pence", 64))


def _read_evidence(item: Any) -> EvidenceRow:
    node = _node(item, "an evidence item")
    status = _enum(EvidenceStatus, _text(node, "status"), "evidence status")
    evidence_id = _text(node, "id")
    context_only = node.get("contextOnly")
    if not isinstance(context_only, bool):
        raise _invalid(f"{evidence_id} has no contextOnly.")
    used_from = node.get("usedFromStep")
    supersedes = node.get("supersedes")
    value = node.get("value")

    evidence = EvidenceItem(
        evidence_id,
        _text(node, "category"),
        status,
        None if value is None else _read_value(_node(value, "a value")),
        context_only,
        None if used_from is None else _as_whole_number(used_from, "usedFromStep"),
        None if supersedes is None else _as_text(supersedes, "supersedes"),
    )
    return EvidenceRow(_text(node, "subjectType"), _text(node, "subjectId"), evidence)


def _read_value(value: dict[str, Any]) -> EvidenceValue:
    kind = _text(value, "kind")
    if kind == "money":
        pence = _read_pence(value, "A money value has no pence.")
        return MoneyValue(pence, _enum(Period, _text(value, "period"), "period"))
    if kind == "rate":
        return RateValue(_number(value, "basisPoints"))
    if kind == "quantity" and _text(value, "unit") == "years":
        return YearsValue(_number(value, "amount"))
    return OtherValue()
