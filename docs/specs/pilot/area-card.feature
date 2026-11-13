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
    standard, a ui:// resource, decision 0037). Every scenario here is tagged for both and runs once per
    version: our chat component in the playwright-bdd suite (ui tag), the widget in the MCP suite (mcp tag).
    Neither version computes a position or a distance: both draw what the tool result gives them
    (design, Accuracy 2), so the two can't drift on the facts.
  Tap a pin (founder, 13 Nov 2026: "Tap a pin for its name", FE-14): tapping or focusing a pin shows its
    name, distance and source.
  Copy: quoted messages are proposed wording, finalised in the build.
  Required states (design docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md, "Isometric area card"
    and "Accuracy"; decision 0046's map rules; AGENTS.md rules 4 and 7):
    drawn at the listed distances, the same in both versions -> CARD-01, CARD-02
    tap, keyboard and screen reader; the text answer as the accessible version -> CARD-03 to CARD-06
    sources, no risk shading, approximate heights, the postcode centre -> CARD-07 to CARD-10
    no network, nothing stored -> CARD-11, CARD-12
    hosts without widgets, no places, reduced motion -> CARD-13, CARD-14, CARD-15

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-01 every place sits at its listed distance, or is named off the map
    Given a nearby places result for a sample postcode
    When the card is drawn
    Then every place is drawn at its listed straight-line distance within 2%, in list order, or is named "off the map"

  # fixture needed: #216
  @ui @mcp
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
    Then the text beside the card lists every place on the card, in the same order, with its distance and source

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-07 the card shows its sources and dates
    Given the card is drawn for a sample postcode
    When the card is shown
    Then it names each source it draws from, with its data date

  @ui @mcp
  Scenario: CARD-08 the card has no flood or crime shading
    Given the card is drawn for a sample postcode
    When the card is shown
    Then no area of the card is shaded, coloured or marked for flood, crime or any other risk

  @ui @mcp
  Scenario: CARD-09 building heights are labelled approximate
    Given the card is drawn for a sample postcode
    When the card is shown
    Then the card says building heights are "approximate"

  @ui @mcp
  Scenario: CARD-10 the centre pin is the postcode centre, never an address
    Given the card is drawn for a sample postcode
    When the card is shown
    Then the centre pin is labelled "Postcode centre", and no address pin is shown

  @ui @mcp
  Scenario: CARD-11 the card makes no network request
    Given the card is drawn for a sample postcode
    When the user taps every pin
    Then the card has made no network request of any kind

  @ui @mcp
  Scenario: CARD-12 the card stores nothing
    Given the card has been drawn and its pins tapped
    When the card is closed
    Then nothing from the card is in local storage, session storage, IndexedDB or cookies

  # fixture needed: #216
  @ui @mcp
  Scenario: CARD-13 a host without widgets still gets every place as text
    Given a host that does not show widgets
    When an answer about nearby places is shown
    Then the text lists every place with its distance and source, and nothing says a card is missing

  @ui @mcp
  Scenario: CARD-14 a result with no places shows no card
    Given a nearby places result with no place within the radius
    When the answer is shown
    Then no card is drawn, and the text says "No places found within <radius>", never an empty card

  @ui @mcp
  Scenario: CARD-15 the card does not move when reduced motion is set
    Given the user's device asks for reduced motion
    When the card is drawn
    Then no pin or building animates
