"""Proofs that the pytest-bdd runner meets decision 0049 item 4 (issue #193).

Each test runs pytest in a child process with the repository's own configuration (``-c
pyproject.toml``), so the marker rules and warnings-as-errors are the ones ``make test`` uses.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest
from specs_support import repository_root

_TESTS = Path(__file__).resolve().parent
_ROOT = repository_root()
_SCENARIOS_MODULE = _TESTS / "test_specs_scenarios.py"
_RULE_FEATURE = _TESTS / "features" / "rule_blocks_proof.feature"

_PROOF_MODULE = """\
from pytest_bdd import given, scenarios
from specs_runner import name_scenarios_by_id
from specs_steps import *  # noqa: F403

scenarios({feature!r})
name_scenarios_by_id(globals())


@given("a proof step")
def a_proof_step() -> None:
    pass
"""


def _pytest(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603  (fixed arguments, no shell)
        [
            sys.executable,
            "-m",
            "pytest",
            "-c",
            str(_ROOT / "pyproject.toml"),
            "--rootdir",
            str(_ROOT),
            "-p",
            "no:cacheprovider",
            "-o",
            f"pythonpath={_TESTS}",
            *arguments,
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=_ROOT,
    )


def _run_feature(
    tmp_path: Path, feature_text: str, *arguments: str
) -> subprocess.CompletedProcess[str]:
    feature = tmp_path / "proof.feature"
    feature.write_text(feature_text, encoding="utf-8")
    module = tmp_path / "test_proof_module.py"
    module.write_text(_PROOF_MODULE.format(feature=str(feature)), encoding="utf-8")
    return _pytest(str(module), *arguments)


def test_scenario_id_in_the_test_name_costs_02_is_selectable_with_k() -> None:
    result = _pytest(str(_SCENARIOS_MODULE), "-k", "COSTS-02", "--collect-only", "-q")

    assert result.stdout.count("::test_COSTS-02_") == 1, result.stdout
    assert "COSTS-01" not in result.stdout
    assert "1/" in result.stdout or "1 test" in result.stdout, result.stdout


def test_scenario_id_in_the_test_name_dotted_id_is_selectable_with_k(tmp_path: Path) -> None:
    result = _run_feature(
        tmp_path,
        'Feature: Dots\n\n  Scenario: BUY-3.2 dotted id\n    Given home "B1" is at story step 1\n',
        "-k",
        "BUY-3.2",
        "--collect-only",
        "-q",
    )

    assert result.stdout.count("::test_BUY-3.2_dotted_id") == 1, result.stdout


@pytest.mark.parametrize("tag", ["rule_tag", "scenario_tag", "proof"])
def test_rule_block_scenario_inside_a_rule_runs_and_keeps_its_tags(
    tmp_path: Path, tag: str
) -> None:
    module = tmp_path / "test_rule_module.py"
    module.write_text(_PROOF_MODULE.format(feature=str(_RULE_FEATURE)), encoding="utf-8")

    selected = _pytest(str(module), "-m", tag, "-v")
    named = _pytest(str(module), "-m", tag, "--collect-only", "-q")
    others = _pytest(str(module), "-m", f"not {tag}")

    assert "::test_PROOF-1.1_a_scenario_inside_a_rule_runs" in named.stdout, named.stdout
    assert "1 passed" in selected.stdout, selected.stdout
    assert "1 deselected" in others.stdout, others.stdout


def test_feature_files_from_docs_specs_are_loaded_in_place_without_copying() -> None:
    declared = 0
    for feature in sorted((_ROOT / "docs" / "specs").rglob("*.feature")):
        declared += len(re.findall(r"^\s*Scenario:", feature.read_text(encoding="utf-8"), re.M))
    collected = _pytest(str(_SCENARIOS_MODULE), "--collect-only", "-q")

    assert declared > 0
    assert collected.stdout.count("::test_") == declared, collected.stdout
    assert not list((_ROOT / "packages").rglob("05-real-costs.feature"))


def test_unknown_tag_fails_the_run(tmp_path: Path) -> None:
    result = _run_feature(
        tmp_path,
        "@bogus_tag\nFeature: Tag\n\n  Scenario: TAG-01 unknown tag\n"
        '    Given home "B1" is at story step 1\n',
    )

    assert result.returncode != 0
    assert "bogus_tag" in result.stdout, result.stdout


def test_missing_figure_id_fails_the_scenario_naming_the_id(tmp_path: Path) -> None:
    result = _run_feature(
        tmp_path,
        "Feature: Missing\n\n  Scenario: MISS-01 cites a missing figure\n"
        '    Given home "B1" is at story step 1\n'
        '    Then figure "B1.from-step-1.monthly.no-such-line" exists\n',
    )

    assert result.returncode == 1
    assert "B1.from-step-1.monthly.no-such-line" in result.stdout, result.stdout


def test_undefined_step_fails_the_scenario(tmp_path: Path) -> None:
    result = _run_feature(
        tmp_path,
        "Feature: Undefined\n\n  Scenario: UNDEF-01 nonsense step\n    Given the moon is full\n",
    )

    assert result.returncode == 1
    assert "Step definition is not found" in result.stdout, result.stdout


def test_scenario_without_a_permanent_id_fails_collection_naming_the_scenario(
    tmp_path: Path,
) -> None:
    result = _run_feature(
        tmp_path,
        "Feature: No id\n\n  Scenario: an unnumbered scenario\n"
        '    Given home "B1" is at story step 1\n',
    )

    assert result.returncode != 0
    assert "an unnumbered scenario" in result.stdout, result.stdout


@pytest.mark.parametrize("excluded", ["ui", "mcp", "withdrawn"])
def test_marker_filter_excludes_the_tag(tmp_path: Path, excluded: str) -> None:
    result = _run_feature(
        tmp_path,
        f"Feature: Tagged\n\n  @{excluded}\n  Scenario: TAG-02 excluded\n"
        "    Given the moon is full\n",
        "-m",
        "not ui and not mcp and not withdrawn",
    )

    assert "1 deselected" in result.stdout, result.stdout
    assert result.returncode == 5
