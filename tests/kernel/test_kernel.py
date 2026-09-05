import pytest

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
    Claim,
    ClaimEvidenceBinding,
    DecisionReasonCode,
    Evidence,
    NonSuccessDecisionAudit,
    Operation,
    OperationResult,
    Outcome,
    Residual,
    State,
    StructuralAdmissionGate,
    StructurallyAdmissibleTransition,
    Trace,
    TransitionCandidate,
    TransitionDecision,
    TransitionKind,
)


class _DefaultProvenance:
    pass


# Distinguishes omitted provenance from an explicit None in branch-birth tests.
_DEFAULT_PROVENANCE = _DefaultProvenance()

_KIND_FOR_OUTCOME = {
    Outcome.IDENTITY_PRESERVING_TRANSFORMATION: (
        TransitionKind.IDENTITY_PRESERVATION_CLAIM
    ),
    Outcome.CERTIFIED_BRANCH_BIRTH: TransitionKind.BRANCH_BIRTH_CLAIM,
}


def claim(claim_id: str = "claim-1", statement: str = "supported") -> Claim:
    return Claim(claim_id, statement)


def evidence(claim_id: str = "claim-1", basis: str = "record") -> Evidence:
    return Evidence(claim_id, basis)


def make_candidate(
    outcome: Outcome,
    preserved: tuple[str, ...] = ("identity",),
    changed: tuple[str, ...] = ("component",),
    transition_claim: Claim | None = None,
    transition_evidence: tuple[Evidence, ...] | None = None,
    anchor: Anchor | None = None,
    operation: Operation | None = None,
    result: OperationResult | None = OperationResult("result"),
    branch_origin_provenance: (
        BranchOriginProvenance | _DefaultProvenance | None
    ) = _DEFAULT_PROVENANCE,
    target_anchor: Anchor | _DefaultProvenance | None = _DEFAULT_PROVENANCE,
    kind: TransitionKind | _DefaultProvenance | None = _DEFAULT_PROVENANCE,
) -> TransitionCandidate:
    anchor = anchor or Anchor("a", "D")
    transition_claim = transition_claim or claim()
    if transition_evidence is None:
        transition_evidence = (evidence(transition_claim.claim_id),)
    if target_anchor is _DEFAULT_PROVENANCE:
        if outcome is Outcome.CERTIFIED_BRANCH_BIRTH:
            target_anchor = Anchor("branch", "D")
        else:
            target_anchor = anchor
    if (
        branch_origin_provenance is _DEFAULT_PROVENANCE
        and outcome is Outcome.CERTIFIED_BRANCH_BIRTH
    ):
        branch_origin_provenance = BranchOriginProvenance(
            origin_anchor=anchor,
            branch_anchor=target_anchor,
            preserved_components=preserved,
        )
    if branch_origin_provenance is _DEFAULT_PROVENANCE:
        branch_origin_provenance = None
    if kind is _DEFAULT_PROVENANCE:
        kind = _KIND_FOR_OUTCOME.get(outcome)
    return TransitionCandidate(
        anchor=anchor,
        before_state=State("before"),
        operation=operation or Operation("op", "component"),
        after_state=State("after"),
        claim=transition_claim,
        evidence=transition_evidence,
        preserved=preserved,
        changed=changed,
        trace=Trace(("started",)),
        residuals=(Residual("remainder"),),
        outcome=outcome,
        result=result,
        branch_origin_provenance=branch_origin_provenance,
        target_anchor=target_anchor,
        kind=kind,
    )


def make_audit(
    candidate: TransitionCandidate | None = None,
) -> NonSuccessDecisionAudit:
    if candidate is not None:
        trace = candidate.trace
        residuals = candidate.residuals
    else:
        trace = Trace(("assessed",))
        residuals = (Residual("remainder"),)
    return NonSuccessDecisionAudit(
        trace=trace,
        residuals=residuals,
        reason="structural admission refused",
        candidate=candidate,
    )


def admit_candidate(candidate: TransitionCandidate) -> StructurallyAdmissibleTransition:
    return StructuralAdmissionGate.admit(candidate)


def make_transition(
    outcome: Outcome, preserved: tuple[str, ...] = ("identity",)
) -> StructurallyAdmissibleTransition:
    return admit_candidate(make_candidate(outcome, preserved=preserved))


