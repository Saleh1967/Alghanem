"""جبرُ `zero-one`: أصغرُ كلٍّ مكتمل، ثمّ أوّلُ انتقالٍ حقيقيٍّ بلا فائزٍ مفروض.

ولا يدخل هذا الملفَّ لسانٌ ولا جذرٌ ولا وزنٌ ولا معجم؛ الرموزُ مُصطنَعةٌ بحتة.
"""

from __future__ import annotations

from itertools import product

import pytest

from alghanem.structural_dal import (
    ZERO_ONE_BOUND,
    AcceptanceItem,
    ComparativeStanding,
    ContractOutcome,
    OutputContractComponent,
    PartWholeRelation,
    PromotionStanding,
    ResidualClass,
    ShapePartitionHypothesis,
    SlotRole,
    StructuralDalError,
    StructuralDecomposition,
    StructuralPart,
    StructuralSlot,
    StructuralWhole,
    ascend_one_slot,
    decompose,
    enumerate_shape_partitions,
    origin_whole,
    promote_part_to_whole,
    prove_zero_one_algebra,
    zero_structural_state,
)


def _whole(*tokens: str) -> StructuralWhole:
    return origin_whole(
        whole_id="whole.test",
        anchor_id="anchor.test",
        carrier_id="carrier.test",
        tokens=tokens,
    )


def test_zero_is_the_smallest_complete_whole_not_nothing() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert zero.whole.slot_count == 1
    assert zero.decomposition.part_of(SlotRole.CORE).tokens == ("SlotA",)
    assert zero.decomposition.part_of(SlotRole.TRANSFORM).is_empty
    assert zero.decomposition.part_of(SlotRole.RESIDUAL).is_empty


def test_zero_reconstructs_exactly_and_keeps_its_anchor() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert zero.decomposition.reconstruction == zero.whole.tokens
    assert zero.reconstructs_exactly
    assert zero.covers_every_slot_once
    assert zero.preserves_identity
    assert zero.preserves_trace
    assert (
        zero.decomposition.part_of(SlotRole.CORE).parent_anchor_id
        == zero.whole.anchor_id
    )


def test_zero_establishes_nothing_linguistic() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert "StructuralBaseCase != LinguisticRootProof" in zero.does_not_establish
    assert "root" not in str(zero.establishes)


def test_zero_is_refused_on_more_than_one_slot() -> None:
    with pytest.raises(StructuralDalError):
        zero_structural_state(_whole("SlotA", "SlotB"))


def test_one_produces_every_shape_hypothesis_without_a_winner() -> None:
    whole = _whole("SlotA", "SlotB")
    hypotheses = enumerate_shape_partitions(whole)
    assert hypotheses.count == len(tuple(SlotRole)) ** whole.slot_count
    assert hypotheses.forced_winner is None
    shapes = {item.roles for item in hypotheses.hypotheses}
    assert shapes == set(product(tuple(SlotRole), repeat=whole.slot_count))


def test_the_hypothesis_set_declares_what_it_is_not() -> None:
    hypotheses = enumerate_shape_partitions(_whole("SlotA", "SlotB"))
    statements = " ".join(hypotheses.what_it_is_not)
    assert "ShapePartitionHypothesis != RootCandidate" in statements
    assert "ShapePartitionHypothesis != WeightCandidate" in statements


def test_enumeration_above_the_bound_is_refused() -> None:
    whole = _whole(*[f"Slot{index}" for index in range(ZERO_ONE_BOUND + 1)])
    with pytest.raises(StructuralDalError):
        enumerate_shape_partitions(whole)


def test_every_decomposition_covers_each_slot_exactly_once() -> None:
    whole = _whole("SlotA", "SlotB")
    for hypothesis in enumerate_shape_partitions(whole).hypotheses:
        decomposition = decompose(whole, hypothesis)
        assert decomposition.covers_every_slot_once
        assert decomposition.reconstructs_whole
        assert decomposition.preserves_parent_anchor


def test_a_dropped_slot_is_refused_not_absorbed() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.dropped",
        roles=(SlotRole.CORE, SlotRole.TRANSFORM),
    )
    parts = tuple(
        StructuralPart(
            part_id=f"part.{role.value}",
            parent_anchor_id=whole.anchor_id,
            role=role,
            slot_map=(whole.slots[0],) if role is SlotRole.CORE else (),
        )
        for role in SlotRole
    )
    with pytest.raises(StructuralDalError):
        StructuralDecomposition(
            decomposition_id="decomposition.dropped",
            whole=whole,
            hypothesis=hypothesis,
            parts=parts,
        )


def test_a_part_that_does_not_carry_its_parent_anchor_is_refused() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.orphan", roles=(SlotRole.CORE, SlotRole.CORE)
    )
    parts = tuple(
        StructuralPart(
            part_id=f"part.{role.value}",
            parent_anchor_id="anchor.other"
            if role is SlotRole.CORE
            else (whole.anchor_id),
            role=role,
            slot_map=tuple(whole.slots) if role is SlotRole.CORE else (),
        )
        for role in SlotRole
    )
    with pytest.raises(StructuralDalError):
        StructuralDecomposition(
            decomposition_id="decomposition.orphan",
            whole=whole,
            hypothesis=hypothesis,
            parts=parts,
        )


def test_a_scattered_part_is_an_ordered_projection_not_a_substring() -> None:
    part = StructuralPart(
        part_id="part.scattered",
        parent_anchor_id="anchor.test",
        role=SlotRole.CORE,
        slot_map=(
            StructuralSlot(index=0, token="SlotA"),
            StructuralSlot(index=2, token="SlotC"),
        ),
    )
    assert part.relation_to_whole is PartWholeRelation.ORDERED_PROJECTION
    assert "StructuralPart != Substring" in part.refusal


