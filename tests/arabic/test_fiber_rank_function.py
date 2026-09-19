"""شهودٌ على دالّة الرتبة: كفايةٌ ووحدانيّةٌ في المحيط، وسقوطُهما في المرصود."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import fiber_rank_function as rank_module
from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.decomposition_reconstruction_theorem import (
    MeasurementInstrument,
    Population,
)
from alghanem.arabic.fiber_rank_function import (
    FIBER_RANK_NAMED_RESIDUALS,
    ClaimVerdict,
    EqualRankWitness,
    FiberRankError,
    ObservedRankRefutation,
    UnequalChainWitness,
    maximum_rank_by_instrument,
    observed_fibers,
    prove_rank_on_the_ambient_lattice,
    rank_by_carrier,
    refute_rank_on_the_observed_population,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

# --- الحدودُ البنيويّة ------------------------------------------------------------


def test_the_rank_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(rank_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="fiber-rank-function",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_there_are_six_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(FIBER_RANK_NAMED_RESIDUALS) == 6
    assert len(set(FIBER_RANK_NAMED_RESIDUALS)) == 6
    assert all(note.strip() for note in FIBER_RANK_NAMED_RESIDUALS)


def test_the_residuals_refuse_to_license_a_refine_slot() -> None:
    joined = "\n".join(FIBER_RANK_NAMED_RESIDUALS)
    assert "ARankFunctionDoesNotLicenseRefineSlot" in joined


def test_no_refinement_or_split_operation_is_exported_here() -> None:
    exported = [
        name
        for name in rank_module.__all__
        if callable(getattr(rank_module, name))
        and ("refine" in name.lower() or "split" in name.lower())
    ]
    assert exported == []
    assert not hasattr(rank_module, "RefineSlot")


# --- الشبكةُ المحيطة: الكفايةُ والوحدانيّة --------------------------------------


def test_the_ambient_lattice_is_the_power_set_of_the_measured_universe() -> None:
    proof = prove_rank_on_the_ambient_lattice()
    assert proof.universe_size == 7
    assert proof.lattice_size == 2**7


def test_every_ambient_cover_raises_the_rank_by_exactly_one() -> None:
    proof = prove_rank_on_the_ambient_lattice()
    assert proof.every_cover_raises_the_rank_by_one
    assert proof.covers_examined == 7 * 2**6


def test_sufficiency_is_proven_on_the_ambient_lattice_by_exhaustion() -> None:
    proof = prove_rank_on_the_ambient_lattice()
    assert proof.sufficiency is ClaimVerdict.PROVEN_BY_EXHAUSTION


def test_uniqueness_is_proven_on_the_ambient_lattice_and_is_one_constant() -> None:
    proof = prove_rank_on_the_ambient_lattice()
    assert proof.uniqueness is ClaimVerdict.PROVEN_BY_EXHAUSTION
    assert proof.hasse_diagram_is_connected
    assert proof.free_constants == 1


def test_the_forced_values_are_the_counting_function_itself() -> None:
    proof = prove_rank_on_the_ambient_lattice()
    assert proof.forced_values_agree_on_every_decomposition
    assert proof.forced_values_equal_cardinality


def test_a_lattice_size_that_is_not_a_power_of_two_is_refused() -> None:
    with pytest.raises(FiberRankError):
        rank_module.AmbientRankProof(
            universe_size=7,
            lattice_size=127,
            covers_examined=448,
            every_cover_raises_the_rank_by_one=True,
            hasse_diagram_is_connected=True,
            forced_values_agree_on_every_decomposition=True,
            forced_values_equal_cardinality=True,
        )


def test_uniqueness_is_not_asked_when_ambient_existence_fails() -> None:
    proof = rank_module.AmbientRankProof(
        universe_size=3,
        lattice_size=8,
        covers_examined=12,
        every_cover_raises_the_rank_by_one=False,
        hasse_diagram_is_connected=True,
        forced_values_agree_on_every_decomposition=True,
        forced_values_equal_cardinality=True,
    )
    assert proof.sufficiency is ClaimVerdict.REFUTED_BY_COUNTER_WITNESS
    assert proof.uniqueness is ClaimVerdict.NOT_ASKED_BECAUSE_EXISTENCE_FAILED


# --- المرصود: سقوطُ الوجود قبل الوحدانيّة ---------------------------------------


def test_the_refutation_is_labelled_with_the_observed_population_and_fiber() -> None:
    refutation = refute_rank_on_the_observed_population()
    assert refutation.population is Population.OBSERVED
    assert refutation.instrument is MeasurementInstrument.OBSERVED_FIBER


def test_the_refutation_counts_match_the_live_fiber_measurement() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()
    refutation = refute_rank_on_the_observed_population(table)
    assert refutation.carrier_count == len(table.fibers) == 23
    assert refutation.distinct_fiber_count == 16
    assert refutation.source_id == table.deposit.source_id


def test_no_rank_function_exists_on_the_observed_subposet() -> None:
    refutation = refute_rank_on_the_observed_population()
    assert refutation.existence is ClaimVerdict.REFUTED_BY_COUNTER_WITNESS
    assert refutation.unequal_chain_witnesses


def test_uniqueness_is_not_asked_because_existence_failed() -> None:
    refutation = refute_rank_on_the_observed_population()
    assert refutation.uniqueness is ClaimVerdict.NOT_ASKED_BECAUSE_EXISTENCE_FAILED


def test_the_counter_witness_names_two_chains_of_different_lengths() -> None:
    refutation = refute_rank_on_the_observed_population()
    witness = next(
        item
        for item in refutation.unequal_chain_witnesses
        if item.lower_carriers == ("س",)
    )
    assert witness.upper_carriers == ("ل",)
    assert witness.chain_lengths == (3, 4)
    assert len(witness.shortest_chain) < len(witness.longest_chain)


def test_every_named_chain_step_is_a_carrier_measured_in_the_deposit() -> None:
    fibers = observed_fibers()
    refutation = refute_rank_on_the_observed_population()
    for witness in refutation.unequal_chain_witnesses:
        for carrier in witness.shortest_chain + witness.longest_chain:
            assert carrier in fibers


def test_a_witness_with_equal_chain_lengths_is_refused() -> None:
    with pytest.raises(FiberRankError):
        UnequalChainWitness(
            lower_carriers=("س",),
            upper_carriers=("ل",),
            lower_rank=1,
            upper_rank=6,
            chain_lengths=(3, 3),
            shortest_chain=("س", "ه", "ل"),
            longest_chain=("س", "غ", "ل"),
        )


def test_the_comparability_graph_is_disconnected_so_constants_are_not_one() -> None:
    refutation = refute_rank_on_the_observed_population()
    assert refutation.comparability_component_count == 2
    assert refutation.free_constants == 2


def test_the_observed_rank_range_has_a_hole_at_five() -> None:
    refutation = refute_rank_on_the_observed_population()
    assert refutation.rank_values == (1, 2, 3, 4, 6)
    assert not refutation.rank_range_is_contiguous


def test_rank_does_not_determine_the_fiber_it_ranks() -> None:
    refutation = refute_rank_on_the_observed_population()
    assert not refutation.rank_determines_the_fiber
    assert refutation.distinct_fiber_count > len(refutation.rank_values)


def test_two_carriers_of_equal_rank_have_incomparable_fibers() -> None:
    fibers = observed_fibers()
    refutation = refute_rank_on_the_observed_population()
    witness = next(
        item
        for item in refutation.equal_rank_witnesses
        if {item.first_carrier, item.second_carrier} == {"م", "ي"}
    )
    assert witness.shared_rank == 4
    assert not witness.comparable
    assert fibers["م"] != fibers["ي"]
    assert witness.shared_states == len(fibers["م"] & fibers["ي"])


def test_an_equal_rank_witness_refuses_a_comparable_pair() -> None:
    with pytest.raises(FiberRankError):
        EqualRankWitness(
            first_carrier="م",
            second_carrier="ي",
            shared_rank=4,
            shared_states=2,
            comparable=True,
        )


def test_the_refutation_refuses_the_declared_population() -> None:
    refutation = refute_rank_on_the_observed_population()
    with pytest.raises(FiberRankError):
        ObservedRankRefutation(
            population=Population.DECLARED,
            instrument=refutation.instrument,
            source_id=refutation.source_id,
            carrier_count=refutation.carrier_count,
            distinct_fiber_count=refutation.distinct_fiber_count,
            rank_values=refutation.rank_values,
            unequal_chain_witnesses=refutation.unequal_chain_witnesses,
            comparability_component_count=refutation.comparability_component_count,
            equal_rank_witnesses=refutation.equal_rank_witnesses,
        )


def test_the_refutation_refuses_the_codec_instrument_for_fiber_ranks() -> None:
    refutation = refute_rank_on_the_observed_population()
    with pytest.raises(FiberRankError):
        ObservedRankRefutation(
            population=refutation.population,
            instrument=MeasurementInstrument.CODEC_UNIT,
            source_id=refutation.source_id,
            carrier_count=refutation.carrier_count,
            distinct_fiber_count=refutation.distinct_fiber_count,
            rank_values=refutation.rank_values,
            unequal_chain_witnesses=refutation.unequal_chain_witnesses,
            comparability_component_count=refutation.comparability_component_count,
            equal_rank_witnesses=refutation.equal_rank_witnesses,
        )


# --- الرتبةُ نسبيّةٌ بآلتها -------------------------------------------------------


def test_the_two_instruments_report_different_maximum_ranks() -> None:
    maxima = maximum_rank_by_instrument()
    assert maxima[MeasurementInstrument.OBSERVED_FIBER] == 6
    assert maxima[MeasurementInstrument.CODEC_UNIT] == 4


def test_the_rank_of_each_carrier_is_its_measured_fiber_size() -> None:
    fibers = observed_fibers()
    ranks = rank_by_carrier()
    assert ranks == {carrier: len(fiber) for carrier, fiber in fibers.items()}
    assert ranks["ل"] == 6
