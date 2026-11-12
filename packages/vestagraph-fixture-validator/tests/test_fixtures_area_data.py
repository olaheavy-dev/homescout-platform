"""Story and consistency checks on data/area.json (ported from AreaDataTests, issue 120).

Every England home has each topic or an explicit gap, Wales is not covered, every link points at
a real record, and the wording rules hold.
"""

import itertools
import re

import pytest
from fixtures_support import (
    Json,
    area_items,
    fixtures_directory,
    home,
    load,
    schema_directory,
)
from fixtures_support import read_file as _read_json

_ENGLAND_HOMES = ["B1", "B2", "R1", "R2"]

# Doc 02 section 7 / issue 120 topic order.
_TOPICS = [
    "transport-stop", "school", "crime", "flood", "sold-price", "amenity", "energy-certificate",
    "school-inspection", "broadband", "bank-rate", "commute", "planning", "leasehold-company",
]  # fmt: skip

_CRIME_FIELDS = ["month", "counts", "neighbourhoodTeam"]
_HEALTHCARE_SUBTYPES = ["pharmacy", "hospital", "gp-surgery", "clinic", "dentist"]
_AMENITY_SUBTYPES = [
    "supermarket", "shop", "park", "pharmacy", "police-station", "hospital", "gp-surgery",
    "clinic", "dentist", "childcare", "place-of-worship",
]  # fmt: skip
_R2_CERTIFICATE = ["R2-EPC"]
_ALLOWED_ORIGINS = ["official-dataset", "user-entered", "plan"]
_RECORDED_CRIME_MONTHS = ["2026-07", "2026-08"]
_AMENITY_CATEGORIES = [
    ["supermarket", "shop"],
    ["park"],
    ["hospital", "gp-surgery", "clinic", "dentist", "pharmacy"],
    ["police-station"],
    ["childcare"],
    ["place-of-worship"],
]
_LIVE_FLOOD_HOMES = ["B2"]
_WORSHIP_VALUE_FIELDS = ["name", "distanceMetres", "distanceMethod", "religion"]
_WORSHIP_LIMIT = (
    "does not establish service times, which community it serves, "
    "or that the list of places is complete."
)
_GAP_STATUSES = ["no-record-in-source", "stale", "source-failed", "not-covered"]


def _for_home(home_id: str) -> list[Json]:
    return [i for i in area_items() if i.get("homeId") == home_id]


def _topic(topic: str) -> list[Json]:
    return [i for i in area_items() if i["topic"] == topic]


def _snapshot_date() -> str:
    date: str = load("snapshot")["snapshot"]["snapshotDate"]
    return date


def test_area_every_home_id_is_a_home_in_the_homes_file() -> None:
    home_ids = {h["id"] for h in load("homes")["homes"]}

    used = [i["homeId"] for i in area_items() if "homeId" in i]

    assert used != []
    assert all(home_id in home_ids for home_id in used)


def test_area_ids_are_unique() -> None:
    ids = [i["id"] for i in area_items()]

    assert len(ids) == len(set(ids))


def test_area_every_id_follows_home_area_topic_number() -> None:
    for item in area_items():
        owner = item.get("homeId", "UK")
        topic = item["topic"].upper()
        assert re.fullmatch(re.escape(f"{owner}-AREA-{topic}-") + "[0-9]+", item["id"]), item["id"]


def test_area_every_topic_is_in_the_agreed_enum_order() -> None:
    schema = _read_json(schema_directory() / "area.schema.json")

    assert schema["$defs"]["areaItem"]["properties"]["topic"]["enum"] == _TOPICS


@pytest.mark.parametrize("home_id", _ENGLAND_HOMES)
def test_area_each_england_home_has_every_required_topic_or_an_explicit_gap(home_id: str) -> None:
    tenure = home(home_id)["tenure"]
    required = [
        t
        for t in _TOPICS
        if t != "bank-rate" and (t != "leasehold-company" or tenure == "leasehold")
    ]
    present = {i["topic"] for i in _for_home(home_id)}

    assert [t for t in required if t not in present] == []


def test_area_every_home_item_of_an_england_home_is_covered_or_a_gap_that_says_why() -> None:
    for home_id in _ENGLAND_HOMES:
        statuses = [i["status"] for i in _for_home(home_id)]
        assert statuses != [], home_id
        assert "not-covered" not in statuses, home_id


