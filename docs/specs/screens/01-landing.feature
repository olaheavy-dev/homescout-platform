@screen @buying @renting
Feature: Landing
  Question it answers: "What can this help me do?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: the postcode-level sample area data for the hero is not in the fixtures yet
    (fixture needed: #216); inputs: none yet; figures: none.
  Route: / (the landing is the area check: the postcode box is the main action; decision 0046).
  Sections, in order, from the information architecture's "Landing": the promise with the postcode
    box; the hero map; Data from (the source wall); How it works; How to read a result; Honest by
    design; Coming next, with a free account; Questions; the footer.
  Required states (doc 03 §5):
    basic/paid boundaries -> LAND-05
    narrow and mobile layouts with a list alternative to the map -> LAND-11
    invalid postcode on the landing's own box -> LAND-12
    A complete postcode hands over to Check an area (14-check-an-area.feature), which holds the
    loading, not found, source failed and outside England states.
  Free and paid: the area check is free and needs no account. Account features (cost estimate,
    compare, questions) are described only as "Coming next … not available yet" (LAND-05; decision 0046).

  @ui
  Scenario: LAND-01 the postcode box is the main action
    Given the user is not signed in
    When the user opens the landing page
    Then the first action is a field with a persistent "Postcode" label, hint text under it and a "Check postcode" button

  @ui
  Scenario: LAND-02 the landing says it covers England only
    Given the user is not signed in
    When the user opens the landing page
    Then "England only for now" is shown under the postcode box

  @ui
  Scenario: LAND-03 checking a postcode opens Check an area with the postcode in the fragment
    Given the user is on the landing page
    When the user checks a complete postcode
    Then Check an area opens with the postcode after "#postcode=", and the query string holds no postcode

  @ui
  Scenario: LAND-04 the example opens the sample area
    Given the user is on the landing page
    When the user chooses "Try an example"
    Then Check an area opens on the sample postcode, labelled "Sample data"

  @ui
  Scenario: LAND-05 account features are described, never offered
    Given the user is not signed in
    When the user opens the landing page
    Then the cost estimate, compare, and tracking questions and answers per home appear only in a "Coming next" panel labelled "not available yet", with no active control

  # fixture needed: #216 (the hero's nearest places, distances and "+N more nearby" count)
  @ui
  Scenario: LAND-06 the hero's places come from the sample data
    Given the user is not signed in
    When the user opens the landing page
    Then the hero summary card's four nearest places, their distances and the "+N more nearby" count come from the postcode-level sample data, the pin is labelled "Postcode centre", and the hero map and card carry a visible "Sample area" label (M5: the town is invented and the page sits beside real data)

  @ui
  Scenario: LAND-07 the hero map is a static image
    Given the user is not signed in
    When the user opens the landing page
    Then the hero map is a static image, and the live map library is not loaded

  @ui
  # Changed 14 Nov 2026 (FE-34): the "can't tell you" line is gone from the cards; limits live in About the data.
  Scenario: LAND-08 the source wall names each source and links About the data
    Given the user is not signed in
    When the user opens the landing page
    Then each "Data from" card shows a source's name and what it covers, with no logo and no "can't tell you" line, and links to About the data, where the source's limits are

  @ui
  Scenario: LAND-09 the example result is labelled as a sample
    Given the user is not signed in
    When the user opens the landing page
    Then the Schools card in "How to read a result" is labelled "Sample"

  @ui
  Scenario: LAND-10 the landing never calls an area or home safe
    Given the user is not signed in
    When the user opens the landing page
    Then no text calls an area or a home "safe", "verified" or "approved" (AGENTS.md rule 4)

  @ui
  Scenario: LAND-11 on a phone the postcode box comes first and the hero's places are text
    Given the user is not signed in
    And the screen is 390 pixels wide
    When the user opens the landing page
    Then the postcode box is the first control, and the hero's places and distances are readable as text, not only in the image

  @ui
  Scenario: LAND-12 an incomplete postcode on the landing is not searched
    Given the user is on the landing page
    When the user checks an incomplete postcode
    Then an inline message under the "Postcode" field explains the format, and the page does not move to Check an area