def test_core_objects_are_immutable():
    anchor = Anchor("a", "D")
    with pytest.raises(AttributeError):
        anchor.domain = "other"  # type: ignore[misc]


def test_state_and_claim_evidence_binding_are_immutable_core_objects():
    state = State("opaque")
    binding = ClaimEvidenceBinding(claim(), (evidence(),))
    assert state.value == "opaque"
    assert binding.claim.statement == "supported"
    with pytest.raises(AttributeError):
        binding.claim = claim("claim-2", "changed")  # type: ignore[misc]


def test_trace_and_residual_are_preserved():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert transition.trace.events == ("started",)
    assert transition.residuals == (Residual("remainder"),)


def test_structurally_admissible_transition_cannot_be_constructed_directly():
    with pytest.raises(ValueError, match="StructuralAdmissionGate"):
        StructurallyAdmissibleTransition(
            anchor=Anchor("a", "D"),
            before_state=State("before"),
            operation=Operation("op", "component"),
            after_state=State("after"),
            claim=claim(),
            evidence=(evidence(),),
            preserved=("identity",),
            changed=("component",),
            trace=Trace(("started",)),
            residuals=(),
            outcome=Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            result=OperationResult("result"),
        )


def test_structural_admission_gate_issues_successful_transition():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert isinstance(transition, StructurallyAdmissibleTransition)


def test_structural_admission_gate_rejects_already_admitted_transition():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    with pytest.raises(ValueError, match="re-admitted"):
        StructuralAdmissionGate.admit(transition)


def test_identity_preserving_requires_declared_invariant():
    with pytest.raises(ValueError, match="invariant"):
        admit_candidate(
            make_candidate(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, preserved=())
        )


def test_identity_preserving_requires_declared_change():
    with pytest.raises(ValueError, match="declared change"):
        admit_candidate(
            make_candidate(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, changed=())
        )


def test_preserved_and_changed_must_be_disjoint():
    with pytest.raises(ValueError, match="disjoint"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                preserved=("component",),
                changed=("component",),
            )
        )


def test_branch_birth_is_distinct_from_identity_preservation():
    assert (
        make_transition(Outcome.CERTIFIED_BRANCH_BIRTH).outcome
        is not Outcome.IDENTITY_PRESERVING_TRANSFORMATION
    )


def test_admitted_transition_carries_the_matching_claimed_kind():
    identity_transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert identity_transition.kind is TransitionKind.IDENTITY_PRESERVATION_CLAIM
    branch_transition = make_transition(Outcome.CERTIFIED_BRANCH_BIRTH)
    assert branch_transition.kind is TransitionKind.BRANCH_BIRTH_CLAIM


def test_successful_outcome_requires_a_declared_kind():
    with pytest.raises(ValueError, match="declared transition kind"):
        make_candidate(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, kind=None)


def test_declared_kind_must_match_the_outcome():
    with pytest.raises(ValueError, match="must match the candidate's outcome"):
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            kind=TransitionKind.BRANCH_BIRTH_CLAIM,
        )


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_transition_outcomes_cannot_declare_a_kind(outcome: Outcome):
    with pytest.raises(ValueError, match="cannot declare a claimed transition kind"):
        make_candidate(
            outcome, result=None, kind=TransitionKind.IDENTITY_PRESERVATION_CLAIM
        )


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_transition_outcomes_default_to_no_kind(outcome: Outcome):
    candidate = make_candidate(outcome, result=None)
    assert candidate.kind is None


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_outcomes_are_not_successes(outcome: Outcome):
    with pytest.raises(ValueError, match="non-transition"):
        make_transition(outcome)


def test_non_transition_decision_cannot_contain_a_transition():
    with pytest.raises(ValueError, match="non-transition"):
        TransitionDecision(
            Outcome.BLOCK,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
            make_audit(),
        )


def test_success_without_evidence_is_rejected():
    with pytest.raises(ValueError, match="evidence"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                transition_evidence=(),
            )
        )


def test_success_without_result_is_rejected():
    with pytest.raises(ValueError, match="result"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                result=None,
            )
        )


def test_claim_evidence_binding_without_evidence_is_rejected():
    with pytest.raises(ValueError, match="evidence"):
        ClaimEvidenceBinding(claim(), ())


