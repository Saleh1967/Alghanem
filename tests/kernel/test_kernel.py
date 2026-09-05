import pytest

from alghanem.kernel import (
    Anchor,
    Claim,
    Evidence,
    LicensedTransition,
    Operation,
    OperationResult,
    Outcome,
    Residual,
    Trace,
)


def make_transition(
    outcome: Outcome, preserved: tuple[str, ...] = ("identity",)
) -> LicensedTransition:
    return LicensedTransition(
        anchor=Anchor("a", "D"),
        operation=Operation("op", "changed"),
        evidence=(Evidence(Claim("supported"), "record"),),
        preserved=preserved,
        changed=("component",),
        trace=Trace(("started",)),
        residuals=(Residual("remainder"),),
        outcome=outcome,
        result=OperationResult("result")
        if outcome
        in {
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            Outcome.CERTIFIED_BRANCH_BIRTH,
        }
        else None,
    )


def test_core_objects_are_immutable():
    anchor = Anchor("a", "D")
    with pytest.raises(AttributeError):
        anchor.domain = "other"  # type: ignore[misc]


def test_trace_and_residual_are_preserved():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert transition.trace.events == ("started",)
    assert transition.residuals == (Residual("remainder"),)


def test_identity_preserving_requires_declared_invariant():
    with pytest.raises(ValueError, match="invariant"):
        make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, ())


def test_branch_birth_is_distinct_from_identity_preservation():
    assert (
        make_transition(Outcome.CERTIFIED_BRANCH_BIRTH).outcome
        is not Outcome.IDENTITY_PRESERVING_TRANSFORMATION
    )


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_outcomes_are_not_successes(outcome):
    transition = make_transition(outcome)
    assert transition.result is None


def test_non_success_cannot_contain_a_result():
    with pytest.raises(ValueError, match="non-success"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            operation=Operation("op", "changed"),
            evidence=(),
            preserved=(),
            changed=(),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.BLOCK,
            result=OperationResult("unexpected"),
        )


def test_success_without_evidence_is_rejected():
    with pytest.raises(ValueError, match="evidence"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            operation=Operation("op", "changed"),
            evidence=(),
            preserved=("identity",),
            changed=("component",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=OperationResult("result"),
        )
