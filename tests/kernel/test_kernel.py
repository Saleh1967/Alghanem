import pytest

from alghanem.kernel import (
    Anchor,
    Certificate,
    Claim,
    Evidence,
    LicensedTransition,
    Operation,
    OperationResult,
    Outcome,
    Residual,
    State,
    Trace,
    TransitionDecision,
)


def make_transition(
    outcome: Outcome, preserved: tuple[str, ...] = ("identity",)
) -> LicensedTransition:
    return LicensedTransition(
        anchor=Anchor("a", "D"),
        before_state=State("before"),
        operation=Operation("op", "changed"),
        after_state=State("after"),
        evidence=(Evidence(Claim("supported"), "record"),),
        preserved=preserved,
        changed=("component",),
        trace=Trace(("started",)),
        residuals=(Residual("remainder"),),
        outcome=outcome,
        result=OperationResult("result"),
    )


def test_core_objects_are_immutable():
    anchor = Anchor("a", "D")
    with pytest.raises(AttributeError):
        anchor.domain = "other"  # type: ignore[misc]


def test_state_and_certificate_are_immutable_core_objects():
    state = State("opaque")
    certificate = Certificate(
        Claim("supported"), (Evidence(Claim("supported"), "record"),)
    )
    assert state.value == "opaque"
    assert certificate.claim.statement == "supported"
    with pytest.raises(AttributeError):
        certificate.claim = Claim("changed")  # type: ignore[misc]


def test_trace_and_residual_are_preserved():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert transition.trace.events == ("started",)
    assert transition.residuals == (Residual("remainder"),)


def test_identity_preserving_requires_declared_invariant():
    with pytest.raises(ValueError, match="invariant"):
        make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, ())


def test_identity_preserving_requires_declared_change():
    with pytest.raises(ValueError, match="declared change"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "changed"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("identity",),
            changed=(),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            result=OperationResult("result"),
        )


def test_preserved_and_changed_must_be_disjoint():
    with pytest.raises(ValueError, match="disjoint"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "changed"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("component",),
            changed=("component",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            result=OperationResult("result"),
        )


def test_branch_birth_is_distinct_from_identity_preservation():
    assert (
        make_transition(Outcome.CERTIFIED_BRANCH_BIRTH).outcome
        is not Outcome.IDENTITY_PRESERVING_TRANSFORMATION
    )


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_outcomes_are_not_successes(outcome):
    with pytest.raises(ValueError, match="non-transition"):
        make_transition(outcome)


def test_non_transition_decision_cannot_contain_a_transition():
    with pytest.raises(ValueError, match="non-transition"):
        TransitionDecision(
            Outcome.BLOCK,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
        )


def test_success_without_evidence_is_rejected():
    with pytest.raises(ValueError, match="evidence"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "changed"),
            after_state=State("after"),
            evidence=(),
            preserved=("identity",),
            changed=("component",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=OperationResult("result"),
        )


def test_success_without_result_is_rejected():
    with pytest.raises(ValueError, match="result"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "changed"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("identity",),
            changed=("component",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            result=None,  # type: ignore[arg-type]
        )


def test_branch_birth_requires_evidence_and_result():
    with pytest.raises(ValueError, match="evidence"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "changed"),
            after_state=State("after"),
            evidence=(),
            preserved=(),
            changed=("new",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=OperationResult("result"),
        )
    with pytest.raises(ValueError, match="result"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "changed"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=(),
            changed=("new",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=None,  # type: ignore[arg-type]
        )


def test_certificate_without_evidence_is_rejected():
    with pytest.raises(ValueError, match="evidence"):
        Certificate(Claim("supported"), ())


def test_successful_decision_contains_a_transition():
    decision = TransitionDecision(
        Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
        make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
    )
    assert decision.transition is not None
