"""جبرُ `zero-one`: أصغرُ كلٍّ مكتمل، ثمّ أوّلُ انتقالٍ حقيقيٍّ بلا فائزٍ مفروض.

ولا يدخل هذا الملفَّ لسانٌ ولا جذرٌ ولا وزنٌ ولا معجم؛ الرموزُ مُصطنَعةٌ بحتة.
"""

from __future__ import annotations

from itertools import product

import pytest

from alghanem.structural_dal import (
    ZERO_ONE_BOUND,
    AcceptanceItem,
    ContractOutcome,
    IdentityTransitionAvailability,
    IdentityTransitionMode,
    OutputContractComponent,
    PartWholeRelation,
    PromotionStanding,
    ResidualClass,
    SelfDefinedContractReading,
    ShapePartitionHypothesis,
    SlotRole,
    StructuralDalError,
    StructuralDecomposition,
    StructuralPart,
    StructuralSlot,
    StructuralWhole,
    ascend_one_slot,
    availability_of,
    decompose,
    enumerate_shape_partitions,
    origin_whole,
    prove_zero_one_algebra,
    request_part_branch_birth,
    zero_structural_state,
)


def _whole(*tokens: str) -> StructuralWhole:
    return origin_whole(
        whole_id="whole.test",
        anchor_id="anchor.test",
        carrier_id="carrier.test",
        tokens=tokens,
    )


def _rescale(before: StructuralWhole, token: str):
    return ascend_one_slot(
        before, token, mode=IdentityTransitionMode.SAME_ENTITY_RESCALING
    )


def test_zero_is_the_smallest_complete_whole_not_nothing() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert zero.whole.slot_count == 1
    assert zero.neutral_part.tokens == ("SlotA",)
    for role in SlotRole:
        if role.is_positive:
            assert zero.decomposition.part_of(role).is_empty


def test_zero_assigns_no_positive_role_to_a_neutral_input() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert zero.assigns_no_positive_role
    assert zero.decomposition.hypothesis.roles == (SlotRole.UNASSIGNED,)
    assert not zero.decomposition.hypothesis.assigns_a_positive_role
    assert "neutral_start" in zero.establishes


def test_a_neutral_zero_is_refused_promotion_by_a_blocking_residual() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert zero.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
    assert all(
        reading.residual_class is ResidualClass.BLOCKING for reading in zero.residuals
    )


def test_a_zero_state_that_declares_a_positive_role_is_refused() -> None:
    whole = _whole("SlotA")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.core", roles=(SlotRole.CORE,)
    )
    from alghanem.structural_dal.hypothesis import ZeroStructuralState

    with pytest.raises(StructuralDalError):
        ZeroStructuralState(whole=whole, decomposition=decompose(whole, hypothesis))


def test_an_unproved_role_basis_is_a_blocking_residual() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.core_core", roles=(SlotRole.CORE, SlotRole.CORE)
    )
    decomposition = decompose(whole, hypothesis)
    assert decomposition.reconstructs_whole
    assert decomposition.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
    reasons = " ".join(reading.reason for reading in decomposition.residuals)
    assert "UnprovedRoleBasis -> BlockingResidual" in reasons


def test_zero_reconstructs_exactly_and_keeps_its_anchor() -> None:
    zero = zero_structural_state(_whole("SlotA"))
    assert zero.decomposition.reconstruction == zero.whole.tokens
    assert zero.reconstructs_exactly
    assert zero.covers_every_slot_once
    assert zero.preserves_identity
    assert zero.preserves_trace
    assert zero.neutral_part.parent_anchor_id == zero.whole.anchor_id
    assert zero.neutral_part.part_anchor_id != zero.whole.anchor_id


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
            part_anchor_id=f"anchor.part.{role.value}",
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
            part_anchor_id=f"anchor.part.{role.value}",
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
        part_anchor_id="anchor.part.scattered",
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
            part_anchor_id="anchor.part.repeated",
            parent_anchor_id="anchor.test",
            role=SlotRole.CORE,
            slot_map=(
                StructuralSlot(index=1, token="SlotB"),
                StructuralSlot(index=0, token="SlotA"),
            ),
        )


def test_a_part_carries_an_identity_distinct_from_its_lineage() -> None:
    whole = _whole("SlotA", "SlotB")
    decomposition = decompose(
        whole,
        ShapePartitionHypothesis(
            hypothesis_id="shape.core_transform",
            roles=(SlotRole.CORE, SlotRole.TRANSFORM),
        ),
    )
    assert decomposition.parts_carry_distinct_identity
    anchors = {part.part_anchor_id for part in decomposition.parts}
    assert len(anchors) == len(decomposition.parts)
    for part in decomposition.parts:
        assert part.identity_is_distinct_from_lineage
        assert part.parent_anchor_id == whole.anchor_id


def test_a_part_whose_identity_is_its_lineage_is_refused() -> None:
    with pytest.raises(StructuralDalError):
        StructuralPart(
            part_id="part.identity_is_lineage",
            part_anchor_id="anchor.test",
            parent_anchor_id="anchor.test",
            role=SlotRole.CORE,
            slot_map=(StructuralSlot(index=0, token="SlotA"),),
        )


def test_two_parts_cannot_share_one_identity() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.shared_identity",
        roles=(SlotRole.CORE, SlotRole.TRANSFORM),
    )
    parts = tuple(
        StructuralPart(
            part_id=f"part.{role.value}",
            part_anchor_id="anchor.shared",
            parent_anchor_id=whole.anchor_id,
            role=role,
            slot_map=tuple(
                slot
                for index, slot in enumerate(whole.slots)
                if hypothesis.roles[index] is role
            ),
        )
        for role in SlotRole
    )
    with pytest.raises(StructuralDalError):
        StructuralDecomposition(
            decomposition_id="decomposition.shared_identity",
            whole=whole,
            hypothesis=hypothesis,
            parts=parts,
        )


