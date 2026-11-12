"""Shared helpers for the generator tests.

Inputs and expected values come from the repository's fixture files and the hand-worked cases,
never from a copy kept here (AGENTS rule 2). The generator runs again on every call: nothing is
cached, so one test can never decide the result of another.
"""

import json
import shutil
from pathlib import Path
from typing import Any

from vestagraph_generator.costs_generator import generate


def repository_root() -> Path:
    for folder in Path(__file__).resolve().parents:
        if (folder / "packages" / "fixtures" / "data").is_dir():
            return folder
    message = "The repository root was not found above the tests."
    raise RuntimeError(message)


def fixtures_directory() -> Path:
    return repository_root() / "packages" / "fixtures"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def generated_json() -> str:
    """The text the generator makes from the real data (it fails the test if the engine fails)."""
    result = generate(fixtures_directory())
    assert result.is_success, result.error.code if result.is_failure else ""
    return result.value


def output() -> dict[str, Any]:
    parsed: dict[str, Any] = json.loads(generated_json())
    return parsed


def home(home_id: str) -> dict[str, Any]:
    matches = [h for h in output()["homes"] if h["homeId"] == home_id]
    assert len(matches) == 1, home_id
    found: dict[str, Any] = matches[0]
    return found


def scenario(home_id: str, scenario_id: str) -> dict[str, Any]:
    matches = [s for s in home(home_id)["scenarios"] if s["scenarioId"] == scenario_id]
    assert len(matches) == 1, (home_id, scenario_id)
    found: dict[str, Any] = matches[0]
    return found


def worked_case(case_id: str) -> dict[str, Any]:
    cases = read_json(fixtures_directory() / "test-cases" / "story-calculations.json")["cases"]
    matches = [c for c in cases if c["id"] == case_id]
    assert len(matches) == 1, case_id
    found: dict[str, Any] = matches[0]
    return found


def copy_data_to(tmp_path: Path) -> Path:
    """Copy the real data files to a new fake repository and return its fixtures folder.

    The fake repository root is ``tmp_path``, with the data under ``packages/fixtures/data``.
    """
    fixtures = tmp_path / "packages" / "fixtures"
    shutil.copytree(fixtures_directory() / "data", fixtures / "data")
    return fixtures


def remove_evidence(fixtures: Path, evidence_id: str) -> None:
    path = fixtures / "data" / "evidence.json"
    document = read_json(path)
    document["evidence"] = [e for e in document["evidence"] if e["id"] != evidence_id]
    write_json(path, document)
