"""The command line: ``python -m vestagraph_generator [repo-root]`` and its exit codes."""

import io
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from generator_support import (
    copy_data_to,
    fixtures_directory,
    read_json,
    remove_evidence,
    repository_root,
    write_json,
)
from vestagraph_generator.__main__ import find_repository_root, main


def _fake_repository(tmp_path: Path) -> Path:
    copy_data_to(tmp_path)
    return tmp_path


def test_main_real_data_exits_zero_and_names_the_file_it_wrote(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([str(root)], out, err, root)

    written = root / "packages" / "fixtures" / "generated" / "costs.json"
    assert exit_code == 0
    assert out.getvalue() == f"Generated {written}\n"
    assert err.getvalue() == ""
    assert written.read_bytes() == (fixtures_directory() / "generated" / "costs.json").read_bytes()


def test_main_no_argument_finds_the_repository_above_the_working_folder(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    deep = root / "packages" / "fixtures" / "data"

    exit_code = main([], io.StringIO(), io.StringIO(), deep)

    assert exit_code == 0
    assert (root / "packages" / "fixtures" / "generated" / "costs.json").is_file()


def test_main_engine_failure_exits_one_with_the_error_code_on_standard_error(
    tmp_path: Path,
) -> None:
    root = _fake_repository(tmp_path)
    remove_evidence(root / "packages" / "fixtures", "B1-PRICE")
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([str(root)], out, err, root)

    assert exit_code == 1
    assert out.getvalue() == ""
    assert err.getvalue().startswith("Generator failed [input.missing.asking-price]: B1: ")


def test_main_missing_data_file_exits_two_with_a_plain_message(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    (root / "packages" / "fixtures" / "data" / "snapshot.json").unlink()
    err = io.StringIO()

    exit_code = main([str(root)], io.StringIO(), err, root)

    assert exit_code == 2
    assert err.getvalue().startswith("Generator could not run: ")
    assert "snapshot" in err.getvalue()


def test_main_unreadable_data_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    (root / "packages" / "fixtures" / "data" / "homes.json").write_text("{nope", encoding="utf-8")
    err = io.StringIO()

    exit_code = main([str(root)], io.StringIO(), err, root)

    assert exit_code == 2
    assert err.getvalue().startswith("Generator could not run: ")


def test_main_no_repository_above_the_working_folder_exits_two(tmp_path: Path) -> None:
    err = io.StringIO()

    exit_code = main([], io.StringIO(), err, tmp_path)

    assert exit_code == 2
    assert err.getvalue().startswith("Generator could not run: ")


def test_find_repository_root_walks_up_to_the_folder_holding_the_fixture_data() -> None:
    assert find_repository_root(Path(__file__).resolve().parent) == repository_root()


def test_find_repository_root_nothing_above_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        find_repository_root(tmp_path)


def test_python_dash_m_runs_the_generator_and_returns_its_exit_code(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)

    done = subprocess.run(  # noqa: S603 - runs this interpreter on our own package, no outside input
        [sys.executable, "-m", "vestagraph_generator", str(root)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )

    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("Generated ")
    assert (root / "packages" / "fixtures" / "generated" / "costs.json").is_file()

    (root / "packages" / "fixtures" / "data" / "household.json").unlink()
    failed = subprocess.run(  # noqa: S603 - same as above
        [sys.executable, "-m", "vestagraph_generator", str(root)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert failed.returncode == 2


def _exit_two_message(root: Path) -> str:
    err = io.StringIO()
    exit_code = main([str(root)], io.StringIO(), err, root)
    assert exit_code == 2
    assert err.getvalue().startswith("Generator could not run: ")
    return err.getvalue()


def _edit(root: Path, name: str, change: Callable[[Any], None]) -> None:
    path = root / "packages" / "fixtures" / "data" / f"{name}.json"
    document = read_json(path)
    change(document)
    write_json(path, document)


def test_main_rate_basis_points_beyond_32_bits_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)

    def change(document: Any) -> None:
        item = next(e for e in document["evidence"] if e["value"]["kind"] == "rate")
        item["value"]["basisPoints"] = 2**40

    _edit(root, "evidence", change)

    assert "basisPoints" in _exit_two_message(root)


def test_main_pence_beyond_64_bits_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)

    def change(document: Any) -> None:
        item = next(e for e in document["evidence"] if e["value"]["kind"] == "money")
        item["value"]["pence"] = 2**70

    _edit(root, "evidence", change)

    assert "pence" in _exit_two_message(root)


def test_main_story_step_beyond_32_bits_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    _edit(root, "snapshot", lambda d: d["snapshot"]["stories"][0]["steps"][0].update(step=2**40))

    assert "step" in _exit_two_message(root)


def test_main_file_that_is_not_utf8_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    (root / "packages" / "fixtures" / "data" / "homes.json").write_bytes(b'{"homes": "\xff"}')

    message = _exit_two_message(root)
    assert "homes" in message
    assert "UTF-8" in message


def test_main_number_with_thousands_of_digits_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    path = root / "packages" / "fixtures" / "data" / "household.json"
    text = path.read_text(encoding="utf-8")
    original = read_json(path)["household"]["monthlyBudget"]["pence"]
    assert f'"pence": {original}' in text
    path.write_text(
        text.replace(f'"pence": {original}', '"pence": ' + "9" * 5000), encoding="utf-8"
    )

    assert "household" in _exit_two_message(root)


def test_main_decimal_pence_exits_two_saying_a_whole_number_is_needed(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    path = root / "packages" / "fixtures" / "data" / "household.json"
    text = path.read_text(encoding="utf-8")
    original = read_json(path)["household"]["monthlyBudget"]["pence"]
    path.write_text(text.replace(f'"pence": {original}', '"pence": 12.5'), encoding="utf-8")

    assert "whole number" in _exit_two_message(root)


def test_main_not_a_number_value_exits_two(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    path = root / "packages" / "fixtures" / "data" / "household.json"
    text = path.read_text(encoding="utf-8")
    original = read_json(path)["household"]["monthlyBudget"]["pence"]
    path.write_text(text.replace(f'"pence": {original}', '"pence": NaN'), encoding="utf-8")

    assert "NaN" in _exit_two_message(root)
