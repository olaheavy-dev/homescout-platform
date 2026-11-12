"""Reads the fixture data, asks the cost engine for every figure and writes ``costs.json``.

Ported from the C# ``CostsGenerator``. Nothing in the file is typed by hand (AGENTS rule 2). The
output depends only on the data files, never on the clock.
"""

import json
import os
from pathlib import Path
from typing import TextIO

from vestagraph_engine import (
    ChangeKind,
    CostChange,
    Error,
    ErrorCategory,
    HomeCosts,
    HomeFacts,
    LineResult,
    MortgageSummary,
    Nation,
    PartialReason,
    Pence,
    Result,
    ScenarioCosts,
    build_home_costs,
    figure_ids,
)
from vestagraph_engine.cost_categories import category_id, status_id

from vestagraph_generator.costs_document import (
    BudgetDocument,
    ChangeDocument,
    CostsDocument,
    FigureDocument,
    HomeDocument,
    LineDocument,
    MonthlyDocument,
    MortgageDocument,
    PartialReasonDocument,
    ScenarioDocument,
    TotalDocument,
    UpfrontDocument,
    to_json_value,
)
from vestagraph_generator.fixture_reader import (
    FixtureData,
    HomeData,
    InvalidDataError,
    StoryData,
    read_fixtures,
)

FILE_NAME = "costs.json"

_NOT_YET_COVERED = "not-yet-covered"

_ROUNDING = (
    "Each yearly amount is divided by 12 and rounded once to the nearest penny, halves away from "
    "zero; a total is the sum of its rounded lines; a mortgage repayment is rounded once from the "
    "exact fraction (decisions 0034 and 0036)."
)


def run(fixtures_directory: Path, error: TextIO) -> int:
    """Generate the file and write it to ``generated/``, deleting any other ``*.json`` there.

    Writes nothing when the engine reports a failure. Returns the exit code: 0 for success, 1 when
    the engine or the data's story links report a problem (printed to ``error`` with its code).

    Raises ``OSError`` when a data file is missing or cannot be read or written, and
    ``InvalidDataError`` when a data file holds something the reader does not understand.
    """
    generated = generate(fixtures_directory)
    if generated.is_failure:
        error.write(f"Generator failed [{generated.error.code}]: {generated.error.message}\n")
        return 1

    folder = fixtures_directory / "generated"
    folder.mkdir(parents=True, exist_ok=True)

    # Write the new file beside the old one and swap it in, so a failure never leaves a
    # half-written costs.json. Only then remove the other *.json files. Bytes, so no platform
    # changes the line endings.
    target = folder / FILE_NAME
    temporary = folder / f"{FILE_NAME}.tmp"
    try:
        temporary.write_bytes(generated.value.encode("utf-8"))
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)

    for other in folder.glob("*.json"):
        if other.name != FILE_NAME and not other.is_dir():
            other.unlink()
    return 0


def generate(fixtures_directory: Path) -> Result[str]:
    """The text of ``costs.json``: two-space indent, LF line endings and one final newline."""
    data = read_fixtures(fixtures_directory)
    homes: list[HomeDocument] = []

    for home_id in data.home_ids:
        outcome = _home_document(data, home_id)
        if isinstance(outcome, Error):
            return Result.failure(
                Error(outcome.code, f"{home_id}: {outcome.message}", outcome.category)
            )
        homes.append(outcome)

    document = CostsDocument(
        schema="../schema/generated-costs.schema.json",
        format_version=1,
        generated_by="Vestagraph cost engine",
        snapshot_date=data.snapshot_date,
        money="integer pence",
        rounding=_ROUNDING,
        homes=tuple(homes),
    )
    text = json.dumps(to_json_value(document), indent=2, ensure_ascii=False) + "\n"
    return Result.success(text)


