"""The stories and cross-file links in the approved sample data (ported from StoryTests).

Stage 2 plan, section 1.
"""

import pytest
from fixtures_support import Json, evidence_item, load

_RECORD_FILES = ["evidence", "documents", "questions", "replies"]
_DATA_FILES = ["household", "homes", "evidence", "documents", "questions", "replies", "snapshot"]


@pytest.mark.parametrize(
    ("item_id", "rating", "year"),
    [("B1-EPC", "C", 2019), ("B2-EPC", "D", 2021), ("R1-EPC", "C", 2022)],
)
def test_energy_certificate_of_each_home_with_one_has_the_approved_rating_and_year(
    item_id: str, rating: str, year: int
) -> None:
    value = evidence_item(item_id)["value"]

    assert value["rating"] == rating
    assert value["issuedYear"] == year


def test_r1_water_listing_claim_when_checked_against_the_statement_is_conflicting() -> None:
    listing = evidence_item("R1-WATER-LISTING")

    assert listing["status"] == "conflicting"
    assert listing["value"]["text"] == "Water included"


def test_r1_water_written_statement_in_bills_section_says_tenant_pays_water() -> None:
    statement = evidence_item("R1-WATER-WSOT")

    assert statement["value"]["text"] == "Tenant pays water"
    assert statement["source"]["documentType"] == "written-statement-of-terms"


def test_r1_water_estimate_after_the_user_confirms_is_used_from_step4() -> None:
    assert evidence_item("R1-WATER-ESTIMATE")["usedFromStep"] == 4


def test_b1_service_charge_budget_after_the_user_confirms_is_used_from_step4() -> None:
    assert evidence_item("B1-SC-BUDGET")["usedFromStep"] == 4


def test_r2_council_tax_when_rent_includes_bills_is_present_and_not_included() -> None:
    charge = evidence_item("R2-CT-CHARGE")
    band = evidence_item("R2-CT-BAND")

    assert charge["status"] == "available"
    assert charge["value"]["pence"] == 185000
    assert band["status"] == "available"


def test_ids_across_evidence_documents_questions_and_replies_are_unique() -> None:
    ids = [record["id"] for file in _RECORD_FILES for record in load(file)[file]]

    assert len(ids) > 0
    assert len(ids) == len(set(ids))


def test_snapshot_household_and_home_ids_resolve_to_records() -> None:
    snapshot = load("snapshot")["snapshot"]
    household_id = load("household")["household"]["id"]
    home_ids = [h["id"] for h in load("homes")["homes"]]

    assert snapshot["householdId"] == household_id
    assert sorted(snapshot["homeIds"]) == sorted(home_ids)


def test_story_home_ids_resolve_to_homes_in_the_snapshot() -> None:
    snapshot = load("snapshot")["snapshot"]
    home_ids = set(snapshot["homeIds"])
    story_homes = [h for story in snapshot["stories"] for h in story["homeIds"]]

    assert story_homes != []
    assert [h for h in story_homes if h not in home_ids] == []


def _not_synthetic(node: Json, path: str) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if "origin" in node and node.get("synthetic") is not True:
            found.append(path)
        for key, child in node.items():
            found.extend(_not_synthetic(child, f"{path}/{key}"))
    elif isinstance(node, list):
        for index, child in enumerate(node):
            found.extend(_not_synthetic(child, f"{path}/{index}"))
    return found


def test_source_synthetic_flag_is_true_in_every_data_file() -> None:
    not_synthetic = [p for file in _DATA_FILES for p in _not_synthetic(load(file), file)]

    assert not_synthetic == [], "; ".join(not_synthetic)


def test_not_synthetic_a_source_without_the_flag_is_found() -> None:
    document = {"a": [{"origin": "plan"}], "b": {"origin": "plan", "synthetic": True}}

    assert _not_synthetic(document, "x") == ["x/a/0"]
