@screen @buying
Feature: Every data step wording runs against the real data (proof for issue #193)
  The wording is the contract in docs/specs/README.md; the real specifications use only some of it.

  Scenario: WORD-01 all seven steps accept the documented wording
    Given home "B1" is at story step 2
    Then figure "B1.from-step-1.monthly.buildings-insurance" exists
    And figure "B1.from-step-1.monthly.buildings-insurance" has status "missing"
    And figure "B1.from-step-1.monthly.buildings-insurance" shows no amount
    And figure "B1.from-step-1.monthly.service-charge" cites evidence "B1-SC-LISTING"
    And the total "B1.from-step-1.monthly.total" is partial with reason "buildings-insurance"
    And evidence "B1-STAMP-DUTY" exists
