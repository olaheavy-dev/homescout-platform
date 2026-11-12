"""Every worked case in test-cases/story-calculations.json must be run by a data-driven test, so a
new case cannot be added to the file and quietly never checked (ported from the C#
StoryCalculationCoverageTests).

No case is deferred any more: the service-charge difference runs through the home cost builder.
"""

from engine_support import CASES
from test_engine_budget_beat import BUDGET_BEAT_CASE_IDS
from test_engine_home_cost_builder import CASE_IDS as BUILDER_CASE_IDS
from test_engine_monthly_cost import MONTHLY_CASE_IDS
from test_engine_mortgage import MORTGAGE_CASE_IDS
from test_engine_upfront_cash import UPFRONT_CASE_IDS


def test_story_calculations_every_case_is_run_by_a_data_driven_test() -> None:
    run = [
        *MORTGAGE_CASE_IDS,
        *MONTHLY_CASE_IDS,
        *UPFRONT_CASE_IDS,
        *BUDGET_BEAT_CASE_IDS,
        *BUILDER_CASE_IDS,
    ]

    # Each case once (a case run by two groups, or by none, fails).
    assert sorted(run) == sorted(case["id"] for case in CASES)
