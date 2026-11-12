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
# Standard-library modules the engine may import. Extend only with a reason:
#   dataclasses, enum, typing: value types; fractions: exact rational input for Pence.from_exact;
#   collections.abc: abstract types for later cost lines. Nothing here can read a clock, a file,
#   the network, the environment or a random number.
ALLOWED_IMPORTS = frozenset(
    {"__future__", "dataclasses", "enum", "fractions", "typing", "collections"}
)
ALLOWED_COLLECTIONS_SUBMODULES = frozenset({"collections.abc"})
FORBIDDEN_NAMES = frozenset(
    {"float", "round", "eval", "exec", "open", "__import__", "input", "print"}
)
FORBIDDEN_ATTRIBUTES = frozenset({"now", "today", "utcnow"})
# Division in any form is only allowed inside this one function (and `/` nowhere: it makes a float).
DIVISION_FUNCTION = "round_ratio"
DIVISION_OPERATORS = (ast.FloorDiv, ast.Mod)


class _Rules(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[str] = []
        self._functions: list[str] = []

    def _report(self, node: ast.AST, text: str) -> None:
        self.violations.append(f"line {getattr(node, 'lineno', '?')}: {text}")

    def _in_division_function(self) -> bool:
        return DIVISION_FUNCTION in self._functions

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._functions.append(node.name)
        self.generic_visit(node)
        self._functions.pop()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._check_module(node, alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level > 0:
            return  # a relative import stays inside this package
        self._check_module(node, node.module or "")

    def _check_module(self, node: ast.AST, module: str) -> None:
        top = module.split(".")[0]
        if top == OWN_PACKAGE:
            return
        if top == "collections":
            if module not in ALLOWED_COLLECTIONS_SUBMODULES:
                self._report(node, f"import of {module} (only collections.abc is allowed)")
            return
        if top not in ALLOWED_IMPORTS:
            self._report(node, f"import of {module} is not on the allow-list")

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in FORBIDDEN_NAMES:
            self._report(node, f"use of {node.id}")
        if node.id == "divmod" and not self._in_division_function():
            self._report(node, f"divmod outside {DIVISION_FUNCTION}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr in FORBIDDEN_ATTRIBUTES:
            self._report(node, f"use of .{node.attr} (clock)")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "int"
            and not self._in_division_function()
        ):
            self._report(node, f"int(...) outside {DIVISION_FUNCTION}")
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self._check_operator(node, node.op)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._check_operator(node, node.op)
        self.generic_visit(node)

    def _check_operator(self, node: ast.AST, operator: ast.operator) -> None:
        if isinstance(operator, ast.Div):
            self._report(node, "true division (/) makes a float")
        elif isinstance(operator, DIVISION_OPERATORS) and not self._in_division_function():
            self._report(node, f"// or % outside {DIVISION_FUNCTION}")


def violations_in(source: str) -> list[str]:
    rules = _Rules()
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
    assert violations_in(path.read_text(encoding="utf-8")) == []


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