def test_area_wales1_has_only_not_covered_items() -> None:
    items = _for_home("WALES-1")

    assert items != []
    assert {i["status"] for i in items} == {"not-covered"}


def test_area_wales1_has_an_item_for_each_per_home_topic_except_leasehold_and_bank_rate() -> None:
    topics = {i["topic"] for i in _for_home("WALES-1")}

    missing = [
        t for t in _TOPICS if t not in ("bank-rate", "leasehold-company") and t not in topics
    ]
    assert missing == []


def test_area_gap_examples_include_every_status_the_issue_requires() -> None:
    statuses = {i["status"] for i in area_items()}

    assert [s for s in _GAP_STATUSES if s not in statuses] == []


def test_area_every_source_is_synthetic_and_labelled() -> None:
    for item in area_items():
        assert item["source"]["synthetic"] is True, item["id"]
        assert item["source"]["origin"] in _ALLOWED_ORIGINS, item["id"]


def test_area_dates_are_not_after_the_snapshot_date() -> None:
    snapshot = _snapshot_date()
    for item in area_items():
        date = item["source"]["date"]
        assert date <= snapshot[: len(date)], item["id"]


def test_area_file_never_uses_safe_unsafe_verified_or_approved_wording() -> None:
    # Rule 4: the product never says a home is verified, safe or approved,
    # and crime is never presented as safe or unsafe.
    text = (fixtures_directory() / "data" / "area.json").read_text(encoding="utf-8")

    found = [
        m.group(0) for m in re.finditer(r"\b(safe|unsafe|verified|approved)\b", text, re.IGNORECASE)
    ]
    assert found == []


def test_area_schema_file_has_no_rating_or_score_field_on_crime() -> None:
    crime = _read_json(schema_directory() / "area.schema.json")["$defs"]["crimeValue"]

    assert crime["additionalProperties"] is False
    assert sorted(crime["properties"]) == sorted(_CRIME_FIELDS)


def test_area_every_distance_names_its_synthetic_method() -> None:
    with_distance = [i for i in area_items() if "distanceMetres" in (i.get("value") or {})]

    assert with_distance != []
    for item in with_distance:
        assert "synthetic" in item["value"]["distanceMethod"], item["id"]


@pytest.mark.parametrize(
    ("home_id", "topic"),
    [
        *itertools.product(_ENGLAND_HOMES, ["transport-stop", "school", "crime"]),
        ("B1", "sold-price"),
        ("B2", "sold-price"),
    ],
)
def test_area_priority_topic_has_two_to_four_items_for_each_home(home_id: str, topic: str) -> None:
    count = sum(1 for i in _for_home(home_id) if i["topic"] == topic)

    assert 2 <= count <= 4


def test_area_crime_for_b1_and_b2_covers_two_different_months() -> None:
    for home_id in ("B1", "B2"):
        months = {
            i["value"]["month"]
            for i in _for_home(home_id)
            if i["topic"] == "crime" and i["status"] == "recorded"
        }
        assert len(months) >= 2, home_id


def test_area_every_home_has_a_healthcare_location() -> None:
    for home_id in _ENGLAND_HOMES:
        assert any(
            i["topic"] == "amenity" and i.get("subtype") in _HEALTHCARE_SUBTYPES
            for i in _for_home(home_id)
        ), home_id


def test_area_amenities_cover_every_subtype_somewhere_in_england() -> None:
    present = {
        i["subtype"]
        for home_id in _ENGLAND_HOMES
        for i in _for_home(home_id)
        if i["topic"] == "amenity" and "subtype" in i
    }

    assert [s for s in _AMENITY_SUBTYPES if s not in present] == []


def test_area_flood_warnings_exactly_one_home_has_a_live_warning() -> None:
    live = [i["homeId"] for i in _topic("flood") if i["status"] == "recorded"]

    assert live == _LIVE_FLOOD_HOMES


def test_area_flood_items_with_no_record_point_the_user_to_the_long_term_checker() -> None:
    no_record = [i for i in _topic("flood") if i["status"] == "no-record-in-source"]

    assert no_record != []
    for item in no_record:
        assert item["link"]["url"] == "https://www.gov.uk/check-long-term-flood-risk", item["id"]


def test_area_every_england_home_has_a_flood_item() -> None:
    for home_id in _ENGLAND_HOMES:
        assert any(i["topic"] == "flood" for i in _for_home(home_id)), home_id


