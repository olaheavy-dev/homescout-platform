"""The output schema must refuse a wrong cost file, not only accept a right one.

Ported from GeneratedCostsSchemaTests.

The sample below only shows the shape of the file. Its figures are placeholders for the schema to
check; they are not cost-engine results and no test quotes them as expected values.
"""

import copy
import json
from pathlib import Path

import pytest
from fixtures_support import (
    Json,
    copy_fixture_folders,
    lines,
    number,
    parse,
    schema_directory,
)
from vestagraph_fixture_validator.validator import validate_fixtures, validate_instance

_SCHEMA = "generated-costs.schema.json"

_SAMPLE = """
{
  "$schema": "../schema/generated-costs.schema.json",
  "formatVersion": 1,
  "generatedBy": "Vestagraph cost engine",
  "snapshotDate": "2026-10-23",
  "money": "integer pence",
  "rounding": "Nearest penny, exact halves away from zero (decisions 0034 and 0036).",
  "homes": [
    {
      "homeId": "B1",
      "mode": "buy",
      "nation": "England",
      "coverage": "covered",
      "storyId": "BUYER",
      "scenarios": [
        {
          "scenarioId": "from-step-1",
          "fromStep": 1,
          "toStep": 3,
          "mortgage": {
            "id": "B1.from-step-1.mortgage",
            "loan": { "id": "B1.from-step-1.mortgage.loan", "pence": 100 },
            "rateBasisPoints": 550,
            "termYears": 25,
            "payments": 300,
            "monthlyRepayment": { "id": "B1.from-step-1.mortgage.repayment", "pence": 10 },
            "evidenceIds": ["B1-PRICE", "HH-MORTGAGE-DEPOSIT"]
          },
          "monthly": {
            "lines": [
              {
                "id": "B1.from-step-1.monthly.service-charge",
                "category": "service-charge",
                "status": "calculated",
                "pence": 20,
                "sourcePeriod": "year",
                "evidenceIds": ["B1-SC-LISTING"]
              },
              {
                "id": "B1.from-step-1.monthly.buildings-insurance",
                "category": "buildings-insurance",
                "status": "included",
                "evidenceIds": ["B1-INSURANCE"]
              },
              {
                "id": "B1.from-step-1.monthly.maintenance",
                "category": "maintenance",
                "status": "not-calculated",
                "evidenceIds": ["B1-MAINTENANCE"]
              },
              {
                "id": "B1.from-step-1.monthly.water",
                "category": "water",
                "status": "conflicting",
                "evidenceIds": ["R1-WATER-LISTING", "R1-WATER-WSOT"]
              },
              {
                "id": "B1.from-step-1.monthly.energy",
                "category": "energy",
                "status": "missing",
                "evidenceIds": []
              }
            ],
            "total": {
              "id": "B1.from-step-1.monthly.total",
              "pence": 20,
              "isPartial": true,
              "partialReasons": [
                {
                  "lineId": "B1.from-step-1.monthly.maintenance",
                  "category": "maintenance",
                  "status": "not-calculated"
                },
                {
                  "lineId": "B1.from-step-1.monthly.water",
                  "category": "water",
                  "status": "conflicting"
                },
                {
                  "lineId": "B1.from-step-1.monthly.energy",
                  "category": "energy",
                  "status": "missing"
                }
              ]
            },
            "budget": {
              "id": "B1.from-step-1.monthly.budget",
              "budgetPence": 160000,
              "budgetSource": "household:RIVERS.monthlyBudget",
              "differencePence": 159980,
              "withinBudget": true,
              "basedOnPartialTotal": true
            }
          },
          "upfront": {
            "lines": [
              {
                "id": "B1.from-step-1.upfront.moving-costs",
                "category": "moving-costs",
                "status": "calculated",
                "pence": 30,
                "sourcePeriod": "once",
                "evidenceIds": ["HH-MOVING-COSTS"]
              }
            ],
            "total": {
              "id": "B1.from-step-1.upfront.total",
              "pence": 30,
              "isPartial": false,
              "partialReasons": []
            }
          },
          "changesFromPrevious": []
        },
        {
          "scenarioId": "from-step-4",
          "fromStep": 4,
          "toStep": 4,
          "mortgage": {
            "id": "B1.from-step-4.mortgage",
            "loan": { "id": "B1.from-step-4.mortgage.loan", "pence": 100 },
            "rateBasisPoints": 550,
            "termYears": 25,
            "payments": 300,
            "monthlyRepayment": { "id": "B1.from-step-4.mortgage.repayment", "pence": 10 },
            "evidenceIds": ["B1-PRICE", "HH-MORTGAGE-DEPOSIT"]
          },
          "monthly": {
            "lines": [
              {
                "id": "B1.from-step-4.monthly.service-charge",
                "category": "service-charge",
                "status": "calculated",
                "pence": 31,
                "sourcePeriod": "year",
                "evidenceIds": ["B1-SC-BUDGET"]
              }
            ],
            "total": {
              "id": "B1.from-step-4.monthly.total",
              "pence": 31,
              "isPartial": false,
              "partialReasons": []
            },
            "budget": {
              "id": "B1.from-step-4.monthly.budget",
              "budgetPence": 160000,
              "budgetSource": "household:RIVERS.monthlyBudget",
              "differencePence": 159969,
              "withinBudget": true,
              "basedOnPartialTotal": false
            }
          },
          "upfront": {
            "lines": [],
            "total": {
              "id": "B1.from-step-4.upfront.total",
              "pence": 0,
              "isPartial": false,
              "partialReasons": []
            }
          },
          "changesFromPrevious": [
            {
              "id": "B1.from-step-4.change.service-charge",
              "category": "service-charge",
              "kind": "value-changed",
              "previousEvidenceIds": ["B1-SC-LISTING"],
              "currentEvidenceIds": ["B1-SC-BUDGET"],
              "monthlyDifferencePence": 11,
              "annualDifferencePence": 132
            }
          ],
          "monthlyTotalChange": { "id": "B1.from-step-4.change.monthly-total", "pence": 11 }
        }
      ]
    },
    {
      "homeId": "WALES-1",
      "nation": "Wales",
      "coverage": "not-yet-covered",
      "scenarios": []
    }
  ]
}
"""