def test_claim_evidence_binding_rejects_evidence_for_another_claim_id():
    with pytest.raises(ValueError, match="binding claim"):
        ClaimEvidenceBinding(claim("claim-1", "same"), (evidence("claim-2"),))


def test_same_statement_does_not_make_same_claim_identity():
    transition_claim = claim("claim-1", "same statement")
    unrelated_evidence = evidence("claim-2")
    with pytest.raises(ValueError, match="transition evidence"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                transition_claim=transition_claim,
                transition_evidence=(unrelated_evidence,),
            )
        )


def test_transition_evidence_bound_to_transition_claim_is_accepted():
    transition_claim = claim("claim-1", "transition claim")
    transition = admit_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            transition_claim=transition_claim,
            transition_evidence=(evidence(transition_claim.claim_id),),
        )
    )

    assert transition.evidence[0].claim_id == transition.claim.claim_id


def test_transition_change_must_include_operation_declared_change():
    with pytest.raises(ValueError, match="declared change"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                operation=Operation("op", "declared"),
                changed=("recorded",),
            )
        )


def test_operation_source_domain_must_match_anchor_domain():
    with pytest.raises(ValueError, match="source domain"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                anchor=Anchor("a", "DOMAIN_A"),
                operation=Operation(
                    "op",
                    "component",
                    source_domain="DOMAIN_B",
                    target_domain="DOMAIN_C",
                ),
            )
        )


def test_operation_source_domain_matching_anchor_domain_is_accepted():
    transition = admit_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            anchor=Anchor("a", "DOMAIN_A"),
            operation=Operation(
                "op",
                "component",
                source_domain="DOMAIN_A",
            ),
        )
    )

    assert transition.operation.source_domain == transition.anchor.domain


def test_operation_without_source_domain_is_accepted():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert transition.operation.source_domain is None


def test_branch_birth_requires_preserved_information():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="preserved information"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=(),
                changed=("new",),
                anchor=anchor,
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    origin_anchor=anchor,
                    branch_anchor=Anchor("branch", "D"),
                    preserved_components=("origin-data",),
                ),
            )
        )


def test_branch_birth_requires_explicit_origin_provenance():
    with pytest.raises(ValueError, match="origin provenance"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=None,
            )
        )


def test_branch_origin_provenance_requires_preserved_components():
    with pytest.raises(ValueError, match="preserved components"):
        BranchOriginProvenance(
            origin_anchor=Anchor("a", "D"),
            branch_anchor=Anchor("branch", "D"),
            preserved_components=(),
        )


def test_branch_origin_provenance_requires_distinct_branch_anchor():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="distinct branch anchor"):
        BranchOriginProvenance(anchor, anchor, ("origin-data",))


def test_branch_origin_provenance_must_match_transition_anchor():
    with pytest.raises(ValueError, match="transition anchor"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    Anchor("other", "D"), Anchor("branch", "D"), ("origin-data",)
                ),
            )
        )


def test_branch_origin_provenance_branch_anchor_must_be_target_anchor():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="target anchor"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                anchor=anchor,
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    anchor, Anchor("other-branch", "D"), ("origin-data",)
                ),
            )
        )


def test_branch_origin_provenance_components_must_be_declared_preserved():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="declared preserved"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                anchor=anchor,
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    anchor, Anchor("branch", "D"), ("invented-origin-data",)
                ),
            )
        )


@pytest.mark.parametrize(
    "factory,args,error",
    [
        (Anchor, (" ", "D"), "anchor"),
        (Anchor, ("a", " "), "anchor"),
        (Claim, (" ", "statement"), "claim"),
        (Claim, ("claim-1", " "), "claim"),
        (Evidence, (" ", "basis"), "evidence"),
        (Evidence, ("claim-1", " "), "evidence"),
        (Operation, (" ", "change"), "operation"),
        (Operation, ("op", " "), "operation"),
        (Operation, ("op", "change", " "), "source domain"),
        (Operation, ("op", "change", None, " "), "target domain"),
        (Residual, (" ",), "residual"),
        (Trace, ((" ",),), "trace"),
    ],
)
def test_blank_structural_names_are_rejected(
    factory: object, args: tuple[object, ...], error: str
):
    with pytest.raises(ValueError, match=error):
        factory(*args)  # type: ignore[operator]