def test_a_part_projection_is_ordered_and_never_repeats_a_slot() -> None:
    with pytest.raises(StructuralDalError):
        StructuralPart(
            part_id="part.repeated",
            parent_anchor_id="anchor.test",
            role=SlotRole.CORE,
            slot_map=(
                StructuralSlot(index=1, token="SlotB"),
                StructuralSlot(index=0, token="SlotA"),
            ),
        )


def test_the_ascent_keeps_the_anchor_and_extends_the_trace() -> None:
    before = _whole("SlotA")
    ascent = ascend_one_slot(before, "SlotB")
    assert ascent.after.anchor_id == before.anchor_id
    assert ascent.after.tokens == ("SlotA", "SlotB")
    assert ascent.trace_is_cumulative
    assert ascent.after.trace_steps == before.trace_steps + 1


def test_the_ascent_transition_reads_all_seven_contract_fields() -> None:
    transition = ascend_one_slot(_whole("SlotA"), "SlotB").transition
    assert transition.input_identity == transition.output_identity
    assert transition.difference.dimension == "slot_accretion"
    assert transition.invariant
    assert len(transition.gate) == 2
    assert transition.residual == ()
    assert len(transition.trace.steps) == 1
    assert transition.added_slot_index == 1


def test_an_ascent_above_the_bound_is_refused() -> None:
    ascent = ascend_one_slot(_whole("SlotA"), "SlotB")
    with pytest.raises(StructuralDalError):
        ascend_one_slot(ascent.after, "SlotC")


def test_a_partition_without_a_core_still_reconstructs_but_is_blocked() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.no_core",
        roles=(SlotRole.TRANSFORM, SlotRole.RESIDUAL),
    )
    decomposition = decompose(whole, hypothesis)
    assert decomposition.reconstructs_whole
    assert decomposition.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
    classes = {reading.residual_class for reading in decomposition.residuals}
    assert ResidualClass.BLOCKING in classes
    with pytest.raises(StructuralDalError):
        promote_part_to_whole(decomposition, SlotRole.TRANSFORM)


def test_every_decomposition_names_a_non_blocking_residual_too() -> None:
    whole = _whole("SlotA", "SlotB")
    for hypothesis in enumerate_shape_partitions(whole).hypotheses:
        classes = [
            reading.residual_class for reading in decompose(whole, hypothesis).residuals
        ]
        assert ResidualClass.NON_BLOCKING in classes


def test_a_promoted_part_keeps_its_parent_anchor() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.core_transform",
        roles=(SlotRole.CORE, SlotRole.TRANSFORM),
    )
    promoted = promote_part_to_whole(decompose(whole, hypothesis), SlotRole.CORE)
    assert promoted.keeps_parent_anchor
    assert promoted.whole.parent_anchor_id == whole.anchor_id
    assert promoted.whole.anchor_id != whole.anchor_id
    assert promoted.whole.descent_depth == whole.descent_depth + 1
    assert promoted.whole.tokens == ("SlotA",)


def test_an_empty_part_does_not_become_a_whole() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.core_core", roles=(SlotRole.CORE, SlotRole.CORE)
    )
    with pytest.raises(StructuralDalError):
        promote_part_to_whole(decompose(whole, hypothesis), SlotRole.TRANSFORM)


def test_a_new_anchor_without_provenance_depth_is_refused() -> None:
    whole = _whole("SlotA")
    with pytest.raises(StructuralDalError):
        StructuralWhole(
            whole_id="whole.orphan",
            node=whole.node,
            provenance="نسبٌ مُصرَّح",
            parent_anchor_id="anchor.parent",
            descent_depth=0,
        )


def test_a_whole_is_not_its_own_parent() -> None:
    whole = _whole("SlotA")
    with pytest.raises(StructuralDalError):
        StructuralWhole(
            whole_id="whole.self_parent",
            node=whole.node,
            provenance="نسبٌ مُصرَّح",
            parent_anchor_id=whole.anchor_id,
            descent_depth=1,
        )


def test_the_report_holds_all_eight_acceptance_items() -> None:
    report = prove_zero_one_algebra()
    assert set(report.findings) == set(AcceptanceItem)
    assert report.unmet_items == ()
    assert report.algebra_holds


def test_the_report_counts_are_derived_from_the_run() -> None:
    report = prove_zero_one_algebra()
    assert report.one_hypotheses.count == len(report.one_decompositions)
    assert len(report.promotion_attempts) == len(report.one_decompositions)
    assert report.blocked_attempts
    assert report.permitted_attempts
    assert all(attempt.promoted is None for attempt in report.blocked_attempts)


def test_the_weaker_model_reaches_the_same_symbols_but_not_the_contract() -> None:
    report = prove_zero_one_algebra()
    assert report.weaker.output == report.ascent.after.tokens
    assert report.weaker.satisfied == (OutputContractComponent.WHOLE_RECONSTRUCTION,)
    assert report.weaker.outcome is ContractOutcome.CONTRACT_PARTIAL
    assert report.structural_outcome is ContractOutcome.CONTRACT_MET
    assert report.standing is ComparativeStanding.STRUCTURAL_ONLY


def test_the_report_names_what_it_does_not_establish() -> None:
    report = prove_zero_one_algebra()
    statements = " ".join(report.what_is_not_established)
    assert "LinguisticRootProof" in statements
    assert "RootCandidate" in statements
    assert "WeightCandidate" in statements