def _sample() -> Json:
    return parse(_SAMPLE)


def _first_scenario(file: Json) -> Json:
    return file["homes"][0]["scenarios"][0]


def _first_monthly_line(file: Json) -> Json:
    return _first_scenario(file)["monthly"]["lines"][0]


def _problems(file: Json) -> list[str]:
    return lines(validate_instance(file, _SCHEMA, schema_directory()))


def _mentions(file: Json, text: str) -> bool:
    return any(text in line for line in _problems(file))


def test_validate_instance_generated_costs_sample_shape_is_accepted() -> None:
    assert _problems(_sample()) == []


def test_validate_instance_generated_costs_calculated_line_without_pence_is_rejected() -> None:
    file = _sample()
    del _first_monthly_line(file)["pence"]

    assert _mentions(file, "pence")


def test_validate_instance_generated_costs_calculated_line_without_source_period_is_rejected() -> (
    None
):
    file = _sample()
    del _first_monthly_line(file)["sourcePeriod"]

    assert _mentions(file, "sourcePeriod")


@pytest.mark.parametrize("line_index", [1, 2, 3])
def test_validate_instance_generated_costs_non_calculated_line_with_pence_is_rejected(
    line_index: int,
) -> None:
    # Lines 1, 2, 3 are included, not-calculated and conflicting. None may carry an amount (rule 7).
    file = _sample()
    _first_scenario(file)["monthly"]["lines"][line_index]["pence"] = 0

    assert _mentions(file, f"/monthly/lines/{line_index}/pence")