@pytest.mark.parametrize(
    ("home_id", "certificate_id", "cost_id"),
    [
        ("B1", "B1-EPC", "B1-EPC-COST"),
        ("B2", "B2-EPC", "B2-EPC-COST"),
        ("R1", "R1-EPC", "R1-EPC-COST"),
    ],
)
def test_area_energy_item_points_at_the_certificate_and_its_cost_in_the_evidence_file(
    home_id: str, certificate_id: str, cost_id: str
) -> None:
    (item,) = [i for i in _for_home(home_id) if i["topic"] == "energy-certificate"]

    assert item["status"] == "recorded"
    assert item["value"]["evidenceItemIds"] == [certificate_id, cost_id]


def test_area_r2_energy_is_stale_and_points_at_its_expired_certificate_only() -> None:
    (item,) = [i for i in _for_home("R2") if i["topic"] == "energy-certificate"]

    assert item["status"] == "stale"
    assert item["value"]["evidenceItemIds"] == _R2_CERTIFICATE


def test_area_bank_rate_is_one_shared_item_with_a_source_date() -> None:
    items = _topic("bank-rate")

    assert len(items) == 1
    assert "homeId" not in items[0]
    assert items[0]["source"]["date"] != ""


def test_area_commute_uses_the_household_commute_criterion() -> None:
    criterion_ids = [p["id"] for p in load("household")["household"]["priorities"]]
    recorded = [i for i in _topic("commute") if i["status"] == "recorded"]

    assert recorded != []
    for item in recorded:
        assert item["value"]["criterionId"] in criterion_ids, item["id"]


def test_area_every_england_home_has_a_commute_item() -> None:
    for home_id in _ENGLAND_HOMES:
        assert any(i["topic"] == "commute" for i in _for_home(home_id)), home_id


def test_area_school_inspections_point_at_a_school_of_the_same_home() -> None:
    inspections = [i for i in _topic("school-inspection") if i.get("value") is not None]
    by_id = {i["id"]: i for i in area_items()}

    assert inspections != []
    for item in inspections:
        school = by_id[item["value"]["schoolItemId"]]
        assert school["topic"] == "school", school["id"]
        assert school["homeId"] == item["homeId"], school["id"]


# Places of worship are listed as the nearest places only, every faith alike: never counts,
# densities or an area's religious makeup (founder decision, 11 Nov 2026; register PD-13).
def test_area_places_of_worship_are_single_places_with_a_religion_and_one_shared_limit() -> None:
    worship = [
        i
        for home_id in _ENGLAND_HOMES
        for i in _for_home(home_id)
        if i["topic"] == "amenity" and i.get("subtype") == "place-of-worship"
    ]

    assert worship != []
    shown = [i for i in worship if i["status"] in ("recorded", "stale")]
    assert shown != []
    for item in shown:
        assert sorted(item["value"]) == sorted(_WORSHIP_VALUE_FIELDS), item["id"]
    assert all(_WORSHIP_LIMIT in i["doesNotEstablish"] for i in worship)


@pytest.mark.parametrize("home_id", _ENGLAND_HOMES)
def test_area_each_england_home_has_every_amenity_category_or_an_explicit_no_record_item(
    home_id: str,
) -> None:
    amenities = [i for i in _for_home(home_id) if i["topic"] == "amenity" and "subtype" in i]

    for category in _AMENITY_CATEGORIES:
        assert any(
            i["subtype"] in category and i["status"] in ("recorded", "no-record-in-source", "stale")
            for i in amenities
        ), f"{home_id}: {'/'.join(category)}"


def test_area_energy_items_point_at_evidence_items_that_exist() -> None:
    evidence_ids = {e["id"] for e in load("evidence")["evidence"]}
    with_value = [i for i in _topic("energy-certificate") if i.get("value") is not None]

    assert with_value != []
    for item in with_value:
        assert all(e in evidence_ids for e in item["value"]["evidenceItemIds"]), item["id"]


def test_area_energy_items_never_say_this_flat() -> None:
    shown = [i for i in _topic("energy-certificate") if i["status"] != "not-covered"]

    assert shown != []
    for item in shown:
        text = item["doesNotEstablish"]
        assert "this flat" not in text, item["id"]
        assert "this home" in text, item["id"]
        assert "not actual bills" in text, item["id"]


def test_area_flood_items_never_use_surface_water_as_a_subtype_and_say_why_and_where_to_look() -> (
    None
):
    shown = [i for i in _topic("flood") if i["status"] != "not-covered"]

    assert shown != []
    for item in shown:
        assert item["subtype"] in ("rivers-and-sea", "groundwater"), item["id"]
        assert "Warnings are not issued for surface water flooding" in item["doesNotEstablish"], (
            item["id"]
        )


