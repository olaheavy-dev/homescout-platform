"""The area schema must refuse bad data (ported from AreaSchemaRejectionTests).

Each test starts from a real area record, breaks one thing, and expects the schema to complain
about that thing.
"""

import shutil
from pathlib import Path

import pytest
from fixtures_support import (
    Json,
    area_item,
    lines,
    mentions,
    number,
    schema_directory,
    validate_record,
)
from vestagraph_fixture_validator.validator import validate_fixtures

_SCHOOL = "B1-AREA-SCHOOL-1"
_CRIME = "B1-AREA-CRIME-1"
_INSPECTION = "B1-AREA-SCHOOL-INSPECTION-1"


def _problems(item: Json) -> list[str]:
    return lines(validate_record("area", "area", item))


def _mentions(item: Json, text: str) -> bool:
    return mentions(validate_record("area", "area", item), text)


@pytest.mark.parametrize(
    "item_id",
    [
        _SCHOOL,
        _CRIME,
        _INSPECTION,
        "UK-AREA-BANK-RATE-1",
        "B1-AREA-ENERGY-CERTIFICATE-1",
        "B1-AREA-COMMUTE-1",
        "B1-AREA-AMENITY-7",
    ],
)
def test_validate_instance_area_unchanged_real_record_is_accepted(item_id: str) -> None:
    assert _problems(area_item(item_id)) == []


def test_validate_instance_area_item_with_no_source_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["source"]

    assert _mentions(item, "source")


def test_validate_instance_area_source_with_no_synthetic_flag_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["source"]["synthetic"]

    assert _mentions(item, "synthetic")


def test_validate_instance_area_source_with_no_date_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["source"]["date"]

    assert _mentions(item, "date")


def test_validate_instance_area_item_with_no_does_not_establish_text_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["doesNotEstablish"]

    assert _mentions(item, "doesNotEstablish")


def test_validate_instance_area_item_with_no_coverage_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["coverage"]

    assert _mentions(item, "coverage")


@pytest.mark.parametrize("field", ["rating", "score", "safetyLevel"])
def test_validate_instance_area_crime_item_with_a_rating_field_is_rejected(field: str) -> None:
    item = area_item(_CRIME)
    item["value"][field] = "low"

    assert _mentions(item, "/value")


def test_validate_instance_area_crime_count_of_zero_is_rejected() -> None:
    # A category with no recorded crimes is simply absent; a zero would read as "none happened"
    # (rule 7).
    item = area_item(_CRIME)
    item["value"]["counts"][0]["count"] = 0

    assert _mentions(item, "/value/counts/0/count")


def test_validate_instance_area_crime_category_outside_the_list_is_rejected() -> None:
    item = area_item(_CRIME)
    item["value"]["counts"][0]["category"] = "dangerous-area"

    assert _mentions(item, "/value/counts/0/category")


def test_validate_instance_area_school_inspection_with_no_framework_is_rejected() -> None:
    item = area_item(_INSPECTION)
    del item["value"]["framework"]

    assert _mentions(item, "framework")


def test_validate_instance_area_school_inspection_with_no_inspection_date_is_rejected() -> None:
    item = area_item(_INSPECTION)
    del item["value"]["inspectionDate"]

    assert _mentions(item, "inspectionDate")


def test_validate_instance_area_school_inspection_with_a_single_overall_grade_is_rejected() -> None:
    # Doc 02 section 7: no single overall grade; outcomes are listed per area under their framework.
    item = area_item(_INSPECTION)
    item["value"]["overallGrade"] = "Good"

    assert _mentions(item, "/value")


def test_validate_instance_area_topic_outside_the_enum_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["topic"] = "council-tax"

    assert _mentions(item, "/topic")


@pytest.mark.parametrize("status", ["none", "available", "zero"])
def test_validate_instance_area_status_outside_the_enum_is_rejected(status: str) -> None:
    item = area_item(_SCHOOL)
    item["status"] = status

    assert _mentions(item, "/status")


def test_validate_instance_area_not_covered_item_that_carries_a_value_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["status"] = "not-covered"

    assert _mentions(item, "/value")


def test_validate_instance_area_recorded_item_with_no_value_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["value"]

    assert _mentions(item, "value")


def test_validate_instance_area_distance_with_no_method_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["value"]["distanceMethod"]

    assert _mentions(item, "distanceMethod")


def test_validate_instance_area_distance_as_a_decimal_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["value"]["distanceMetres"] = number("450.5")

    assert _mentions(item, "/value/distanceMetres")


def test_validate_instance_area_amenity_with_no_subtype_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-1")
    del item["subtype"]

    assert _mentions(item, "subtype")


def test_validate_instance_area_amenity_subtype_outside_the_list_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-1")
    item["subtype"] = "casino"

    assert _mentions(item, "/subtype")


def test_validate_instance_area_place_of_worship_with_no_religion_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-7")
    del item["value"]["religion"]

    assert _mentions(item, "religion")


def test_validate_instance_area_stale_place_of_worship_with_no_religion_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-7")
    item["status"] = "stale"
    del item["value"]["religion"]

    assert _mentions(item, "religion")


def test_validate_instance_area_place_of_worship_religion_outside_the_list_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-7")
    item["value"]["religion"] = "unknown-faith"

    assert _mentions(item, "/value/religion")


def test_validate_instance_area_religion_on_a_non_worship_amenity_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-1")
    item["value"]["religion"] = "christian"

    assert _mentions(item, "religion")


