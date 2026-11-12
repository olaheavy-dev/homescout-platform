"""The real data files must pass their schemas and match the approved sample data.

Ported from RealDataTests.

Expected figures below are copied from docs/planning/stage-2-plan.md section 1 (pounds converted
to pence by hand), not read back from the data files.
"""

from collections.abc import Iterator
from fractions import Fraction
from pathlib import Path

import pytest
from fixtures_support import (
    Json,
    evidence_item,
    fixtures_directory,
    home,
    lines,
    load,
    mentions,
    parse,
    question,
    read_file,
)
from vestagraph_fixture_validator.validator import validate_fixtures

_EXPECTED_CONTEXT_ONLY = ["B1-EPC-COST", "B2-EPC-COST", "R1-EPC-COST"]


def test_validate_fixtures_all_fixture_files_validate_against_their_schemas_with_no_problems() -> (
    None
):
    problems = validate_fixtures(fixtures_directory())

    assert problems == [], "\n".join(lines(problems))


def test_validate_fixtures_data_file_with_no_schema_available_is_reported(tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "mystery.json").write_text("{}", encoding="utf-8")

    problems = validate_fixtures(tmp_path)

    assert problems != []


def test_validate_fixtures_non_string_schema_field_is_reported_readably(tmp_path: Path) -> None:
    (tmp_path / "test-cases").mkdir()
    (tmp_path / "test-cases" / "bad.json").write_text('{ "$schema": 5 }', encoding="utf-8")

    assert mentions(validate_fixtures(tmp_path), "Must be a string")


def test_snapshot_date_in_snapshot_file_is_the_approved_date() -> None:
    assert load("snapshot")["snapshot"]["snapshotDate"] == "2026-10-23"


def test_wales1_address_is_wales_and_not_yet_covered() -> None:
    item = home("WALES-1")

    assert item["address"]["nation"] == "Wales"
    assert item["coverage"] == "not-yet-covered"


def test_home_in_every_record_has_a_nation() -> None:
    homes = load("homes")["homes"]

    assert len(homes) == 5
    assert all(h["address"].get("nation") is not None for h in homes)


def test_northbridge_homes_postcodes_start_with_nb() -> None:
    postcodes = [
        h["address"]["postcode"]
        for h in load("homes")["homes"]
        if h["address"]["town"] == "Northbridge"
    ]

    assert len(postcodes) == 4
    assert all(p.startswith("NB") for p in postcodes)


def test_b1_postcode_matches_six_candidate_units_and_the_selected_one_is_among_them() -> None:
    unit = home("B1")["unit"]
    candidate_ids = [c["id"] for c in unit["candidateUnits"]]

    assert len(candidate_ids) == 6
    assert unit["selectedUnitId"] in candidate_ids
    assert len(set(candidate_ids)) == len(candidate_ids)


@pytest.mark.parametrize("item_id", ["R2-ENERGY", "R2-WATER", "R2-BROADBAND"])
def test_r2_bills_are_included_not_zero(item_id: str) -> None:
    item = evidence_item(item_id)

    assert item["status"] == "included"
    assert "value" not in item


@pytest.mark.parametrize("item_id", ["B1-INSURANCE"])
def test_b1_buildings_insurance_is_included_in_the_service_charge_not_zero(item_id: str) -> None:
    item = evidence_item(item_id)

    assert item["status"] == "included"
    assert "value" not in item


def test_b1_buildings_insurance_is_used_from_step_three_when_its_only_source_arrives() -> None:
    # Its only source is the management pack, which arrives at story step 3 (issue #37).
    # Before that the line is missing, not included.
    item = evidence_item("B1-INSURANCE")

    assert item["usedFromStep"] == 3
    assert item["source"]["documentId"] == "B1-MGMT-PACK"


@pytest.mark.parametrize(
    "item_id",
    ["B1-MAINTENANCE", "B1-STAMP-DUTY", "B1-LEGAL-FEES", "B2-STAMP-DUTY", "B2-LEGAL-FEES"],
)
def test_not_calculated_items_are_not_calculated_not_zero(item_id: str) -> None:
    item = evidence_item(item_id)

    assert item["status"] == "not-calculated"
    assert "value" not in item


