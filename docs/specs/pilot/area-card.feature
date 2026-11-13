@screen @buying @renting
Feature: Area card (the isometric scene of the nearest places, in our chat and in ChatGPT and Claude)
  Question it answers: "Where are the nearest places, at a glance?"
  Modes: both (and anyone, with no account; decisions 0046 and 0051)
  Fixtures: the postcode-level sample area data is not in the fixtures yet (fixture needed: #216);
    figures: none (distances and positions come from the area tools' tested geometry module).
  What it is: the nearest places from the nearby places tool's result (area-tools.feature), drawn as a
    small isometric scene in the approved style (FE-10), with the postcode centre in the middle. It comes
    after the plain answers work in every host (decision 0037).
  How many (founder, 13 Nov 2026, typed "1km might not have a lot of places most time, will mobile view not
    be useless", then in a prompt window: "Up to 10 (Recommended)", FE-19): the card shows the places in the
    result, of the kinds asked for (any kind when none is named), nearest first, at most 10, looked up to 5 km (FE-12), and the map's scale fits the places shown, so a
    sparse area still gets a useful card; it is never a fixed radius such as 1 km.
  Two versions (founder, 13 Nov 2026: "Two versions", FE-15): a component in our own chat
    (area-chat.feature, CHAT-31 to CHAT-33) and a widget for ChatGPT and Claude (the open MCP Apps
    standard, a ui:// resource, decision 0037). A scenario tagged with both ui and mcp runs once per
    version: our chat component in the playwright-bdd suite (ui), the widget in the MCP suite (mcp).
    CARD-02 compares the two versions in one test and runs in the ui suite, which loads the widget
    bundle in a test frame; CARD-13 and the sandbox scenarios apply to the widget only (mcp).
    Neither version computes a position or a distance: both draw the distance and bearing each place
    carries in the tool result (TOOLS-05, TOOLS-29; design, Accuracy 2), so the two can't drift on the facts.
  The text: in our chat it is our answer beside the card; in ChatGPT and Claude the host's model writes
    the answer, which we can't control (decision 0037), so the widget's scenarios check the text content
    of our tool result instead.
  Tap a pin (founder, 13 Nov 2026: "Tap a pin for its name", FE-14): tapping a pin, or pressing Enter or
    Space on it, shows its name, distance and source.
  Expand (founder, 13 Nov 2026: "Yes, Expand button", FE-16): the card in an answer is compact; an Expand
    button opens a larger view of the same places (a dialog on desktop, full screen on a phone in our chat).
    The widget asks the host for full screen with the MCP Apps ui/request-display-mode method
    (https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx), only
    when the host lists fullscreen in its availableDisplayModes; the host may refuse and returns the mode
    in effect. The widget declares availableDisplayModes ["inline", "fullscreen"] in ui/initialize, since a
    host may decline views that didn't declare it. In the widget, Close asks for inline again.
  The expanded view holds the map at a larger size, a "Selected" panel for the chosen place, and every
    place as a selectable row; the compact card holds the map, Expand and the list of places (in our chat on
    a phone, the preview with "Open map" instead, CARD-36; "Open map" is the phone's Expand, and CARD-23 and
    CARD-28 hold for it).
  Widths: the ui suite runs the pin scenarios (CARD-01, CARD-03 to CARD-10) at desktop width; on a phone they
    apply to the expanded view, since the preview shows no place pins.
  The expanded view keeps every guarantee of CARD-11, CARD-12 and CARD-16 to CARD-19; its only message to
    the host is the display-mode request.
  Phone chat preview (founder, 13 Nov 2026, prompt window: "Preview + Open map", FE-18): in our chat on a
    phone the card is a preview, not a squeezed map: a small map strip with only the postcode centre, the
    number of places and the nearest one, and a full-width "Open map" button (the phone's Expand) that opens
    the full-screen view; the list of places with their icons stays in the answer.
  Icons (founder, 13 Nov 2026, typed: "we need to make sure icon logos are beside the text", FE-17): every
    place in a list, and the selected place, shows its category icon beside its name, the same icon as its pin.
  Copy: quoted messages are proposed wording, finalised in the build.
  Required states (design docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md, "Isometric area card"
    and "Accuracy"; decision 0046's map rules; AGENTS.md rules 4 and 7):
    drawn at the listed distances and bearings, the same in both versions -> CARD-01, CARD-02
    tap, keyboard and screen reader; the text as the accessible version -> CARD-03 to CARD-06
    sources, no risk shading, approximate heights, the postcode centre -> CARD-07 to CARD-10
    no network from load, nothing stored -> CARD-11, CARD-12
    hosts without widgets, no places, reduced motion -> CARD-13, CARD-14, CARD-15
    the widget's sandbox: names as text, messages only from the host, no tool calls, no secrets -> CARD-16 to CARD-19
    no silent change between versions (screenshot test) -> CARD-20
    Expand: the larger view, keyboard, focus trap, labelled dialog, list rows -> CARD-21 to CARD-24, CARD-27, CARD-28
    full screen in hosts that allow it, leaving it, and no Expand where it can't work -> CARD-25, CARD-26, CARD-29
    an icon beside every place name, matching its pin -> CARD-30
    on a phone, a closer expanded map that moves by dragging, by choosing a place or by Tab, and zooms, with every place still listed -> CARD-31 to CARD-35
    in the phone chat, a preview with Open map instead of a squeezed map -> CARD-36 to CARD-42
    at most 10 places, up to 5 km, the map fitted to them, also in a sparse area -> CARD-43, CARD-44

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-01 every place sits at its listed distance, or is named off the map
    Given a nearby places result for a sample postcode
    When the card is drawn
    Then every place is drawn at its listed straight-line distance within 2% and in its listed bearing, in list order, or is named "off the map"

  # fixture needed: #216
  @ui
  Scenario: CARD-02 both versions draw the same places in the same positions
    Given the same nearby places result for a sample postcode
    When our chat card and the widget are both drawn from it
    Then each place is in the same position on both, with the same name and distance

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-03 tapping a pin shows its name, distance and source
    Given the card is drawn for a sample postcode
    When the user taps a pin
    Then the pin's place name, straight-line distance and source with its date are shown beside it

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-04 the pins work with the keyboard alone
    Given the card is drawn for a sample postcode
    When the user moves to a pin with Tab and presses Enter or Space, then presses Escape
    Then Enter or Space shows the same details as a tap, and Escape hides them and keeps focus on the pin

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-05 each pin is a named button for screen readers
    Given the card is drawn for a sample postcode
    When a screen reader moves through the card
    Then each pin is announced as a button named with its place and distance

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-06 the text answer lists the same places in the same order
    Given the card is drawn for a sample postcode
    When the answer is shown
    Then the text (our answer beside the card in our chat; the tool result's text content for the widget) lists every place on the card, in the same order, with its distance and source

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-07 the card shows its sources and dates
    Given the card is drawn for a sample postcode
    When the card is shown
    Then it names each source it draws from, with its data date

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-08 the card has no flood or crime shading
    Given the card is drawn for a sample postcode
    When the card is shown
    Then no area of the card is shaded, coloured or marked for flood, crime or any other risk

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-09 building heights are labelled approximate
    Given the card is drawn for a sample postcode
    When the card is shown
    Then the card says building heights are "approximate"

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-10 the centre pin is the postcode centre, never an address
    Given the card is drawn for a sample postcode
    When the card is shown
    Then the centre pin is labelled "Postcode centre", and no address pin is shown

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-11 the card makes no network request
    Given the card is drawn for a sample postcode
    When the card loads, the user taps every pin, opens Expand and chooses every row
    Then the card has made no network request of any kind from the moment it loads, and the widget declares no allowed outside origin in its content security policy

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-12 the card stores nothing
    Given the card has been drawn, its pins tapped, and Expand opened and closed
    When the card is closed
    Then nothing from the card is in local storage, session storage, IndexedDB or cookies

  # fixture needed: #216
  @mcp
  Scenario: CARD-13 a host without widgets still gets every place as text
    Given a host that does not show widgets
    When it calls the nearby places tool for a sample postcode
    Then the tool result's text content lists every place with its distance and source, and does not depend on the card

  @ui @mcp
  Scenario: CARD-14 a result with no places shows no card
    Given a nearby places result with no place within 5 km
    When the answer is shown
    Then no card is drawn, and the text says "No places found within 5 km" (TOOLS-06), never an empty card

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-15 the card does not move when reduced motion is set
    Given the user's device asks for reduced motion
    When the card is drawn, zoomed, or moved to show a chosen place
    Then no pin, building or map movement animates

  @mcp
  Scenario: CARD-16 place names are drawn as text, never as markup
    Given a nearby places result in which one place name contains HTML markup and a script
    When the widget is drawn
    Then the name shows as plain text, and no markup or script from it takes effect

  @mcp
  Scenario: CARD-17 the widget accepts data only from its host, carrying our tool result
    Given the widget is drawn inside a host
    When a message arrives that does not come from the host's parent window, or does not carry a tool result from our server
    Then the widget ignores it and draws nothing from it

  @mcp
  Scenario: CARD-18 the widget calls no tools and sends nothing to the host's model
    Given the widget is drawn for a sample postcode
    When the user taps every pin, opens Expand and closes it
    Then the widget has made no tool call and sent no message or context update to the host other than ui/request-display-mode

  @mcp
  Scenario: CARD-19 the widget bundle holds no key, token or internal address
    Given the widget bundle the server serves as its ui:// resource
    When its contents are inspected
    Then it holds no key, token, secret or internal URL

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-20 a card does not change silently between versions
    Given a saved screenshot of the card for a fixed sample result
    When the card is drawn again from the same result after a change to the code
    Then it matches the saved screenshot, or the difference is reviewed and the screenshot updated in the same pull request

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-21 Expand opens a larger view of the same places
    Given the compact card is drawn for a sample postcode, in our chat or in a host that grants full screen
    When the user chooses "Expand"
    Then a larger view opens with every place at the same true distance and bearing as on the compact card (the drawing is larger, the distances are not), and the same places in the list

  @ui
  Scenario: CARD-22 in our chat the expanded view is a dialog on desktop and full screen on a phone
    Given an answer about nearby places in our chat
    When the user chooses "Expand" on a 1280 px wide screen, and "Open map" on a 390 px wide screen
    Then it opens as a dialog over the chat on the wide screen, and full screen on the phone, each with a "Close" button

  @ui
  Scenario: CARD-23 the expanded view works with the keyboard and returns focus
    Given the compact card is drawn in our chat for a sample postcode
    When the user reaches "Expand" with Tab, opens it with Enter, then presses Escape
    Then the view opens with focus inside it, Escape closes it, and focus returns to the "Expand" button

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-24 choosing a row in the expanded list selects its pin
    Given the expanded view is open for a sample postcode, in our chat or in a host that granted full screen
    When the user chooses a place in the list
    Then that place's pin is selected on the map, and its name, distance and source with its date are shown, the same as a tap

  @mcp
  Scenario: CARD-25 the widget asks for full screen and follows the mode the host returns
    Given the widget is drawn in a host that lists fullscreen as an available display mode
    When the user chooses "Expand"
    Then the widget sends ui/request-display-mode with fullscreen and shows the expanded view only if the host returns fullscreen

  @mcp
  Scenario: CARD-26 Close in the widget's full screen returns it to the compact card
    Given the widget is in full screen with the expanded view
    When the user chooses "Close"
    Then the widget sends ui/request-display-mode with inline and shows the compact card again

  @ui
  Scenario: CARD-27 focus stays inside the expanded view while it is open
    Given the expanded view is open in our chat
    When the user presses Tab and Shift+Tab past its last and first controls
    Then focus moves round the controls inside the view only, and the chat behind it cannot be reached or read out

  @ui
  Scenario: CARD-28 the expanded view is a labelled dialog
    Given the compact card is drawn in our chat for a sample postcode
    When the user chooses "Expand"
    Then a screen reader announces a dialog named "Nearest places to <postcode>"

  @mcp
  Scenario: CARD-29 the widget shows no Expand where full screen can't work
    Given the widget is drawn in a host that does not list fullscreen, or that refused it once
    When the card is shown
    Then no Expand button is shown, and the compact card keeps every place, its list and its details

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-30 every place name has its category icon beside it, matching its pin
    Given the card is drawn for a sample postcode
    When the list and the expanded view are shown
    Then each place in the list, and the selected place, shows its category icon beside its name, the same icon and colour as its pin on the map

  # fixture needed: #216
  @ui
  Scenario: CARD-31 on a phone the expanded map opens closer, centred on the postcode
    Given the preview is shown in our chat for a sample postcode on a 390 px wide screen
    When the user chooses "Open map"
    Then the map opens full screen with the place pins, at a larger scale than the desktop compact card, with the postcode centre in the middle of the visible part

  # fixture needed: #216
  @ui
  Scenario: CARD-32 on a phone the expanded map moves by dragging
    Given the expanded map is open on a 390 px wide screen
    When the user drags the map
    Then the visible part moves with the drag, and the list below still shows every place

  # fixture needed: #216
  @ui
  Scenario: CARD-33 the zoom buttons change the scale and keep every place at its distance
    Given the expanded map is open on a 390 px wide screen
    When the user chooses "Zoom in" and then "Zoom out"
    Then the scale changes each time, and every place stays at its listed distance and bearing within 2%

  # fixture needed: #216
  @ui
  Scenario: CARD-34 choosing a place, or tabbing to its pin, moves the map to show it
    Given the expanded map is open on a 390 px wide screen and one place is outside the visible part
    When the user chooses that place in the list, or moves to its pin with Tab
    Then the map moves so that pin is fully visible and not covered, with no dragging needed

  # fixture needed: #216
  @ui
  Scenario: CARD-35 a place scrolled out of view is not off the map
    Given the expanded map is open on a 390 px wide screen and one place is outside the visible part
    When the map is shown
    Then that place is not labelled "off the map", and it is reachable by dragging, by its list row or by Tab

  # fixture needed: #216
  @ui
  Scenario: CARD-36 in the phone chat the card is a preview, not a squeezed map
    Given an answer about nearby places in our chat on a 390 px wide screen
    When the answer is shown
    Then the card shows a map strip with only the postcode centre, no place pins or place labels, and a full-width "Open map" button

  # fixture needed: #216
  @ui
  # The count is the number of places the card shows, from the tool result (TOOLS-43), not a sum of figures; the distance is the
  # farthest shown place's listed distance, quoted, not calculated (AGENTS.md rule 2).
  Scenario: CARD-37 the preview's count comes from the tool result
    Given an answer about nearby places in our chat on a 390 px wide screen
    When the preview is shown
    Then "Nearest <n> places · up to <distance>" uses the number of places the card shows (at most 10) and the listed distance of the farthest of them, and reads "Nearest place · <distance>" when there is one

  @ui
  Scenario: CARD-38 Open map opens the full-screen view
    Given the preview is shown in our chat on a 390 px wide screen
    When the user chooses "Open map"
    Then the expanded view opens full screen (CARD-31)

  # fixture needed: #216
  @ui
  Scenario: CARD-39 the preview's nearest place is the result's nearest
    Given an answer about nearby places in our chat on a 390 px wide screen
    When the preview is shown
    Then "Closest:" names the first place of the nearby places result, which lists places nearest first (TOOLS-42), with its listed distance

  @ui
  Scenario: CARD-40 Close returns focus to Open map
    Given the full-screen view was opened from "Open map" on a 390 px wide screen
    When the user chooses "Close"
    Then focus returns to the "Open map" button

  # fixture needed: #216
  @ui
  Scenario: CARD-41 the preview's map strip is hidden from screen readers, and Open map says what it opens
    Given the preview is shown in our chat on a 390 px wide screen
    When a screen reader moves through the preview
    Then the map strip is skipped as decorative, and the button is announced as "Open map, nearest <n> places up to <distance>, button", or "Open map, nearest place, <distance>, button" when there is one

  # fixture needed: #216
  @ui
  Scenario: CARD-42 on a phone the list of places stays in the answer
    Given the preview is shown in our chat on a 390 px wide screen
    When the answer is shown
    Then every place in the result is listed below the preview with its icon, name, type and distance

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-43 the card never shows more than 10 places
    Given a sample postcode with more than 10 places within 5 km
    When the card is drawn
    Then it shows the 10 nearest, and the text answer states the total number of places within 5 km that the result reports (TOOLS-42)

  # fixture needed: #216 (a sparse sample postcode, with its nearest places between 1 and 5 km away)
  @ui @mcp
  Scenario: CARD-44 in a sparse area the map widens to fit the nearest places
    Given a sparse sample postcode whose nearest places are between 1 and 5 km away
    When the card is drawn
    Then it shows those places, at most 10, with the map's scale fitted so every pin is on the map at its listed distance and bearing within 2%
