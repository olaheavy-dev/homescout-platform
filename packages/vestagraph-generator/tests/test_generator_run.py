"""The generator as a program: what it writes, what it deletes, how it fails."""

import io
from pathlib import Path
from typing import Any

import pytest
from generator_support import (
    copy_data_to,
    fixtures_directory,
    generated_json,
    read_json,
    remove_evidence,
    write_json,
)
from vestagraph_generator.costs_generator import generate, run
from vestagraph_generator.fixture_reader import InvalidDataError


def _edit_snapshot(fixtures: Path, change: Any) -> None:
    path = fixtures / "data" / "snapshot.json"
    document = read_json(path)
    change(document["snapshot"])
    write_json(path, document)


def test_run_real_data_writes_costs_json_as_utf8_without_byte_order_mark(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)

    exit_code = run(fixtures, io.StringIO())

    written = (fixtures / "generated" / "costs.json").read_bytes()
    assert exit_code == 0
    assert written[:3] != b"\xef\xbb\xbf"
    assert written == generated_json().encode("utf-8")
    assert written[-1:] == b"\n"
    assert written[-2:-1] != b"\n"
    assert b"\r" not in written


def test_run_twice_gives_byte_identical_files(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "generated" / "costs.json"

    run(fixtures, io.StringIO())
    first = path.read_bytes()
    run(fixtures, io.StringIO())

    assert path.read_bytes() == first


def test_run_other_json_file_in_generated_is_deleted_and_other_files_are_kept(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    generated = fixtures / "generated"
    generated.mkdir()
    (generated / "old.json").write_text("{}", encoding="utf-8")
    (generated / "notes.md").write_text("keep me", encoding="utf-8")

    exit_code = run(fixtures, io.StringIO())

    assert exit_code == 0
    assert not (generated / "old.json").exists()
    assert (generated / "notes.md").exists()
    assert (generated / "costs.json").exists()


def test_run_engine_failure_exits_non_zero_names_the_error_code_and_writes_nothing(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    remove_evidence(fixtures, "B1-PRICE")
    error = io.StringIO()

    exit_code = run(fixtures, error)

    assert exit_code == 1
    assert "input.missing.asking-price" in error.getvalue()
    assert "B1" in error.getvalue()
    assert not (fixtures / "generated").exists()


def test_run_engine_failure_leaves_an_existing_generated_folder_untouched(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    generated = fixtures / "generated"
    generated.mkdir()
    (generated / "costs.json").write_text("previous", encoding="utf-8")
    (generated / "old.json").write_text("{}", encoding="utf-8")
    remove_evidence(fixtures, "B1-PRICE")

    exit_code = run(fixtures, io.StringIO())

    assert exit_code == 1
    assert (generated / "costs.json").read_text(encoding="utf-8") == "previous"
    assert (generated / "old.json").exists()


def test_generate_covered_home_in_no_story_fails_with_its_code_not_guessing(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    _edit_snapshot(fixtures, lambda s: s["stories"][0].update(homeIds=["B2"]))

    result = generate(fixtures)

    assert result.is_failure
    assert result.error.code == "home.not-in-a-story"
    assert result.error.message.startswith("B1: ")


def test_generate_home_in_two_stories_fails_with_its_code(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    _edit_snapshot(fixtures, lambda s: s["stories"][1]["homeIds"].append("B1"))

    result = generate(fixtures)

    assert result.is_failure
    assert result.error.code == "home.in-several-stories"


def test_generate_data_file_missing_raises_instead_of_writing_guesses(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    (fixtures / "data" / "household.json").unlink()

    with pytest.raises(OSError, match="household"):
        generate(fixtures)


def test_generate_unknown_evidence_status_raises_instead_of_guessing(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "evidence.json"
    document = read_json(path)
    document["evidence"][0]["status"] = "surprising"
    write_json(path, document)

    with pytest.raises(InvalidDataError):
        generate(fixtures)


def test_generate_text_where_a_number_is_expected_raises_invalid_data_not_a_stack_trace(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "evidence.json"
    document = read_json(path)
    document["evidence"][0]["id"] = 5
    write_json(path, document)

    with pytest.raises(InvalidDataError):
        generate(fixtures)


def test_generate_list_where_an_object_is_expected_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    write_json(fixtures / "data" / "homes.json", {"homes": 3})

    with pytest.raises(InvalidDataError):
        generate(fixtures)


def test_generate_quantity_in_other_units_is_read_as_another_kind_of_value_not_an_error(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "evidence.json"
    document = read_json(path)
    extra = dict(document["evidence"][0])
    extra.update(
        id="B1-ROOMS",
        subjectType="home",
        subjectId="B1",
        category="lease-term",
        value={"kind": "quantity", "amount": 3, "unit": "rooms"},
    )
    document["evidence"].append(extra)
    write_json(path, document)

    result = generate(fixtures)

    assert result.is_success
    assert result.value == generated_json()


def test_generate_home_in_the_snapshot_but_not_in_homes_raises_invalid_data(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "homes.json"
    document = read_json(path)
    document["homes"] = [h for h in document["homes"] if h["id"] != "B2"]
    write_json(path, document)

    with pytest.raises(InvalidDataError, match="B2"):
        generate(fixtures)


def test_run_costs_json_cannot_be_replaced_keeps_the_other_json_files_and_leaves_no_temporary_file(
    tmp_path: Path,
) -> None:
    fixtures = copy_data_to(tmp_path)
    generated = fixtures / "generated"
    (generated / "costs.json").mkdir(parents=True)
    (generated / "old.json").write_text("{}", encoding="utf-8")

    with pytest.raises(OSError, match="costs"):
        run(fixtures, io.StringIO())

    assert (generated / "old.json").exists()
    assert not (generated / "costs.json.tmp").exists()


def test_run_success_leaves_no_temporary_file(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)

    run(fixtures, io.StringIO())

    assert not (fixtures / "generated" / "costs.json.tmp").exists()


def test_run_committed_costs_json_matches_what_the_generator_produces() -> None:
    committed = fixtures_directory() / "generated" / "costs.json"

    assert committed.read_bytes() == generated_json().encode("utf-8"), (
        "Run 'make generate' and commit the result."
    )


def test_run_into_a_temporary_folder_writes_the_bytes_of_the_committed_costs_json(
    tmp_path: Path,
) -> None:
    # The port proof (BE-31): the Python generator reproduces the committed file with no byte moved.
    fixtures = copy_data_to(tmp_path)

    exit_code = run(fixtures, io.StringIO())

    committed = fixtures_directory() / "generated" / "costs.json"
    assert exit_code == 0
    assert (fixtures / "generated" / "costs.json").read_bytes() == committed.read_bytes()