@pytest.mark.parametrize(
    "preserved,changed,error",
    [
        ((" ",), ("component",), "preserved components"),
        (("identity", "identity"), ("component",), "preserved components"),
        (("identity",), (" ",), "changed components"),
        (("identity",), ("component", "component"), "changed components"),
    ],
)
def test_malformed_transition_components_are_rejected(
    preserved: tuple[str, ...], changed: tuple[str, ...], error: str
):
    with pytest.raises(ValueError, match=error):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                preserved=preserved,
                changed=changed,
            )
        )


def test_successful_decision_contains_a_transition():
    decision = TransitionDecision(
        Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
        make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
    )
    assert decision.admissible is not None


def test_successful_decision_must_match_transition_outcome():
    with pytest.raises(ValueError, match="outcomes must match"):
        TransitionDecision(
            Outcome.CERTIFIED_BRANCH_BIRTH,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
        )


def test_successful_decision_cannot_carry_a_non_success_audit():
    with pytest.raises(ValueError, match="non-success audit"):
        TransitionDecision(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
            make_audit(),
        )


def test_identity_preserving_rejects_a_distinct_target_anchor():
    with pytest.raises(ValueError, match="unchanged anchor"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                target_anchor=Anchor("other", "D"),
            )
        )


def test_identity_preserving_accepts_target_anchor_equal_to_source():
    anchor = Anchor("a", "D")
    transition = admit_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            anchor=anchor,
            target_anchor=anchor,
        )
    )
    assert transition.target_anchor == transition.anchor


def test_branch_birth_rejects_target_anchor_equal_to_source():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="distinct target anchor"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                anchor=anchor,
                operation=Operation("op", "new"),
                target_anchor=anchor,
                branch_origin_provenance=BranchOriginProvenance(
                    anchor, Anchor("branch", "D"), ("origin-data",)
                ),
            )
        )


def test_branch_birth_binds_target_anchor_to_provenance_branch():
    anchor = Anchor("a", "D")
    target = Anchor("branch", "D")
    transition = admit_candidate(
        make_candidate(
            Outcome.CERTIFIED_BRANCH_BIRTH,
            anchor=anchor,
            target_anchor=target,
        )
    )
    provenance = transition.branch_origin_provenance
    assert provenance is not None
    assert provenance.origin_anchor == transition.anchor
    assert provenance.branch_anchor == transition.target_anchor == target
    assert transition.target_anchor != transition.anchor


def test_branch_origin_provenance_origin_must_match_source_anchor():
    with pytest.raises(ValueError, match="transition anchor"):
        admit_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    Anchor("other", "D"), Anchor("branch", "D"), ("origin-data",)
                ),
            )
        )


def test_operation_target_domain_must_match_target_anchor_domain():
    anchor = Anchor("a", "DOMAIN_A")
    with pytest.raises(ValueError, match="target domain"):
        admit_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                anchor=anchor,
                operation=Operation(
                    "op",
                    "component",
                    source_domain="DOMAIN_A",
                    target_domain="DOMAIN_C",
                ),
            )
        )


def test_operation_target_domain_matching_target_anchor_domain_is_accepted():
    transition = admit_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            anchor=Anchor("a", "DOMAIN_A"),
            operation=Operation(
                "op",
                "component",
                source_domain="DOMAIN_A",
                target_domain="DOMAIN_A",
            ),
        )
    )
    assert transition.operation.target_domain == transition.anchor.domain


def test_cross_domain_branch_birth_is_structurally_representable():
    origin = Anchor("a", "DOMAIN_A")
    target = Anchor("branch", "DOMAIN_B")
    transition = admit_candidate(
        make_candidate(
            Outcome.CERTIFIED_BRANCH_BIRTH,
            anchor=origin,
            operation=Operation(
                "op",
                "component",
                source_domain="DOMAIN_A",
                target_domain="DOMAIN_B",
            ),
            target_anchor=target,
        )
    )
    provenance = transition.branch_origin_provenance
    assert provenance is not None
    assert provenance.branch_anchor.domain != provenance.origin_anchor.domain
    assert transition.operation.target_domain == target.domain


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_decisions_cannot_contain_a_transition(outcome: Outcome):
    with pytest.raises(ValueError, match="non-transition"):
        TransitionDecision(
            outcome,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
            make_audit(),
        )


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_decisions_require_an_audit(outcome: Outcome):
    with pytest.raises(ValueError, match="audit"):
        TransitionDecision(outcome)


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_decisions_preserve_trace_and_residuals(outcome: Outcome):
    decision = TransitionDecision(outcome, audit=make_audit())
    assert decision.audit is not None
    assert decision.audit.trace.events == ("assessed",)
    assert decision.audit.residuals == (Residual("remainder"),)


