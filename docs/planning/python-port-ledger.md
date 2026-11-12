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
| P2 | `rounding-boundaries.json` | `round-positive-just-below-half` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `round-positive-exactly-half` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `round-positive-just-above-half` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `round-negative-just-below-half` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `round-negative-exactly-half` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `round-negative-just-above-half` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-5` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-5` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-6` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-6` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-7` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-7` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-18` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-18` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-30` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-30` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-25000` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-25000` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-pos-185000` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | `rounding-boundaries.json` | `annual-to-monthly-neg-185000` | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P3a | `story-calculations.json` | `b1-service-charge-difference` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_service_charge_difference_case_matches_the_difference_of_the_two_monthly_lines; end-to-end check also in P3b's builder test |
| P3a | `story-calculations.json` | `b1-mortgage-repayment` | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `b2-mortgage-repayment` | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `mortgage-repayment-boundary-10025200` | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `mortgage-repayment-boundary-10060700` | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `b1-monthly-housing-cost-listing-service-charge` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `b1-monthly-housing-cost-management-pack-arrived` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `b1-monthly-housing-cost-2026-budget` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `b2-monthly-housing-cost` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `r1-monthly-housing-cost-before-water` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `r1-monthly-housing-cost-after-water` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | `story-calculations.json` | `r2-monthly-housing-cost` | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3b | `story-calculations.json` | `b1-upfront-cash` | |
| P3b | `story-calculations.json` | `b2-upfront-cash` | |
| P3b | `story-calculations.json` | `r1-upfront-cash` | |
| P3b | `story-calculations.json` | `r2-upfront-cash` | |
| P3a | `story-calculations.json` | `b1-budget-beat` | packages/vestagraph-engine/tests/test_engine_budget_beat.py::test_budget_beat_story_case_lands_as_worked |

## C# tests

| Port step | Project | Class | Test | Cases | Python test |
|---|---|---|---|---|---|
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `ClockAndRandomTypeRule_appliedToCodeThatUsesRandom_failsAsExpected` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_import_rule_applied_to_a_disallowed_import_fails_as_expected |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `ClockRule_appliedToCodeThatReadsTheTime_failsAsExpected` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_clock_rule_applied_to_code_that_reads_the_time_fails_as_expected |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_hasNoDependencyOnClockOrRandom` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_engine_source_obeys_every_purity_rule |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_hasNoDependencyOnIoNetworkCloudOrAi` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_engine_source_obeys_every_purity_rule |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_hasNoDependencyOnSystemTextJson` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_engine_source_obeys_every_purity_rule (json is not on the import allow-list) |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_neverReadsTheClockOrMakesGuids` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_engine_source_obeys_every_purity_rule |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_assembly_referencesOnlyTheFrameworkAndSystemLibraries` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_engine_source_obeys_every_purity_rule (the import allow-list replaces the assembly reference check) |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_everyTypeOutsideTheCoverageTracker_livesUnderTheEngineNamespace` |  | No Python equivalent (.NET-only): the engine is one package, `vestagraph_engine`, so every module is inside it by construction, and the import rule forbids other Vestagraph packages |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `CostEngine_publicSignatures_useNoDoubleOrFloat` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_engine_source_obeys_every_purity_rule; packages/vestagraph-engine/tests/test_engine_architecture.py::test_forbidden_name_rule_applied_to_a_float_annotation_fails_as_expected |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `DependencyRule_appliedToCodeThatUsesFiles_failsAsExpected` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_import_rule_applied_to_a_disallowed_import_fails_as_expected; packages/vestagraph-engine/tests/test_engine_architecture.py::test_forbidden_name_rule_applied_to_code_using_it_fails_as_expected |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `FloatingPointRule_appliedToCodeThatExposesDouble_failsAsExpected` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_forbidden_name_rule_applied_to_a_float_annotation_fails_as_expected; packages/vestagraph-engine/tests/test_engine_architecture.py::test_true_division_rule_applied_to_true_division_fails_as_expected |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `ForbiddenMemberRule_appliedToCodeThatCallsGuidNewGuid_failsAsExpected` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_import_rule_applied_to_a_disallowed_import_fails_as_expected (includes `import uuid`) |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `FrameworkOnlyRule_appliedToTheTestAssembly_failsAsExpected` |  | No Python equivalent (.NET-only): it checked that the rule also fails for a test assembly; the Python import rule is proved by `test_import_rule_applied_to_a_disallowed_import_fails_as_expected` and `test_import_rule_applied_to_an_allowed_import_passes` |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `JsonRule_appliedToCodeThatUsesJson_failsAsExpected` |  | packages/vestagraph-engine/tests/test_engine_architecture.py::test_import_rule_applied_to_a_disallowed_import_fails_as_expected |
| P2 | Vestagraph.CostEngine.Tests | ArchitectureTests | `NamespaceMatch_prefixThatIsNotAWholeNamespaceSegment_isNotInside` | 6 | packages/vestagraph-engine/tests/test_engine_architecture.py::test_import_rule_applied_to_a_disallowed_import_fails_as_expected; packages/vestagraph-engine/tests/test_engine_architecture.py::test_import_rule_applied_to_an_allowed_import_passes (modules match by whole top-level name: `vestagraph_generator` is rejected) |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Add_negatedAmount_returnsZero` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_add_negated_amount_returns_zero |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Add_threeAmounts_isAssociative` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_add_three_amounts_is_associative |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Add_twoAmounts_isCommutative` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_add_two_amounts_is_commutative |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `AnnualToMonthly_anyInput_matchesRoundingTheExactQuotient` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_annual_to_monthly_any_input_is_the_nearest_penny_to_the_exact_quotient |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `AnnualToMonthly_negatedInput_isNegatedResult` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_annual_to_monthly_negated_input_is_negated_result |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `AnnualToMonthly_twelveTimesMonthly_returnsMonthly` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_annual_to_monthly_twelve_times_monthly_returns_monthly |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `CompareTo_twoAmounts_agreesWithSign` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_compare_two_amounts_agrees_with_sign |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_anyInput_isWithinHalfAPennyOfTheInput` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_from_exact_any_input_is_within_half_a_penny_of_the_input |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_appliedTwice_equalsAppliedOnce` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_from_exact_applied_twice_equals_applied_once |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_exactHalf_roundsAwayFromZero` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_from_exact_exact_half_rounds_away_from_zero |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_negatedInput_isNegatedResult` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_from_exact_negated_input_is_negated_result |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Round_wholePence_isIdempotent` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_from_exact_whole_pence_is_idempotent |
| P2 | Vestagraph.CostEngine.Tests | PenceProperties | `Subtract_amount_equalsAddingTheNegation` |  | packages/vestagraph-engine/tests/test_engine_pence_properties.py::test_subtract_amount_equals_adding_the_negation |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Add_negativeAmount_reducesTotal` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_add_negative_amount_reduces_total |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Add_overflow_throwsOverflowException` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_add_overflow_raises_overflow_error |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Add_twoAmounts_returnsSum` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_add_two_amounts_returns_sum |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `AnnualToMonthly_exactMultipleOfTwelve_isExact` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_annual_to_monthly_exact_multiple_of_twelve_is_exact |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `AnnualToMonthly_maxValue_doesNotOverflow` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_annual_to_monthly_max_value_does_not_overflow |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `AnnualToMonthly_minValue_doesNotOverflow` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_annual_to_monthly_min_value_does_not_overflow |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `CompareTo_smallerAndLarger_ordersByValue` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_compare_smaller_and_larger_orders_by_value |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `ComparisonOperators_variousPairs_followValueOrder` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_comparison_operators_various_pairs_follow_value_order |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Comparison_equalAmounts_areNotStrictlyLessOrGreater` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_comparison_equal_amounts_are_not_strictly_less_or_greater |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Equals_sameValue_isEqual` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_equals_same_value_is_equal |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Multiply_byWholeNumber_returnsProduct` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_multiply_by_whole_number_returns_product |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Multiply_overflow_throwsOverflowException` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_multiply_overflow_raises_overflow_error |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_minValue_throwsOverflowException` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_negate_min_value_raises_overflow_error |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_negative_returnsPositive` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_negate_negative_returns_positive |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_positive_returnsNegative` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_negate_positive_returns_negative |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Negate_zero_returnsZero` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_negate_zero_returns_zero |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Round_amountTooLargeForLong_throwsOverflowException` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_from_exact_amount_too_large_raises_overflow_error |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Round_halfPenny_isNotBankersRounding` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_from_exact_half_penny_is_not_bankers_rounding |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Round_wholeNumber_isUnchanged` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_from_exact_whole_number_is_unchanged |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Subtract_methodForm_matchesOperator` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_subtract_method_form_matches_operator |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Subtract_overflow_throwsOverflowException` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_subtract_overflow_raises_overflow_error |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Subtract_twoAmounts_returnsDifference` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_subtract_two_amounts_returns_difference |
| P2 | Vestagraph.CostEngine.Tests | PenceTests | `Zero_default_equalsNewPenceOfZero` |  | packages/vestagraph-engine/tests/test_engine_pence.py::test_zero_default_equals_pence_of_zero |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ErrorCategory_definedValues_areExactlyTheFourDecided` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_error_category_defined_values_are_exactly_the_four_decided |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_blankCode_throwsArgumentException` | 2 | packages/vestagraph-engine/tests/test_engine_result.py::test_error_blank_code_raises_value_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_blankMessage_throwsArgumentException` | 2 | packages/vestagraph-engine/tests/test_engine_result.py::test_error_blank_message_raises_value_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_created_keepsCodeAndMessage` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_error_created_keeps_code_and_message |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_eachCategory_isKeptOnTheError` | 4 | packages/vestagraph-engine/tests/test_engine_result.py::test_error_each_category_is_kept_on_the_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_sameParts_areEqual` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_error_same_parts_are_equal |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Error_undefinedCategory_throwsArgumentOutOfRangeException` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_error_non_category_raises_type_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `FailureOfT_nullError_throwsArgumentNullException` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_failure_non_error_raises_type_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `FailureOfT_withError_hidesValueAndExposesError` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_failure_of_t_with_error_hides_value_and_exposes_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Failure_nullError_throwsArgumentNullException` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_failure_non_error_raises_type_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Failure_withError_isFailureCarryingThatError` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_failure_with_error_is_failure_carrying_that_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `SuccessOfT_nullValue_throwsArgumentNullException` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_success_none_value_raises_value_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `SuccessOfT_withValue_exposesValue` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_success_with_value_exposes_value |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `Success_noValue_isSuccessWithNoError` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_ok_no_value_is_success_with_no_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ToResult_failure_keepsError` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_to_result_failure_keeps_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ToResult_failure_keepsTheError` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_to_result_failure_keeps_error |
| P2 | Vestagraph.CostEngine.Tests | ResultTests | `ToResult_successWithAValue_isASuccess` |  | packages/vestagraph-engine/tests/test_engine_result.py::test_to_result_success_with_a_value_is_a_success |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `BoundaryFile_loaded_hasAllSixRatioCases` |  | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_boundary_file_loaded_has_all_six_direct_rounding_cases |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_boundaryCaseFromFile_matchesWorkedResult` |  | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_largeExactHalf_roundsAwayFromZeroWithoutLosingPrecision` |  | packages/vestagraph-engine/tests/test_engine_round_ratio.py::test_round_ratio_large_exact_half_rounds_away_from_zero_without_losing_precision |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_resultTooBigForALong_throwsOverflow` |  | packages/vestagraph-engine/tests/test_engine_round_ratio.py::test_round_ratio_result_too_big_for_64_bit_raises_overflow |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_resultTooSmallForALong_throwsOverflow` |  | packages/vestagraph-engine/tests/test_engine_round_ratio.py::test_round_ratio_result_too_small_for_64_bit_raises_overflow |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_signsAndHalves_roundAwayFromZero` | 10 | packages/vestagraph-engine/tests/test_engine_round_ratio.py::test_round_ratio_signs_and_halves_round_away_from_zero |
| P2 | Vestagraph.CostEngine.Tests | RoundRatioTests | `RoundRatio_zeroDenominator_throwsDivideByZero` |  | packages/vestagraph-engine/tests/test_engine_round_ratio.py::test_round_ratio_zero_denominator_raises_zero_division |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `AnnualToMonthly_boundaryCaseFromFile_matchesWorkedResult` |  | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_annual_to_monthly_boundary_case_from_file_matches_worked_result |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `BoundaryFile_loaded_hasAllSixDirectRoundingCases` |  | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_boundary_file_loaded_has_all_six_direct_rounding_cases |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `BoundaryFile_loaded_hasTheAnnualToMonthlyCases` |  | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_boundary_file_loaded_has_the_annual_to_monthly_cases |
| P2 | Vestagraph.CostEngine.Tests | RoundingBoundaryTests | `Round_boundaryCaseFromFile_matchesWorkedResult` |  | packages/vestagraph-engine/tests/test_engine_boundaries.py::test_round_ratio_boundary_case_from_file_matches_worked_result |
| P3a | Vestagraph.CostEngine.Tests | BudgetBeatTests | `BudgetBeat_file_hasOneBudgetBeatCase` |  | packages/vestagraph-engine/tests/test_engine_budget_beat.py::test_budget_beat_file_has_one_budget_beat_case |
| P3a | Vestagraph.CostEngine.Tests | BudgetBeatTests | `BudgetBeat_storyCase_landsAsWorked` |  | packages/vestagraph-engine/tests/test_engine_budget_beat.py::test_budget_beat_story_case_lands_as_worked |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_aNonCalculatedLineNeverCarriesPence` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_cost_any_lines_a_non_calculated_line_never_carries_pence |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_budgetDifferenceIsBudgetMinusTotalAndWithinMeansAtOrBelow` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_cost_any_lines_budget_difference_is_budget_minus_total |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_isPartialExactlyWhenALineIsNotCalculatedConflictingOrMissing` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_cost_any_lines_is_partial_exactly_when_a_line_has_no_amount |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_noLineOrTotalIsNegative` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_cost_any_lines_no_line_or_total_is_negative |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_anyLines_totalEqualsTheSumOfTheCalculatedLines` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_cost_any_lines_total_equals_the_sum_of_the_calculated_lines |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyCost_higherRent_neverLowersTheTotal` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_cost_higher_rent_never_lowers_the_total |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyRepayment_anyValidInput_isNeverNegative` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_repayment_any_valid_input_is_never_negative |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyRepayment_higherRate_neverLowersTheRepayment` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_repayment_higher_rate_never_lowers_the_repayment |
| P3a | Vestagraph.CostEngine.Tests | CalculationProperties | `MonthlyRepayment_largerLoan_neverLowersTheRepayment` |  | packages/vestagraph-engine/tests/test_engine_calculation_properties.py::test_monthly_repayment_larger_loan_never_lowers_the_repayment |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `CostCategories_missingStatus_isNamedMissing` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_cost_categories_missing_status_is_named_missing |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `CostCategories_undefinedValues_throw` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_cost_categories_undefined_values_raise_type_error |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCases_file_hasTheSevenWorkedMonthlyCases` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cases_file_has_the_seven_worked_monthly_cases |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_amountNotPositive_failsAsNotPositive` | 2 | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_amount_not_positive_fails_as_not_positive |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_anchorLineThatIsNotAnAmount_failsAsMissing` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_anchor_line_that_is_not_an_amount_fails_as_missing |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_billGivenOnce_failsAsWrongPeriod` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_bill_given_once_fails_as_wrong_period |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_budgetNotPositive_failsAsNotPositive` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_budget_not_positive_fails_as_not_positive |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_includedLine_doesNotMakeTheTotalPartial` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_included_line_does_not_make_the_total_partial |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_lineThatDoesNotBelongToTheMode_failsAsNotForMode` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_line_that_does_not_belong_to_the_mode_fails_as_not_for_mode |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_linesGivenOutOfOrder_comeBackInTheFixedBuyOrder` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_lines_given_out_of_order_come_back_in_the_fixed_buy_order |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_linesGivenOutOfOrder_comeBackInTheFixedRentOrder` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_lines_given_out_of_order_come_back_in_the_fixed_rent_order |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_missingLine_makesTheTotalPartialWithACodedReason` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_missing_line_makes_the_total_partial_with_a_coded_reason |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_noAnchorLine_failsAsMissing` | 2 | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_no_anchor_line_fails_as_missing |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_nonCalculatedLines_haveNoAmountAndNoSourcePeriod` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_non_calculated_lines_have_no_amount_and_no_source_period |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_nullLineInTheList_throws` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_none_in_the_list_of_lines_raises_type_error |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_nullLines_throws` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_non_sequence_lines_raises_type_error |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_rentGivenYearly_failsAsWrongPeriod` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_rent_given_yearly_fails_as_wrong_period |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_sameCategoryTwice_failsAsAmbiguous` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_same_category_twice_fails_as_ambiguous |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_storyCase_matchesWorkedResult` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_story_case_matches_worked_result |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_tinyYearlyAmount_roundsToZeroButStaysCalculated` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_tiny_yearly_amount_rounds_to_zero_but_stays_calculated |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_totalExactlyEqualToBudget_isWithinBudget` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_total_exactly_equal_to_budget_is_within_budget |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_totalOnePennyOverBudget_isNotWithinBudget` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_total_one_penny_over_budget_is_not_within_budget |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_totalTooBigForALong_throwsOverflow` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_total_too_big_for_64_bits_raises_overflow |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_undefinedMode_throws` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_undefined_mode_raises_type_error |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_unknownKindOfLine_throwsForThatLine` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_unknown_kind_of_line_raises_type_error |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_upfrontCategoryInAMonthlyList_failsAsNotForMode` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_upfront_category_in_a_monthly_list_fails_as_not_for_mode |
| P3a | Vestagraph.CostEngine.Tests | MonthlyCostTests | `MonthlyCost_yearlyLine_keepsItsSourcePeriodAndEvidence` |  | packages/vestagraph-engine/tests/test_engine_monthly_cost.py::test_monthly_cost_yearly_line_keeps_its_source_period_and_evidence |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `BasisPoints_rateThatIsNotWholeBasisPoints_failsTheTest` |  | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_basis_points_rate_that_is_not_whole_basis_points_fails_the_test |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_invalidInput_failsWithTheCode` | 6 | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_invalid_input_fails_with_the_code |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_storyCase_matchesWorkedResult` |  | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_story_case_matches_worked_result |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_termOf100Years_isCalculated` |  | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_term_of_100_years_is_calculated |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_termOver100Years_failsAsTooLong` | 3 | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_term_over_100_years_fails_as_too_long |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MonthlyRepayment_veryLargeLoan_neverGivesAWrongSuccess` | 3 | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_monthly_repayment_very_large_loan_never_gives_a_wrong_success |
| P3a | Vestagraph.CostEngine.Tests | MortgageTests | `MortgageCases_file_hasTheFourWorkedMortgageCases` |  | packages/vestagraph-engine/tests/test_engine_mortgage.py::test_mortgage_cases_file_has_the_four_worked_mortgage_cases |
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
