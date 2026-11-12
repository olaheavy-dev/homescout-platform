"""Gives each collected scenario a test name that starts with its permanent ID (0049 item 4).

pytest-bdd names a test after the scenario title and drops punctuation, so ``COSTS-02 missing ...``
would become ``test_costs02_missing_...``: ``-k COSTS-02`` would find nothing, and ``BUY-3.2`` could
not be told from ``BUY-32``. After ``scenarios()`` has put the tests in a module, the module calls
``name_scenarios_by_id(globals())``, which renames each one to ``test_<ID>_<title in snake case>``
(for example ``test_COSTS-02_missing_buildings_insurance_is_not_shown_as_zero``).
Decision 0043 rule 1 says every scenario starts with an ID; one without an ID fails collection.
"""

import re
from typing import Any

# pytest-bdd sets each test's docstring to "<feature name>: <scenario name>".
_ID_AND_TITLE = re.compile(r"(?:^|: )([A-Z][A-Z0-9]*-[0-9][0-9.]*[0-9]) (.+)$")


def name_scenarios_by_id(namespace: dict[str, Any]) -> None:
    for name, test in list(namespace.items()):
        if not name.startswith("test_") or not callable(test):
            continue
        description = getattr(test, "__doc__", None)
        if not description:
            continue
        found = _ID_AND_TITLE.search(description)
        if found is None:
            message = (
                f'Scenario "{description}" does not start with a permanent ID such as COSTS-02 '
                "(docs/specs/README.md, rule 1)."
            )
            raise ValueError(message)
        title = re.sub(r"\W+", "_", found.group(2)).strip("_").lower()
        new_name = f"test_{found.group(1)}_{title}"
        if new_name in namespace:
            message = f"Two scenarios would both be named {new_name}: an ID is never reused."
            raise ValueError(message)
        del namespace[name]
        namespace[new_name] = test