def test_an_ascent_without_a_declared_identity_mode_is_refused() -> None:
    with pytest.raises(TypeError):
        ascend_one_slot(_whole("SlotA"), "SlotB")  # type: ignore[call-arg]


def test_branch_birth_is_not_an_available_ascent_mode() -> None:
    assert (
        availability_of(IdentityTransitionMode.SAME_ENTITY_RESCALING)
        is IdentityTransitionAvailability.OPEN
    )
    assert (
        availability_of(IdentityTransitionMode.CERTIFIED_BRANCH_BIRTH)
        is IdentityTransitionAvailability.DEFERRED
    )
    with pytest.raises(StructuralDalError):
        ascend_one_slot(
            _whole("SlotA"),
            "SlotB",
            mode=IdentityTransitionMode.CERTIFIED_BRANCH_BIRTH,
        )


def test_a_part_cannot_be_born_a_branch_without_an_external_certificate() -> None:
    whole = _whole("SlotA", "SlotB")
    decomposition = decompose(
        whole,
        ShapePartitionHypothesis(
            hypothesis_id="shape.core_transform",
            roles=(SlotRole.CORE, SlotRole.TRANSFORM),
        ),
    )
    deferred = request_part_branch_birth(decomposition, SlotRole.CORE)
    assert deferred.availability is IdentityTransitionAvailability.DEFERRED
    assert deferred.requested_mode is IdentityTransitionMode.CERTIFIED_BRANCH_BIRTH
    assert (
        deferred.requested_anchor_id
        == decomposition.part_of(SlotRole.CORE).part_anchor_id
    )
    assert "NoBranchBirthWithoutExternalCertificate" in deferred.refusal


def test_the_rescaling_keeps_the_anchor_and_extends_the_trace() -> None:
    before = _whole("SlotA")
    ascent = _rescale(before, "SlotB")
    assert ascent.mode is IdentityTransitionMode.SAME_ENTITY_RESCALING
    assert ascent.preserves_instance_identity
    assert ascent.after.anchor_id == before.anchor_id
    assert ascent.after.tokens == ("SlotA", "SlotB")
    assert ascent.trace_is_cumulative
    assert ascent.after.trace_steps == before.trace_steps + 1


def test_the_ascent_transition_reads_all_seven_contract_fields() -> None:
    transition = _rescale(_whole("SlotA"), "SlotB").transition
    assert transition.input_identity == transition.output_identity
    assert transition.difference.dimension == "slot_accretion"
    assert transition.invariant
    assert len(transition.gate) == 2
    assert transition.residual == ()
    assert len(transition.trace.steps) == 1
    assert transition.added_slot_index == 1


def test_an_ascent_above_the_bound_is_refused() -> None:
    ascent = _rescale(_whole("SlotA"), "SlotB")
    with pytest.raises(StructuralDalError):
        _rescale(ascent.after, "SlotC")


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


def test_every_decomposition_at_one_is_blocked_from_promotion() -> None:
    whole = _whole("SlotA", "SlotB")
    for hypothesis in enumerate_shape_partitions(whole).hypotheses:
        decomposition = decompose(whole, hypothesis)
        assert decomposition.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
        assert any(
            reading.residual_class is ResidualClass.BLOCKING
            for reading in decomposition.residuals
        )


def test_an_empty_part_is_not_even_a_birth_request() -> None:
    whole = _whole("SlotA", "SlotB")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.core_core", roles=(SlotRole.CORE, SlotRole.CORE)
    )
    with pytest.raises(StructuralDalError):
        request_part_branch_birth(decompose(whole, hypothesis), SlotRole.TRANSFORM)


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


def test_the_report_holds_every_acceptance_item() -> None:
    report = prove_zero_one_algebra()
    assert set(report.findings) == set(AcceptanceItem)
    assert report.unmet_items == ()
    assert report.algebra_holds


def test_the_report_counts_are_derived_from_the_run() -> None:
    report = prove_zero_one_algebra()
    assert report.one_hypotheses.count == len(report.one_decompositions)
    assert len(report.promotion_attempts) == len(report.one_decompositions)
    assert report.blocked_attempts
    assert report.permitted_attempts == ()
    assert report.deferred_births
    assert all(
        birth.availability is IdentityTransitionAvailability.DEFERRED
        for birth in report.deferred_births
    )


def test_the_weaker_model_reaches_the_same_symbols_but_not_the_contract() -> None:
    report = prove_zero_one_algebra()
    assert report.weaker.output == report.ascent.after.tokens
    assert report.weaker.satisfied == (OutputContractComponent.WHOLE_RECONSTRUCTION,)
    assert report.weaker.outcome is ContractOutcome.CONTRACT_PARTIAL
    assert report.structural_outcome is ContractOutcome.CONTRACT_MET
    assert (
        report.self_defined_contract_reading
        is SelfDefinedContractReading.THIS_LAYER_MEETS_ITS_OWN_CONTRACT_ALONE
    )
    assert (
        "SelfDefinedContract" in report.self_defined_contract_reading.does_not_establish
    )


def test_the_report_names_what_it_does_not_establish() -> None:
    report = prove_zero_one_algebra()
    statements = " ".join(report.what_is_not_established)
    assert "LinguisticRootProof" in statements
    assert "RootCandidate" in statements
    assert "WeightCandidate" in statements
    assert "SelfDefinedContract" in statements
    assert "EligibleForFiberIntegration" in statements
