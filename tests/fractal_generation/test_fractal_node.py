"""البذرةُ والعقدةُ والبقيّة: هويّةُ نسخةٍ محفوظةٌ صراحةً، وبصمةٌ مُشتَقّةٌ لا مكتوبة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest
from fractal_cases import ALPHA_IDENTITY, ALPHA_REF, BETA_REF, SEED, SEED_NODE

from alghanem.canonical_content import is_canonical_digest
from alghanem.fractal_generation import (
    FractalIdentity,
    FractalNode,
    FractalNodeError,
    FractalResidual,
    FractalResidualKind,
    FractalSeed,
)


def test_an_identity_is_located_at_a_referenced_scale() -> None:
    assert ALPHA_IDENTITY.scale_ref == ALPHA_REF
    assert is_canonical_digest(ALPHA_IDENTITY.content_id)


def test_an_identity_refuses_a_bare_scale_identifier() -> None:
    with pytest.raises(FractalNodeError):
        FractalIdentity(
            identity_id="identity.void",
            scale_ref="scale.alpha",  # type: ignore[arg-type]
            identity_criterion_id="criterion.instance",
        )


def test_sameness_is_of_the_instance_not_of_the_criterion() -> None:
    twin = FractalIdentity(
        identity_id="identity.alpha",
        scale_ref=ALPHA_REF,
        identity_criterion_id="criterion.instance",
    )
    other_instance = FractalIdentity(
        identity_id="identity.alpha.other",
        scale_ref=ALPHA_REF,
        identity_criterion_id="criterion.instance",
    )
    other_scale = FractalIdentity(
        identity_id="identity.alpha",
        scale_ref=BETA_REF,
        identity_criterion_id="criterion.instance",
    )
    assert ALPHA_IDENTITY.is_same_instance_as(twin)
    assert not ALPHA_IDENTITY.is_same_instance_as(other_instance)
    assert not ALPHA_IDENTITY.is_same_instance_as(other_scale)


def test_a_seed_refuses_a_duplicated_content_key() -> None:
    with pytest.raises(FractalNodeError):
        FractalSeed(
            seed_id="seed.duplicate",
            identity=ALPHA_IDENTITY,
            carrier_id="carrier.alpha",
            content=(("mark", "m0"), ("mark", "m1")),
        )


def test_a_node_born_of_a_seed_records_its_origin() -> None:
    assert SEED_NODE.origin_id == SEED.content_id
    assert SEED_NODE.identity is SEED.identity
    assert SEED_NODE.carrier_id == SEED.carrier_id
    assert SEED_NODE.content == SEED.content


def test_a_node_reference_binds_the_content_of_its_node() -> None:
    ref = SEED_NODE.as_ref()
    assert ref.node_id == SEED_NODE.node_id
    assert ref.content_id == SEED_NODE.content_id
    assert is_canonical_digest(ref.content_id)


def test_two_nodes_differing_in_content_differ_in_digest() -> None:
    other = FractalNode(
        node_id="node.alpha.0",
        identity=ALPHA_IDENTITY,
        carrier_id="carrier.alpha",
        content=(("mark", "m9"),),
        origin_id=SEED.content_id,
    )
    assert other.content_id != SEED_NODE.content_id


def test_a_residual_is_a_record_not_a_disposition() -> None:
    residual = FractalResidual(
        kind=FractalResidualKind.DEFERRED_BRANCH,
        subject_id="branch.C",
        reason="لا دليلَ عند المقياس الجاري",
    )
    assert residual.blocking is False
    assert not hasattr(residual, "standing")
    assert not hasattr(residual, "verdict")


def test_a_residual_refuses_an_unnamed_reason() -> None:
    with pytest.raises(FractalNodeError):
        FractalResidual(
            kind=FractalResidualKind.DEFERRED_BRANCH,
            subject_id="branch.C",
            reason="   ",
        )


def test_the_residual_kinds_are_a_closed_vocabulary() -> None:
    assert [member.name for member in FractalResidualKind] == [
        "UNRESOLVED_DIFFERENCE",
        "UNVERIFIED_PATTERN_PROOF",
        "UNCOVERED_MINIMUM_REQUIREMENT",
        "DEFERRED_BRANCH",
        "BLOCKED_BRANCH",
        "IRREDUCIBLE_AT_CURRENT_SCALE",
    ]