def test_non_success_decisions_preserve_the_assessed_candidate():
    candidate = make_candidate(Outcome.BLOCK, result=None)
    decision = TransitionDecision(Outcome.BLOCK, audit=make_audit(candidate))
    assert decision.audit is not None
    assert decision.audit.candidate is candidate


def test_non_success_audit_rejects_an_admitted_transition_as_candidate():
    with pytest.raises(ValueError, match="structurally admissible transition"):
        make_audit(make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION))


def test_non_success_decision_audit_accepts_an_optional_reason_code():
    audit = NonSuccessDecisionAudit(
        trace=Trace(("assessed",)),
        residuals=(),
        reason="target anchor mismatch",
        reason_code=DecisionReasonCode.TARGET_ANCHOR_MISMATCH,
    )
    assert audit.reason_code is DecisionReasonCode.TARGET_ANCHOR_MISMATCH
    assert audit.reason == "target anchor mismatch"


@pytest.mark.parametrize("reason_code", list(DecisionReasonCode))
def test_non_success_decision_audit_accepts_every_reason_code(
    reason_code: DecisionReasonCode,
):
    audit = NonSuccessDecisionAudit(
        trace=Trace(("assessed",)),
        residuals=(),
        reason="structural admission refused",
        reason_code=reason_code,
    )
    assert audit.reason_code is reason_code


def test_non_success_decision_audit_reason_code_defaults_to_none():
    audit = NonSuccessDecisionAudit(
        trace=Trace(("assessed",)),
        residuals=(),
        reason="structural admission refused",
    )
    assert audit.reason_code is None


@pytest.mark.parametrize("reason", ["", "  "])
def test_non_success_decisions_require_a_non_blank_reason(reason: str):
    with pytest.raises(ValueError, match="structural reason"):
        NonSuccessDecisionAudit(
            trace=Trace(("assessed",)),
            residuals=(),
            reason=reason,
        )


def test_undefined_decision_is_representable_without_a_candidate():
    decision = TransitionDecision(Outcome.UNDEFINED, audit=make_audit())
    assert decision.audit is not None
    assert decision.audit.candidate is None


def test_candidate_cannot_be_audited_with_another_trace():
    candidate = make_candidate(Outcome.BLOCK, result=None)
    with pytest.raises(ValueError, match="candidate trace"):
        NonSuccessDecisionAudit(
            trace=Trace(("fabricated",)),
            residuals=candidate.residuals,
            reason="structural admission refused",
            candidate=candidate,
        )


def test_candidate_cannot_be_audited_with_other_residuals():
    candidate = make_candidate(Outcome.BLOCK, result=None)
    with pytest.raises(ValueError, match="candidate"):
        NonSuccessDecisionAudit(
            trace=candidate.trace,
            residuals=(Residual("invented"),),
            reason="structural admission refused",
            candidate=candidate,
        )


def test_audit_bound_to_candidate_preserves_the_candidate_history():
    candidate = make_candidate(Outcome.DEFER, result=None)
    decision = TransitionDecision(Outcome.DEFER, audit=make_audit(candidate))
    assert decision.audit is not None
    assert decision.audit.trace == candidate.trace
    assert decision.audit.residuals == candidate.residuals
    assert decision.audit.candidate is candidate


@pytest.mark.parametrize(
    "outcome",
    [Outcome.IDENTITY_PRESERVING_TRANSFORMATION, Outcome.CERTIFIED_BRANCH_BIRTH],
)
def test_success_without_explicit_target_anchor_cannot_be_admitted(outcome: Outcome):
    with pytest.raises(ValueError, match="explicit target anchor"):
        admit_candidate(make_candidate(outcome, target_anchor=None))


def test_explicit_target_anchor_equal_to_source_is_admitted():
    anchor = Anchor("a", "D")
    transition = admit_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            anchor=anchor,
            target_anchor=anchor,
        )
    )
    assert transition.target_anchor is anchor
