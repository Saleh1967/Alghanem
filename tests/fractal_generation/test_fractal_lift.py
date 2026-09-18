"""رتبةُ الرفع في `G0.FGEN-0`: الأنواعُ معرَّفةٌ، والسلطةُ غيرُ مفتوحةٍ بعد.

الشاهدُ هنا شاهدُ رتبةٍ لا شاهدُ أبد:

    FGEN0SpecHasNoIssuancePathToNextScaleSeed

أي أنّ الواجهةَ العامّةَ وبوّاباتِ هذا الإصدار لا تُصدِر `ScaleNecessityCertificate`
ولا `NextScaleSeed`. وغيابُ المسار اليومَ حالُ مرحلةٍ (`NotIssuedAtThisStage`)
لا قانونُ أبدٍ (`MustNeverExist`): فتحُ السلطة يأتي بمرحلةٍ مستقلّةٍ لاحقة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import inspect
from typing import Any

import pytest
from fractal_cases import ALPHA_REF, BETA_REF

import alghanem.fractal_generation as fgen
from alghanem.fractal_generation import (
    NO_SCALE_NECESSITY_AUTHORITY,
    LiftCandidate,
    LiftDecision,
    LiftError,
    LiftGate,
    LiftStatus,
    NextScaleSeed,
    ScaleExhaustionCandidate,
    ScaleNecessityCertificate,
    ScaleTransitionRequirement,
)

_WITHHELD = ("ScaleNecessityCertificate", "NextScaleSeed")


def _requirement() -> ScaleTransitionRequirement:
    return ScaleTransitionRequirement(
        from_scale_ref=ALPHA_REF,
        to_scale_ref=BETA_REF,
        necessity_claim="دعوى ضرورةٍ مكتوبةٌ بيد صاحبها",
    )


def test_a_requirement_names_two_distinct_scales() -> None:
    with pytest.raises(LiftError):
        ScaleTransitionRequirement(
            from_scale_ref=ALPHA_REF,
            to_scale_ref=ALPHA_REF,
            necessity_claim="دعوى",
        )


def test_an_exhaustion_claim_is_authored_not_proven(closed_node: Any) -> None:
    claim = ScaleExhaustionCandidate(
        closed_node=closed_node,
        claim="استنفدتُ المقياسَ ألف",
        irreducible_residuals=(),
    )
    assert claim.closed_node is closed_node
    assert not isinstance(claim, ScaleNecessityCertificate)


def test_the_certificate_has_no_issuance_path_at_this_stage(closed_node: Any) -> None:
    exhaustion = ScaleExhaustionCandidate(
        closed_node=closed_node,
        claim="استنفدتُ المقياسَ ألف",
        irreducible_residuals=(),
    )
    with pytest.raises(LiftError):
        ScaleNecessityCertificate(
            requirement=_requirement(),
            exhaustion=exhaustion,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_next_scale_seed_has_no_issuance_path_at_this_stage() -> None:
    with pytest.raises(LiftError):
        NextScaleSeed(
            certificate=None,  # type: ignore[arg-type]
            seed=None,  # type: ignore[arg-type]
        )


def test_a_lift_candidate_carries_its_own_closed_node(closed_node: Any) -> None:
    exhaustion = ScaleExhaustionCandidate(
        closed_node=closed_node,
        claim="استنفدتُ المقياسَ ألف",
        irreducible_residuals=(),
    )
    candidate = LiftCandidate(
        closed_node=closed_node,
        exhaustion=exhaustion,
        requirement=_requirement(),
    )
    assert candidate.closed_node is closed_node


def test_the_lift_gate_defers_for_absence_of_authority(closed_node: Any) -> None:
    exhaustion = ScaleExhaustionCandidate(
        closed_node=closed_node,
        claim="استنفدتُ المقياسَ ألف",
        irreducible_residuals=(),
    )
    decision = LiftGate.assess(
        candidate=LiftCandidate(
            closed_node=closed_node,
            exhaustion=exhaustion,
            requirement=_requirement(),
        )
    )
    assert decision.status is LiftStatus.DEFERRED_NO_SCALE_NECESSITY_AUTHORITY
    assert decision.next_scale_seed is None
    assert decision.blocking_gap is NO_SCALE_NECESSITY_AUTHORITY


def test_the_lift_gate_reads_no_caller_evidence() -> None:
    parameters = inspect.signature(LiftGate.assess).parameters
    assert tuple(parameters) == ("candidate",)
    assert parameters["candidate"].kind is inspect.Parameter.KEYWORD_ONLY


def test_a_lift_decision_cannot_carry_a_seed(closed_node: Any) -> None:
    with pytest.raises(LiftError):
        LiftDecision(
            status=LiftStatus.DEFERRED_NO_SCALE_NECESSITY_AUTHORITY,
            reason="سبب",
            blocking_gap=NO_SCALE_NECESSITY_AUTHORITY,
            next_scale_seed=closed_node,  # type: ignore[arg-type]
        )


def test_the_deferral_is_the_only_status_of_this_stage() -> None:
    assert [member.name for member in LiftStatus] == [
        "DEFERRED_NO_SCALE_NECESSITY_AUTHORITY"
    ]


def test_fgen0_spec_has_no_issuance_path_to_next_scale_seed() -> None:
    """لا دالّةً ولا بوّابةً في واجهة هذا الإصدار تُرجِع المحجوبَين."""

    for name in fgen.__all__:
        member = getattr(fgen, name)
        callables: list[Any] = []
        if inspect.isclass(member) and name not in _WITHHELD:
            callables.extend(
                getattr(member, key)
                for key in vars(member)
                if not key.startswith("_") and callable(getattr(member, key, None))
            )
        elif inspect.isfunction(member):
            callables.append(member)
        for entry in callables:
            annotation = str(inspect.signature(entry).return_annotation)
            for withheld in _WITHHELD:
                assert withheld not in annotation, (name, annotation)


def test_the_absence_of_authority_is_a_stage_not_an_eternity() -> None:
    assert NO_SCALE_NECESSITY_AUTHORITY.discharge_condition.strip()
    assert "مرحلةٌ مستقلّةٌ" in NO_SCALE_NECESSITY_AUTHORITY.discharge_condition
