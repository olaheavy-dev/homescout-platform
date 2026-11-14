@screen @buying @renting
Feature: Nearby
  Question it answers: "Would daily life work?"
  Modes: both
  Fixtures: homes B1, R1, WALES-1; inputs: area records "R1-AREA-CRIME-2", "B1-AREA-FLOOD-1",
    "B1-AREA-SCHOOL-INSPECTION-1", "B1-AREA-AMENITY-6", "B1-AREA-COMMUTE-1", "WALES-1-AREA-FLOOD-1",
    household criterion "COMMUTE" (packages/fixtures/data/household.json); figures: none
    (Nearby shows recorded facts with distances from the fixtures, never calculated figures).
  Route: /homes/[slug]/nearby. Each topic's detail opens as a bottom sheet on a phone and a side panel on
    desktop, never a separate page, and the open topic is linkable through the "#" part (register line FE-20;
    corrected 14 Nov 2026, C1 of the pilot design review; .design/prototype/INFORMATION_ARCHITECTURE.md, "Nearby").
    One thing at a time on the right column or the phone screen: see "Layering" there (FE-26).
  Required states (doc 03 §5 and AGENTS.md rule 7):
    a source request that failed, not shown as a clean result -> NEAR-01, NEAR-07
    a source that does not cover the location -> NEAR-04, NEAR-10
    an address in Wales, Scotland or Northern Ireland, "not yet covered" -> NEAR-04, NEAR-10
    stale information keeps its date -> NEAR-03, NEAR-09
    missing never shown as zero or a favourable value -> NEAR-02, NEAR-05, NEAR-08
    narrow and mobile layouts with a list alternative to the map -> NEAR-11
    what a topic doesn't tell you, on the row and in the sheet -> NEAR-13
    basic/paid boundaries -> NEAR-16
  Free and paid (doc 02 §8): the Nearby map and list with straight-line distances are free; routed
    travel times to the household's own destinations are paid (routing is a metered third-party
    cost), so the prototype shows them only as a labelled, simulated boundary (NEAR-16). Walking times
    from the postcode centre to nearby places (a self-hosted batch, pilot wave 2, DA-08) are free.

  Scenario: NEAR-01 a failed crime lookup is not shown as no crime
    Then area record "R1-AREA-CRIME-2" has status "source-failed"
    And area record "R1-AREA-CRIME-2" shows no value

  Scenario: NEAR-02 no flood record in the source is a gap, not a clean result
    Then area record "B1-AREA-FLOOD-1" has status "no-record-in-source"
    And area record "B1-AREA-FLOOD-1" shows no value

  Scenario: NEAR-03 a stale school inspection keeps its record
    Then area record "B1-AREA-SCHOOL-INSPECTION-1" has status "stale"

  Scenario: NEAR-04 a home in Wales is not yet covered
    Then home "WALES-1" has coverage "not-yet-covered"
    And area record "WALES-1-AREA-FLOOD-1" has status "not-covered"
    And area record "WALES-1-AREA-FLOOD-1" shows no value

  Scenario: NEAR-05 a missing childcare place is a gap
    Then area record "B1-AREA-AMENITY-6" has status "no-record-in-source"
    And area record "B1-AREA-AMENITY-6" shows no value

  @ui
  Scenario: NEAR-06 the page opens as one summary row per topic
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then one row per topic shows its headline fact, and opening a row opens its sheet or panel, not a new page, in the order of the information architecture: your commute, getting around, everyday places, places of worship, schools, flood, recorded crime, sold nearby, planning nearby and broadband

  @ui
  Scenario: NEAR-07 the failed crime topic says it is unavailable
    Given home "R1" is at story step 1
    When the user opens Nearby
    Then the recorded crime topic shows "Unavailable", "Couldn't fetch this time · Try again" and "This doesn't mean there's nothing to report" for "R1-AREA-CRIME-2"

  @ui
  Scenario: NEAR-08 the flood gap is never a reassuring label
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then the flood topic shows the label and the "What this doesn't tell you" note of "B1-AREA-FLOOD-1" as recorded, with its long-term flood risk link, and no "no risk", "low risk" or "clear" label

  @ui
  Scenario: NEAR-09 the stale inspection shows its date
    Given home "B1" is at story step 1
    When the user opens the schools topic
    Then "B1-AREA-SCHOOL-INSPECTION-1" shows its inspection date and source date with the "Old" label

  @ui
  Scenario: NEAR-10 Wales shows one not yet covered card
    Given the user has opened the home "WALES-1"
    When the user opens Nearby
    Then one "Not yet covered" card is shown, and no topic is shown as empty

  @ui
  Scenario: NEAR-11 on a phone every topic has a list, and the map is optional
    Given home "B1" is at story step 1
    And the screen is 390 pixels wide
    When the user opens a topic
    Then the topic opens as a bottom sheet with a visible Close, it shows a list, and the map is a view the user can choose

  @ui
  Scenario: NEAR-12 crime is shown as counts and never on the map
    Given home "B1" is at story step 1
    When the user opens the recorded crime topic
    Then crime shows as counts by month and category, and the map shows no crime marker

  @ui
  # Changed 14 Nov 2026 (M3, register line FE-28): the full note on every row made the list long again.
  # The short list carries a one-line limit only where the limit changes the meaning; the full note is
  # always open at the top of the topic's sheet or panel. P2: "as prominent" means the same text size
  # and contrast as the fact it qualifies.
  Scenario: NEAR-13 what a topic doesn't tell you stays in view where it changes the meaning
    Given home "B1" is at story step 1
    And the screen is 390 pixels wide
    When the user opens Nearby and then a topic
    Then the flood, recorded crime, sold nearby and schools rows each show a one-line limit under their headline fact, and the opened topic's sheet shows the full "What this doesn't tell you" note at the top, never collapsed, in the same text size and contrast as the fact it qualifies

  @ui
  Scenario: NEAR-14 the commute row gives no verdict
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then the commute row shows "B1-AREA-COMMUTE-1" next to the household's criterion "COMMUTE", with no verdict

  # FE-25 (13 Nov 2026): on the pilot area check, the flood topic's own flat map (FE-20) may draw the
  # official outlines if an open dataset is licensed; on Nearby the main map still shows no flood marker.
  @ui
  Scenario: NEAR-15 flood is shown in the list and never on the map
    Given home "B1" is at story step 1
    When the user opens the flood topic
    Then flood shows in the list only, and the map shows no flood marker

  @ui
  Scenario: NEAR-16 distances are straight-line and routed times to the household's own destinations are a labelled boundary
    Given home "B1" is at story step 1
    When the user opens getting around
    Then every distance is labelled straight-line, and routed travel time to the household's own destinations appears only as a labelled, simulated paid feature, never as a working control; walking times from the postcode centre to nearby places (pilot wave 2) are a separate free feature
