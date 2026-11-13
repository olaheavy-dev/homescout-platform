@screen @buying @renting
Feature: Check an area
  Question it answers: "What is around this postcode?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: home WALES-1 (outside England); inputs: area record "WALES-1-AREA-SCHOOL-1";
    the postcode-level sample area data is not in the fixtures yet (fixture needed: #216); figures: none.
  Route: /area#postcode=… (the postcode lives in the URL fragment, never the query string, so it
    never reaches a server, application or hosting log; decisions 0014 and 0046).
  Reuses the Nearby topic summary and topic details (04-nearby.feature), without the commute row.
  Required states (doc 03 §5, the information architecture's "Check an area" and AGENTS.md rule 7):
    the postcode never reaches a log (decisions 0014, 0046) -> AREA-03, AREA-15
    loading -> AREA-06
    invalid format -> AREA-04
    postcode not found, never shown as empty topics -> AREA-05
    a source request that failed, not shown as a clean result -> AREA-07, AREA-14
    an address in Wales, Scotland or Northern Ireland, "not yet covered" -> AREA-01, AREA-02, AREA-08
    narrow and mobile layouts with a list alternative to the map -> covered by NEAR-11 (same topic details)
  Free and paid: the area check is free and needs no account. Saving a home needs an account that
    doesn't exist yet, so it appears only as "Coming next · not available yet" (AREA-11; decision 0046).

  # Home "WALES-1" stands in for a postcode outside England until the postcode-level fixture (#216).
  Scenario: AREA-01 a postcode outside England is not yet covered
    Then home "WALES-1" has coverage "not-yet-covered"

  Scenario: AREA-02 a not covered topic has nothing to show
    Then area record "WALES-1-AREA-SCHOOL-1" has status "not-covered"
    And area record "WALES-1-AREA-SCHOOL-1" shows no value

  @ui
  Scenario: AREA-03 the postcode stays out of the query string
    Given the user is on Check an area
    When the user checks a complete postcode
    Then the address bar shows the postcode after "#postcode=", and the query string holds no postcode

  @ui
  Scenario: AREA-04 an incomplete postcode is not searched
    Given the user is on Check an area
    When the user checks an incomplete postcode
    Then an inline message under the "Postcode" field explains the format, and no search is made

  # fixture needed: #216 (one well-formed but unknown postcode)
  @ui
  Scenario: AREA-05 an unknown postcode shows only that it wasn't found
    Given the user is on Check an area
    When the user checks a well-formed postcode that the sample data doesn't know
    Then "We couldn't find that postcode" is shown, and no topic is shown

  @ui
  Scenario: AREA-06 topics load as skeletons, never as empty rows
    Given the user is on Check an area
    When the user checks a complete postcode and the results are still loading
    Then each topic shows a loading skeleton, and no topic shows as empty

  @ui
  Scenario: AREA-07 a source that is down is labelled Unavailable and the rest still shows
    Given the user is on Check an area
    When the user checks a complete postcode and one topic's source fails
    Then that topic shows "Unavailable" with "Couldn't fetch this time · Try again", and the other topics still show

  @ui
  Scenario: AREA-08 outside England shows a not yet covered card
    Given the user is on Check an area
    When the user checks the postcode of home "WALES-1"
    Then a "Not yet covered" card is shown on Check an area with the postcode still only after "#postcode=", and no topic is shown as empty

  @ui
  Scenario: AREA-09 the map's centre pin is the postcode centre
    Given the user has checked a complete postcode
    When the user opens the map view
    Then the centre pin is labelled "Postcode centre", and no address pin is shown

  @ui
  Scenario: AREA-10 there is no commute row
    Given the user is on Check an area
    When the user checks a complete postcode
    Then the topic summary has no commute row

  @ui
  Scenario: AREA-11 saving a home is only described, never offered
    Given the user has checked a complete postcode
    When the results are shown
    Then saving a home appears only in a "Coming next · not available yet" panel, with no active button

  @ui
  Scenario: AREA-12 the printout keeps every topic, including gaps
    Given the user has checked a complete postcode and one topic's source failed
    When the user chooses "Print or save as PDF"
    Then the print page lists every topic with its source, data date and label, the failed topic prints as "Unavailable", and the header says "Sample data"

  @ui
  Scenario: AREA-16 a not covered postcode prints as not covered
    Given the user has checked the postcode of home "WALES-1"
    When the user chooses "Print or save as PDF"
    Then the print page shows "Not yet covered" and leaves nothing out

  @ui
  Scenario: AREA-17 the printout is made in the browser
    Given the user has checked a complete postcode
    When the user chooses "Print or save as PDF"
    Then the print page is made in the browser, and no request is sent that carries the postcode

  # fixture needed: #216 (distances from the postcode centre)
  @ui
  Scenario: AREA-13 distances are measured from the postcode centre
    Given the user has checked a sample postcode
    When the results are shown
    Then every distance comes from the postcode-level sample data, measured from the postcode centre, not from a home

  # fixture needed: #216 (no flood source-failed record exists yet)
  @ui
  Scenario: AREA-14 a failed flood source is not the same as no warning
    Given the user is on Check an area
    When the user checks a complete postcode and the flood source fails
    Then the flood topic shows "Unavailable", "Couldn't fetch this time · Try again" and "This is not the same as no warning"

  @ui
  Scenario: AREA-15 no request carries the postcode in its address
    Given the user is on Check an area
    When the user checks a complete postcode
    Then no request the page makes carries the postcode in its URL path or query string
