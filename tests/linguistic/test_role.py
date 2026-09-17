"""الدورُ النسبيُّ غيرُ مرجع التمثيل، والفصلُ مفحوصٌ على الأنواع لا على الأسماء."""

from __future__ import annotations

import ast
from dataclasses import fields
from pathlib import Path

import pytest

from alghanem.linguistic.role import (
    LinguisticObjectSignature,
    RelationalRole,
    RelationalRoleError,
    RelationalRoleRef,
    RepresentationRef,
)


def _representation() -> RepresentationRef:
    return RepresentationRef(carrier_id="carrier-1", state_id="state-1")


def _role() -> RelationalRoleRef:
    return RelationalRoleRef(
        role=RelationalRole.TERM_ANCHOR, read_from="قراءةٌ مُصرَّحٌ بمصدرها"
    )


def test_a_linguistic_object_carries_both_a_representation_and_a_role() -> None:
    signature = LinguisticObjectSignature(
        object_id="obj-1", representation=_representation(), relational_role=_role()
    )

    assert signature.representation is not signature.relational_role


def test_a_role_in_the_representation_position_is_refused() -> None:
    with pytest.raises(RelationalRoleError):
        LinguisticObjectSignature(
            object_id="obj-1",
            representation=_role(),  # type: ignore[arg-type]
            relational_role=_role(),
        )


def test_a_representation_in_the_role_position_is_refused() -> None:
    with pytest.raises(RelationalRoleError):
        LinguisticObjectSignature(
            object_id="obj-1",
            representation=_representation(),
            relational_role=_representation(),  # type: ignore[arg-type]
        )


def test_the_role_is_a_closed_vocabulary_member_not_free_text() -> None:
    with pytest.raises(RelationalRoleError):
        RelationalRoleRef(role="TERM_ANCHOR", read_from="x")  # type: ignore[arg-type]


def test_an_unread_role_is_a_declared_member_not_an_absence() -> None:
    assert RelationalRole.UNREAD in set(RelationalRole)
    unread = RelationalRoleRef(
        role=RelationalRole.UNREAD, read_from="لم تُقرأ بعد"
    )
    assert unread.role is RelationalRole.UNREAD


def test_neither_type_declares_a_field_of_the_other_type() -> None:
    for owner, forbidden in (
        (RepresentationRef, RelationalRoleRef),
        (RelationalRoleRef, RepresentationRef),
    ):
        for field in fields(owner):
            assert field.type is not forbidden
            assert forbidden.__name__ not in str(field.type)


def test_the_module_declares_no_result_or_verdict_field() -> None:
    path = Path(__file__).resolve().parents[2] / "src" / "alghanem" / "linguistic"
    tree = ast.parse((path / "role.py").read_text(encoding="utf-8"))
    names = {
        node.target.id
        for node in ast.walk(tree)
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    }
    assert not names & {"result", "verdict", "outcome", "score"}