def test_area_commute_is_the_households_own_estimate_not_a_routed_journey() -> None:
    shown = [i for i in _topic("commute") if i["status"] != "not-covered"]

    assert shown != []
    for item in shown:
        assert item["source"]["origin"] == "user-entered", item["id"]
        assert item["source"]["label"] == "the household's own estimate", item["id"]
        assert "not a routed or timetabled journey" in item["doesNotEstablish"], item["id"]
        assert (
            item["value"]["method"]
            == "estimated by the household; not a routed journey time (routing is DA-06)"
        ), item["id"]


def test_area_sold_price_addresses_are_unique_so_no_address_has_two_prices() -> None:
    addresses = [
        i["value"]["addressText"] for i in _topic("sold-price") if i.get("value") is not None
    ]

    assert addresses != []
    assert len(addresses) == len(set(addresses))


def test_area_a_school_inspected_is_inspected_the_same_way_everywhere_it_appears() -> None:
    by_school: dict[str, set[str]] = {}
    for item in _topic("school-inspection"):
        if item.get("value") is not None:
            value = item["value"]
            by_school.setdefault(value["schoolName"], set()).add(
                value["framework"] + "|" + value["inspectionDate"]
            )

    assert by_school != {}
    for school, ways in by_school.items():
        assert len(ways) == 1, school


def test_area_crime_months_are_the_two_lagged_months() -> None:
    months = [i["value"]["month"] for i in _topic("crime") if i.get("value") is not None]

    assert months != []
    assert all(m in _RECORDED_CRIME_MONTHS for m in months)


def test_area_every_england_home_with_crime_covers_both_lagged_months_or_names_a_failure() -> None:
    for home_id in _ENGLAND_HOMES:
        crime = [i for i in _for_home(home_id) if i["topic"] == "crime"]
        for month in _RECORDED_CRIME_MONTHS:
            recorded = any(
                i.get("value") is not None and i["value"]["month"] == month for i in crime
            )
            failed = any(i["status"] == "source-failed" and month in i["label"] for i in crime)
            assert recorded or failed, f"{home_id} {month}"


def test_area_energy_items_that_are_stale_do_not_copy_the_certificate_year() -> None:
    stale = [i for i in _topic("energy-certificate") if i["status"] == "stale"]

    assert stale != []
    for item in stale:
        assert re.search(r"\d{4}", item["label"]) is None, item["id"]


def test_area_value_dates_are_not_after_the_snapshot_date() -> None:
    snapshot = _snapshot_date()
    date_fields = [
        "month",
        "saleDate",
        "inspectionDate",
        "statusDate",
        "receivedDate",
        "effectiveDate",
    ]
    checked = 0
    for item in area_items():
        if item.get("value") is None:
            continue
        for field in (f for f in date_fields if f in item["value"]):
            date = item["value"][field]
            checked += 1
            assert date <= snapshot[: len(date)], f"{item['id']} {field}"
    assert checked > 0


def test_area_bank_rate_is_labelled_as_a_sample_not_the_actual_rate() -> None:
    (item,) = _topic("bank-rate")

    assert "sample value, not the actual Bank Rate" in item["label"]
    assert "sample value, not the actual Bank Rate" in item["doesNotEstablish"]


def _values_as_text(home_id: str) -> list[str]:
    return [
        str(v)
        for i in _for_home(home_id)
        if i.get("value") is not None
        for v in i["value"].values()
    ]


def test_area_r1_is_set_on_station_road_and_r2_on_canal_street() -> None:
    assert _values_as_text("R1") != []
    assert _values_as_text("R2") != []
    assert not any("Canal" in text for text in _values_as_text("R1"))
    assert not any("Station Road" in text for text in _values_as_text("R2"))


def test_area_crime_categories_are_unique_within_each_item() -> None:
    crime = [i for i in _topic("crime") if i.get("value") is not None]

    assert crime != []
    for item in crime:
        categories = [c["category"] for c in item["value"]["counts"]]
        assert len(categories) == len(set(categories)), item["id"]


def test_area_council_tax_is_not_area_data() -> None:
    # Council tax is a user-entered cost input already (evidence file); it has no area topic.
    assert not any("council" in i["topic"] for i in area_items())