def test_validate_instance_generated_costs_missing_line_with_pence_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["monthly"]["lines"][4]["pence"] = 0

    assert _mentions(file, "/monthly/lines/4/pence")


def test_validate_instance_generated_costs_included_line_with_no_evidence_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["monthly"]["lines"][1]["evidenceIds"] = []

    assert _mentions(file, "/monthly/lines/1/evidenceIds")


def test_validate_instance_generated_costs_missing_line_that_names_evidence_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["monthly"]["lines"][4]["evidenceIds"] = ["B1-PRICE"]

    assert _mentions(file, "/monthly/lines/4/evidenceIds")


def test_validate_instance_generated_costs_negative_pence_on_a_calculated_line_is_rejected() -> (
    None
):
    file = _sample()
    _first_monthly_line(file)["pence"] = -1

    assert _mentions(file, "/monthly/lines/0/pence")


def test_validate_instance_generated_costs_decimal_pence_is_rejected() -> None:
    file = _sample()
    _first_monthly_line(file)["pence"] = number("20.5")

    assert _mentions(file, "/monthly/lines/0/pence")


@pytest.mark.parametrize(
    "figure_id",
    [
        "b1.from-step-1.monthly.total",
        "B1.From-Step-1.monthly.total",
        "B1",
        "B1..monthly.total",
        "B1.from-step-1.monthly.total.",
        "B1.from_step_1.monthly.total",
        "B1.from-step-1.monthly total",
    ],
)
def test_validate_instance_generated_costs_bad_figure_id_is_rejected(figure_id: str) -> None:
    file = _sample()
    _first_scenario(file)["monthly"]["total"]["id"] = figure_id

    assert _mentions(file, "/monthly/total/id")


def test_validate_instance_generated_costs_not_yet_covered_home_with_scenarios_is_rejected() -> (
    None
):
    file = _sample()
    file["homes"][1]["scenarios"] = [copy.deepcopy(_first_scenario(file))]

    assert _mentions(file, "/homes/1/scenarios")


def test_validate_instance_generated_costs_covered_home_with_no_scenarios_is_rejected() -> None:
    file = _sample()
    file["homes"][0]["scenarios"] = []

    assert _mentions(file, "/homes/0/scenarios")


def test_validate_instance_generated_costs_wales_marked_covered_is_rejected() -> None:
    file = _sample()
    file["homes"][1]["coverage"] = "covered"

    assert _mentions(file, "/homes/1/coverage")


def test_validate_instance_generated_costs_partial_total_with_no_reasons_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["monthly"]["total"]["partialReasons"] = []

    assert _mentions(file, "/monthly/total/partialReasons")


def test_validate_instance_generated_costs_complete_total_with_reasons_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["monthly"]["total"]["isPartial"] = False

    assert _mentions(file, "/monthly/total/partialReasons")


def test_validate_instance_generated_costs_partial_reason_for_a_calculated_line_is_rejected() -> (
    None
):
    file = _sample()
    _first_scenario(file)["monthly"]["total"]["partialReasons"][0]["status"] = "calculated"

    assert _mentions(file, "/partialReasons/0/status")


def test_validate_instance_generated_costs_unknown_key_in_a_line_is_rejected() -> None:
    file = _sample()
    _first_monthly_line(file)["verified"] = True

    assert _mentions(file, "verified")


def test_validate_instance_generated_costs_unknown_line_status_is_rejected() -> None:
    file = _sample()
    _first_monthly_line(file)["status"] = "verified"

    assert _mentions(file, "/monthly/lines/0/status")


def test_validate_instance_generated_costs_unknown_category_is_rejected() -> None:
    file = _sample()
    _first_monthly_line(file)["category"] = "service-charges"

    assert _mentions(file, "/monthly/lines/0/category")


