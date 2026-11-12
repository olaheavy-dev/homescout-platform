"""Gives each collected scenario a test name that starts with its permanent ID (0049 item 4).

pytest-bdd names a test after the scenario title and drops punctuation, so ``COSTS-02 missing ...``
would become ``test_costs02_missing_...``: ``-k COSTS-02`` would find nothing, and ``BUY-3.2`` could
not be told from ``BUY-32``. After ``scenarios(paths)`` has put the tests in a module, the
module calls ``name_scenarios_by_id(globals(), paths)``, which renames each one to
``test_<ID>_<title in snake case>`` (for example
``test_COSTS-02_missing_buildings_insurance_is_not_shown_as_zero``).
Decision 0043 rule 1 says every scenario starts with an ID; one without an ID fails collection.
"""

import re
from typing import Any

from pytest_bdd.feature import get_features

# The ID is the first word of the scenario name: "COSTS-02", "BUY-3", "BUY-3.2".
_ID_AND_TITLE = re.compile(r"^([A-Z][A-Z0-9]*-[0-9](?:[0-9.]*[0-9])?)(?: (.*))?$")


def name_scenarios_by_id(namespace: dict[str, Any], *feature_paths: str) -> None:
    # pytest-bdd sets each test's docstring to "<feature file path>: <scenario name>". A scenario
    # name may itself contain ": ", so match whole descriptions against the files' real scenarios.
    names = {
        f"{feature.filename}: {name}": name
        for feature in get_features(list(feature_paths))
        for name in feature.scenarios
    }
    for attribute, test in list(namespace.items()):
        if not attribute.startswith("test_"):
            continue
        description = getattr(test, "__doc__", None)
        if not description or description not in names:
            message = (
                f"{attribute} is not a scenario of {', '.join(feature_paths)} (no pytest-bdd "
                "description); a scenarios module holds only scenarios."
            )
            raise ValueError(message)
        scenario_name = names[description]
        found = _ID_AND_TITLE.match(scenario_name)
        if found is None:
            message = (
                f'Scenario "{scenario_name}" does not start with a permanent ID such as COSTS-02 '
                "(docs/specs/README.md, rule 1)."
            )
            raise ValueError(message)
        title = re.sub(r"\W+", "_", found.group(2) or "").strip("_").lower()
        new_name = f"test_{found.group(1)}_{title}" if title else f"test_{found.group(1)}"
        if new_name in namespace:
            message = f"Two scenarios would both be named {new_name}: an ID is never reused."
            raise ValueError(message)
        del namespace[attribute]
        namespace[new_name] = test
