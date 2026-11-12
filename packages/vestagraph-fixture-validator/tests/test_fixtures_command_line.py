"""The command line: ``python -m vestagraph_fixture_validator [repo-root]`` and its exit codes.

Ported from the C# ``Program.cs``: exit 0 when every file is valid, 1 when something is wrong
(each problem is printed on standard error), 2 on a setup error.
"""

import io
import subprocess
import sys
from pathlib import Path

import pytest
from fixtures_support import copy_fixture_folders, fixtures_directory, repository_root
from vestagraph_fixture_validator.__main__ import main
from vestagraph_fixture_validator.validator import find_repository_root

_OK = "Fixtures: every data file, test case and generated file matches its schema.\n"


def _fake_repository(tmp_path: Path) -> Path:
    """A copy of the real fixtures (with the generated file) under ``packages/fixtures``."""
    fixtures = tmp_path / "packages" / "fixtures"
    copy_fixture_folders(fixtures, ("schema", "data", "test-cases", "generated"))
    return tmp_path


def test_main_real_fixtures_exit_zero_and_say_so(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([str(root)], out, err, root)

    assert exit_code == 0
    assert out.getvalue() == _OK
    assert err.getvalue() == ""


def test_main_no_argument_finds_the_repository_above_the_working_folder(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    deep = root / "packages" / "fixtures" / "data"
    out = io.StringIO()

    exit_code = main([], out, io.StringIO(), deep)

    assert exit_code == 0
    assert out.getvalue() == _OK


def test_main_the_real_repository_exits_zero() -> None:
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([], out, err, Path(__file__).resolve().parent)

    assert err.getvalue() == ""
    assert exit_code == 0


def test_main_a_bad_file_exits_one_and_prints_each_problem_then_the_count(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    data = root / "packages" / "fixtures" / "data"
    (data / "homes.json").write_text("{nope", encoding="utf-8")
    (data / "snapshot.json").write_text("[1", encoding="utf-8")
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([str(root)], out, err, root)

    assert exit_code == 1
    assert out.getvalue() == ""
    printed = err.getvalue().splitlines()
    assert len(printed) == 3
    assert printed[0].startswith("homes.json: /: Not valid JSON: ")
    assert printed[1].startswith("snapshot.json: /: Not valid JSON: ")
    assert printed[2] == "Fixtures: 2 problem(s) found."


def test_main_a_schema_problem_is_printed_with_file_pointer_and_message(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)
    path = root / "packages" / "fixtures" / "data" / "household.json"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace('"pence": 160000', '"pence": 0'), encoding="utf-8")
    err = io.StringIO()

    exit_code = main([str(root)], io.StringIO(), err, root)

    assert exit_code == 1
    assert any(
        line.startswith("household.json: /household/monthlyBudget/pence: ")
        for line in err.getvalue().splitlines()
    )


def test_main_a_folder_with_no_fixture_files_exits_one(tmp_path: Path) -> None:
    (tmp_path / "packages" / "fixtures").mkdir(parents=True)
    err = io.StringIO()

    exit_code = main([str(tmp_path)], io.StringIO(), err, tmp_path)

    assert exit_code == 1
    assert "No fixture files found in data/, test-cases/ or generated/." in err.getvalue()
    assert err.getvalue().endswith("Fixtures: 1 problem(s) found.\n")


def test_main_no_repository_above_the_working_folder_exits_two_with_a_plain_message(
    tmp_path: Path,
) -> None:
    out, err = io.StringIO(), io.StringIO()

    exit_code = main([], out, err, tmp_path)

    assert exit_code == 2
    assert out.getvalue() == ""
    assert err.getvalue() == f"packages/fixtures/schema not found above {tmp_path}.\n"


def test_find_repository_root_walks_up_to_the_folder_holding_the_fixture_schemas() -> None:
    assert find_repository_root(Path(__file__).resolve().parent) == repository_root()


def test_find_repository_root_nothing_above_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        find_repository_root(tmp_path)


def test_python_dash_m_runs_the_validator_and_returns_its_exit_code(tmp_path: Path) -> None:
    root = _fake_repository(tmp_path)

    done = subprocess.run(  # noqa: S603 - runs this interpreter on our own package, no outside input
        [sys.executable, "-m", "vestagraph_fixture_validator", str(root)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )

    assert done.returncode == 0, done.stderr
    assert done.stdout == _OK

    (root / "packages" / "fixtures" / "data" / "household.json").write_text("{", encoding="utf-8")
    failed = subprocess.run(  # noqa: S603 - same as above
        [sys.executable, "-m", "vestagraph_fixture_validator", str(root)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert failed.returncode == 1
    assert failed.stderr.endswith("Fixtures: 1 problem(s) found.\n")


def test_fixtures_directory_reads_no_environment_variable_for_its_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # A leftover variable must never make the data tests check another copy of the fixtures.
    monkeypatch.setenv("VESTAGRAPH_FIXTURES_DIR", str(tmp_path))

    assert fixtures_directory() == repository_root() / "packages" / "fixtures"
