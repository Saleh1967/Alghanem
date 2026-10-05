"""أوّليّاتُ النسبة: مرساةٌ أعمُّ من الجنس، ورتبةٌ مُرخَّصة، وموضعٌ بلا اسمٍ دلاليّ."""

from __future__ import annotations

import pytest

from alghanem.linguistic.nisbah import (
    ArgumentSlot,
    ArityLicenseGenus,
    ConstraintKind,
    ConstraintSpecification,
    NisbahError,
    NisbahSignature,
    OperatorSignature,
    PredicateSignature,
    TermAnchorKind,
    TermAnchorSignature,
)


def _slot(position: int) -> ArgumentSlot:
    return ArgumentSlot(
        slot_id=f"slot-{position}",
        position=position,
        admissibility_condition="طرفٌ محفوظُ الهويّة",
    )


def _predicate(arity: int = 2) -> PredicateSignature:
    return PredicateSignature(
        predicate_id="pred-1",
        arity=arity,
        arity_license=ArityLicenseGenus.PRIOR_SPECIFICATION,
        slots=tuple(_slot(index) for index in range(1, arity + 1)),
    )


def _anchor(anchor_id: str, kind: TermAnchorKind) -> TermAnchorSignature:
    return TermAnchorSignature(
        anchor_id=anchor_id,
        candidate_kind=kind,
        identity_condition="شرطُ حفظ الهويّة مُصرَّحٌ به",
    )


def test_a_term_anchor_is_wider_than_a_genus() -> None:
    kinds = set(TermAnchorKind)
    assert TermAnchorKind.GENUS in kinds
    assert kinds - {TermAnchorKind.GENUS}


def test_an_anchor_kind_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(NisbahError):
        TermAnchorSignature(
            anchor_id="a",
            candidate_kind="GENUS",  # type: ignore[arg-type]
            identity_condition="x",
        )


def test_an_arity_read_off_the_target_state_is_refused_by_name() -> None:
    assert ArityLicenseGenus.DERIVED_FROM_THE_TARGET_STATE in set(ArityLicenseGenus)
    with pytest.raises(NisbahError):
        PredicateSignature(
            predicate_id="pred-1",
            arity=1,
            arity_license=ArityLicenseGenus.DERIVED_FROM_THE_TARGET_STATE,
            slots=(_slot(1),),
        )


def test_a_predicate_may_carry_more_than_one_argument_position() -> None:
    assert _predicate(3).arity == 3


def test_slots_must_cover_the_arity_without_a_gap() -> None:
    with pytest.raises(NisbahError):
        PredicateSignature(
            predicate_id="pred-1",
            arity=2,
            arity_license=ArityLicenseGenus.PRIOR_SPECIFICATION,
            slots=(_slot(1), _slot(3)),
        )


@pytest.mark.parametrize("name", ["Agent", "Patient", "Cause", "Result"])
def test_a_slot_named_with_a_semantic_role_is_refused(name: str) -> None:
    with pytest.raises(NisbahError):
        ArgumentSlot(slot_id=name, position=1, admissibility_condition="x")


def test_an_operator_without_a_named_scope_is_refused() -> None:
    with pytest.raises(NisbahError):
        OperatorSignature(operator_id="op-1", scope_target="   ")


def test_a_nisbah_gathers_a_predicate_with_its_anchors_and_constraints() -> None:
    nisbah = NisbahSignature(
        nisbah_id="nisbah-1",
        predicate=_predicate(),
        anchors=(
            _anchor("anchor-1", TermAnchorKind.INDIVIDUAL),
            _anchor("anchor-2", TermAnchorKind.REFERENCE),
        ),
        operators=(OperatorSignature(operator_id="op-1", scope_target="pred-1"),),
        constraints=(
            ConstraintSpecification(
                constraint_id="c-1",
                kind=ConstraintKind.TIME,
                licensed_by="مواصفةٌ سابقة",
            ),
        ),
    )

    assert nisbah.predicate.arity == len(nisbah.anchors)


def test_a_duplicated_anchor_name_is_refused_not_folded() -> None:
    with pytest.raises(NisbahError):
        NisbahSignature(
            nisbah_id="nisbah-1",
            predicate=_predicate(),
            anchors=(
                _anchor("anchor-1", TermAnchorKind.INDIVIDUAL),
                _anchor("anchor-1", TermAnchorKind.REFERENCE),
            ),
            operators=(),
            constraints=(),
        )