def test_validate_instance_generated_costs_wrong_scenario_id_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["scenarioId"] = "step-1"

    assert _mentions(file, "/scenarioId")


def test_validate_instance_generated_costs_wrong_format_version_is_rejected() -> None:
    file = _sample()
    file["formatVersion"] = 2

    assert _mentions(file, "/formatVersion")


def test_validate_instance_generated_costs_missing_snapshot_date_is_rejected() -> None:
    file = _sample()
    del file["snapshotDate"]

    assert _mentions(file, "snapshotDate")


def test_validate_instance_generated_costs_budget_without_partial_flag_is_rejected() -> None:
    file = _sample()
    del _first_scenario(file)["monthly"]["budget"]["basedOnPartialTotal"]

    assert _mentions(file, "basedOnPartialTotal")


def test_validate_instance_generated_costs_change_with_unknown_kind_is_rejected() -> None:
    file = _sample()
    file["homes"][0]["scenarios"][1]["changesFromPrevious"][0]["kind"] = "cheaper"

    assert _mentions(file, "/changesFromPrevious/0/kind")


def test_validate_instance_generated_costs_buying_scenario_with_no_mortgage_is_rejected() -> None:
    file = _sample()
    del file["homes"][0]["scenarios"][0]["mortgage"]

    assert _mentions(file, "/homes/0/scenarios/0")


def test_validate_instance_generated_costs_mortgage_loan_of_zero_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["mortgage"]["loan"]["pence"] = 0

    assert _mentions(file, "/mortgage/loan/pence")


def test_validate_instance_generated_costs_mortgage_repayment_of_zero_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["mortgage"]["monthlyRepayment"]["pence"] = 0

    assert _mentions(file, "/mortgage/monthlyRepayment/pence")


def test_validate_instance_generated_costs_mortgage_term_over_100_years_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["mortgage"]["termYears"] = 101

    assert _mentions(file, "/mortgage/termYears")


def test_validate_instance_generated_costs_mortgage_with_zero_rate_is_rejected() -> None:
    file = _sample()
    _first_scenario(file)["mortgage"]["rateBasisPoints"] = 0

    assert _mentions(file, "/mortgage/rateBasisPoints")


def _fixtures_with_generated(tmp_path: Path, file: Json | None) -> Path:
    """A throwaway copy of the real fixtures, with ``generated/costs.json`` added if given."""
    fixtures = copy_fixture_folders(tmp_path, ("schema", "data", "test-cases"))
    if file is not None:
        (fixtures / "generated").mkdir()
        (fixtures / "generated" / "costs.json").write_text(json.dumps(file), encoding="utf-8")
    return fixtures


def test_validate_fixtures_invalid_generated_file_is_reported(tmp_path: Path) -> None:
    file = _sample()
    del _first_monthly_line(file)["pence"]
    fixtures = _fixtures_with_generated(tmp_path, file)

    problems = lines(validate_fixtures(fixtures))

    assert any(
        line.startswith("costs.json: /homes/0/scenarios/0/monthly/lines/0") for line in problems
    )


def test_validate_fixtures_generated_file_with_no_schema_line_is_reported(tmp_path: Path) -> None:
    file = _sample()
    del file["$schema"]
    fixtures = _fixtures_with_generated(tmp_path, file)

    problems = lines(validate_fixtures(fixtures))

    assert any("costs.json: /$schema" in line for line in problems)


def test_validate_fixtures_valid_generated_file_is_accepted(tmp_path: Path) -> None:
    fixtures = _fixtures_with_generated(tmp_path, _sample())

    assert validate_fixtures(fixtures) == []


def test_validate_fixtures_no_generated_folder_is_accepted(tmp_path: Path) -> None:
    # The validator does not require generated/ to exist: make generated-check is what insists the
    # committed costs.json is current.
    fixtures = _fixtures_with_generated(tmp_path, None)

    assert not (fixtures / "generated").exists()
    assert validate_fixtures(fixtures) == []
