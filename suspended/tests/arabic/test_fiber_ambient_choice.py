"""شهودٌ على أنّ المحيطَ اختيار، وأنّ الثغرةَ تُقاضى فردًا لا تُعَدّ جملةً."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import fiber_ambient_choice as ambient_module
from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.decomposition_reconstruction_theorem import (
    MeasurementInstrument,
    Population,
)
from alghanem.arabic.fiber_ambient_choice import (
    FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS,
    AmbientChoiceError,
    ClosureOperator,
    GapAdjudication,
    GapCensus,
    GapStatus,
    adjudicate_gaps,
    build_ambient,
    compare_closure_operators,
    gap_counts_by_operator,
    the_empty_fiber_is_refused_live,
)
from alghanem.arabic.fiber_rank_function import observed_fibers
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

# --- الحدودُ البنيويّة ------------------------------------------------------------


def test_the_ambient_choice_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(ambient_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="fiber-ambient-choice",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_there_are_seven_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS) == 7
    assert len(set(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)) == 7
    assert all(note.strip() for note in FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)


def test_no_refinement_or_split_operation_is_exported_here() -> None:
    exported = [
        name
        for name in ambient_module.__all__
        if callable(getattr(ambient_module, name))
        and ("refine" in name.lower() or "split" in name.lower())
    ]
    assert exported == []
    assert not hasattr(ambient_module, "RefineSlot")


# --- المحيطُ اختيارٌ لا قياس -------------------------------------------------


def test_five_named_closure_operators_are_offered_and_no_more() -> None:
    assert len(ClosureOperator) == 5


def test_an_ambient_refuses_to_be_built_without_a_named_operator() -> None:
    with pytest.raises(AmbientChoiceError):
        build_ambient("∪∩")  # type: ignore[arg-type]


def test_the_five_closures_yield_four_distinct_ambient_sizes() -> None:
    sizes = {
        measurement.operator: measurement.size
        for measurement in compare_closure_operators()
    }
    assert sizes[ClosureOperator.OBSERVED_ONLY] == 16
    assert sizes[ClosureOperator.DOWNWARD] == 75
    assert sizes[ClosureOperator.UNION_INTERSECTION] == 96
    assert sizes[ClosureOperator.UNION_INTERSECTION_DIFFERENCE] == 128
    assert sizes[ClosureOperator.POWER_SET] == 128


def test_closing_under_difference_is_not_closing_under_union_and_intersection() -> None:
    union_intersection = set(build_ambient(ClosureOperator.UNION_INTERSECTION))
    with_difference = set(build_ambient(ClosureOperator.UNION_INTERSECTION_DIFFERENCE))
    assert union_intersection < with_difference
    assert len(with_difference - union_intersection) == 32


def test_the_union_intersection_closure_contains_the_empty_fiber() -> None:
    members = build_ambient(ClosureOperator.UNION_INTERSECTION)
    assert frozenset() in members


def test_every_closure_keeps_all_sixteen_observed_fibers() -> None:
    distinct = set(observed_fibers().values())
    assert len(distinct) == 16
    for measurement in compare_closure_operators():
        assert measurement.observed_member_count == 16


def test_the_verdict_survives_every_closure_that_exceeds_the_observed() -> None:
    for measurement in compare_closure_operators():
        if measurement.operator is ClosureOperator.OBSERVED_ONLY:
            assert not measurement.a_rank_function_exists
            assert measurement.free_constants == 2
        else:
            assert measurement.a_rank_function_exists
            assert measurement.free_constants == 1


def test_the_observed_population_alone_is_neither_graded_nor_connected() -> None:
    (observed,) = (
        measurement
        for measurement in compare_closure_operators()
        if measurement.operator is ClosureOperator.OBSERVED_ONLY
    )
    assert observed.is_graded is False
    assert observed.component_count == 2
    assert observed.cover_count == 20


def test_the_power_set_and_the_difference_closure_agree_member_for_member() -> None:
    assert set(build_ambient(ClosureOperator.POWER_SET)) == set(
        build_ambient(ClosureOperator.UNION_INTERSECTION_DIFFERENCE)
    )


def test_an_ambient_measurement_refuses_counts_that_do_not_sum() -> None:
    with pytest.raises(AmbientChoiceError):
        ambient_module.AmbientLatticeMeasurement(
            operator=ClosureOperator.UNION_INTERSECTION,
            size=96,
            cover_count=304,
            is_graded=True,
            component_count=1,
            gap_count=79,
            observed_member_count=16,
        )


# --- عددُ الثغرات نسبيٌّ بالعمليّة ---------------------------------------------


def test_the_gap_count_is_four_different_numbers_not_one() -> None:
    counts = gap_counts_by_operator()
    assert counts[ClosureOperator.OBSERVED_ONLY] == 0
    assert counts[ClosureOperator.DOWNWARD] == 59
    assert counts[ClosureOperator.UNION_INTERSECTION] == 80
    assert counts[ClosureOperator.UNION_INTERSECTION_DIFFERENCE] == 112
    assert counts[ClosureOperator.POWER_SET] == 112


def test_the_residuals_name_the_operator_relativity_of_the_gap_count() -> None:
    joined = "\n".join(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)
    assert "TheGapCountIsOperatorRelative" in joined
    assert "TheAmbientIsAChoiceNotAMeasurement" in joined


# --- مقاضاةُ الثغرات ----------------------------------------------------------


def test_the_empty_fiber_bar_is_verified_live_not_asserted() -> None:
    assert the_empty_fiber_is_refused_live() is True


def test_exactly_one_gap_is_barred_by_the_representation_contract() -> None:
    for operator in ClosureOperator:
        census = adjudicate_gaps(operator)
        barred = census.barred
        if operator is ClosureOperator.OBSERVED_ONLY:
            assert barred == ()
            continue
        assert len(barred) == 1
        assert barred[0].states == frozenset()


def test_the_union_intersection_census_splits_one_and_forty_one_and_thirty_eight() -> (
    None
):
    census = adjudicate_gaps(ClosureOperator.UNION_INTERSECTION)
    assert len(census.adjudications) == 80
    assert census.count_of(GapStatus.BARRED_BY_THE_CURRENT_REPRESENTATION_CONTRACT) == 1
    assert census.count_of(GapStatus.AN_AMBIENT_MEMBER_JOINTLY_ATTESTED) == 41
    assert census.count_of(GapStatus.NOT_JOINTLY_ATTESTED_UNDECIDED) == 38


def test_the_power_set_census_splits_one_and_fifty_eight_and_fifty_three() -> None:
    census = adjudicate_gaps(ClosureOperator.POWER_SET)
    assert len(census.adjudications) == 112
    assert census.count_of(GapStatus.BARRED_BY_THE_CURRENT_REPRESENTATION_CONTRACT) == 1
    assert census.count_of(GapStatus.AN_AMBIENT_MEMBER_JOINTLY_ATTESTED) == 58
    assert census.count_of(GapStatus.NOT_JOINTLY_ATTESTED_UNDECIDED) == 53


def test_the_downward_closure_leaves_no_gap_undecided() -> None:
    census = adjudicate_gaps(ClosureOperator.DOWNWARD)
    assert census.count_of(GapStatus.NOT_JOINTLY_ATTESTED_UNDECIDED) == 0
    assert census.count_of(GapStatus.AN_AMBIENT_MEMBER_JOINTLY_ATTESTED) == 58


def test_every_census_count_sums_to_the_gap_count_of_its_operator() -> None:
    counts = gap_counts_by_operator()
    for operator in ClosureOperator:
        census = adjudicate_gaps(operator)
        assert sum(census.count_of(status) for status in GapStatus) == counts[operator]


def test_every_attested_gap_names_a_carrier_that_really_contains_it() -> None:
    fibers = observed_fibers()
    census = adjudicate_gaps(ClosureOperator.POWER_SET)
    attested = [
        item
        for item in census.adjudications
        if item.status is GapStatus.AN_AMBIENT_MEMBER_JOINTLY_ATTESTED
    ]
    assert attested
    for item in attested:
        assert item.witness_carrier is not None
        assert item.states <= fibers[item.witness_carrier]
        assert item.size == len(item.states)


def test_an_attested_adjudication_without_a_witness_is_refused() -> None:
    with pytest.raises(AmbientChoiceError):
        GapAdjudication(
            states=frozenset({("a", "b")}),
            status=GapStatus.AN_AMBIENT_MEMBER_JOINTLY_ATTESTED,
            witness_carrier=None,
            grounds="اجتماعٌ مُدَّعًى",
        )


def test_an_undecided_adjudication_may_not_name_a_witness() -> None:
    with pytest.raises(AmbientChoiceError):
        GapAdjudication(
            states=frozenset({("a", "b")}),
            status=GapStatus.NOT_JOINTLY_ATTESTED_UNDECIDED,
            witness_carrier="ل",
            grounds="غيابٌ مع شاهد",
        )


def test_an_adjudication_refuses_a_blank_ground() -> None:
    with pytest.raises(AmbientChoiceError):
        GapAdjudication(
            states=frozenset(),
            status=GapStatus.BARRED_BY_THE_CURRENT_REPRESENTATION_CONTRACT,
            witness_carrier=None,
            grounds="   ",
        )


def test_the_undecided_gaps_are_not_read_as_structurally_barred() -> None:
    census = adjudicate_gaps(ClosureOperator.UNION_INTERSECTION)
    undecided = [
        item
        for item in census.adjudications
        if item.status is GapStatus.NOT_JOINTLY_ATTESTED_UNDECIDED
    ]
    assert undecided
    assert all(
        item.status is not GapStatus.BARRED_BY_THE_CURRENT_REPRESENTATION_CONTRACT
        for item in undecided
    )
    joined = "\n".join(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)
    assert "AnUndecidedGapIsNotABarredOne" in joined


def test_the_empty_gap_bar_is_named_a_representation_contract_not_an_absolute() -> None:
    census = adjudicate_gaps(ClosureOperator.UNION_INTERSECTION)
    (barred,) = census.barred
    assert "عقد التمثيل" in barred.grounds
    assert "بديل" in barred.grounds
    joined = "\n".join(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)
    assert "OnlyOneGapIsBarredByTheCurrentRepresentationContract" in joined


def test_an_attested_ambient_member_is_not_a_licensed_arabic_fiber() -> None:
    census = adjudicate_gaps(ClosureOperator.UNION_INTERSECTION)
    attested = [
        item
        for item in census.adjudications
        if item.status is GapStatus.AN_AMBIENT_MEMBER_JOINTLY_ATTESTED
    ]
    assert attested
    assert all(item.is_a_licensed_arabic_fiber is False for item in attested)
    assert all(
        ClosureOperator.UNION_INTERSECTION.value in item.grounds for item in attested
    )
    joined = "\n".join(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)
    assert "AnAmbientMemberIsNotALicensedFiber" in joined


def test_individual_attestation_is_recorded_as_a_refused_criterion() -> None:
    census = adjudicate_gaps(ClosureOperator.POWER_SET)
    assert census.every_state_is_individually_attested is True
    joined = "\n".join(FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS)
    assert "IndividualAttestationIsNotJointAttestation" in joined
    assert "AttestationIsNotACorpusConstruction" in joined


# --- فصلُ الجمهور والآلة ------------------------------------------------------


def test_a_census_refuses_the_declared_population_label() -> None:
    with pytest.raises(AmbientChoiceError):
        GapCensus(
            operator=ClosureOperator.UNION_INTERSECTION,
            population=Population.DECLARED,
            instrument=MeasurementInstrument.OBSERVED_FIBER,
            ambient_size=96,
            adjudications=(),
        )


def test_a_census_refuses_to_be_attributed_to_the_codec_instrument() -> None:
    with pytest.raises(AmbientChoiceError):
        GapCensus(
            operator=ClosureOperator.UNION_INTERSECTION,
            population=Population.OBSERVED,
            instrument=MeasurementInstrument.CODEC_UNIT,
            ambient_size=96,
            adjudications=(),
        )


def test_the_census_carries_the_observed_population_and_fiber_instrument() -> None:
    census = adjudicate_gaps()
    assert census.population is Population.OBSERVED
    assert census.instrument is MeasurementInstrument.OBSERVED_FIBER
    assert census.operator is ClosureOperator.UNION_INTERSECTION


def test_the_numbers_are_derived_from_the_deposited_table_not_written_beside_it() -> (
    None
):
    table = run_observed_fiber_on_the_deposited_fatiha()
    assert len(build_ambient(ClosureOperator.OBSERVED_ONLY, table)) == 16
    assert gap_counts_by_operator(table)[ClosureOperator.UNION_INTERSECTION] == 80
