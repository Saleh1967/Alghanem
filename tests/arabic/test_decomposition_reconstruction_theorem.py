"""شهودٌ على مبرهنة التفكيك وإعادة البناء، وعلى فصل المفردتين والآلتين."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import decomposition_reconstruction_theorem as theorem
from alghanem.arabic.carrier_state_observed_fiber import (
    capacity_by_carrier,
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.decomposition_reconstruction_theorem import (
    DECOMPOSITION_THEOREM_NAMED_RESIDUALS,
    INSTRUMENT_DIVERGENCES,
    DeclaredPopulationCensus,
    InstrumentDivergence,
    MeasurementInstrument,
    ObservedPopulationCensus,
    Population,
    PopulationSubstitutionError,
    ReconstructionReport,
    ResidueField,
    census_of_declared_population,
    census_of_observed_population,
    decompose_with_residue,
    prove_decomposition_reconstructs,
    prove_the_residue_is_necessary,
    reconstruct,
)
from alghanem.arabic.encoding.carrier_state_candidate import (
    DECLARED_CARRIERS,
    CarrierState,
    CarrierStateCodec,
)
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

# --- الحدودُ البنيويّة ------------------------------------------------------------


def test_the_theorem_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(theorem.__file__)),),
        ImportBoundaryPolicy(
            policy_id="decomposition-reconstruction-theorem",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_the_theorem_module_does_not_reach_the_excluded_syllabifier() -> None:
    report = audit_import_boundary(
        (Path(str(theorem.__file__)),),
        ImportBoundaryPolicy(
            policy_id="decomposition-reconstruction-theorem-syllabifier",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert "alghanem.arabic.syllabifier" not in report.reached_modules


def test_there_are_six_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(DECOMPOSITION_THEOREM_NAMED_RESIDUALS) == 6
    assert len(set(DECOMPOSITION_THEOREM_NAMED_RESIDUALS)) == 6
    assert all(note.strip() for note in DECOMPOSITION_THEOREM_NAMED_RESIDUALS)


def test_the_residuals_refuse_a_cv_birth_and_an_unlicensed_refine_slot() -> None:
    joined = "\n".join(DECOMPOSITION_THEOREM_NAMED_RESIDUALS)
    assert "ThisIsNotACVBirthTheorem" in joined
    assert "RefineSlotIsUnlicensed" in joined


def test_no_refine_slot_operation_is_exported_yet() -> None:
    operations = [
        name
        for name in theorem.__all__
        if callable(getattr(theorem, name)) and "refine" in name.lower()
    ]
    assert operations == []
    assert not hasattr(theorem, "RefineSlot")


# --- فصلُ المفردتين ----------------------------------------------------------------


def test_the_two_populations_are_distinct_members() -> None:
    assert len({member.value for member in Population}) == 2


def test_an_observed_census_refuses_the_declared_label() -> None:
    with pytest.raises(PopulationSubstitutionError):
        ObservedPopulationCensus(
            population=Population.DECLARED,
            source_id="x",
            word_count=1,
            unit_count=1,
            distinct_carriers=1,
            observed_capacities=(1,),
        )


def test_a_declared_census_refuses_the_observed_label() -> None:
    with pytest.raises(PopulationSubstitutionError):
        DeclaredPopulationCensus(
            population=Population.OBSERVED, carrier_count=1, state_count=1
        )


def test_an_observed_census_refuses_more_carriers_than_the_declared_vocabulary() -> (
    None
):
    with pytest.raises(PopulationSubstitutionError):
        ObservedPopulationCensus(
            population=Population.OBSERVED,
            source_id="x",
            word_count=1,
            unit_count=1,
            distinct_carriers=len(DECLARED_CARRIERS) + 1,
            observed_capacities=(1,),
        )


def test_the_declared_product_is_an_upper_bound_not_an_occurrence_count() -> None:
    declared = census_of_declared_population()
    observed = census_of_observed_population()
    assert declared.carrier_count == len(DECLARED_CARRIERS)
    assert declared.state_count == len(CarrierState)
    assert declared.upper_bound == declared.carrier_count * declared.state_count
    assert observed.unit_count < declared.upper_bound


def test_the_declared_vocabulary_is_thirty_seven_not_twenty_seven() -> None:
    assert census_of_declared_population().carrier_count == 37


def test_the_observed_carrier_count_is_below_the_declared_one() -> None:
    observed = census_of_observed_population()
    assert observed.distinct_carriers < census_of_declared_population().carrier_count


def test_the_observed_census_is_measured_not_declared() -> None:
    small = census_of_observed_population(("بِسْمِ",), source_id="one-word")
    assert small.word_count == 1
    assert small.source_id == "one-word"
    assert small.distinct_carriers < census_of_observed_population().distinct_carriers


# --- فصلُ الآلتين ------------------------------------------------------------------


def test_the_two_instruments_are_distinct_members() -> None:
    assert len({member.value for member in MeasurementInstrument}) == 2


def test_the_observed_census_records_which_instrument_measured_it() -> None:
    assert (
        census_of_observed_population().instrument is MeasurementInstrument.CODEC_UNIT
    )


def test_a_divergence_refuses_a_blank_explanation() -> None:
    with pytest.raises(PopulationSubstitutionError):
        InstrumentDivergence(
            quantity="س", codec_value=1, fiber_value=2, why_they_differ="  "
        )


def test_a_divergence_refuses_to_record_an_agreement() -> None:
    with pytest.raises(PopulationSubstitutionError):
        InstrumentDivergence(
            quantity="س", codec_value=2, fiber_value=2, why_they_differ="علّة"
        )


def test_the_recorded_carrier_divergence_matches_both_live_instruments() -> None:
    recorded = next(d for d in INSTRUMENT_DIVERGENCES if "الحوامل" in d.quantity)
    fiber = run_observed_fiber_on_the_deposited_fatiha()
    assert recorded.fiber_value == len(fiber.carriers)
    assert recorded.codec_value == census_of_observed_population().distinct_carriers


def test_the_recorded_position_divergence_matches_both_live_instruments() -> None:
    recorded = next(d for d in INSTRUMENT_DIVERGENCES if "المواضع" in d.quantity)
    fiber = run_observed_fiber_on_the_deposited_fatiha()
    assert recorded.fiber_value == len(fiber.rows)
    assert recorded.codec_value == census_of_observed_population().unit_count


def test_the_recorded_capacity_divergence_matches_both_live_instruments() -> None:
    recorded = next(d for d in INSTRUMENT_DIVERGENCES if "سعة" in d.quantity)
    fiber = run_observed_fiber_on_the_deposited_fatiha()
    assert recorded.fiber_value == max(capacity_by_carrier(fiber).values())
    assert recorded.codec_value == max(
        census_of_observed_population().observed_capacities
    )


def test_the_instruments_disagree_on_the_hamza_seat_as_recorded() -> None:
    fiber = run_observed_fiber_on_the_deposited_fatiha()
    codec = CarrierStateCodec()
    seen = {
        unit.carrier
        for line in FATIHA_LINES
        for word in line.split()
        for unit in codec.generate(word)
    }
    assert {"أ", "إ"} <= set(fiber.carriers)
    assert not {"أ", "إ"} & seen
    assert "ء" in seen


def test_the_fiber_capacity_range_has_a_hole_so_one_to_six_overstates_it() -> None:
    fiber = run_observed_fiber_on_the_deposited_fatiha()
    capacities = sorted(set(capacity_by_carrier(fiber).values()))
    assert 5 not in capacities
    assert capacities != list(range(capacities[0], capacities[-1] + 1))


def test_a_contiguous_range_is_reported_as_contiguous() -> None:
    census = ObservedPopulationCensus(
        population=Population.OBSERVED,
        source_id="x",
        word_count=1,
        unit_count=1,
        distinct_carriers=1,
        observed_capacities=(1, 2, 3),
    )
    assert census.capacity_range_is_contiguous


def test_a_range_with_a_hole_is_reported_as_not_contiguous() -> None:
    census = ObservedPopulationCensus(
        population=Population.OBSERVED,
        source_id="x",
        word_count=1,
        unit_count=1,
        distinct_carriers=1,
        observed_capacities=(1, 2, 4),
    )
    assert not census.capacity_range_is_contiguous


# --- البقيّة ----------------------------------------------------------------------


def test_decomposition_pairs_every_element_with_a_residue() -> None:
    decomposition = decompose_with_residue("الرَّحْمَٰنِ")
    assert len(decomposition.elements) == len(decomposition.residue)
    assert [item.unit_index for item in decomposition.residue] == list(
        range(len(decomposition.residue))
    )


def test_a_decomposition_refuses_the_declared_population() -> None:
    decomposition = decompose_with_residue("بِسْمِ")
    with pytest.raises(PopulationSubstitutionError):
        theorem.WordDecomposition(
            surface=decomposition.surface,
            population=Population.DECLARED,
            elements=decomposition.elements,
            residue=decomposition.residue,
        )


def test_a_decomposition_refuses_a_residue_shorter_than_its_elements() -> None:
    decomposition = decompose_with_residue("بِسْمِ")
    with pytest.raises(PopulationSubstitutionError):
        theorem.WordDecomposition(
            surface=decomposition.surface,
            population=Population.OBSERVED,
            elements=decomposition.elements,
            residue=decomposition.residue[:-1],
        )


def test_the_sukun_kind_is_carried_by_the_residue_not_by_the_elements() -> None:
    decomposition = decompose_with_residue("بَحْ")
    kinds = {
        item.state
        for item in decomposition.residue
        if ResidueField.SUKUN_KIND in item.carried_fields
    }
    assert CarrierState.SUKUN_EXPLICIT in kinds


def test_the_structural_state_is_named_in_the_residue_of_the_dagger_word() -> None:
    decomposition = decompose_with_residue("الرَّحْمَٰنِ")
    assert any(
        ResidueField.STRUCTURAL_STATE in item.carried_fields
        for item in decomposition.residue
    )


def test_not_every_unit_leaves_a_residue_field() -> None:
    decomposition = decompose_with_residue("الرَّحْمَٰنِ")
    assert len(decomposition.residue_bearing_units) < len(decomposition.residue)
    assert decomposition.residue_bearing_units


def test_the_seat_is_carried_where_the_deposit_wrote_one() -> None:
    codec = CarrierStateCodec()
    seated = [
        word
        for line in FATIHA_LINES
        for word in line.split()
        if any(unit.seat is not None for unit in codec.generate(word))
    ]
    assert seated
    for word in seated:
        decomposition = decompose_with_residue(word, codec=codec)
        assert any(
            ResidueField.SEAT in item.carried_fields for item in decomposition.residue
        )


# --- المبرهنة ---------------------------------------------------------------------


def test_the_theorem_closes_exactly_on_the_named_deposit() -> None:
    report = prove_decomposition_reconstructs()
    assert report.word_count == 29
    assert report.exact_rebuilds == 29
    assert report.broken_words == ()
    assert report.closes


def test_the_theorem_rebuilds_every_word_character_for_character() -> None:
    codec = CarrierStateCodec()
    for line in FATIHA_LINES:
        for word in line.split():
            decomposition = decompose_with_residue(word, codec=codec)
            assert reconstruct(decomposition, codec=codec) == word


def test_dropping_the_residue_breaks_the_reconstruction() -> None:
    report = prove_the_residue_is_necessary()
    assert report.broken_words
    assert report.exact_rebuilds < report.word_count
    assert not report.closes


def test_the_residue_necessity_witness_is_measured_not_asserted() -> None:
    with_residue = prove_decomposition_reconstructs()
    without_residue = prove_the_residue_is_necessary()
    assert with_residue.word_count == without_residue.word_count
    assert without_residue.exact_rebuilds < with_residue.exact_rebuilds


def test_the_report_refuses_a_count_that_does_not_add_up() -> None:
    with pytest.raises(PopulationSubstitutionError):
        ReconstructionReport(
            population=Population.OBSERVED,
            source_id="x",
            word_count=5,
            exact_rebuilds=2,
            broken_words=("a",),
        )


def test_an_empty_population_does_not_close_the_theorem() -> None:
    report = prove_decomposition_reconstructs((), source_id="empty")
    assert report.word_count == 0
    assert not report.closes


def test_the_theorem_closes_on_another_named_text_only_by_running_it() -> None:
    report = prove_decomposition_reconstructs(("بِسْمِ",), source_id="one-word")
    assert report.source_id == "one-word"
    assert report.closes
    assert report.word_count == 1
