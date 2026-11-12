"""Checks fixture files against their JSON Schema 2020-12 schemas (decision 0018, BE-07).

Ported from the C# ``FixtureValidator.cs``. Convention: ``data/NAME.json`` is checked against
``schema/NAME.schema.json``. Any file in ``test-cases/`` or ``generated/`` names its schema in a
top-level ``$schema`` field (a path relative to the file, such as
``../schema/test-case.schema.json``).

The two validators must accept and reject exactly the same files, so each place where the Python
library behaves differently from JsonSchema.Net (the C# library) is settled here and tested in
``tests/test_fixtures_parity_probes.py``:

* ``format`` is an annotation, never an assertion. The library only checks it when given a
  format checker, and none is given. (JsonSchema.Net's 2020-12 default is the same.)
* Decimals are read as exact fractions (``Fraction``), so ``minimum``, ``maximum`` and
  ``multipleOf`` are exact, and a whole-valued decimal such as ``5.0`` or ``1e2`` is an integer.
* ``pattern`` is ASCII only (``\\d`` is 0-9), as .NET's ECMAScript mode is; Python's default
  would also accept other scripts' digits.
* A ``$ref`` is resolved only from the schema files in the schema folder, by their ``$id``.
  Nothing is ever fetched from the network; an unknown reference is reported as a problem.
"""

import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

# jsonschema ships no type information, and no stub package is added (P5 adds no packages).
from jsonschema import Draft202012Validator, TypeChecker, validators  # type: ignore[import-untyped]
from jsonschema.exceptions import ValidationError  # type: ignore[import-untyped]
from referencing import Registry, Resource
from referencing.exceptions import CannotDetermineSpecification, Unresolvable
from referencing.jsonschema import DRAFT202012

SCHEMA_SUFFIX = ".schema.json"


@dataclass(frozen=True)
class FixtureProblem:
    """One thing wrong with one fixture file."""

    file: str
    location: str
    message: str

    def __str__(self) -> str:
        return f"{self.file}: {self.location}: {self.message}"


def find_repository_root(start: Path) -> Path:
    """The nearest folder at or above ``start`` that holds ``packages/fixtures/schema``."""
    for folder in (start.resolve(), *start.resolve().parents):
        if (folder / "packages" / "fixtures" / "schema").is_dir():
            return folder
    message = f"packages/fixtures/schema not found above {start}."
    raise FileNotFoundError(message)


# --- The validator class ----------------------------------------------------------------------


def _is_integer(_checker: TypeChecker, instance: object) -> bool:
    """JSON Schema 2020-12: a number with no fractional part is an integer (``5.0``, ``1e2``)."""
    if isinstance(instance, bool):
        return False
    if isinstance(instance, int):
        return True
    if isinstance(instance, Fraction):
        return instance.denominator == 1
    return isinstance(instance, float) and instance.is_integer()


def _pattern(
    validator: Draft202012Validator, pattern: str, instance: object, _schema: object
) -> Iterator[ValidationError]:
    # Same as the library's own ``pattern`` (an unanchored search), but ASCII only.
    if validator.is_type(instance, "string") and not re.search(pattern, str(instance), re.ASCII):
        yield ValidationError(f"{instance!r} does not match {pattern!r}")


def _properties(
    validator: Draft202012Validator, properties: dict[str, Any], instance: object, _schema: object
) -> Iterator[ValidationError]:
    # Same as the library's own ``properties``, with one fix: jsonschema 4.26 leaves the property
    # name out of the path of an error from a ``false`` subschema (``"value": false`` in our
    # schemas means "no value here"), so the pointer would name the parent instead of the property.
    # Errors from other subschemas already carry the name. ``false`` under any other keyword that
    # adds a path part (items, patternProperties...) would lose it the same way; a test checks that
    # the schemas use none.
    if not isinstance(instance, dict):
        return
    for name, subschema in properties.items():
        if name in instance:
            for error in validator.descend(instance[name], subschema, path=name, schema_path=name):
                if subschema is False:
                    error.path.appendleft(name)
                    error.schema_path.appendleft(name)
                yield error


_Validator = validators.extend(
    Draft202012Validator,
    validators={"pattern": _pattern, "properties": _properties},
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine("integer", _is_integer),
)


# --- Reading ----------------------------------------------------------------------------------


def _reject_constant(name: str) -> object:
    message = f"{name} is not allowed in JSON"
    raise ValueError(message)


def _parse(text: str) -> Any:
    """Read JSON text with decimals as exact fractions, rejecting NaN and Infinity."""
    return json.loads(text, parse_float=Fraction, parse_constant=_reject_constant)


def _read_text(path: Path) -> str:
    # Like .NET's File.ReadAllText: a byte-order mark is dropped and bytes that are not UTF-8 are
    # replaced, not rejected.
    return path.read_bytes().decode("utf-8-sig", errors="replace")


def _load_registry(schema_directory: Path) -> tuple[Registry[Any], dict[str, Any]]:
    """Every ``*.schema.json`` file, registered under its ``$id`` so ``$ref`` finds it."""
    registry: Registry[Any] = Registry()
    by_file_name: dict[str, Any] = {}
    for path in sorted(schema_directory.glob("*" + SCHEMA_SUFFIX)):
        contents = _parse(_read_text(path))
        resource = Resource.from_contents(contents, default_specification=DRAFT202012)
        registry = registry.with_resource(resource.id() or f"urn:vestagraph:{path.name}", resource)
        by_file_name[path.name] = contents
    return registry, by_file_name


