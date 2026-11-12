"""The fixture reader: real data in, the engine's own types out; anything else is an error."""

from pathlib import Path
from typing import Any

import pytest
from generator_support import copy_data_to, fixtures_directory, read_json, write_json
from vestagraph_engine import (
    EvidenceStatus,
    Mode,
    MoneyValue,
    Nation,
    OtherValue,
    Pence,
    Period,
    RateValue,
    YearsValue,
)
from vestagraph_generator.fixture_reader import InvalidDataError, read_fixtures


def _edit(tmp_path: Path, name: str, change: Any) -> Path:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / f"{name}.json"
    document = read_json(path)
    change(document)
    write_json(path, document)
    return fixtures


def test_read_fixtures_real_data_gives_the_snapshot_in_file_order() -> None:
    snapshot = read_json(fixtures_directory() / "data" / "snapshot.json")["snapshot"]

    data = read_fixtures(fixtures_directory())

    assert data.snapshot_date == snapshot["snapshotDate"]
    assert data.household_id == snapshot["householdId"]
    assert list(data.home_ids) == snapshot["homeIds"]
    assert [s.id for s in data.stories] == [s["id"] for s in snapshot["stories"]]
    assert [list(s.steps) for s in data.stories] == [
        [step["step"] for step in s["steps"]] for s in snapshot["stories"]
    ]
    assert [list(s.home_ids) for s in data.stories] == [s["homeIds"] for s in snapshot["stories"]]


def test_read_fixtures_real_data_gives_homes_with_mode_and_nation() -> None:
    raw = {h["id"]: h for h in read_json(fixtures_directory() / "data" / "homes.json")["homes"]}

    homes = {h.id: h for h in read_fixtures(fixtures_directory()).homes}

    assert set(homes) == set(raw)
    assert homes["B1"].mode is Mode.BUY
    assert homes["R1"].mode is Mode.RENT
    assert homes["WALES-1"].mode is None
    assert homes["WALES-1"].nation is Nation.WALES
    assert homes["B1"].nation is Nation.ENGLAND
    assert all(h.nation.value == raw[h.id]["address"]["nation"] for h in homes.values())


def test_read_fixtures_real_data_gives_the_monthly_budget_as_pence() -> None:
    budget = read_json(fixtures_directory() / "data" / "household.json")["household"][
        "monthlyBudget"
    ]

    data = read_fixtures(fixtures_directory())

    assert data.monthly_budget == Pence(budget["pence"])


def test_read_fixtures_real_data_reads_every_evidence_item_with_its_value_kind() -> None:
    raw = read_json(fixtures_directory() / "data" / "evidence.json")["evidence"]

    rows = read_fixtures(fixtures_directory()).evidence

    assert [r.item.id for r in rows] == [e["id"] for e in raw]
    assert [r.subject_type for r in rows] == [e["subjectType"] for e in raw]
    assert [r.subject_id for r in rows] == [e["subjectId"] for e in raw]
    by_id = {r.item.id: r.item for r in rows}
    deposit = by_id["HH-MORTGAGE-DEPOSIT"]
    assert deposit.value == MoneyValue(Pence(3000000), Period.ONCE)
    assert deposit.status is EvidenceStatus.AVAILABLE
    assert deposit.context_only is False
    kinds = {type(r.item.value) for r in rows}
    assert {MoneyValue, RateValue, YearsValue, OtherValue} <= kinds


def test_read_fixtures_real_data_carries_used_from_step_and_supersedes() -> None:
    raw = {
        e["id"]: e for e in read_json(fixtures_directory() / "data" / "evidence.json")["evidence"]
    }

    rows = read_fixtures(fixtures_directory()).evidence

    for row in rows:
        assert row.item.used_from_step == raw[row.item.id].get("usedFromStep")
        assert row.item.supersedes == raw[row.item.id].get("supersedes")
    assert any(r.item.used_from_step is not None for r in rows)
    assert any(r.item.supersedes is not None for r in rows)


