"""Runs the proof feature that uses every documented data-step wording (issue #193).

The real specifications in docs/specs/ use only some of the seven steps, so a reworded step there
would go unnoticed; this module runs all seven against the real data. See ``features/``.
"""

from pathlib import Path

from pytest_bdd import scenarios
from specs_runner import name_scenarios_by_id
from specs_steps import *  # noqa: F403  (steps and fixtures must live in this module)

scenarios(str(Path(__file__).resolve().parent / "features" / "data_steps_wording.feature"))
name_scenarios_by_id(globals())
