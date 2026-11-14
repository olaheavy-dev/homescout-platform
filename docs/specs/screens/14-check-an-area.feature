@screen @buying @renting
Feature: Check an area
  Question it answers: "What is around this postcode?"
  Modes: both (and anyone, with no account; decision 0046)
  Fixtures: home WALES-1 (outside England); inputs: area record "WALES-1-AREA-SCHOOL-1";
    the postcode-level sample area data is not in the fixtures yet (fixture needed: #216); figures: none.
  Route: /area#postcode=… (the postcode lives in the URL fragment, never the query string, so it
    never reaches a server, application or hosting log of ours; decisions 0014 and 0046). The one
    exception is an outbound link the visitor clicks, which may carry the postcode to that site and
    says so (register line FE-11).
  Reuses the Nearby topic summary and topic details (04-nearby.feature), without the commute row.
  A topic's detail opens as a bottom sheet on a phone and a side panel on desktop, never a separate
    page (register line FE-20), and the open topic is linkable through the same "#" part as the postcode.
  Layering (register line FE-26): one thing at a time on the right column or the phone screen; the rule
    is written once in the site plan (.design/prototype/INFORMATION_ARCHITECTURE.md, "Layering").
  Words for gaps and states: the site plan's vocabulary table (P1, 14 Nov 2026): "Unavailable" (we hold
    no current copy of a source), "Couldn't load this" (the visitor's request to us failed), "No record
    in this source", "No <place> found within <radius>", "Old", "Not yet covered".
  Changed 14 Nov 2026 (FE-33, DA-12): on the page, a fact shows only its source's icon, name and link, with
    no status word and no date; a fact whose source is unavailable says "Not known right now" in its own
    text. "Unavailable" and "Old" (with the date and the flood check time) are shown on About the data
    (AREA-25); the stored data, the area tools and our chat's grounding keep them (area-tools.feature).
  Required states (doc 03 §5, the information architecture's "Check an area" and AGENTS.md rule 7):
    the postcode never reaches a log (decisions 0014, 0046) -> AREA-03, AREA-15
    an outbound link says where it goes and whether it carries the postcode (FE-11) -> AREA-18
    loading -> AREA-06
    invalid format -> AREA-04
    postcode not found, never shown as empty topics -> AREA-05
    our stored copy of a source is missing or failed, not shown as a clean result -> AREA-07, AREA-14
    the visitor's own request to us failed, a different state with Try again -> AREA-19
    flood warnings: official link first, the check time on the row but no label; Old after 1 hour and Unavailable after 1 day on About the data -> AREA-21, AREA-22, AREA-23, AREA-25
    a fact's stamp is its source's icon, name and link, with no status word and no date -> AREA-26
    the printout: the sample postcode says "Sample data", any other postcode its made-at time -> AREA-12, AREA-20
    distances in England: metres under 1 mile, miles from 1 mile, stored in metres -> AREA-24
    an address in Wales, Scotland or Northern Ireland, "not yet covered" -> AREA-01, AREA-02, AREA-08
    narrow and mobile layouts with a list alternative to the map -> covered by NEAR-11 (same topic details; a sheet on a phone, FE-20)
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
  # Changed 14 Nov 2026 (FE-33, DA-12): the row says "Not known right now" in its own text; the label "Unavailable" is on About the data.
  Scenario: AREA-07 a source we hold no current copy of says it is not known right now and the rest still shows
    Given the user is on Check an area
    When the user checks a complete postcode and our stored copy of one topic's source is missing or failed to load
    Then that topic shows "Not known right now" with "We don't hold a current copy of this source", its official link where one exists and no "Try again", and the other topics still show

  # Corrected 14 Nov 2026 (C3 of the pilot design review): the pilot reads only our stored copies, never
  # a source live, so asking again cannot change the result until our next refresh.
  @ui
  Scenario: AREA-19 a request to our own service that fails offers Try again
    Given the user is on Check an area
    When the user checks a complete postcode and the request to our service fails (network or our API down)
    Then the page shows "Couldn't load this · Try again", never "We couldn't find that postcode" and never an empty or clean result

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
    Then saving a home, and tracking questions and answers per home, appear only in a "Coming next · not available yet" panel, with no active button

  @ui
  Scenario: AREA-12 the printout of the example postcode keeps every topic, including gaps, and says "Sample data"
    Given the user has checked the example sample postcode and one topic has no current copy
    When the user chooses "Print or save as PDF"
    Then the print page lists every topic with its source's name, the topic with no copy prints as "Not known right now", the closing "How we got this" page gives each source's data date and status, and the header says "Sample data"

  # Split 14 Nov 2026 (C5): real postcodes are real data, so "Sample data" belongs only to the example.
  @ui
  Scenario: AREA-20 the printout of any other postcode shows when it was made, not "Sample data"
    Given the user has checked a postcode that is not the example and one topic has no current copy
    When the user chooses "Print or save as PDF"
    Then the print page header shows the time the report was made, each topic shows its source's name, the topic with no copy prints as "Not known right now", the closing "How we got this" page gives each source's data date and status, and nothing says "Sample data"

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

  # Units follow the country (register line FE-27, 14 Nov 2026): stored values stay in metres; the display
  # unit comes from the country entry in the data contract. Crime stays police.uk's own "within 1 mile".
  # fixture needed: #216
  @ui
  Scenario: AREA-24 in England distances show in metres under 1 mile and in miles from 1 mile
    Given the user has checked a sample postcode in England
    When the results are shown
    Then a distance under 1 mile reads in metres rounded to the nearest 10 m, like "120 m" or "1,450 m"
    And a distance of 1 mile or more reads in miles to one decimal, like "1.3 miles"
    And crime reads "within 1 mile", the stored values are in metres, and no distance is shown in kilometres

  # fixture needed: #216 (no flood source-failed record exists yet)
  @ui
  Scenario: AREA-14 a missing flood copy is not the same as no warning
    Given the user is on Check an area
    When the user checks a complete postcode and we hold no current copy of the flood warnings
    Then the flood topic shows "Not known right now", "We don't hold a current copy of this source", the official flood-warning link first and "This is not the same as no warning", with no "Try again" and no status word or date on the row

  # Flood warnings (register line DA-12, 14 Nov 2026). The Environment Agency says its flood data is updated
  # every 15 minutes, gives no service-level guarantee and is not for safety-critical use
  # (https://environment.data.gov.uk/flood-monitoring/doc/reference, read 14 Nov 2026). The 1 hour and
  # 1 day limits below are the founder's accepted default, not an Environment Agency rule.
  # fixture needed: #216 (flood copies of a known age for AREA-21 to AREA-23)
  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): no status label on the flood row (founder: "No exceptions"); About the data shows it (AREA-25).
  # Changed again 14 Nov 2026 (DA-12): the flood row keeps its check time (founder: "keep time for the flood"); its limit sits in "How we got this" (FE-34).
  Scenario: AREA-21 the flood row puts the official link first and shows the check time but no label
    Given the user is on Check an area and our flood copy was refreshed within the last hour
    When the user views the flood row
    Then it shows the warnings in force "when we last checked, at <time>", the official flood-warning link comes first, no status word, and the word "live" and any "clear" or "safe" label are not shown
    And when our copy holds no warning for the area, the row says "No flood warnings in force when we last checked, at <time>", with the long-term flood risk link (FE-25), and "This is not a flood risk check" sits inside the topic's "How we got this" (FE-34)

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the Old label and the check time move to About the data.
  Scenario: AREA-22 a flood copy over 1 hour old is labelled Old on About the data
    Given our flood copy is more than 1 hour old and less than 1 day old
    When the user views the flood row and then About the data
    Then the flood row still shows the source's icon, name and link with the official link first and "when we last checked, at <time>", but no label, and About the data shows the flood source as "Old" with the time we last checked

  @ui
  # Changed 14 Nov 2026 (FE-33, DA-12): the row says "Not known right now" in its own text; "Unavailable" is on About the data.
  Scenario: AREA-23 a flood copy over 1 day old is Unavailable on About the data
    Given our flood copy is more than 1 day old
    When the user views the flood row and then About the data
    Then the row shows "Not known right now" and "This is not the same as no warning", no warning status from the old copy is shown, and About the data shows the flood source as "Unavailable" with the time we last checked

  # Added 14 Nov 2026 (FE-33, DA-12): where the source date and status now live.
  # fixture needed: #216 (sources with known dates and statuses)
  @ui
  Scenario: AREA-25 About the data lists every source with its date and status
    Given the user is on Check an area and has checked a postcode
    When the user opens About the data
    Then every source the area check uses is listed with its icon, name and official link, its data date and its status (Cached, Fallback, Old or Unavailable, never Live in the pilot), and the flood source shows when we last checked

  # Added 14 Nov 2026 (FE-33): the stamp on a fact.
  # fixture needed: #216
  @ui
  Scenario: AREA-26 a fact's source stamp is the source's icon, name and link only
    Given the user is on Check an area and has checked a postcode
    When the user looks at the source on any fact
    Then it shows the source's icon, its name and a "↗" mark and is a link to the official page, with no status word (Cached, Old, Unavailable or Fallback) and no date

  @ui
  Scenario: AREA-15 no request carries the postcode in its address
    Given the user is on Check an area
    When the user checks a complete postcode
    Then no request the page makes by itself carries the postcode in its URL path or query string

  @ui
  Scenario: AREA-18 an outbound link says where it goes and that it carries the postcode
    Given the user is on Check an area
    When the user checks a complete postcode
    Then each outbound link that carries the postcode names its site and says that site will see the postcode
    And no outbound link sends a referrer, and nothing is sent until the user clicks it
