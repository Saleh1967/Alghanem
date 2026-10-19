"""شواهدُ «حيادِ الألف»: ما انعقد قياسًا، وما اختير قرارًا، وما انتقض."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from alghanem.arabic import alif_neutrality as module
from alghanem.arabic.alif_neutrality import (
    ALIF,
    ALIF_NEUTRALITY_NAMED_RESIDUALS,
    THE_CLAIM,
    AlifClaimReading,
    AlifNeutralityError,
    AlifVerdict,
    CarrierConstancy,
    NeutralityReading,
    identity_state,
    measure_constancies,
    measure_rectangle_fill,
    read_the_alif_claim,
)
from alghanem.arabic.carrier_state_observed_fiber import (
    ABSENT,
    ObservedFiberTable,
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


@pytest.fixture(scope="module")
def table() -> ObservedFiberTable:
    return run_observed_fiber_on_the_deposited_fatiha()


@pytest.fixture(scope="module")
def constancies(table: ObservedFiberTable) -> tuple[CarrierConstancy, ...]:
    return measure_constancies(table)


@pytest.fixture(scope="module")
def readings(table: ObservedFiberTable) -> tuple[NeutralityReading, ...]:
    return read_the_alif_claim(table)


def _reading(
    readings: tuple[NeutralityReading, ...], which: AlifClaimReading
) -> NeutralityReading:
    return next(item for item in readings if item.reading is which)


def _constancy(
    constancies: tuple[CarrierConstancy, ...], carrier: str
) -> CarrierConstancy:
    return next(item for item in constancies if item.carrier == carrier)


def test_the_claim_is_stated_before_it_is_divided() -> None:
    assert "محايدٌ للعملية" in THE_CLAIM


def test_every_reading_is_read_and_none_is_dropped(
    readings: tuple[NeutralityReading, ...],
) -> None:
    assert {item.reading for item in readings} == set(AlifClaimReading)


def test_the_readings_do_not_share_one_verdict(
    readings: tuple[NeutralityReading, ...],
) -> None:
    assert len({item.verdict for item in readings}) == len(AlifVerdict)


# --- المحايد ----------------------------------------------------------------------


def test_the_identity_is_absence_on_every_measured_axis(
    table: ObservedFiberTable,
) -> None:
    identity = identity_state(table)
    assert set(identity) == {ABSENT}
    assert len(identity) == len(table.rows[0].state_vector)


def test_alif_is_constant_and_sits_exactly_on_the_identity(
    table: ObservedFiberTable, constancies: tuple[CarrierConstancy, ...]
) -> None:
    alif = _constancy(constancies, ALIF)
    assert alif.is_constant
    assert alif.sole_state == identity_state(table)


def test_alif_is_the_only_carrier_resting_on_the_identity(
    table: ObservedFiberTable, constancies: tuple[CarrierConstancy, ...]
) -> None:
    identity = identity_state(table)
    resting = [item.carrier for item in constancies if item.sole_state == identity]
    assert resting == [ALIF]


# --- الثبات مقيسًا ضدّ الشُّح -------------------------------------------------------


def test_alif_is_not_the_only_carrier_with_capacity_one(
    constancies: tuple[CarrierConstancy, ...],
) -> None:
    assert len([item for item in constancies if item.is_constant]) > 1


def test_only_alif_survives_the_scarcity_control(
    constancies: tuple[CarrierConstancy, ...],
) -> None:
    survivors = [
        item.carrier for item in constancies if item.survives_the_scarcity_control
    ]
    assert survivors == [ALIF]


def test_alifs_constancy_exponent_is_orders_beyond_its_nearest_rival(
    constancies: tuple[CarrierConstancy, ...],
) -> None:
    alif = _constancy(constancies, ALIF)
    rivals = [
        item.constancy_exponent
        for item in constancies
        if item.is_constant and item.carrier != ALIF
    ]
    assert alif.constancy_exponent < min(rivals) / Fraction(10**10)


def test_alif_rests_on_many_occurrences_not_on_scarcity(
    constancies: tuple[CarrierConstancy, ...],
) -> None:
    alif = _constancy(constancies, ALIF)
    others = [
        item.occurrences
        for item in constancies
        if item.is_constant and item.carrier != ALIF
    ]
    assert alif.occurrences > max(others)


def test_the_background_excludes_the_carrier_being_controlled(
    table: ObservedFiberTable, constancies: tuple[CarrierConstancy, ...]
) -> None:
    alif = _constancy(constancies, ALIF)
    identity = identity_state(table)
    pooled = Fraction(
        sum(
            1
            for row in table.rows
            if tuple(value for _axis, value in row.state_vector) == identity
        ),
        len(table.rows),
    )
    assert alif.background_share != pooled


def test_a_varying_carrier_carries_no_sole_state(
    constancies: tuple[CarrierConstancy, ...],
) -> None:
    varying = [item for item in constancies if not item.is_constant]
    assert varying
    assert all(item.sole_state is None for item in varying)


def test_a_sole_state_without_capacity_one_is_refused() -> None:
    with pytest.raises(AlifNeutralityError, match="السَّعةِ الواحدة"):
        CarrierConstancy(
            carrier="ب",
            occurrences=4,
            capacity=3,
            sole_state=(ABSENT,),
            background_share=Fraction(0),
            constancy_exponent=Fraction(1),
        )


def test_capacity_one_without_a_sole_state_is_refused() -> None:
    with pytest.raises(AlifNeutralityError, match="السَّعةِ الواحدة"):
        CarrierConstancy(
            carrier="ب",
            occurrences=4,
            capacity=1,
            sole_state=None,
            background_share=Fraction(0),
            constancy_exponent=Fraction(1),
        )


# --- المستطيل ---------------------------------------------------------------------


def test_the_deposit_is_not_a_full_product(table: ObservedFiberTable) -> None:
    fill = measure_rectangle_fill(table)
    assert not fill.is_a_full_product
    assert fill.realized_pairs < fill.rectangle


def test_removing_alif_does_not_make_it_a_product(table: ObservedFiberTable) -> None:
    fill = measure_rectangle_fill(table, excluding=ALIF)
    assert not fill.is_a_full_product


def test_removing_alif_leaves_the_capacities_ragged(
    table: ObservedFiberTable,
) -> None:
    fill = measure_rectangle_fill(table, excluding=ALIF)
    assert min(fill.capacity_spread) < max(fill.capacity_spread)


def test_removing_alif_removes_exactly_one_carrier_and_one_pair(
    table: ObservedFiberTable,
) -> None:
    whole = measure_rectangle_fill(table)
    without = measure_rectangle_fill(table, excluding=ALIF)
    assert without.carriers == whole.carriers - 1
    assert without.realized_pairs == whole.realized_pairs - 1


def test_removing_alif_does_not_reduce_the_state_set(
    table: ObservedFiberTable,
) -> None:
    whole = measure_rectangle_fill(table)
    without = measure_rectangle_fill(table, excluding=ALIF)
    assert without.states == whole.states


def test_a_fill_exceeding_its_rectangle_is_refused() -> None:
    with pytest.raises(AlifNeutralityError, match="مُحال"):
        module.RectangleFill(
            carriers=2, states=2, realized_pairs=5, capacity_spread=(2, 3)
        )


def test_excluding_every_carrier_is_refused(table: ObservedFiberTable) -> None:
    only_alif = replace(
        table, rows=tuple(row for row in table.rows if row.carrier == ALIF)
    )
    with pytest.raises(AlifNeutralityError, match="لا يُقاس على خلاء"):
        measure_rectangle_fill(only_alif, excluding=ALIF)


# --- الأحكام ----------------------------------------------------------------------


def test_accepting_one_combination_is_held_by_measurement(
    readings: tuple[NeutralityReading, ...],
) -> None:
    item = _reading(readings, AlifClaimReading.ALIF_ACCEPTS_ONE_COMBINATION)
    assert item.verdict is AlifVerdict.HELD_BY_MEASUREMENT


def test_resting_on_the_identity_is_held_by_measurement(
    readings: tuple[NeutralityReading, ...],
) -> None:
    item = _reading(readings, AlifClaimReading.THAT_COMBINATION_IS_THE_IDENTITY)
    assert item.verdict is AlifVerdict.HELD_BY_MEASUREMENT


def test_exclusion_from_C_is_a_choice_not_a_measurement(
    readings: tuple[NeutralityReading, ...],
) -> None:
    item = _reading(readings, AlifClaimReading.ALIF_IS_NOT_AN_ELEMENT_OF_C)
    assert item.verdict is AlifVerdict.ADMISSIBLE_BUT_CHOSEN
    assert "قرارُ نمذجة" in item.what_decided_it
    assert any("الإخراجُ مختار" in note for note in item.residuals)


def test_the_product_restoration_claim_is_refuted(
    readings: tuple[NeutralityReading, ...],
) -> None:
    item = _reading(readings, AlifClaimReading.REMOVING_ALIF_RESTORES_THE_PRODUCT)
    assert item.verdict is AlifVerdict.REFUTED


def test_the_deferred_madd_axis_is_named_as_the_rival_explanation(
    readings: tuple[NeutralityReading, ...],
) -> None:
    item = _reading(readings, AlifClaimReading.THAT_COMBINATION_IS_THE_IDENTITY)
    assert any("محورُ المدّ" in note for note in item.residuals)


def test_a_reading_without_a_written_reason_is_refused() -> None:
    with pytest.raises(AlifNeutralityError, match="سببٍ مكتوب"):
        NeutralityReading(
            reading=AlifClaimReading.ALIF_ACCEPTS_ONE_COMBINATION,
            verdict=AlifVerdict.REFUTED,
            what_decided_it="  ",
            residuals=("بقيّة",),
        )


def test_a_reading_without_a_named_residual_is_refused() -> None:
    with pytest.raises(AlifNeutralityError, match="بلا بقيّةٍ مُسمّاة"):
        NeutralityReading(
            reading=AlifClaimReading.ALIF_ACCEPTS_ONE_COMBINATION,
            verdict=AlifVerdict.REFUTED,
            what_decided_it="سبب",
            residuals=(),
        )


def test_a_varying_alif_would_raise_the_claim_not_fold_it(
    table: ObservedFiberTable,
) -> None:
    without_alif = replace(
        table, rows=tuple(row for row in table.rows if row.carrier != ALIF)
    )
    with pytest.raises(AlifNeutralityError, match="لا ألفَ في الإيداع"):
        read_the_alif_claim(without_alif)


def test_a_table_without_rows_has_no_identity() -> None:
    with pytest.raises(AlifNeutralityError, match="لا يُقاس على خلاء"):
        identity_state(replace(run_observed_fiber_on_the_deposited_fatiha(), rows=()))


# --- البقايا والحدود ---------------------------------------------------------------


def test_the_named_residuals_are_all_present() -> None:
    assert len(ALIF_NEUTRALITY_NAMED_RESIDUALS) == 5
    assert all(note.strip() for note in ALIF_NEUTRALITY_NAMED_RESIDUALS)


def test_the_artifact_residual_is_named() -> None:
    assert any(
        "AlifsNeutralityMayBeAnArtifactOfTheDeferredMaddAxis" in note
        for note in ALIF_NEUTRALITY_NAMED_RESIDUALS
    )


def test_the_writing_only_ceiling_is_named() -> None:
    assert any(
        "ANeutralityHereIsANeutralityInWriting" in note
        for note in ALIF_NEUTRALITY_NAMED_RESIDUALS
    )


def test_this_reading_reaches_no_kernel_module() -> None:
    source = Path(str(module.__file__))
    report = audit_import_boundary(
        (source,),
        ImportBoundaryPolicy(
            policy_id="alif-neutrality-reaches-no-kernel",
            permitted_modules=("alghanem.arabic",),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]
