"""Architecture test: the engine stays pure and does its money arithmetic in one place.

Replaces the C# NetArchTest rules (decision 0039 section 2). It reads every .py file under
vestagraph_engine/ with ``ast`` and applies the rules below. Each rule also has a test that applies
it to a small bad source string and expects a violation, so a rule that silently matches nothing is
caught (the C# ``*_failsAsExpected`` tests).
"""

import ast
from importlib import import_module
from pathlib import Path

import pytest

OWN_PACKAGE = "vestagraph_engine"
# The only imports the engine may make, and only as `from <module> import <name>` so nothing can be
# reached through a module object (`fractions.math`, `typing.sys`). Extend only with a reason:
#   dataclasses, enum, typing: value types; fractions: exact rational input for Pence.from_exact;
#   collections.abc: abstract types for later cost lines. Nothing here reads a clock, a file, the
#   network, the environment or a random number.
ALLOWED_IMPORTS: dict[str, frozenset[str]] = {
    "__future__": frozenset({"annotations"}),
    "dataclasses": frozenset({"dataclass"}),
    "enum": frozenset({"Enum"}),
    "fractions": frozenset({"Fraction"}),
    "typing": frozenset({"ClassVar", "Final", "Literal", "Never", "Protocol", "Self", "overload"}),
    "collections.abc": frozenset(
        {"Callable", "Iterable", "Iterator", "Mapping", "Sequence", "Set"}
    ),
}
FORBIDDEN_NAMES = frozenset(
    {"float", "round", "eval", "exec", "open", "__import__", "input", "print"}
)
FORBIDDEN_ATTRIBUTES = frozenset({"now", "today", "utcnow"})
# Dunder routes to division, truncation or rounding that would sidestep the rules below.
FORBIDDEN_DUNDERS = frozenset(
    {
        "__floordiv__",
        "__mod__",
        "__divmod__",
        "__truediv__",
        "__rshift__",
        "__floor__",
        "__trunc__",
        "__round__",
        "__int__",
    }
)
# Division in any form is only allowed inside this one module-level function, in this one module
# (and `/` nowhere: it makes a float; register line BE-32).
DIVISION_FUNCTION = "round_ratio"
DIVISION_MODULE = "pence.py"
DIVISION_OPERATORS = (ast.FloorDiv, ast.Mod, ast.RShift)


