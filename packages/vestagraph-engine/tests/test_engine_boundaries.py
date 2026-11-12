"""Worked rounding cases read from rounding-boundaries.json (decision 0034).

Expectations come only from the file, which was worked by hand; never from the engine.
"""

import json
from fractions import Fraction
from pathlib import Path

import pytest
from vestagraph_engine import Pence, round_ratio


def _repository_root() -> Path:
    for folder in Path(__file__).resolve().parents:
        if (folder / "packages" / "fixtures" / "test-cases").is_dir():
            return folder
    message = "Repository root not found above the test file."
    raise FileNotFoundError(message)


def _cases() -> list[dict[str, dict[str, object]]]:
    path = _repository_root() / "packages" / "fixtures" / "test-cases" / "rounding-boundaries.json"
    document = json.loads(path.read_text(encoding="utf-8"), parse_float=Fraction)
    cases: list[dict[str, dict[str, object]]] = document["cases"]
    return cases


def _cases_with(input_key: str, expected_key: str) -> list[tuple[str, str, int]]:
    return [
        (str(case["id"]), str(case["inputs"][input_key]), int(str(case["expected"][expected_key])))
        for case in _cases()
        if input_key in case["inputs"]
    ]


DIRECT = _cases_with("unroundedPence", "pence")
ANNUAL = _cases_with("annualPence", "monthlyPence")


def test_boundary_file_loaded_has_all_six_direct_rounding_cases() -> None:
    assert len(DIRECT) == 6


def test_boundary_file_loaded_has_the_annual_to_monthly_cases() -> None:
    assert len(ANNUAL) == 14


@pytest.mark.parametrize(("case_id", "unrounded", "expected"), DIRECT, ids=[c[0] for c in DIRECT])
def test_round_ratio_boundary_case_from_file_matches_worked_result(
    case_id: str, unrounded: str, expected: int
) -> None:
    exact = Fraction(unrounded)
    assert round_ratio(exact.numerator, exact.denominator) == Pence(expected), case_id
    assert Pence.from_exact(exact) == Pence(expected), case_id


@pytest.mark.parametrize(("case_id", "annual", "expected"), ANNUAL, ids=[c[0] for c in ANNUAL])
def test_annual_to_monthly_boundary_case_from_file_matches_worked_result(
    case_id: str, annual: str, expected: int
) -> None:
    assert Pence(int(annual)).annual_to_monthly() == Pence(expected), case_id
