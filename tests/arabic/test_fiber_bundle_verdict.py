"""شهودٌ على الحزمة: التدريجُ عموديٌّ، والمقياسُ جمعيّ، والدعوى تبقى دعوى."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import fiber_bundle_verdict as bundle_module
from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.compression_model_preregistration import FROZEN_CORPUS
from alghanem.arabic.decomposition_reconstruction_theorem import (
    MeasurementInstrument,
    Population,
)
from alghanem.arabic.fiber_ambient_choice import ClosureOperator
from alghanem.arabic.fiber_bundle_verdict import (
    FIBER_BUNDLE_NAMED_RESIDUALS,
    WIDER_CORPUS_CLAIMS,
    Axis,
    BundleVerdict,
    FiberBundleError,
    PairStepVerdict,
    StepCensus,
    WiderCorpusClaim,
    additive_measure_holds,
    downward_closure_failures,
    measure_the_bundle,
    survey_step_counts,
    vertical_grading_census,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

# --- الحدودُ البنيويّة ------------------------------------------------------------


def test_the_bundle_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(bundle_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="fiber-bundle-verdict",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_there_are_seven_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(FIBER_BUNDLE_NAMED_RESIDUALS) == 7
    assert len(set(FIBER_BUNDLE_NAMED_RESIDUALS)) == 7
    assert all(note.strip() for note in FIBER_BUNDLE_NAMED_RESIDUALS)


def test_neither_a_refine_slot_nor_a_base_rank_operation_is_exported() -> None:
    exported = [
        name
        for name in bundle_module.__all__
        if callable(getattr(bundle_module, name))
        and ("refine" in name.lower() or "split" in name.lower())
    ]
    assert exported == []
    assert not hasattr(bundle_module, "RefineSlot")
    assert not hasattr(bundle_module, "FiberRank")


# --- عموديًّا: بلا استثناء -----------------------------------------------------


def test_every_observed_fiber_is_graded_with_zero_exceptions() -> None:
    graded, total = vertical_grading_census()
    assert (graded, total) == (23, 23)


def test_the_bundle_carries_the_deposited_shape() -> None:
    verdict = measure_the_bundle()
    assert verdict.carrier_count == 23
    assert verdict.distinct_fiber_count == 16
    assert verdict.state_count == 7
    assert verdict.observed_depths == (1, 2, 3, 4, 6)


def test_the_rank_exists_vertically_and_fails_horizontally() -> None:
    verdict = measure_the_bundle()
    assert verdict.rank_exists_on(Axis.VERTICAL_WITHIN_A_FIBER) is True
    assert verdict.rank_exists_on(Axis.HORIZONTAL_ACROSS_THE_BASE) is False
    assert verdict.vertical_grading_is_exceptionless is True


def test_the_base_is_neither_graded_nor_connected() -> None:
    verdict = measure_the_bundle()
    assert verdict.base_is_graded is False
    assert verdict.base_component_count == 2


def test_the_fallen_base_rank_is_witnessed_by_chains_not_by_capacity_jumps() -> None:
    verdict = measure_the_bundle()
    assert verdict.base_grading_is_settled_by_chains is True
    assert len(verdict.base_grading_counterexamples) == 4
    lengths = {
        witness.chain_lengths for witness in verdict.base_grading_counterexamples
    }
    assert lengths == {(2, 3), (3, 4)}
    assert all(
        len(set(witness.chain_lengths)) > 1
        for witness in verdict.base_grading_counterexamples
    )


def test_the_capacity_jumps_are_recorded_beside_the_verdict_not_as_its_ground() -> None:
    verdict = measure_the_bundle()
    assert verdict.base_cover_capacity_jumps == 5
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "ACapacityJumpIsNotAFallenRank" in joined


def test_an_ungraded_base_without_a_chain_witness_is_refused() -> None:
    with pytest.raises(FiberBundleError):
        BundleVerdict(
            carrier_count=23,
            distinct_fiber_count=16,
            state_count=7,
            fibers_graded=23,
            base_is_graded=False,
            base_component_count=2,
            observed_depths=(1, 2, 3, 4, 6),
            base_grading_counterexamples=(),
            base_cover_capacity_jumps=5,
        )


def test_a_graded_base_carrying_a_counter_witness_is_refused() -> None:
    witness = measure_the_bundle().base_grading_counterexamples[0]
    with pytest.raises(FiberBundleError):
        BundleVerdict(
            carrier_count=23,
            distinct_fiber_count=16,
            state_count=7,
            fibers_graded=23,
            base_is_graded=True,
            base_component_count=2,
            observed_depths=(1, 2, 3, 4, 6),
            base_grading_counterexamples=(witness,),
            base_cover_capacity_jumps=0,
        )


def test_a_rank_question_without_a_named_axis_is_refused() -> None:
    verdict = measure_the_bundle()
    with pytest.raises(FiberBundleError):
        verdict.rank_exists_on("عموديًّا")  # type: ignore[arg-type]


def test_the_residuals_name_the_axis_confusion_that_produced_two_verdicts() -> None:
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "RankIsVerticalNotHorizontal" in joined


# --- المقياسُ الجمعيّ ---------------------------------------------------------


def test_the_additive_law_is_named_a_capacity_measure_not_a_linguistic_necessity() -> (
    None
):
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "مقياسُ سعةٍ" in joined


def test_the_measure_is_additive_with_zero_breaches_over_every_pair() -> None:
    pairs, breaches = additive_measure_holds()
    assert pairs == 96**2 == 9216
    assert breaches == 0


def test_the_additive_measure_survives_the_difference_closure_too() -> None:
    pairs, breaches = additive_measure_holds(
        ClosureOperator.UNION_INTERSECTION_DIFFERENCE
    )
    assert pairs == 128**2
    assert breaches == 0


def test_the_additive_measure_is_not_licensed_as_a_rank_function() -> None:
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "AnAdditiveMeasureIsNotARankFunction" in joined


# --- الخطوةُ والفرق -----------------------------------------------------------


def test_the_step_count_is_well_defined_for_most_pairs_and_ambiguous_for_four() -> None:
    census = survey_step_counts()
    assert census.comparable_pairs == 46
    assert census.well_defined_steps == 42
    assert census.ambiguous_steps == 4


def test_the_measure_difference_is_defined_for_every_comparable_pair() -> None:
    census = survey_step_counts()
    assert census.the_measure_difference_is_always_defined is True


def test_the_alif_to_lam_step_count_has_exactly_one_answer() -> None:
    census = survey_step_counts()
    (pair,) = (
        item
        for item in census.verdicts
        if item.lower_carrier == "ا" and item.upper_carrier == "ل"
    )
    assert pair.step_counts == (3,)
    assert pair.measure_difference == 5
    assert pair.step_count_is_well_defined is True


def test_the_sin_to_lam_step_count_has_two_answers() -> None:
    census = survey_step_counts()
    (pair,) = (
        item
        for item in census.verdicts
        if item.lower_carrier == "س" and item.upper_carrier == "ل"
    )
    assert pair.step_counts == (3, 4)
    assert pair.step_count_is_well_defined is False


def test_the_residual_refuses_the_claim_that_no_step_count_has_an_answer() -> None:
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "TheStepCountFailsGloballyNotPairwise" in joined


def test_a_comparable_pair_with_a_non_positive_difference_is_refused() -> None:
    with pytest.raises(FiberBundleError):
        PairStepVerdict(
            lower_carrier="ا",
            upper_carrier="ل",
            measure_difference=0,
            step_counts=(3,),
        )


def test_a_comparable_pair_with_no_chain_at_all_is_refused() -> None:
    with pytest.raises(FiberBundleError):
        PairStepVerdict(
            lower_carrier="ا",
            upper_carrier="ل",
            measure_difference=5,
            step_counts=(),
        )


# --- الإغلاقُ النزوليّ --------------------------------------------------------


def test_the_downward_closure_fails_for_ten_of_the_twenty_three_carriers() -> None:
    failures = downward_closure_failures()
    assert len(failures) == 10
    assert set(failures) == {"ب", "د", "ر", "ص", "ض", "ل", "م", "ن", "و", "ي"}


def test_a_downward_gap_is_recorded_as_a_possible_sampling_zero() -> None:
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "ADownwardGapMayBeASamplingZero" in joined
    assert not hasattr(bundle_module, "SamplingZero")


# --- دعاوى المدوّنة الأوسع ----------------------------------------------------


def test_every_wider_corpus_number_is_recorded_as_a_claim_not_a_measurement() -> None:
    assert len(WIDER_CORPUS_CLAIMS) == 8
    assert all(claim.is_a_measurement_here is False for claim in WIDER_CORPUS_CLAIMS)
    assert all(claim.why_not_derivable_here.strip() for claim in WIDER_CORPUS_CLAIMS)


def test_a_claim_without_a_written_reason_is_refused() -> None:
    with pytest.raises(FiberBundleError):
        WiderCorpusClaim(label="حجمُ القاعدة", value="36", why_not_derivable_here="  ")


def test_a_claim_without_a_value_is_refused() -> None:
    with pytest.raises(FiberBundleError):
        WiderCorpusClaim(label="حجمُ القاعدة", value="", why_not_derivable_here="غائبة")


def test_the_wider_corpus_is_fingerprinted_in_the_tree_after_all() -> None:
    assert len(FROZEN_CORPUS.sha256_hex) == 64
    assert FROZEN_CORPUS.sha256_hex.startswith("37633090")
    assert FROZEN_CORPUS.byte_length == 1_319_901
    assert "لا تطبيع" in FROZEN_CORPUS.normalization_policy
    joined = "\n".join(FIBER_BUNDLE_NAMED_RESIDUALS)
    assert "TheCorpusIsFingerprintedThoughItsBytesAreAbsent" in joined


def test_the_claims_carry_the_frozen_corpus_name_and_length() -> None:
    joined = "\n".join(claim.why_not_derivable_here for claim in WIDER_CORPUS_CLAIMS)
    assert FROZEN_CORPUS.source_name in joined
    assert str(FROZEN_CORPUS.byte_length) in joined


# --- فصلُ الجمهور والآلة ------------------------------------------------------


def test_a_step_census_refuses_the_declared_population_label() -> None:
    with pytest.raises(FiberBundleError):
        StepCensus(
            population=Population.DECLARED,
            instrument=MeasurementInstrument.OBSERVED_FIBER,
            verdicts=(),
        )


def test_a_step_census_refuses_to_be_attributed_to_the_codec() -> None:
    with pytest.raises(FiberBundleError):
        StepCensus(
            population=Population.OBSERVED,
            instrument=MeasurementInstrument.CODEC_UNIT,
            verdicts=(),
        )


def test_the_numbers_are_derived_from_the_deposited_table_not_written_beside_it() -> (
    None
):
    table = run_observed_fiber_on_the_deposited_fatiha()
    assert vertical_grading_census(table) == (23, 23)
    assert measure_the_bundle(table).distinct_fiber_count == 16
    assert len(downward_closure_failures(table)) == 10