# --- Validating -------------------------------------------------------------------------------


def _pointer(path: Any) -> str:
    """A JSON Pointer (RFC 6901) for a path of keys and indexes; the whole value is ``/``."""
    parts = [str(part).replace("~", "~0").replace("/", "~1") for part in path]
    return "/" + "/".join(parts)


def _decimal_text(match: re.Match[str]) -> str:
    fraction = Fraction(int(match.group(1)), int(match.group(2)))
    if fraction.denominator == 1:
        return str(fraction.numerator)
    remaining = fraction.denominator
    for factor in (2, 5):
        while remaining % factor == 0:
            remaining //= factor
    if remaining == 1:
        return format(Decimal(fraction.numerator) / Decimal(fraction.denominator), "f")
    return f"{fraction.numerator}/{fraction.denominator}"


def _readable(message: str) -> str:
    """Show an exact fraction as written (``240000.5``), not as ``Fraction(480001, 2)``."""
    return re.sub(r"Fraction\((-?\d+), (\d+)\)", _decimal_text, message)


def _problems_of(error: ValidationError, schema_file_name: str) -> Iterator[FixtureProblem]:
    yield FixtureProblem(
        schema_file_name,
        _pointer(error.absolute_path),
        f"{error.validator}: {_readable(error.message)}",
    )
    for child in error.context or []:
        yield from _problems_of(child, schema_file_name)


def validate_instance(
    instance: Any, schema_file_name: str, schema_directory: Path
) -> list[FixtureProblem]:
    """Check one parsed JSON value against a schema file in ``schema_directory``."""
    if not schema_directory.is_dir():
        return [
            FixtureProblem(schema_file_name, "/", f"Schema folder not found: {schema_directory}.")
        ]

    # Each call uses its own registry. Every schema is loaded first so that
    # "$ref": "common.schema.json#/..." resolves against the $id of the shared definitions.
    try:
        registry, schemas = _load_registry(schema_directory)
    except (ValueError, CannotDetermineSpecification) as exception:
        return [
            FixtureProblem(schema_file_name, "/", f"A schema file could not be loaded: {exception}")
        ]

    target = schemas.get(schema_file_name)
    if target is None:
        return [
            FixtureProblem(schema_file_name, "/", f"Schema file not found in {schema_directory}.")
        ]

    try:
        errors = list(_Validator(target, registry=registry).iter_errors(instance))
    except Unresolvable as exception:
        return [FixtureProblem(schema_file_name, "/", f"A $ref could not be resolved: {exception}")]

    problems: list[FixtureProblem] = []
    for error in errors:
        for problem in _problems_of(error, schema_file_name):
            if problem not in problems:
                problems.append(problem)
    return problems


def _json_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        (p for p in directory.iterdir() if p.is_file() and p.name.endswith(".json")),
        key=lambda p: p.name,
    )


def _file_name(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def _validate_file(
    path: Path,
    expected_schema: str | None,
    schema_directory: Path,
) -> list[FixtureProblem]:
    name = path.name
    try:
        instance = _parse(_read_text(path))
    except (ValueError, RecursionError) as exception:
        return [FixtureProblem(name, "/", f"Not valid JSON: {exception}")]

    declared = instance.get("$schema") if isinstance(instance, dict) else None
    if declared is not None and not isinstance(declared, str):
        return [
            FixtureProblem(
                name,
                "/$schema",
                'Must be a string naming the schema, for example "../schema/NAME.schema.json".',
            )
        ]

    declared_name = None if declared is None else _file_name(declared)
    schema_name = expected_schema if expected_schema is not None else declared_name

    if schema_name is None:
        return [
            FixtureProblem(
                name,
                "/$schema",
                "Missing: name the schema this file follows, "
                'for example "../schema/NAME.schema.json".',
            )
        ]

    if (
        declared_name is not None
        and expected_schema is not None
        and declared_name != expected_schema
    ):
        return [
            FixtureProblem(
                name,
                "/$schema",
                f"Names {declared_name} but the file name requires {expected_schema}.",
            )
        ]

    return [
        FixtureProblem(name, p.location, p.message)
        for p in validate_instance(instance, schema_name, schema_directory)
    ]


def validate_fixtures(fixtures_directory: Path) -> list[FixtureProblem]:
    """Check every data file, test case and generated file under a ``packages/fixtures`` folder."""
    problems: list[FixtureProblem] = []
    schema_directory = fixtures_directory / "schema"
    checked_files = 0

    for path in _json_files(fixtures_directory / "data"):
        checked_files += 1
        expected = path.name.removesuffix(".json") + SCHEMA_SUFFIX
        problems.extend(_validate_file(path, expected, schema_directory))

    for folder in ("test-cases", "generated"):
        # The generator's output lives in generated/. The folder may be absent; make generated-check
        # insists the committed file is current.
        for path in _json_files(fixtures_directory / folder):
            checked_files += 1
            problems.extend(_validate_file(path, None, schema_directory))

    if checked_files == 0:
        problems.append(
            FixtureProblem(
                str(fixtures_directory),
                "/",
                "No fixture files found in data/, test-cases/ or generated/.",
            )
        )
    return problems
