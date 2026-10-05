"""فضاءُ المقاييس: عقدٌ لا وسمٌ، وعلاقاتٌ رأسيّةٌ لا أخوّةَ فيها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest
from fractal_cases import ALPHA_REF, ALPHA_SCALE, BETA_SCALE, SCALE_SPACE

from alghanem.canonical_content import is_canonical_digest
from alghanem.fractal_generation import (
    FractalScaleContract,
    FractalScaleError,
    FractalScaleRef,
    ScaleRelation,
    ScaleRelationEdge,
    ScaleSpace,
)


def test_a_scale_is_a_contract_not_a_label() -> None:
    for field in (
        "unit_criterion",
        "identity_criterion",
        "admissible_operation_contract",
        "closure_contract",
    ):
        assert getattr(ALPHA_SCALE, field).strip()
    assert is_canonical_digest(ALPHA_SCALE.content_id)


def test_a_contract_refuses_an_unnamed_criterion() -> None:
    with pytest.raises(FractalScaleError):
        FractalScaleContract(
            scale_id="scale.void",
            domain_id="domain.synthetic",
            unit_criterion="  ",
            identity_criterion="هويّة",
            admissible_operation_contract="عمليّة",
            closure_contract="إغلاق",
        )


def test_a_reference_binds_the_content_of_its_contract() -> None:
    assert ALPHA_REF == ALPHA_SCALE.as_ref()
    assert ALPHA_REF.contract_content_id == ALPHA_SCALE.content_id


def test_the_space_admits_only_a_registered_contract() -> None:
    stranger = FractalScaleContract(
        scale_id="scale.alpha",
        domain_id="domain.synthetic",
        unit_criterion="معيارٌ آخر لم يُسجَّل",
        identity_criterion="هويّة",
        admissible_operation_contract="عمليّة",
        closure_contract="إغلاق",
    )
    assert SCALE_SPACE.admits(ALPHA_REF)
    assert not SCALE_SPACE.admits(stranger.as_ref())
    with pytest.raises(FractalScaleError):
        SCALE_SPACE.resolve(stranger.as_ref())


def test_the_space_resolves_a_registered_reference_to_its_contract() -> None:
    assert SCALE_SPACE.resolve(ALPHA_REF) is ALPHA_SCALE
    assert SCALE_SPACE.ref_for("scale.beta") == BETA_SCALE.as_ref()


def test_the_vertical_relations_are_two_and_no_more() -> None:
    assert [member.name for member in ScaleRelation] == ["REFINES", "AGGREGATES"]
    assert "SIBLING" not in {member.name for member in ScaleRelation}


def test_a_relation_refuses_to_join_a_scale_to_itself() -> None:
    with pytest.raises(FractalScaleError):
        ScaleRelationEdge(
            relation=ScaleRelation.AGGREGATES,
            lower_scale_id="scale.alpha",
            higher_scale_id="scale.alpha",
        )


def test_a_space_refuses_a_relation_over_an_unregistered_scale() -> None:
    with pytest.raises(FractalScaleError):
        ScaleSpace(
            contracts=(ALPHA_SCALE,),
            relations=(
                ScaleRelationEdge(
                    relation=ScaleRelation.AGGREGATES,
                    lower_scale_id="scale.alpha",
                    higher_scale_id="scale.beta",
                ),
            ),
        )


def test_the_space_reads_the_relation_between_two_scales() -> None:
    assert (
        SCALE_SPACE.relation_between(
            lower_scale_id="scale.alpha", higher_scale_id="scale.beta"
        )
        is ScaleRelation.AGGREGATES
    )
    assert (
        SCALE_SPACE.relation_between(
            lower_scale_id="scale.beta", higher_scale_id="scale.alpha"
        )
        is None
    )


def test_a_reference_is_not_accepted_as_a_bare_identifier() -> None:
    with pytest.raises(FractalScaleError):
        FractalScaleRef(scale_id="scale.alpha", contract_content_id="ليس بصمة")