@pytest.mark.parametrize(
    ("item_id", "pence", "price_basis"),
    [
        ("B1-EPC-COST", 78000, "2019 prices"),
        ("B2-EPC-COST", 115000, "2021 prices"),
        ("R1-EPC-COST", 72000, "2022 prices"),
    ],
)
def test_energy_certificate_costs_are_flagged_context_only_at_their_old_prices(
    item_id: str, pence: int, price_basis: str
) -> None:
    item = evidence_item(item_id)

    assert item["contextOnly"] is True
    assert item["value"]["pence"] == pence
    assert item["value"]["period"] == "year"
    assert item["priceBasis"] == price_basis


def test_evidence_item_marked_context_only_is_an_energy_certificate_cost() -> None:
    context_only = [i["id"] for i in load("evidence")["evidence"] if i["contextOnly"]]

    assert sorted(context_only) == sorted(_EXPECTED_CONTEXT_ONLY)


def test_r2_certificate_is_expired_2025_issued_2015_with_cited_gov_uk_text() -> None:
    item = evidence_item("R2-EPC")
    source = item["source"]

    assert item["status"] == "stale"
    assert item["value"]["issuedYear"] == 2015
    assert item["value"]["expiredYear"] == 2025
    assert (
        source["citationUrl"]
        == "https://www.gov.uk/buy-sell-your-home/energy-performance-certificates"
    )
    assert "renting out a property" in source["citedText"]


# Expected values from the plan, section 1. Pounds converted to pence by hand: pounds x 100.
@pytest.mark.parametrize(
    ("item_id", "pence", "period"),
    [
        ("B1-PRICE", 19000000, "once"),
        ("B1-SC-LISTING", 240000, "year"),
        ("B1-SC-BUDGET", 372000, "year"),
        ("B1-GROUND-RENT", 25000, "year"),
        ("B1-CT-CHARGE", 210000, "year"),
        ("B1-ENERGY-ESTIMATE", 8500, "month"),
        ("B1-WATER-ESTIMATE", 4500, "month"),
        ("B1-BROADBAND-ESTIMATE", 3000, "month"),
        ("B2-PRICE", 25500000, "once"),
        ("B2-CT-CHARGE", 185000, "year"),
        ("B2-INSURANCE", 3500, "month"),
        ("B2-MAINTENANCE", 6000, "month"),
        ("B2-ENERGY-ESTIMATE", 12000, "month"),
        ("B2-WATER-ESTIMATE", 5000, "month"),
        ("B2-BROADBAND-ESTIMATE", 3000, "month"),
        ("R1-RENT", 120000, "month"),
        ("R1-CT-CHARGE", 160000, "year"),
        ("R1-DEPOSIT", 138000, "once"),
        ("R1-FIRST-MONTH-RENT", 120000, "once"),
        ("R1-ENERGY-ESTIMATE", 8000, "month"),
        ("R1-WATER-ESTIMATE", 4500, "month"),
        ("R1-BROADBAND-ESTIMATE", 3000, "month"),
        ("R2-RENT", 127500, "month"),
        ("R2-CT-CHARGE", 185000, "year"),
        ("R2-DEPOSIT", 147000, "once"),
        ("R2-FIRST-MONTH-RENT", 127500, "once"),
        ("HH-MORTGAGE-DEPOSIT", 3000000, "once"),
        ("HH-MOVING-COSTS", 120000, "once"),
    ],
)
def test_money_input_approved_in_plan_matches_the_file(
    item_id: str, pence: int, period: str
) -> None:
    value = evidence_item(item_id)["value"]

    assert value["pence"] == pence
    assert value["period"] == period


def test_mortgage_and_budget_inputs_approved_in_plan_match_the_file() -> None:
    rate = evidence_item("HH-MORTGAGE-RATE")["value"]
    term = evidence_item("HH-MORTGAGE-TERM")["value"]
    budget = load("household")["household"]["monthlyBudget"]

    assert rate["basisPoints"] == 550, "5.5% is 550 basis points"
    assert term["amount"] == 25
    assert budget["pence"] == 160000
    assert budget["period"] == "month"


def test_lease_and_council_tax_bands_approved_in_plan_match_the_file() -> None:
    lease = evidence_item("B1-LEASE-TERM")["value"]

    assert lease["years"] == 125
    assert lease["startDate"] == "2015-01-01"
    assert evidence_item("B1-CT-BAND")["value"]["band"] == "C"
    assert evidence_item("B2-CT-BAND")["value"]["band"] == "B"
    assert evidence_item("R1-CT-BAND")["value"]["band"] == "A"
    assert evidence_item("R2-CT-BAND")["value"]["band"] == "B"