def _home_document(data: FixtureData, home_id: str) -> HomeDocument | Error:
    matching = [h for h in data.homes if h.id == home_id]
    if len(matching) != 1:
        message = f"Home {home_id} must be in homes.json exactly once (found {len(matching)})."
        raise InvalidDataError(message)
    home: HomeData = matching[0]

    stories = [s for s in data.stories if home_id in s.home_ids]
    if len(stories) > 1:
        return Error(
            "home.in-several-stories",
            "The home is in more than one story, so its steps are ambiguous.",
            ErrorCategory.CONFLICT,
        )
    story: StoryData | None = stories[0] if stories else None

    if home.nation is not Nation.ENGLAND:
        return HomeDocument(
            home.id,
            None if home.mode is None else home.mode.value,
            home.nation.value,
            _NOT_YET_COVERED,
            None if story is None else story.id,
            (),
        )

    if story is None:
        return Error(
            "home.not-in-a-story",
            "The home is in England but in no story, so it has no steps to work out.",
            ErrorCategory.VALIDATION,
        )

    facts = HomeFacts(
        home.id,
        home.mode,
        home.nation,
        tuple(
            row.item
            for row in data.evidence
            if (row.subject_type == "household" and row.subject_id == data.household_id)
            or (row.subject_type == "home" and row.subject_id == home_id)
        ),
        data.monthly_budget,
    )
    costs = build_home_costs(facts, story.steps)
    if costs.is_failure:
        return costs.error
    return _map_home(costs.value, story.id, f"household:{data.household_id}.monthlyBudget")


def _map_home(home: HomeCosts, story_id: str, budget_source: str) -> HomeDocument:
    return HomeDocument(
        home.home_id,
        home.mode.value,
        home.nation.value,
        "covered",
        story_id,
        tuple(_map_scenario(home.home_id, s, budget_source) for s in home.scenarios),
    )


def _map_scenario(home_id: str, scenario: ScenarioCosts, budget_source: str) -> ScenarioDocument:
    sid = scenario.scenario_id
    monthly = scenario.monthly
    upfront = scenario.upfront
    change = scenario.monthly_total_change
    return ScenarioDocument(
        sid,
        scenario.from_step,
        scenario.to_step,
        None if scenario.mortgage is None else _map_mortgage(home_id, sid, scenario.mortgage),
        MonthlyDocument(
            _map_lines(home_id, sid, "monthly", monthly.lines),
            _map_total(
                home_id, sid, "monthly", monthly.total, monthly.is_partial, monthly.partial_reasons
            ),
            BudgetDocument(
                figure_ids.budget(home_id, sid),
                monthly.budget.value,
                budget_source,
                monthly.budget_difference.value,
                monthly.within_budget,
                monthly.based_on_partial_total,
            ),
        ),
        UpfrontDocument(
            _map_lines(home_id, sid, "upfront", upfront.lines),
            _map_total(
                home_id, sid, "upfront", upfront.total, upfront.is_partial, upfront.partial_reasons
            ),
        ),
        tuple(_map_change(home_id, sid, c) for c in scenario.changes),
        None
        if change is None
        else FigureDocument(figure_ids.monthly_total_change(home_id, sid), change.value),
    )


def _map_mortgage(home_id: str, scenario_id: str, mortgage: MortgageSummary) -> MortgageDocument:
    repayment = mortgage.repayment
    return MortgageDocument(
        figure_ids.mortgage(home_id, scenario_id),
        FigureDocument(figure_ids.mortgage_loan(home_id, scenario_id), repayment.loan.value),
        repayment.rate_basis_points,
        repayment.term_years,
        repayment.payments,
        FigureDocument(
            figure_ids.monthly_repayment(home_id, scenario_id), repayment.monthly_repayment.value
        ),
        mortgage.evidence_ids,
    )


def _map_lines(
    home_id: str, scenario_id: str, section: str, lines: tuple[LineResult, ...]
) -> tuple[LineDocument, ...]:
    return tuple(
        LineDocument(
            figure_ids.line(home_id, scenario_id, section, line.category),
            category_id(line.category),
            status_id(line.status),
            None if line.amount is None else line.amount.value,
            None if line.source_period is None else line.source_period.value,
            line.evidence_ids,
        )
        for line in lines
    )


def _map_total(
    home_id: str,
    scenario_id: str,
    section: str,
    total: Pence,
    is_partial: bool,
    reasons: tuple[PartialReason, ...],
) -> TotalDocument:
    return TotalDocument(
        figure_ids.total(home_id, scenario_id, section),
        total.value,
        is_partial,
        tuple(
            PartialReasonDocument(
                figure_ids.line(home_id, scenario_id, section, r.category),
                category_id(r.category),
                status_id(r.status),
            )
            for r in reasons
        ),
    )


def _map_change(home_id: str, scenario_id: str, change: CostChange) -> ChangeDocument:
    kind: ChangeKind = change.kind
    return ChangeDocument(
        figure_ids.change(home_id, scenario_id, change.category),
        category_id(change.category),
        kind.value,
        change.previous_evidence_ids,
        change.current_evidence_ids,
        None if change.monthly_difference is None else change.monthly_difference.value,
        None if change.annual_difference is None else change.annual_difference.value,
    )