class _Rules(ast.NodeVisitor):
    def __init__(self, filename: str) -> None:
        self.violations: list[str] = []
        self._may_divide_here = filename == DIVISION_MODULE
        self._scope: list[ast.AST] = []  # enclosing functions and classes, outermost first
        self._exempt_depth = 0

    def _report(self, node: ast.AST, text: str) -> None:
        self.violations.append(f"line {getattr(node, 'lineno', '?')}: {text}")

    def _exempt(self) -> bool:
        return self._exempt_depth > 0

    def _enter_scope(self, node: ast.FunctionDef | ast.ClassDef) -> None:
        # Exempt only a function defined directly at module level: not nested, not a method.
        is_the_function = (
            isinstance(node, ast.FunctionDef)
            and node.name == DIVISION_FUNCTION
            and not self._scope
            and self._may_divide_here
        )
        self._scope.append(node)
        self._exempt_depth += is_the_function
        self.generic_visit(node)
        self._exempt_depth -= is_the_function
        self._scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._enter_scope(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._enter_scope(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name.split(".")[0] != OWN_PACKAGE:
                self._report(node, f"plain import of {alias.name}: use `from ... import Name`")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level > 0 or (node.module or "").split(".")[0] == OWN_PACKAGE:
            return  # inside this package
        module = node.module or ""
        allowed = ALLOWED_IMPORTS.get(module)
        if allowed is None:
            self._report(node, f"import from {module} is not on the allow-list")
            return
        for alias in node.names:
            if alias.name not in allowed:
                self._report(node, f"import of {module}.{alias.name} is not on the allow-list")

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, float | complex):
            self._report(node, "float or complex literal")

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in FORBIDDEN_NAMES:
            self._report(node, f"use of {node.id}")
        if node.id == "divmod" and not self._exempt():
            self._report(node, f"divmod outside {DIVISION_FUNCTION}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr in FORBIDDEN_ATTRIBUTES:
            self._report(node, f"use of .{node.attr} (clock)")
        if node.attr in FORBIDDEN_DUNDERS:
            self._report(node, f"use of .{node.attr} (sidesteps the division rules)")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id == "int" and not self._exempt():
                self._report(node, f"int(...) outside {DIVISION_FUNCTION}")
            if node.func.id == "pow" and not (
                len(node.args) == 2 and _is_non_negative_int(node.args[1])
            ):
                self._report(node, "pow(...) needs two arguments and a non-negative int exponent")
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self._check_operator(node, node.op, node.right)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._check_operator(node, node.op, node.value)
        self.generic_visit(node)

    def _check_operator(self, node: ast.AST, operator: ast.operator, right: ast.expr) -> None:
        if isinstance(operator, ast.Div):
            self._report(node, "true division (/) makes a float")
        elif isinstance(operator, DIVISION_OPERATORS) and not self._exempt():
            self._report(node, f"//, % or >> outside {DIVISION_FUNCTION}")
        elif isinstance(operator, ast.Pow) and not _is_non_negative_int(right):
            self._report(node, "** needs a non-negative int constant exponent")


def _is_non_negative_int(node: ast.expr) -> bool:
    return isinstance(node, ast.Constant) and type(node.value) is int and node.value >= 0


def violations_in(source: str, filename: str = DIVISION_MODULE) -> list[str]:
    rules = _Rules(filename)
    rules.visit(ast.parse(source))
    return rules.violations


def _engine_files() -> list[Path]:
    package = import_module(OWN_PACKAGE)
    assert package.__file__ is not None
    files = sorted(Path(package.__file__).parent.rglob("*.py"))
    assert files, "no engine source files found"
    return files


def test_engine_sources_found_include_the_money_modules() -> None:
    names = {path.name for path in _engine_files()}
    assert {"pence.py", "result.py", "__init__.py"} <= names


@pytest.mark.parametrize("path", _engine_files(), ids=lambda p: p.name)
def test_engine_source_obeys_every_purity_rule(path: Path) -> None:
    assert violations_in(path.read_text(encoding="utf-8"), path.name) == []


# Each rule applied to a small bad source string: it must fail, or the rule matches nothing.


@pytest.mark.parametrize(
    "source",
    [
        "import random",
        "import os",
        "import json",
        "import decimal",
        "import math",
        "import datetime",
        "from pathlib import Path",
        "from vestagraph_generator import something",
        "import vestagraph_fixture_validator",
        "from collections import OrderedDict",
        "import time",
        "import uuid",
    ],
)
def test_import_rule_applied_to_a_disallowed_import_fails_as_expected(source: str) -> None:
    assert violations_in(source)


@pytest.mark.parametrize(
    "source",
    [
        "from fractions import Fraction",
        "from dataclasses import dataclass",
        "from enum import Enum",
        "from typing import ClassVar",
        "from collections.abc import Sequence",
        "from vestagraph_engine.pence import Pence",
        "from . import pence",
        "from __future__ import annotations",
    ],
)
def test_import_rule_applied_to_an_allowed_import_passes(source: str) -> None:
    assert violations_in(source) == []


@pytest.mark.parametrize("name", sorted(FORBIDDEN_NAMES))
def test_forbidden_name_rule_applied_to_code_using_it_fails_as_expected(name: str) -> None:
    assert violations_in(f"x = {name}")


def test_forbidden_name_rule_applied_to_a_float_annotation_fails_as_expected() -> None:
    assert violations_in("def f(x: float) -> None: ...")


@pytest.mark.parametrize("attribute", sorted(FORBIDDEN_ATTRIBUTES))
def test_clock_rule_applied_to_code_that_reads_the_time_fails_as_expected(attribute: str) -> None:
    assert violations_in(f"x = something.{attribute}()")


@pytest.mark.parametrize(
    "source",
    [
        "x = a // b",
        "x = a % b",
        "x //= b",
        "x %= b",
        "x = divmod(a, b)",
        "x = int(a)",
        "def other():\n    return a // b",
        "def other():\n    return divmod(a, b)",
        "def other():\n    return int(a)",
    ],
)
def test_division_rule_applied_to_division_outside_round_ratio_fails_as_expected(
    source: str,
) -> None:
    assert violations_in(source)


@pytest.mark.parametrize("source", ["x = a / b", "x /= b", "def round_ratio():\n    return a / b"])
def test_true_division_rule_applied_to_true_division_fails_as_expected(source: str) -> None:
    assert violations_in(source)


def test_division_rule_applied_to_division_inside_round_ratio_passes() -> None:
    source = (
        "def round_ratio(n, d):\n"
        "    q, r = divmod(n, d)\n"
        "    a = n // d\n"
        "    b = n % d\n"
        "    c = int(n)\n"
        "    return q + a + b + c\n"
    )
    assert violations_in(source) == []


@pytest.mark.parametrize(
    "source",
    [
        "def other():\n    def round_ratio():\n        return a // b",
        "class X:\n    def round_ratio(self):\n        return a // b",
        "class round_ratio:\n    x = a // b",
    ],
)
def test_division_exemption_applied_to_a_nested_or_method_round_ratio_fails_as_expected(
    source: str,
) -> None:
    assert violations_in(source)


def test_division_exemption_applied_to_round_ratio_in_another_module_fails_as_expected() -> None:
    assert violations_in("def round_ratio(n, d):\n    return n // d", "other.py")


@pytest.mark.parametrize("source", ["x = 0.5 * a", "x = 1e3", "x = 2j", "x = -1.0"])
def test_float_literal_rule_applied_to_float_or_complex_constants_fails_as_expected(
    source: str,
) -> None:
    assert violations_in(source)


@pytest.mark.parametrize("source", ["x = a >> 1", "x >>= 1"])
def test_shift_rule_applied_to_right_shift_outside_round_ratio_fails_as_expected(
    source: str,
) -> None:
    assert violations_in(source)


@pytest.mark.parametrize(
    "source",
    [
        "x = a ** -1",
        "x = a ** b",
        "x = a ** 0.5",
        "x **= -1",
        "x = pow(a, -1)",
        "x = pow(a, b)",
        "x = pow(a, 2, 5)",
        "x = pow(a)",
    ],
)
def test_power_rule_applied_to_a_negative_or_unknown_exponent_fails_as_expected(
    source: str,
) -> None:
    assert violations_in(source)


@pytest.mark.parametrize("source", ["x = a ** 2", "x **= 3", "x = pow(a, 2)", "x = a ** 0"])
def test_power_rule_applied_to_a_non_negative_int_exponent_passes(source: str) -> None:
    assert violations_in(source) == []


@pytest.mark.parametrize("attribute", sorted(FORBIDDEN_DUNDERS))
def test_dunder_rule_applied_to_a_route_around_the_division_rules_fails_as_expected(
    attribute: str,
) -> None:
    assert violations_in(f"x = a.{attribute}(b)")


@pytest.mark.parametrize(
    "source",
    [
        "import fractions\nx = fractions.math.floor(a)",
        "import fractions",
        "import dataclasses",
        "import typing",
        "from typing import sys",
        "from fractions import math",
        "from fractions import *",
        "from collections.abc import ClassVar",
    ],
)
def test_import_rule_applied_to_a_plain_import_or_reach_through_fails_as_expected(
    source: str,
) -> None:
    assert violations_in(source)
