import pytest

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
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
    anchor = Anchor("a", "D")
    return LicensedTransition(
        anchor=anchor,
        before_state=State("before"),
        operation=Operation("op", "component"),
        after_state=State("after"),
        evidence=(Evidence(Claim("supported"), "record"),),
        preserved=preserved,
        changed=("component",),
        trace=Trace(("started",)),
        residuals=(Residual("remainder"),),
        outcome=outcome,
        result=OperationResult("result"),
        branch_origin_provenance=(
            BranchOriginProvenance(anchor)
            if outcome is Outcome.CERTIFIED_BRANCH_BIRTH
            else None
        ),
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
            operation=Operation("op", "component"),
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
            operation=Operation("op", "component"),
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
            operation=Operation("op", "component"),
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
            operation=Operation("op", "component"),
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
            operation=Operation("op", "component"),
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
            operation=Operation("op", "component"),
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


def test_certificate_rejects_evidence_for_another_claim():
    with pytest.raises(ValueError, match="bound to its claim"):
        Certificate(Claim("supported"), (Evidence(Claim("another"), "record"),))


def test_transition_change_must_include_operation_declared_change():
    with pytest.raises(ValueError, match="declared change"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "declared"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("identity",),
            changed=("recorded",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            result=OperationResult("result"),
        )


def test_operation_source_domain_must_match_anchor_domain():
    with pytest.raises(ValueError, match="source domain"):
        LicensedTransition(
            anchor=Anchor("a", "DOMAIN_A"),
            before_state=State("before"),
            operation=Operation(
                "op",
                "component",
                source_domain="DOMAIN_B",
                target_domain="DOMAIN_C",
            ),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("identity",),
            changed=("component",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            result=OperationResult("result"),
        )


def test_operation_source_domain_matching_anchor_domain_is_accepted():
    transition = LicensedTransition(
        anchor=Anchor("a", "DOMAIN_A"),
        before_state=State("before"),
        operation=Operation(
            "op",
            "component",
            source_domain="DOMAIN_A",
            target_domain="DOMAIN_C",
        ),
        after_state=State("after"),
        evidence=(Evidence(Claim("supported"), "record"),),
        preserved=("identity",),
        changed=("component",),
        trace=Trace(("started",)),
        residuals=(),
        outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
        result=OperationResult("result"),
    )

    assert transition.operation.source_domain == transition.anchor.domain


def test_operation_without_source_domain_is_accepted():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert transition.operation.source_domain is None


def test_branch_birth_requires_preserved_information():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="preserved information"):
        LicensedTransition(
            anchor=anchor,
            before_state=State("before"),
            operation=Operation("op", "new"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=(),
            changed=("new",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=OperationResult("result"),
            branch_origin_provenance=BranchOriginProvenance(anchor),
        )


def test_branch_birth_requires_explicit_origin_provenance():
    with pytest.raises(ValueError, match="origin provenance"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "new"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("origin-data",),
            changed=("new",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=OperationResult("result"),
        )


def test_branch_origin_provenance_must_match_transition_anchor():
    with pytest.raises(ValueError, match="transition anchor"):
        LicensedTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "new"),
            after_state=State("after"),
            evidence=(Evidence(Claim("supported"), "record"),),
            preserved=("origin-data",),
            changed=("new",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.CERTIFIED_BRANCH_BIRTH,
            result=OperationResult("result"),
            branch_origin_provenance=BranchOriginProvenance(Anchor("other", "D")),
        )


def test_successful_decision_contains_a_transition():
    decision = TransitionDecision(
        Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
        make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
    )
    assert decision.transition is not None


def test_successful_decision_must_match_transition_outcome():
    with pytest.raises(ValueError, match="outcomes must match"):
        TransitionDecision(
            Outcome.CERTIFIED_BRANCH_BIRTH,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
        )
