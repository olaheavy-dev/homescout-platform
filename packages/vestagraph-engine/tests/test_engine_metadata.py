"""Metadata test: the engine has no runtime dependencies (decision 0039 section 1)."""

from importlib import import_module
from importlib.metadata import requires
from pathlib import Path


def test_requires_engine_package_has_no_runtime_dependencies() -> None:
    assert requires("vestagraph-engine") is None


def test_import_engine_ships_py_typed_marker() -> None:
    package = import_module("vestagraph_engine")
    assert package.__file__ is not None
    assert (Path(package.__file__).parent / "py.typed").is_file()


def test_import_engine_exports_the_public_names_of_the_whole_engine() -> None:
    package = import_module("vestagraph_engine")

    for name in (
        "build_home_costs",
        "select_assumptions",
        "upfront_cash",
        "monthly_cost",
        "monthly_repayment",
        "HomeFacts",
        "EvidenceItem",
        "HomeCosts",
        "ScenarioCosts",
        "UpfrontBreakdown",
    ):
        assert name in package.__all__, name
        assert getattr(package, name) is not None, name