def test_read_fixtures_file_missing_raises_an_os_error(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    (fixtures / "data" / "household.json").unlink()

    with pytest.raises(OSError, match="household"):
        read_fixtures(fixtures)


def test_read_fixtures_text_that_is_not_json_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    (fixtures / "data" / "homes.json").write_text("{not json", encoding="utf-8")

    with pytest.raises(InvalidDataError, match="homes"):
        read_fixtures(fixtures)


def test_read_fixtures_list_where_an_object_is_expected_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    write_json(fixtures / "data" / "homes.json", {"homes": 3})

    with pytest.raises(InvalidDataError):
        read_fixtures(fixtures)


def test_read_fixtures_file_that_is_a_list_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    write_json(fixtures / "data" / "snapshot.json", [1, 2])

    with pytest.raises(InvalidDataError):
        read_fixtures(fixtures)


def test_read_fixtures_number_where_text_is_expected_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(tmp_path, "evidence", lambda d: d["evidence"][0].update(id=5))

    with pytest.raises(InvalidDataError):
        read_fixtures(fixtures)


def test_read_fixtures_unknown_evidence_status_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(tmp_path, "evidence", lambda d: d["evidence"][0].update(status="surprising"))

    with pytest.raises(InvalidDataError, match="surprising"):
        read_fixtures(fixtures)


def test_read_fixtures_decimal_where_whole_pence_are_expected_raises_invalid_data(
    tmp_path: Path,
) -> None:
    fixtures = _edit(
        tmp_path, "household", lambda d: d["household"]["monthlyBudget"].update(pence=1.5)
    )

    with pytest.raises(InvalidDataError):
        read_fixtures(fixtures)


def test_read_fixtures_true_where_a_number_is_expected_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(
        tmp_path, "household", lambda d: d["household"]["monthlyBudget"].update(pence=True)
    )

    with pytest.raises(InvalidDataError):
        read_fixtures(fixtures)


def test_read_fixtures_budget_that_is_not_monthly_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(
        tmp_path, "household", lambda d: d["household"]["monthlyBudget"].update(period="year")
    )

    with pytest.raises(InvalidDataError, match="monthly"):
        read_fixtures(fixtures)


def test_read_fixtures_unknown_mode_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(tmp_path, "homes", lambda d: d["homes"][0].update(mode="lease"))

    with pytest.raises(InvalidDataError, match="lease"):
        read_fixtures(fixtures)


def test_read_fixtures_unknown_nation_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(
        tmp_path, "homes", lambda d: d["homes"][0]["address"].update(nation="Atlantis")
    )

    with pytest.raises(InvalidDataError, match="Atlantis"):
        read_fixtures(fixtures)


def test_read_fixtures_unknown_period_raises_invalid_data(tmp_path: Path) -> None:
    def change(document: Any) -> None:
        item = next(e for e in document["evidence"] if e["value"]["kind"] == "money")
        item["value"]["period"] = "fortnight"

    with pytest.raises(InvalidDataError, match="fortnight"):
        read_fixtures(_edit(tmp_path, "evidence", change))


def test_read_fixtures_evidence_without_context_only_raises_invalid_data(tmp_path: Path) -> None:
    fixtures = _edit(tmp_path, "evidence", lambda d: d["evidence"][0].pop("contextOnly"))

    with pytest.raises(InvalidDataError, match="contextOnly"):
        read_fixtures(fixtures)


def test_read_fixtures_money_without_pence_raises_invalid_data(tmp_path: Path) -> None:
    def change(document: Any) -> None:
        item = next(e for e in document["evidence"] if e["value"]["kind"] == "money")
        del item["value"]["pence"]

    with pytest.raises(InvalidDataError, match="pence"):
        read_fixtures(_edit(tmp_path, "evidence", change))


def test_read_fixtures_quantity_in_other_units_is_another_kind_of_value(tmp_path: Path) -> None:
    def change(document: Any) -> None:
        extra = dict(document["evidence"][0])
        extra.update(id="B1-ROOMS", value={"kind": "quantity", "amount": 3, "unit": "rooms"})
        document["evidence"].append(extra)

    rows = read_fixtures(_edit(tmp_path, "evidence", change)).evidence

    assert rows[-1].item.id == "B1-ROOMS"
    assert rows[-1].item.value == OtherValue()


def test_read_fixtures_home_missing_from_homes_file_is_left_for_the_generator_to_report(
    tmp_path: Path,
) -> None:
    fixtures = _edit(tmp_path, "homes", lambda d: d["homes"].pop(0))

    data = read_fixtures(fixtures)

    assert "B1" in data.home_ids
    assert "B1" not in [h.id for h in data.homes]
