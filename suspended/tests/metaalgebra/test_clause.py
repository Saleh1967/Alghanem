"""البندُ التصريحيُّ غيرُ البند القابل للتنفيذ، والفرقُ نوعيٌّ لا سمةٌ تُقلَب."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.metaalgebra.clause import (
    EXECUTABLE_NODE_NAMES,
    And,
    ClauseError,
    Constant,
    DeclarativeClause,
    Eq,
    ExecutableClause,
    FieldRef,
    MemberOf,
    Not,
    Or,
    PartialApply,
    require_clause,
)


def _expression() -> And:
    return And(
        operands=(
            Eq(left=FieldRef(path=("state", "kind")), right=Constant(value="closed")),
            Not(operand=Constant(value=False)),
        )
    )


def test_a_declarative_clause_is_never_executable() -> None:
    clause = DeclarativeClause(
        clause_id="c0",
        clause_text="نصٌّ التزاميّ",
        why_not_executable="لا دلالةَ مُترجَمةً له بعدُ",
    )
    assert clause.is_executable is False
    assert not hasattr(clause, "expression")


def test_a_declarative_clause_must_say_why_it_stays_prose() -> None:
    with pytest.raises(ClauseError):
        DeclarativeClause(clause_id="c0", clause_text="نصّ", why_not_executable="   ")


def test_an_executable_clause_carries_a_tree_not_a_string() -> None:
    clause = ExecutableClause(
        clause_id="c1", clause_text="وصفٌ للقراءة", expression=_expression()
    )
    assert clause.is_executable is True
    assert clause.as_canonical_content()["expression"]["node"] == "And"


def test_prose_is_never_accepted_where_an_expression_is_required() -> None:
    with pytest.raises(ClauseError):
        ExecutableClause(
            clause_id="c1",
            clause_text="وصف",
            expression="x == 1",  # type: ignore[arg-type]
        )


def test_a_declarative_clause_is_not_silently_promoted_to_executable() -> None:
    prose = DeclarativeClause(
        clause_id="c0", clause_text="نصّ", why_not_executable="سبب"
    )
    with pytest.raises(ClauseError):
        Not(operand=prose)  # type: ignore[arg-type]


def test_require_clause_refuses_a_bare_string() -> None:
    with pytest.raises(ClauseError):
        require_clause("شرطٌ نصّيّ", "شرطُ التحقيق")


def test_the_node_vocabulary_is_closed_and_single_sourced() -> None:
    assert set(EXECUTABLE_NODE_NAMES) == {
        "And",
        "Or",
        "Not",
        "Eq",
        "MemberOf",
        "FieldRef",
        "Constant",
        "PartialApply",
    }


def test_a_junction_of_one_operand_is_not_a_junction() -> None:
    with pytest.raises(ClauseError):
        Or(operands=(Constant(value=True),))


def test_membership_members_are_constants_not_compound_nodes() -> None:
    with pytest.raises(ClauseError):
        MemberOf(
            element=FieldRef(path=("a",)),
            members=(Not(operand=Constant(value=True)),),  # type: ignore[arg-type]
        )


def test_partial_apply_names_a_declared_operation() -> None:
    node = PartialApply(operation_id="L0.op", arguments=(FieldRef(path=("carrier",)),))
    assert node.as_canonical_content()["operation_id"] == "L0.op"
    with pytest.raises(ClauseError):
        PartialApply(operation_id="  ", arguments=())


def test_no_clause_type_carries_a_judgement_field() -> None:
    for declaring_type in (DeclarativeClause, ExecutableClause):
        for field in fields(declaring_type):
            assert "status" not in field.name
            assert "verdict" not in field.name


def test_executable_clause_digest_is_content_bound() -> None:
    first = ExecutableClause(
        clause_id="c1", clause_text="وصف", expression=_expression()
    )
    second = ExecutableClause(
        clause_id="c1", clause_text="وصف", expression=_expression()
    )
    third = ExecutableClause(
        clause_id="c1", clause_text="وصف", expression=Constant(value=True)
    )
    assert first.content_id == second.content_id
    assert first.content_id != third.content_id
