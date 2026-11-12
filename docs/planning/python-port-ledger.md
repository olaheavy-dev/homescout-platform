# Python port ledger

Decision [0049](../decisions/0049-back-to-python-final.md), issue #186. Every C# test and every worked test case, with the Python test that replaces it. Each port pull request fills in the **Python test** column for the rows it covers (`file::test`, or several separated by `;`). P8 (#195), which removes .NET, may merge only when every row has a Python test or a written reason why none is needed.

Generated on 12 Nov 2026 from the test methods (`[Test]`, `[TestCase]`, `[TestCaseSource]` and the FsCheck property attributes `[PenceProperty]` and `[EngineProperty]`) in `packages/` and the cases in `packages/fixtures/test-cases/`. **Cases** is the number of `[TestCase]` rows on a method; the Python test must cover each of them. Gherkin scenarios in `docs/specs/` are not listed: they are the same files, and P6 (#193) runs them with pytest-bdd.

**How to read it:** a row is done when its **Python test** column names a Python test that checks the same thing; a blank means not yet ported. A few C# tests check .NET-only things (for example `NamespaceMatch_*`, `FrameworkOnlyRule_*` and `CostEngine_assembly_hasNoDependencyOnSystemTextJson`); for those, write the Python equivalent if there is one, or a short reason why none is needed. The worked cases are also checked again through the generator in P4 (`WorkedCaseTests`).

**The header of `costs.json` stays as PC set it:** `generatedBy` is `Vestagraph cost engine` and the `rounding` text cites decisions 0034 and 0036 (register line BE-31). This replaces 0039 section 5's plan for those two fields, so P4's port proof expects no change at all.

**Totals:** 487 test methods; 175 `[TestCase]` rows; worked cases below.

## Worked test cases

Independently worked expectations (`AGENTS.md` rule 2). Each needs a Python test that reads the case from the file and checks the engine against `expected`.

| Port step | File | Case ID | Python test |
|---|---|---|---|
| P2 | `rounding-boundaries.json` | `round-positive-just-below-half` | |
| P2 | `rounding-boundaries.json` | `round-positive-exactly-half` | |
| P2 | `rounding-boundaries.json` | `round-positive-just-above-half` | |
| P2 | `rounding-boundaries.json` | `round-negative-just-below-half` | |
| P2 | `rounding-boundaries.json` | `round-negative-exactly-half` | |
| P2 | `rounding-boundaries.json` | `round-negative-just-above-half` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-5` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-5` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-6` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-6` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-7` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-7` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-18` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-18` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-30` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-30` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-25000` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-25000` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-185000` | |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-185000` | |
| P3a | `story-calculations.json` | `b1-service-charge-difference` | |
| P3a | `story-calculations.json` | `b1-mortgage-repayment` | |
| P3a | `story-calculations.json` | `b2-mortgage-repayment` | |
| P3a | `story-calculations.json` | `mortgage-repayment-boundary-10025200` | |
| P3a | `story-calculations.json` | `mortgage-repayment-boundary-10060700` | |
| P3a | `story-calculations.json` | `b1-monthly-housing-cost-listing-service-charge` | |
| P3a | `story-calculations.json` | `b1-monthly-housing-cost-management-pack-arrived` | |
| P3a | `story-calculations.json` | `b1-monthly-housing-cost-2026-budget` | |
| P3a | `story-calculations.json` | `b2-monthly-housing-cost` | |
| P3a | `story-calculations.json` | `r1-monthly-housing-cost-before-water` | |
| P3a | `story-calculations.json` | `r1-monthly-housing-cost-after-water` | |
| P3a | `story-calculations.json` | `r2-monthly-housing-cost` | |
| P3b | `story-calculations.json` | `b1-upfront-cash` | |
| P3b | `story-calculations.json` | `b2-upfront-cash` | |
| P3b | `story-calculations.json` | `r1-upfront-cash` | |
| P3b | `story-calculations.json` | `r2-upfront-cash` | |
| P3a | `story-calculations.json` | `b1-budget-beat` | |

## C# tests

| Port step | Project | Class | Test | Cases | Python test |
|---|---|---|---|---|---|
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `ClockAndRandomTypeRule_appliedToCodeThatUsesRandom_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `ClockRule_appliedToCodeThatReadsTheTime_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_hasNoDependencyOnClockOrRandom` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_hasNoDependencyOnIoNetworkCloudOrAi` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_hasNoDependencyOnSystemTextJson` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_neverReadsTheClockOrMakesGuids` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_referencesOnlyTheFrameworkAndSystemLibraries` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_everyTypeOutsideTheCoverageTracker_livesUnderTheEngineNamespace` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_publicSignatures_useNoDoubleOrFloat` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `DependencyRule_appliedToCodeThatUsesFiles_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `FloatingPointRule_appliedToCodeThatExposesDouble_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `ForbiddenMemberRule_appliedToCodeThatCallsGuidNewGuid_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `FrameworkOnlyRule_appliedToTheTestAssembly_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `JsonRule_appliedToCodeThatUsesJson_failsAsExpected` |  | |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `NamespaceMatch_prefixThatIsNotAWholeNamespaceSegment_isNotInside` | 6 | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Add_negatedAmount_returnsZero` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Add_threeAmounts_isAssociative` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Add_twoAmounts_isCommutative` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `AnnualToMonthly_anyInput_matchesRoundingTheExactQuotient` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `AnnualToMonthly_negatedInput_isNegatedResult` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `AnnualToMonthly_twelveTimesMonthly_returnsMonthly` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `CompareTo_twoAmounts_agreesWithSign` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_anyInput_isWithinHalfAPennyOfTheInput` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_appliedTwice_equalsAppliedOnce` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_exactHalf_roundsAwayFromZero` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_negatedInput_isNegatedResult` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_wholePence_isIdempotent` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Subtract_amount_equalsAddingTheNegation` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Add_negativeAmount_reducesTotal` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Add_overflow_throwsOverflowException` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Add_twoAmounts_returnsSum` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `AnnualToMonthly_exactMultipleOfTwelve_isExact` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `AnnualToMonthly_maxValue_doesNotOverflow` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `AnnualToMonthly_minValue_doesNotOverflow` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `CompareTo_smallerAndLarger_ordersByValue` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `ComparisonOperators_variousPairs_followValueOrder` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Comparison_equalAmounts_areNotStrictlyLessOrGreater` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Equals_sameValue_isEqual` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Multiply_byWholeNumber_returnsProduct` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Multiply_overflow_throwsOverflowException` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_minValue_throwsOverflowException` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_negative_returnsPositive` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_positive_returnsNegative` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_zero_returnsZero` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Round_amountTooLargeForLong_throwsOverflowException` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Round_halfPenny_isNotBankersRounding` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Round_wholeNumber_isUnchanged` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Subtract_methodForm_matchesOperator` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Subtract_overflow_throwsOverflowException` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Subtract_twoAmounts_returnsDifference` |  | |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Zero_default_equalsNewPenceOfZero` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ErrorCategory_definedValues_areExactlyTheFourDecided` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_blankCode_throwsArgumentException` | 2 | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_blankMessage_throwsArgumentException` | 2 | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_created_keepsCodeAndMessage` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_eachCategory_isKeptOnTheError` | 4 | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_sameParts_areEqual` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_undefinedCategory_throwsArgumentOutOfRangeException` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `FailureOfT_nullError_throwsArgumentNullException` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `FailureOfT_withError_hidesValueAndExposesError` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Failure_nullError_throwsArgumentNullException` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Failure_withError_isFailureCarryingThatError` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `SuccessOfT_nullValue_throwsArgumentNullException` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `SuccessOfT_withValue_exposesValue` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Success_noValue_isSuccessWithNoError` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ToResult_failure_keepsError` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ToResult_failure_keepsTheError` |  | |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ToResult_successWithAValue_isASuccess` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `BoundaryFile_loaded_hasAllSixRatioCases` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_boundaryCaseFromFile_matchesWorkedResult` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_largeExactHalf_roundsAwayFromZeroWithoutLosingPrecision` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_resultTooBigForALong_throwsOverflow` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_resultTooSmallForALong_throwsOverflow` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_signsAndHalves_roundAwayFromZero` | 10 | |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_zeroDenominator_throwsDivideByZero` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `AnnualToMonthly_boundaryCaseFromFile_matchesWorkedResult` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `BoundaryFile_loaded_hasAllSixDirectRoundingCases` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `BoundaryFile_loaded_hasTheAnnualToMonthlyCases` |  | |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `Round_boundaryCaseFromFile_matchesWorkedResult` |  | |
| P3a | Vestagraph.CostEngine.Tests | BudgetBeatTests | `BudgetBeat_file_hasOneBudgetBeatCase` |  | |
| P3a | Vestagraph.CostEngine.Tests | BudgetBeatTests | `BudgetBeat_storyCase_landsAsWorked` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_aNonCalculatedLineNeverCarriesPence` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_budgetDifferenceIsBudgetMinusTotalAndWithinMeansAtOrBelow` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_isPartialExactlyWhenALineIsNotCalculatedConflictingOrMissing` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_noLineOrTotalIsNegative` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_totalEqualsTheSumOfTheCalculatedLines` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_higherRent_neverLowersTheTotal` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyRepayment_anyValidInput_isNeverNegative` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyRepayment_higherRate_neverLowersTheRepayment` |  | |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyRepayment_largerLoan_neverLowersTheRepayment` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `CostCategories_missingStatus_isNamedMissing` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `CostCategories_undefinedValues_throw` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCases_file_hasTheSevenWorkedMonthlyCases` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_amountNotPositive_failsAsNotPositive` | 2 | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_anchorLineThatIsNotAnAmount_failsAsMissing` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_billGivenOnce_failsAsWrongPeriod` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_budgetNotPositive_failsAsNotPositive` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_includedLine_doesNotMakeTheTotalPartial` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_lineThatDoesNotBelongToTheMode_failsAsNotForMode` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_linesGivenOutOfOrder_comeBackInTheFixedBuyOrder` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_linesGivenOutOfOrder_comeBackInTheFixedRentOrder` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_missingLine_makesTheTotalPartialWithACodedReason` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_noAnchorLine_failsAsMissing` | 2 | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_nonCalculatedLines_haveNoAmountAndNoSourcePeriod` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_nullLineInTheList_throws` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_nullLines_throws` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_rentGivenYearly_failsAsWrongPeriod` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_sameCategoryTwice_failsAsAmbiguous` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_storyCase_matchesWorkedResult` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_tinyYearlyAmount_roundsToZeroButStaysCalculated` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_totalExactlyEqualToBudget_isWithinBudget` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_totalOnePennyOverBudget_isNotWithinBudget` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_totalTooBigForALong_throwsOverflow` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_undefinedMode_throws` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_unknownKindOfLine_throwsForThatLine` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_upfrontCategoryInAMonthlyList_failsAsNotForMode` |  | |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_yearlyLine_keepsItsSourcePeriodAndEvidence` |  | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `BasisPoints_rateThatIsNotWholeBasisPoints_failsTheTest` |  | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_invalidInput_failsWithTheCode` | 6 | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_storyCase_matchesWorkedResult` |  | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_termOf100Years_isCalculated` |  | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_termOver100Years_failsAsTooLong` | 3 | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_veryLargeLoan_neverGivesAWrongSuccess` | 3 | |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MortgageCases_file_hasTheFourWorkedMortgageCases` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_anchorFromTwoItems_failsAsAmbiguous` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_anchorItemWithStatusMissing_failsAsMissing` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_buyingHome_hasNoMortgageRepaymentLineAndTheDepositUpfront` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_buyingHome_returnsTheMortgageInputsWithTheirEvidence` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_buyingWithoutAnAnchorInput_failsAsMissing` | 4 | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_conflictingItemWithoutAnAmount_givesAConflictingLine` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_conflictingWaterResponsibility_givesConflictingWaterWithBothItems` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_contextOnlyItem_isIgnored` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_depositGivenYearly_failsAsWrongPeriod` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_homeOutsideEngland_failsAsNotCovered` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_homeWithNoMode_failsAsModeMissing` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_includedAlongsideConflicting_givesConflicting` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_includedAlongsideNotApplicable_givesIncluded` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_includedItem_givesAnIncludedLine` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_includedWaterAlongsideConflictingResponsibility_givesConflicting` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_itemNotYetUsed_isIgnoredBeforeItsStep` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_itemWithNoStartStep_isInUseFromTheFirstStep` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_itemWithStatusMissing_givesAMissingLineWithNoEvidence` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_lineThatDoesNotBelongToTheMode_isNotReturned` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_moneyAlongsideConflicting_stillGivesTheAmount` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_moneyItemWithAValue_givesAnAmountWhateverItsStatus` | 3 | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_noEvidenceForACategory_givesAMissingLineWithNoEvidence` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_notApplicableAlongsideConflicting_givesConflicting` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_notApplicableItem_leavesTheLineOut` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_notCalculatedAlongsideIncluded_givesNotCalculatedAsTheMoreCautious` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_notCalculatedItem_givesANotCalculatedLine` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_nullEvidenceList_throws` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_nullFacts_throws` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_priceGivenMonthly_failsAsWrongPeriod` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_priceZero_failsAsNotPositive` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_rateGivenAsMoney_failsAsWrongKind` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_rentGivenYearly_failsAsWrongPeriod` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_rentNotMoreThanZero_failsAsNotPositive` | 2 | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_rentWithWrongKindAndTwoValues_failsAsWrongKind` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_rentingHome_hasNoMortgage` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_rentingWithoutRent_failsAsMissing` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_serviceChargeGivenAsRate_failsAsWrongKind` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_stepBelowOne_failsAsOutOfRange` | 2 | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_supersedeChain_usesOnlyTheLatestItemThatHasStarted` | 4 | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_supersededItem_isUsedUntilTheNewOneStarts` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_termGivenAsRate_failsAsWrongKind` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_twoMoneyItemsForOneCategory_failsAsAmbiguous` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_upfrontCostGivenAsRate_failsAsWrongKind` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_waterEstimate_winsOverConflictingResponsibility` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_waterResponsibility_doesNotAffectAnotherCategory` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_wrongKindAndTwoValues_failsAsWrongKindForAnAnchor` |  | |
| P3b | Vestagraph.CostEngine.Tests | AssumptionSelectorTests | `Select_wrongKindAndTwoValues_failsAsWrongKindForAnOrdinaryLine` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_amountThatChanges_isReportedAsValueChanged` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_amountThenIncluded_isReportedAsNoLongerCalculated` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_amountThenNotApplicable_isReportedAsNoLongerApplies` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_anchorInputMissing_passesOnTheSelectorsFailure` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_anyMonthlyBudget_isCarriedIntoEachScenario` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_buyingHome_hasAMortgageWithTheEvidenceBehindIt` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_changeEvidence_namesThePreviousAndCurrentItems` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_conflictingThenNotApplicable_isReportedAsNoLongerApplies` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_conflictingWaterThenAnEstimate_givesNoMonthlyTotalChange` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_conflictingWaterThenAnEstimate_isReportedAsNowCalculated` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_depositLargerThanThePrice_failsBecauseTheLoanIsNotPositive` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_evidenceChangesAtStepFour_givesTwoScenariosNamedFromTheirFirstStep` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_firstScenario_hasNoChanges` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_homeDetails_comeFromTheFacts` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_homeOutsideEnglandAndNoSteps_reportsTheHomeFirst` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_homeOutsideEngland_failsAsNotCovered` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_homeWithNoMode_failsAsModeMissing` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_lineNotApplicableThenEstimated_isReportedAsNowCalculated` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_lineThatBecomesConflicting_givesNoMonthlyTotalChange` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_missingThenNotApplicable_isReportedAsNoLongerApplies` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_monthlyDifference_isTheDifferenceOfTheRoundedMonthlyLines` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_monthlyLineOnTheSourceEvidenceButNewAmount_hasNoAnnualDifferenceWhenOnlyOneSideIsYearly` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_newEvidenceWithTheSameAmount_isReportedAsEvidenceChangedNotValueChanged` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_noBudget_failsAsNotPositive` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_notApplicableThenMissing_isReportedAsEvidenceChanged` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_nullArguments_throw` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_onlyTheMortgageRateChanges_givesTwoScenariosWithARepaymentChange` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_rentingHome_hasNoMortgage` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_sameAmountChangingPeriod_isReportedAsValueChanged` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_sameEvidenceAtEveryStep_givesOneScenarioCoveringAllSteps` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_sameLinesLeftOutOfBothTotals_keepsTheMonthlyTotalChange` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_statusChangeBetweenTwoLinesWithNoAmount_isReportedAsEvidenceChanged` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_stepsThatAreEmptyBelowOneOrNotIncreasing_failAsOutOfRange` | 4 | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_stepsThatStartAboveOne_areAccepted` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_upfrontAmountChanges_isAValueChangeWithNoMonthlyOrAnnualDifference` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_upfrontAmountThenSameAmountFromNewEvidence_isAnEvidenceChange` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_upfrontLineGivenMonthly_failsAsWrongPeriod` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_upfrontLineOfZero_failsAsNotPositive` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `Build_yearlyAmountRisesByOnePenceButMonthlyRoundingHidesIt_stillReportsTheAnnualDifference` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `FigureIds_lineTotalBudgetAndChange_followTheContractFormat` |  | |
| P3b | Vestagraph.CostEngine.Tests | HomeCostBuilderTests | `ServiceChargeChange_storyCase_matchesWorkedResult` |  | |
| P3b | Vestagraph.CostEngine.Tests | StoryCalculationCoverageTests | `StoryCalculations_everyCase_isRunByADataDrivenTest` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashProperties | `UpfrontCash_anyLines_aNonCalculatedLineNeverCarriesPence` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashProperties | `UpfrontCash_anyLines_isPartialExactlyWhenALineIsNotCalculatedConflictingOrMissing` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashProperties | `UpfrontCash_anyLines_noLineOrTotalIsNegative` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashProperties | `UpfrontCash_anyLines_totalEqualsTheSumOfTheCalculatedLines` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCases_file_hasTheFourWorkedUpfrontCases` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_amountGivenMonthly_failsAsWrongPeriod` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_amountNotPositive_failsAsNotPositive` | 2 | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_buyingWithMortgageDepositMissing_failsAsMissingMortgageDeposit` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_buyingWithNoLines_failsAsMissingMortgageDeposit` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_lineThatDoesNotBelongToTheMode_failsAsNotForMode` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_linesGivenOutOfOrder_comeBackInTheFixedBuyOrder` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_linesGivenOutOfOrder_comeBackInTheFixedRentOrder` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_missingMovingCosts_makesTheTotalPartial` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_nullLines_throws` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_rentingWithNoLines_hasNoLinesAndATotalOfZeroThatIsNotPartial` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_sameCategoryTwice_failsAsAmbiguous` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_stampDutyAndLegalFees_stayNotCalculatedWithNoAmount` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_storyCase_matchesWorkedResult` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_totalTooBigForALong_throwsOverflow` |  | |
| P3b | Vestagraph.CostEngine.Tests | UpfrontCashTests | `UpfrontCash_undefinedMode_throws` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_buyerStory_mergesStepsOneToTwoThenSplitsAtStepsThreeAndFour` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_englishHomes_carryModeNationCoverageAndStory` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_everyFigureId_isUniqueAndMatchesThePattern` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_everyKey_followsTheOrderOfTheContractSchema` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_everyPartialReason_pointsAtALineInTheSameScenario` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_header_copiesTheSnapshotDateAndNamesTheContract` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_noMoneyAnywhere_isAFloatingPointNumber` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_realData_derivesTheExpectedScenarios` | 5 | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_realData_listsTheHomesInTheOrderOfTheSnapshot` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_runTwice_givesIdenticalText` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_text_usesLfLineEndingsTwoSpaceIndentAndOneFinalNewline` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | OutputShapeTests | `Generate_walesHome_isNotYetCoveredWithNoScenariosAndNoMode` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `CommittedCostsFile_matchesWhatTheGeneratorProduces` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_coveredHomeInNoStory_failsWithItsCodeNotGuessing` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_dataFileMissing_throwsInsteadOfWritingGuesses` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_homeInTwoStories_failsWithItsCode` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_listWhereAnObjectIsExpected_throwsInvalidData` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_quantityInOtherUnits_isReadAsAnotherKindOfValueNotAnError` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_textWhereANumberIsExpected_throwsInvalidDataNotAStackTrace` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Generate_unknownEvidenceStatus_throwsInsteadOfGuessing` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_costsJsonCannotBeReplaced_keepsTheOtherJsonFilesAndLeavesNoTemporaryFile` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_engineFailure_exitsNonZeroNamesTheErrorCodeAndWritesNothing` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_engineFailure_leavesAnExistingGeneratedFolderUntouched` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_otherJsonFileInGenerated_isDeletedAndOtherFilesAreKept` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_realData_writesCostsJsonAsUtf8WithoutByteOrderMark` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_success_leavesNoTemporaryFile` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | RunTests | `Run_twice_givesByteIdenticalFiles` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_budgetBeatCase_landsAsWorked` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_energyCertificateCosts_neverEnterAnyLineOrTotal` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_insuranceAtStepThree_isEvidenceChangedWithNoTotalChange` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_monthlyStoryCase_matchesWorkedResult` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_mortgageStoryCases_matchTheWorkedRepayments` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_rentedHomeWhoseBillsAreIncluded_showsThemAsIncludedNotZero` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_serviceChargeDifferenceCase_matchesWorkedResult` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_upfrontStoryCase_matchesWorkedResultInEveryScenario` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_waterAtStepFour_isNowCalculated` |  | |
| P4 | Vestagraph.CostEngine.Generator.Tests | WorkedCaseTests | `Generate_waterAtStepOne_isConflictingWithBothStatementsAsEvidence` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_aSchoolInspected_isInspectedTheSameWayEverywhereItAppears` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_amenities_coverEverySubtypeSomewhereInEngland` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_bankRate_isLabelledAsASampleNotTheActualRate` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_bankRate_isOneSharedItemWithASourceDate` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_commute_isTheHouseholdsOwnEstimateNotARoutedJourney` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_commute_usesTheHouseholdCommuteCriterion` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_councilTax_isNotAreaData` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_crimeCategories_areUniqueWithinEachItem` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_crimeForB1AndB2_coversTwoDifferentMonths` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_crimeMonths_areTheTwoLaggedMonths` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_dates_areNotAfterTheSnapshotDate` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_eachEnglandHome_hasEveryAmenityCategoryOrAnExplicitNoRecordItem` | 4 | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_eachEnglandHome_hasEveryRequiredTopicOrAnExplicitGap` | 4 | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_energyItem_pointsAtTheCertificateAndItsCostInTheEvidenceFile` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_energyItemsThatAreStale_doNotCopyTheCertificateYear` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_energyItems_neverSayThisFlat` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_energyItems_pointAtEvidenceItemsThatExist` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyDistance_namesItsSyntheticMethod` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyEnglandHomeWithCrime_coversBothLaggedMonthsRecordedOrNamedAsFailed` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyEnglandHome_hasACommuteItem` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyEnglandHome_hasAFloodItem` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyHomeId_isAHomeInTheHomesFile` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyHomeItem_ofAnEnglandHome_isCoveredOrAGapThatSaysWhy` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyHome_hasAHealthcareLocation` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyId_followsHomeAreaTopicNumber` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everySource_isSyntheticAndLabelled` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_everyTopic_isInTheAgreedEnumOrder` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_file_neverUsesSafeUnsafeVerifiedOrApprovedWording` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_floodItemsWithNoRecord_pointTheUserToTheLongTermChecker` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_floodItems_neverUseSurfaceWaterAsASubtypeAndSayWhyAndWhereToLook` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_floodWarnings_exactlyOneHomeHasALiveWarning` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_gapExamples_includeEveryStatusTheIssueRequires` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_ids_areUnique` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_placesOfWorship_areSinglePlacesWithAReligionAndOneSharedLimit` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_priorityTopic_hasTwoToFourItemsForEachHome` | 14 | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_r1_isSetOnStationRoadAndR2OnCanalStreet` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_r2Energy_isStaleAndPointsAtItsExpiredCertificateOnly` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_schemaFile_hasNoRatingOrScoreFieldOnCrime` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_schoolInspections_pointAtASchoolOfTheSameHome` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_soldPriceAddresses_areUniqueSoNoAddressHasTwoPrices` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_valueDates_areNotAfterTheSnapshotDate` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_wales1_hasAnItemForEachPerHomeTopicExceptLeaseholdAndBankRate` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaDataTests | `Area_wales1_hasOnlyNotCoveredItems` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_amenitySubtypeOnAFloodItem_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_amenitySubtypeOutsideTheList_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_amenityWithNoSubtype_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_bankRateAsADecimal_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_bankRateTiedToAHome_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_childcareAmenity_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_crimeCategoryOutsideTheList_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_crimeCountOfZero_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_crimeCountsThatAreExactDuplicates_areRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_crimeItemWithARatingField_isRejected` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_distanceAsADecimal_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_distanceWithNoMethod_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_energyItemThatCopiesTheIssuedYear_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_energyItemThatCopiesTheRating_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_energyItemWithAHandMadeCostRange_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_energyItemWithNoEvidenceLink_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_floodItemThatHasNoFloodType_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_floodSubtypeOnAnAmenity_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_gapItemThatCarriesAValue_isRejected` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_homeItemWithNoHomeId_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_idThatDoesNotFollowThePattern_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_itemWithNoCoverage_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_itemWithNoDoesNotEstablishText_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_itemWithNoSource_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_linkThatIsNotHttps_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_liveFloodWarningOnSurfaceWater_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_notCoveredItemThatCarriesAValue_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_placeOfWorshipReligionOutsideTheList_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_placeOfWorshipWithNoReligion_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_recordedItemWithNoValue_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_religionOnAnAmenityThatIsNotAPlaceOfWorship_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_schoolInspectionWithASingleOverallGrade_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_schoolInspectionWithNoFramework_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_schoolInspectionWithNoInspectionDate_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_soldPriceOfAnOtherPropertyType_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_sourceWithNoDate_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_sourceWithNoSyntheticFlag_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_staleItemWithNoValue_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_stalePlaceOfWorshipWithNoReligion_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_statusOutsideTheEnum_isRejected` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_subtypeOnATopicThatHasNone_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_topicOutsideTheEnum_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_unchangedRealRecord_isAccepted` | 7 | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `Area_unknownExtraField_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | AreaSchemaRejectionTests | `ValidateFixtures_invalidAreaFile_isReportedAgainstTheAreaSchema` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_badFigureId_isRejected` | 7 | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_budgetWithoutPartialFlag_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_buyingScenarioWithNoMortgage_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_calculatedLineWithoutPence_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_calculatedLineWithoutSourcePeriod_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_changeWithUnknownKind_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_completeTotalWithReasons_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_coveredHomeWithNoScenarios_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_decimalPence_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_includedLineWithNoEvidence_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_missingLineThatNamesEvidence_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_missingLineWithPence_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_missingSnapshotDate_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_mortgageLoanOfZero_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_mortgageRepaymentOfZero_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_mortgageTermOver100Years_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_mortgageWithZeroRate_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_negativePenceOnACalculatedLine_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_nonCalculatedLineWithPence_isRejected` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_notYetCoveredHomeWithScenarios_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_partialReasonForACalculatedLine_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_partialTotalWithNoReasons_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_sampleShape_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_unknownCategory_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_unknownKeyInALine_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_unknownLineStatus_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_walesMarkedCovered_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_wrongFormatVersion_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `GeneratedCosts_wrongScenarioId_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `ValidateFixtures_generatedFileWithNoSchemaLine_isReported` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `ValidateFixtures_invalidGeneratedFile_isReported` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `ValidateFixtures_noGeneratedFolder_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | GeneratedCostsSchemaTests | `ValidateFixtures_validGeneratedFile_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `AllFixtureFiles_validateAgainstTheirSchemas_withNoProblems` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `B1_buildingsInsurance_isIncludedInTheServiceCharge_notZero` | 1 | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `B1_buildingsInsurance_isUsedFromStepThree_whenItsOnlySourceArrives` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `B1_postcode_matchesSixCandidateUnits_andTheSelectedOneIsAmongThem` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `B1_serviceCharge_keepsTheListingFigureAndTheLaterBudget` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `EnergyCertificateCosts_areFlaggedContextOnly_atTheirOldPrices` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `EvidenceItem_markedContextOnly_isAnEnergyCertificateCost` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `Home_inEveryRecord_hasANation` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `LeaseAndCouncilTaxBands_approvedInPlan_matchTheFile` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `MoneyInput_approvedInPlan_matchesTheFile` | 28 | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `MortgageAndBudgetInputs_approvedInPlan_matchTheFile` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `NorthbridgeHomes_postcodes_startWithNb` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `NotCalculatedItems_areNotCalculated_notZero` | 5 | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `Numbers_inEveryFixtureFile_areWholeNumbers` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `Question_finalStatus_equalsItsLastTransition` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `Question_statuses_matchTheStoriesInThePlan` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `R2_bills_areIncluded_notZero` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `R2_certificate_isExpired2025_issued2015_withCitedGovUkText` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `Reference_inAnyRecord_pointsAtARecordThatExists` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `SnapshotDate_inSnapshotFile_isTheApprovedDate` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `ValidateFixtures_dataFileWithNoSchemaAvailable_isReported` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `ValidateFixtures_nonStringSchemaField_isReportedReadably` |  | |
| P5 | Vestagraph.Fixtures.Tests | RealDataTests | `Wales1_address_isWalesAndNotYetCovered` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_availableItemWithNoValue_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_billRecordedAsZeroInsteadOfIncluded_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_certificateCostNotMarkedContextOnly_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_citedTextWithoutCitationUrl_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_includedBillThatAlsoHasAValue_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_misspeltCategory_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_moneyAsAPoundsString_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_moneyWithDecimals_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_mortgageTermOf100Years_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_mortgageTermOver100Years_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_notCalculatedItemRecordedAsZero_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_notCalculatedItemThatAlsoHasAValue_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_rateAsADecimal_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_sourceWithNoOrigin_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_sourceWithNoSyntheticFlag_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_syntheticOriginWithSyntheticFlagFalse_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_unchangedRealRecord_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_unknownStatus_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Evidence_valueWithNoSource_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Home_addressWithNoNation_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Home_candidateUnitsWithNoSelectedUnit_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Home_englandMarkedAsNotCovered_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Home_englishHomeMissingADescriptiveField_isRejected` | 5 | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Home_selectedUnitOutsideTheCandidates_isNotCaughtBySchemaButIsCaughtByDataTest` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Home_walesMarkedAsCovered_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Question_eachStatusFromDoc02_isAccepted` | 8 | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Question_resolvedStatusThatIsNotInDoc02_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | SchemaRejectionTests | `Question_transitionWithNoReason_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `B1ServiceChargeBudget_afterTheUserConfirms_isUsedFromStep4` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `EnergyCertificate_ofEachHomeWithOne_hasTheApprovedRatingAndYear` | 3 | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `Ids_acrossEvidenceDocumentsQuestionsAndReplies_areUnique` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `R1WaterEstimate_afterTheUserConfirms_isUsedFromStep4` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `R1WaterListingClaim_whenCheckedAgainstTheStatement_isConflicting` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `R1WaterWrittenStatement_inBillsSection_saysTenantPaysWater` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `R2CouncilTax_whenRentIncludesBills_isPresentAndNotIncluded` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `Snapshot_householdAndHomeIds_resolveToRecords` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `Source_syntheticFlag_isTrueInEveryDataFile` |  | |
| P5 | Vestagraph.Fixtures.Tests | StoryTests | `Story_homeIds_resolveToHomesInTheSnapshot` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_caseWithNoRule_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_costLineAsZeroAmount_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_lineStatusMissing_isAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_moneyFieldWithDecimals_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_partialTotalWithNoReason_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_realFile_namesItsSchemaAndIsAccepted` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCaseFile_unknownLineStatus_isRejected` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCases_crossCaseLinks_pointAtCasesThatExist` |  | |
| P5 | Vestagraph.Fixtures.Tests | TestCaseFileTests | `TestCases_idsAreUnique` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `GivenHomeIsAtStoryStep_stepInsideRange_setsTheScenario` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `GivenHomeIsAtStoryStep_stepOutOfRange_fails` | 2 | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `GivenHomeIsAtStoryStep_unknownHome_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureCitesEvidence_citedEvidence_passes` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureCitesEvidence_evidenceNotCitedByFigure_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureCitesEvidence_unknownEvidence_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureExists_figureFromAnotherStep_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureExists_unknownFigure_failsNamingTheId` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureHasStatus_correctStatus_passes` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureHasStatus_total_failsSayingItIsATotal` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureHasStatus_wrongStatus_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureShowsNoAmount_budgetWithBudgetPence_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureShowsNoAmount_lineWithPence_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureShowsNoAmount_lineWithoutAmount_passes` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenFigureShowsNoAmount_total_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenTotalIsPartialWithReason_listedReason_passes` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenTotalIsPartialWithReason_reasonNotListed_fails` |  | |
| P6 | Vestagraph.Specs.Tests | DataStepsTests | `ThenTotalIsPartialWithReason_totalNotPartial_fails` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `EvidenceIds_knownEvidence_containsIt` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `FigureIds_generatedFile_isNotEmpty` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `HasScenarioFromStep_stepInsideAScenarioRange_isTrue` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `HasScenarioFromStep_stepWithNoScenario_isFalse` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `HomeIds_knownHome_containsItAndNotAnUnknownOne` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `TryGetFigure_knownFigureId_findsIt` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `TryGetFigure_unknownFigureId_doesNotFindIt` |  | |
| P6 | Vestagraph.Specs.Tests | SpecDataTests | `TryGetFigure_wrongCase_doesNotFindIt` |  | |