def test_validate_instance_area_subtype_on_a_topic_that_has_none_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["subtype"] = "supermarket"

    assert _mentions(item, "/subtype")


def test_validate_instance_area_id_that_does_not_follow_the_pattern_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["id"] = "b1-school-1"

    assert _mentions(item, "/id")


def test_validate_instance_area_home_item_with_no_home_id_is_rejected() -> None:
    item = area_item(_SCHOOL)
    del item["homeId"]

    assert _mentions(item, "homeId")


def test_validate_instance_area_bank_rate_tied_to_a_home_is_rejected() -> None:
    item = area_item("UK-AREA-BANK-RATE-1")
    item["homeId"] = "B1"

    assert _mentions(item, "homeId")


def test_validate_instance_area_bank_rate_as_a_decimal_is_rejected() -> None:
    item = area_item("UK-AREA-BANK-RATE-1")
    item["value"]["basisPoints"] = number("400.5")

    assert _mentions(item, "/value/basisPoints")


def test_validate_instance_area_flood_item_that_has_no_flood_type_is_rejected() -> None:
    item = area_item("B2-AREA-FLOOD-1")
    del item["subtype"]

    assert _mentions(item, "subtype")


def test_validate_instance_area_link_that_is_not_https_is_rejected() -> None:
    item = area_item("B1-AREA-FLOOD-1")
    item["link"]["url"] = "http://example.invalid/flood"

    assert _mentions(item, "/link/url")


def test_validate_instance_area_unknown_extra_field_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["areaScore"] = 7

    assert _mentions(item, "areaScore")


def test_validate_fixtures_invalid_area_file_is_reported_against_the_area_schema(
    tmp_path: Path,
) -> None:
    (tmp_path / "data").mkdir()
    shutil.copytree(schema_directory(), tmp_path / "schema")
    (tmp_path / "data" / "area.json").write_text('{ "area": [ { "id": "x" } ] }', encoding="utf-8")

    problems = lines(validate_fixtures(tmp_path))

    assert any("area.json" in line for line in problems)
    assert any("topic" in line for line in problems)


@pytest.mark.parametrize("status", ["no-record-in-source", "source-failed", "not-covered"])
def test_validate_instance_area_gap_item_that_carries_a_value_is_rejected(status: str) -> None:
    item = area_item(_SCHOOL)
    item["status"] = status

    assert _mentions(item, "/value")


def test_validate_instance_area_stale_item_with_no_value_is_rejected() -> None:
    item = area_item(_SCHOOL)
    item["status"] = "stale"
    del item["value"]

    assert _mentions(item, "value")


def test_validate_instance_area_flood_subtype_on_an_amenity_is_rejected() -> None:
    item = area_item("B1-AREA-AMENITY-1")
    item["subtype"] = "rivers-and-sea"

    assert _mentions(item, "/subtype")


def test_validate_instance_area_amenity_subtype_on_a_flood_item_is_rejected() -> None:
    item = area_item("B2-AREA-FLOOD-1")
    item["subtype"] = "supermarket"

    assert _mentions(item, "/subtype")


def test_validate_instance_area_live_flood_warning_on_surface_water_is_rejected() -> None:
    # The Environment Agency issues no surface-water warnings; long-term surface-water risk is a
    # link only.
    item = area_item("B2-AREA-FLOOD-1")
    item["subtype"] = "surface-water"

    assert _mentions(item, "/subtype")


def test_validate_instance_area_childcare_amenity_is_accepted() -> None:
    item = area_item("B1-AREA-AMENITY-1")
    item["subtype"] = "childcare"

    assert _problems(item) == []


def test_validate_instance_area_energy_item_with_no_evidence_link_is_rejected() -> None:
    item = area_item("B1-AREA-ENERGY-CERTIFICATE-1")
    del item["value"]["evidenceItemIds"]

    assert _mentions(item, "evidenceItemIds")


def test_validate_instance_area_energy_item_that_copies_the_rating_is_rejected() -> None:
    # Inputs are recorded once (rule 2): the certificate lives in the evidence file, the area
    # item points at it.
    item = area_item("B1-AREA-ENERGY-CERTIFICATE-1")
    item["value"]["rating"] = "C"

    assert _mentions(item, "/value")


def test_validate_instance_area_energy_item_that_copies_the_issued_year_is_rejected() -> None:
    item = area_item("B1-AREA-ENERGY-CERTIFICATE-1")
    item["value"]["issuedYear"] = 2019

    assert _mentions(item, "/value")


def test_validate_instance_area_energy_item_with_a_hand_made_cost_range_is_rejected() -> None:
    item = area_item("B1-AREA-ENERGY-CERTIFICATE-1")
    item["value"]["estimatedAnnualCostRange"] = {"lowPence": 1, "highPence": 2}

    assert _mentions(item, "/value")


def test_validate_instance_area_crime_counts_that_are_exact_duplicates_are_rejected() -> None:
    # uniqueItems catches exact duplicates only; a repeated category with a different count is
    # caught by
    # test_area_crime_categories_are_unique_within_each_item.
    item = area_item(_CRIME)
    item["value"]["counts"].append(dict(item["value"]["counts"][0]))

    assert _mentions(item, "counts")


def test_validate_instance_area_sold_price_of_an_other_property_type_is_accepted() -> None:
    item = area_item("B1-AREA-SOLD-PRICE-1")
    item["value"]["propertyType"] = "other"

    assert _problems(item) == []