def test_b1_service_charge_keeps_the_listing_figure_and_the_later_budget() -> None:
    listing = evidence_item("B1-SC-LISTING")
    budget = evidence_item("B1-SC-BUDGET")

    assert listing["source"]["origin"] == "listing-claim"
    assert budget["source"]["origin"] == "document"
    assert budget["supersedes"] == "B1-SC-LISTING"


def _fractional_numbers(node: Json) -> Iterator[Fraction]:
    """Every number written with a decimal point or an exponent (read as a ``Fraction``)."""
    if isinstance(node, Fraction):
        yield node
    elif isinstance(node, dict):
        for child in node.values():
            yield from _fractional_numbers(child)
    elif isinstance(node, list):
        for child in node:
            yield from _fractional_numbers(child)


def test_numbers_in_every_fixture_file_are_whole_numbers() -> None:
    names = ["household", "homes", "evidence", "documents", "questions", "replies", "snapshot"]
    documents = {name: load(name) for name in names}
    for path in sorted((fixtures_directory() / "test-cases").glob("*.json")):
        documents[path.name] = read_file(path)

    assert len(documents) == 9
    for name, document in documents.items():
        assert list(_fractional_numbers(document)) == [], (
            f"{name} must contain no fractional numbers"
        )


def test_fractional_numbers_a_decimal_or_an_exponent_is_found() -> None:
    document = parse('{"a": [1, 2.5], "b": {"c": 3e2, "d": 4}}')

    assert sorted(_fractional_numbers(document)) == [Fraction(5, 2), Fraction(300)]


def test_question_final_status_equals_its_last_transition() -> None:
    for item in load("questions")["questions"]:
        assert item["status"] == item["statusHistory"][-1]["status"], item["id"]


def test_question_statuses_match_the_stories_in_the_plan() -> None:
    def history(question_id: str) -> list[str]:
        return [h["status"] for h in question(question_id)["statusHistory"]]

    assert question("B1-Q-MAJOR-WORKS")["status"] == "waiting-for-reply"
    assert "partially-answered" in history("B1-Q-SERVICE-CHARGE")
    assert "partially-answered" in history("R1-Q-WATER")


def _ids(file: str, key: str) -> set[str]:
    return {item["id"] for item in load(file)[key]}


def test_reference_in_any_record_points_at_a_record_that_exists() -> None:
    home_ids, evidence_ids = _ids("homes", "homes"), _ids("evidence", "evidence")
    document_ids, question_ids = _ids("documents", "documents"), _ids("questions", "questions")
    reply_ids = _ids("replies", "replies")
    missing: list[str] = []

    def check(ok: bool, what: str) -> None:
        if not ok:
            missing.append(what)

    def check_optional(reference: str | None, known: set[str], what: str) -> None:
        if reference is not None:
            check(reference in known, f"{what} {reference}")

    for item in load("evidence")["evidence"]:
        subject_id = item["subjectId"]
        known_subject = (
            subject_id in home_ids if item["subjectType"] == "home" else subject_id == "RIVERS"
        )
        check(known_subject, f"{item['id']} subject {subject_id}")
        check_optional(item.get("supersedes"), evidence_ids, f"{item['id']} supersedes")
        check_optional(
            item["source"].get("documentId"), document_ids, f"{item['id']} source document"
        )

    for doc in load("documents")["documents"]:
        check(doc["homeId"] in home_ids, f"{doc['id']} home")
        for evidence_id in doc["evidenceIds"]:
            check(evidence_id in evidence_ids, f"{doc['id']} evidence {evidence_id}")

    for item in load("questions")["questions"]:
        check(item["homeId"] in home_ids, f"{item['id']} home")
        for step in item["statusHistory"]:
            check_optional(step.get("replyId"), reply_ids, f"{item['id']} reply")
            check_optional(step.get("documentId"), document_ids, f"{item['id']} document")
        for evidence_id in item.get("relatedEvidenceIds", []):
            check(evidence_id in evidence_ids, f"{item['id']} evidence {evidence_id}")

    for reply in load("replies")["replies"]:
        check(reply["questionId"] in question_ids, f"{reply['id']} question")
        check_optional(reply.get("documentId"), document_ids, f"{reply['id']} document")

    assert missing == [], "; ".join(missing)
