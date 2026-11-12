"""Runs every Gherkin scenario in docs/specs/ that is not excluded by tag (decision 0043, SP-03).

The feature files stay where they are (docs/specs/, repository root): nothing is copied here.
``make test`` adds ``-m "not ui and not mcp and not withdrawn"``, so ``@ui``, ``@mcp`` and
``@withdrawn`` scenarios are collected but not run, as the C# runner did with NUnit categories.
"""

from pytest_bdd import scenarios
from specs_runner import name_scenarios_by_id
from specs_steps import *  # noqa: F403  (steps and fixtures must live in this module)
from specs_support import specs_directory

_SPECS = str(specs_directory())
scenarios(_SPECS)
name_scenarios_by_id(globals(), _SPECS)
