@screen @buying @renting
Feature: Nearby
  Question it answers: "Would daily life work?"
  Modes: both
  Fixtures: homes B1, R1, WALES-1; inputs: area records "R1-AREA-CRIME-2", "B1-AREA-FLOOD-1",
    "B1-AREA-SCHOOL-INSPECTION-1", "B1-AREA-AMENITY-6", "WALES-1-AREA-FLOOD-1"; figures: none
    (Nearby shows recorded facts with distances from the fixtures, never calculated figures).
  Route: /homes/[slug]/nearby, with each topic at /homes/[slug]/nearby/[topic]
    (.design/prototype/INFORMATION_ARCHITECTURE.md, "Nearby").
  Required states (doc 03 §5 and AGENTS.md rule 7):
    a source request that failed, not shown as a clean result -> NEAR-01, NEAR-07
    a source that does not cover the location -> NEAR-04, NEAR-10
    an address in Wales, Scotland or Northern Ireland, "not yet covered" -> NEAR-04, NEAR-10
    stale information keeps its date -> NEAR-03, NEAR-09
    missing never shown as zero or a favourable value -> NEAR-02, NEAR-05, NEAR-08
    narrow and mobile layouts with a list alternative to the map -> NEAR-11
  Free and paid: Nearby is free in the prototype; no limit applies (doc 02 §8, decision 0046).

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
    Then one row per topic shows its headline fact, in the order of the information architecture: your commute, getting around, everyday places, places of worship, schools, flood, recorded crime, sold nearby, planning nearby and broadband

  @ui
  Scenario: NEAR-07 the failed crime topic says it is unavailable
    Given home "R1" is at story step 1
    When the user opens Nearby
    Then the recorded crime topic shows "Unavailable", "Try again" and "This doesn't mean there's nothing to report" for "R1-AREA-CRIME-2"

  @ui
  Scenario: NEAR-08 the flood gap is never a reassuring label
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then the flood topic for "B1-AREA-FLOOD-1" says "This is not the same as no warning" and shows no "no risk" or similar label

  @ui
  Scenario: NEAR-09 the stale inspection shows its date
    Given home "B1" is at story step 1
    When the user opens the schools topic
    Then "B1-AREA-SCHOOL-INSPECTION-1" shows its source date and a stale label

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
    Then the topic shows a list, and the map is a view the user can choose

  @ui
  Scenario: NEAR-12 crime is shown as counts and never on the map
    Given home "B1" is at story step 1
    When the user opens the recorded crime topic
    Then crime shows as counts by month and category, and the map shows no crime marker

  @ui
  Scenario: NEAR-13 what a topic doesn't tell you stays visible on a phone
    Given home "B1" is at story step 1
    And the screen is 390 pixels wide
    When the user opens Nearby
    Then each topic's "What this doesn't tell you" note is visible under its source line, never collapsed

  @ui
  Scenario: NEAR-14 the commute row gives no verdict
    Given home "B1" is at story step 1
    When the user opens Nearby
    Then the commute row shows "B1-AREA-COMMUTE-1" next to the household's limit, with no verdict
