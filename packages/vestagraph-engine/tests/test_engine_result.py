"""Tests for Result, Error and ErrorCategory, ported from the C# ResultTests."""

import pytest
from vestagraph_engine import Error, ErrorCategory, Pence, Result

SAMPLE = Error("input.missing", "A required figure is missing.", ErrorCategory.VALIDATION)


def test_ok_no_value_is_success_with_no_error() -> None:
    result = Result.ok()
    assert result.is_success
    assert not result.is_failure
    with pytest.raises(RuntimeError):
        _ = result.error


def test_failure_with_error_is_failure_carrying_that_error() -> None:
    result: Result[Pence] = Result.failure(SAMPLE)
    assert not result.is_success
    assert result.is_failure
    assert result.error == SAMPLE


def test_failure_non_error_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Result.failure(None)  # type: ignore[arg-type]  # deliberately wrong type
    with pytest.raises(TypeError):
        Result.failure("oops")  # type: ignore[arg-type]  # deliberately wrong type


def test_success_with_value_exposes_value() -> None:
    result = Result.success(Pence(42))
    assert result.is_success
    assert result.value == Pence(42)
    with pytest.raises(RuntimeError):
        _ = result.error


def test_failure_of_t_with_error_hides_value_and_exposes_error() -> None:
    result: Result[Pence] = Result.failure(SAMPLE)
    assert result.is_failure
    assert result.error == SAMPLE
    with pytest.raises(RuntimeError):
        _ = result.value


def test_success_none_value_raises_value_error() -> None:
    with pytest.raises(ValueError, match="value"):
        Result.success(None)


def test_to_result_failure_keeps_error() -> None:
    typed: Result[Pence] = Result.failure(SAMPLE)
    untyped = typed.to_result()
    assert untyped.is_failure
    assert untyped.error == SAMPLE


def test_to_result_success_with_a_value_is_a_success() -> None:
    assert Result.success(Pence(1)).to_result().is_success


@pytest.mark.parametrize(
    "category",
    [
        ErrorCategory.VALIDATION,
        ErrorCategory.NOT_FOUND,
        ErrorCategory.CONFLICT,
        ErrorCategory.UNAVAILABLE,
    ],
)
def test_error_each_category_is_kept_on_the_error(category: ErrorCategory) -> None:
    error = Error("some.code", "Something went wrong.", category)
    assert error.category == category
    assert Result.failure(error).error.category == category


def test_error_category_defined_values_are_exactly_the_four_decided() -> None:
    assert {c.name for c in ErrorCategory} == {"VALIDATION", "NOT_FOUND", "CONFLICT", "UNAVAILABLE"}


@pytest.mark.parametrize("code", ["", "   "])
def test_error_blank_code_raises_value_error(code: str) -> None:
    with pytest.raises(ValueError, match="code"):
        Error(code, "Message.", ErrorCategory.VALIDATION)


@pytest.mark.parametrize("message", ["", "   "])
def test_error_blank_message_raises_value_error(message: str) -> None:
    with pytest.raises(ValueError, match="message"):
        Error("code", message, ErrorCategory.VALIDATION)


def test_error_non_category_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Error("code", "Message.", 99)  # type: ignore[arg-type]  # deliberately wrong type


def test_error_created_keeps_code_and_message() -> None:
    assert SAMPLE.code == "input.missing"
    assert SAMPLE.message == "A required figure is missing."


def test_error_same_parts_are_equal() -> None:
    assert Error("a", "b", ErrorCategory.CONFLICT) == Error("a", "b", ErrorCategory.CONFLICT)


def test_ok_no_value_reading_value_raises_runtime_error() -> None:
    with pytest.raises(RuntimeError):
        _ = Result.ok().value


def test_constructor_value_and_error_both_set_raises_value_error() -> None:
    with pytest.raises(ValueError, match="both"):
        Result(5, SAMPLE)


def test_constructor_non_error_in_error_slot_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Result(None, "oops")  # type: ignore[arg-type]  # deliberately wrong type


def test_constructor_neither_value_nor_error_is_the_same_as_ok() -> None:
    assert Result(None, None) == Result.ok()
