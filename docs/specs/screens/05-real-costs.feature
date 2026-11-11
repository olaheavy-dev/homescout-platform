@screen @buying
Feature: Real costs (sample slice for the executable-specification set-up, issue #121)
  Question it answers: "What will this home really cost me?"
  Modes: buying
  Fixtures: home B1; inputs: B1-STAMP-DUTY; figures: B1.from-step-1.*
  Required states (doc 03 §5) covered by this slice:
    partial answer -> COSTS-01, COSTS-03
    missing is never zero -> COSTS-02
  The full Real costs specification is issue #68; the scenario IDs below are permanent.

  Scenario: COSTS-01 the monthly total says it is partial
    Given home "B1" is at story step 1
    Then the total "B1.from-step-1.monthly.total" is partial with reason "buildings-insurance"

  Scenario: COSTS-02 missing buildings insurance is not shown as zero
    Given home "B1" is at story step 1
    Then figure "B1.from-step-1.monthly.buildings-insurance" has status "missing"
    And figure "B1.from-step-1.monthly.buildings-insurance" shows no amount

  Scenario: COSTS-03 stamp duty is not calculated and cites its evidence
    Given home "B1" is at story step 1
    Then figure "B1.from-step-1.upfront.stamp-duty" has status "not-calculated"
    And evidence "B1-STAMP-DUTY" exists
    And the total "B1.from-step-1.upfront.total" is partial with reason "stamp-duty"
