@screen @buying @renting
Feature: Area card (the isometric scene of the nearest places, in our chat and in ChatGPT and Claude)
  Question it answers: "Where are the nearest places, at a glance?"
  Modes: both (and anyone, with no account; decisions 0046 and 0051)
  Fixtures: the postcode-level sample area data is not in the fixtures yet (fixture needed: #216);
    figures: none (distances and positions come from the area tools' tested geometry module).
  What it is: the nearest places from the nearby places tool's result (area-tools.feature), drawn as a
    small isometric scene in the approved style (FE-10), with the postcode centre in the middle. It comes
    after the plain answers work in every host (decision 0037).
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
    in effect.
  Copy: quoted messages are proposed wording, finalised in the build.
  Required states (design docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md, "Isometric area card"
    and "Accuracy"; decision 0046's map rules; AGENTS.md rules 4 and 7):
    drawn at the listed distances and bearings, the same in both versions -> CARD-01, CARD-02
    tap, keyboard and screen reader; the text as the accessible version -> CARD-03 to CARD-06
    sources, no risk shading, approximate heights, the postcode centre -> CARD-07 to CARD-10
    no network from load, nothing stored -> CARD-11, CARD-12
    hosts without widgets, no places, reduced motion -> CARD-13, CARD-14, CARD-15
    the widget's sandbox: names as text, messages only from the host, no tool calls, no secrets -> CARD-16 to CARD-19
    Expand: the larger view, keyboard and focus, list rows, full screen in hosts that allow it -> CARD-21 to CARD-25
    no silent change between versions (screenshot test) -> CARD-20

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
    When the card loads and the user taps every pin
    Then the card has made no network request of any kind from the moment it loads, and the widget declares no allowed outside origin in its content security policy

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-12 the card stores nothing
    Given the card has been drawn and its pins tapped
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
    Given a nearby places result with no place within the radius
    When the answer is shown
    Then no card is drawn, and the text says "No <place> found within <radius>" (TOOLS-06), never an empty card

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-15 the card does not move when reduced motion is set
    Given the user's device asks for reduced motion
    When the card is drawn
    Then no pin or building animates

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
    When the user taps every pin
    Then the widget has made no tool call and sent no message or context update to the host

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
    Given the compact card is drawn for a sample postcode
    When the user chooses "Expand"
    Then a larger view opens with every place at the same distance and bearing as on the compact card, and the same places in the list

  @ui
  Scenario: CARD-22 in our chat the expanded view is a dialog on desktop and full screen on a phone
    Given the compact card is drawn in our chat
    When the user chooses "Expand" on a 1280 px wide screen, and again on a 390 px wide screen
    Then it opens as a dialog over the chat on the wide screen, and full screen on the phone, each with a "Close" button

  @ui @mcp
  Scenario: CARD-23 the expanded view works with the keyboard and returns focus
    Given the compact card is drawn for a sample postcode
    When the user reaches "Expand" with Tab, opens it with Enter, then presses Escape
    Then the view opens with focus inside it, Escape closes it, and focus returns to the "Expand" button

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-24 choosing a row in the expanded list selects its pin
    Given the expanded view is open for a sample postcode
    When the user chooses a place in the list
    Then that place's pin is selected on the map, and its name, distance and source with its date are shown, the same as a tap

  @mcp
  Scenario: CARD-25 the widget asks for full screen only where the host allows it
    Given the widget is drawn in a host
    When the user chooses "Expand"
    Then the widget requests full screen only if the host lists it as an available display mode, and if the host refuses or does not list it, the card stays compact with nothing lost and no error shown
