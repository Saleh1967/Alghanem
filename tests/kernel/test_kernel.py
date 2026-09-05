"""Foundational kernel test suite.

This module enforces constitutional constraints for the language-agnostic
kernel: immutable core objects, explicit provenance, candidate validation,
evidence-claim binding, strict separation between claimed TransitionKind and
certified outcomes, and structural admission decision invariants.
"""

from __future__ import annotations

import typing

import pytest

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
    CertifiedOutcome,
    Claim,
    ClaimEvidenceBinding,
    DecisionReasonCode,
    Evidence,
    InvariantExtractionError,
    InvariantExtractorRegistry,
    InvariantObservation,
    InvariantSpec,
    InvariantVerification,
    InvariantVerificationGate,
    NonSuccessDecisionAudit,
    Operation,
    OperationResult,
    Residual,
    State,
    StructuralAdmissionDecision,
    StructuralAdmissionError,
    StructuralAdmissionGate,
    StructuralDecisionStatus,
    StructurallyAdmissibleTransition,
    Trace,
    TransitionCandidate,
    TransitionKind,
    UnregisteredExtractorError,
)


class _DefaultProvenance:
    pass


_DEFAULT_PROVENANCE = _DefaultProvenance()


def claim(claim_id: str = "claim-1", statement: str = "supported") -> Claim:
    return Claim(claim_id, statement)


def evidence(claim_id: str = "claim-1", basis: str = "proof") -> Evidence:
    return Evidence(claim_id, basis)


def make_candidate(
    kind: TransitionKind = TransitionKind.IDENTITY_PRESERVATION_CLAIM,
    anchor: Anchor | None = None,
    preserved: tuple[str, ...] = ("identity",),
    changed: tuple[str, ...] = ("component",),
    operation: Operation | None = None,
    branch_origin_provenance: (
        BranchOriginProvenance | _DefaultProvenance | None
    ) = _DEFAULT_PROVENANCE,
    target_anchor: Anchor | _DefaultProvenance | None = _DEFAULT_PROVENANCE,
    transition_claim: Claim | None = None,
    transition_evidence: tuple[Evidence, ...] | None = None,
    result: OperationResult | None = OperationResult("result"),
) -> TransitionCandidate:
    source_anchor = anchor or Anchor("a", "D")
    resolved_claim = claim() if transition_claim is None else transition_claim
    resolved_evidence = (
        (evidence(resolved_claim.claim_id),)
        if transition_evidence is None
        else transition_evidence
    )
    resolved_operation = operation or Operation("op", "component")

    resolved_target_anchor: Anchor | None
    if target_anchor is _DEFAULT_PROVENANCE:
        if kind is TransitionKind.BRANCH_BIRTH_CLAIM:
            resolved_target_anchor = Anchor("branch", "D")
        else:
            resolved_target_anchor = source_anchor
    else:
        resolved_target_anchor = target_anchor  # type: ignore[assignment]

    resolved_provenance: BranchOriginProvenance | None
    if (
        branch_origin_provenance is _DEFAULT_PROVENANCE
        and kind is TransitionKind.BRANCH_BIRTH_CLAIM
    ):
        resolved_provenance = BranchOriginProvenance(
            origin_anchor=source_anchor,
            branch_anchor=resolved_target_anchor,  # type: ignore[arg-type]
            preserved_components=preserved,
        )
    elif branch_origin_provenance is _DEFAULT_PROVENANCE:
        resolved_provenance = None
    else:
        resolved_provenance = branch_origin_provenance  # type: ignore[assignment]

    return TransitionCandidate(
        anchor=source_anchor,
        target_anchor=resolved_target_anchor,
        before_state=State("before"),
        operation=resolved_operation,
        after_state=State("after"),
        claim=resolved_claim,
        evidence=resolved_evidence,
        preserved=preserved,
        changed=changed,
        trace=Trace(("started",)),
        residuals=(Residual("remainder"),),
        kind=kind,
        branch_origin_provenance=resolved_provenance,
        result=result,
    )


def make_audit(
    candidate: TransitionCandidate | None = None,
) -> NonSuccessDecisionAudit:
    return NonSuccessDecisionAudit(
        trace=candidate.trace if candidate is not None else Trace(("assessed",)),
        residuals=(
            candidate.residuals if candidate is not None else (Residual("remainder"),)
        ),
        reason="structural admission refused",
        candidate=candidate,
    )


def admit_candidate(
    candidate: TransitionCandidate,
) -> StructurallyAdmissibleTransition:
    return StructuralAdmissionGate.require_admitted(candidate)


def make_transition(
    kind: TransitionKind = TransitionKind.IDENTITY_PRESERVATION_CLAIM,
    preserved: tuple[str, ...] = ("identity",),
) -> StructurallyAdmissibleTransition:
    return admit_candidate(make_candidate(kind=kind, preserved=preserved))


def test_core_objects_are_immutable() -> None:
    anchor = Anchor("a", "D")
    with pytest.raises(AttributeError):
        anchor.domain = "other"  # type: ignore[misc]


def test_state_and_claim_evidence_binding_are_immutable_core_objects() -> None:
    state = State("opaque")
    binding = ClaimEvidenceBinding(claim(), (evidence(),))
    assert state.value == "opaque"
    assert binding.claim.statement == "supported"
    with pytest.raises(AttributeError):
        binding.claim = claim("claim-2", "changed")  # type: ignore[misc]


def test_trace_and_residual_are_preserved() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert transition.trace.events == ("started",)
    assert transition.residuals == (Residual("remainder"),)


def test_structurally_admissible_transition_cannot_be_constructed_directly() -> None:
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
            kind=TransitionKind.IDENTITY_PRESERVATION_CLAIM,
            result=OperationResult("result"),
        )


def test_structural_admission_gate_issues_successful_transition() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert isinstance(transition, StructurallyAdmissibleTransition)


def test_structural_admission_assessment_issues_an_admitted_decision() -> None:
    decision = StructuralAdmissionGate.assess(make_candidate())
    assert decision.status is StructuralDecisionStatus.ADMITTED
    assert isinstance(decision.transition, StructurallyAdmissibleTransition)
    assert decision.audit is None


def test_structural_admission_assessment_records_structural_failure() -> None:
    candidate = make_candidate(result=None)
    decision = StructuralAdmissionGate.assess(candidate)
    assert decision.status is StructuralDecisionStatus.BLOCK
    assert decision.transition is None
    assert decision.audit is not None
    assert decision.audit.candidate is candidate
    assert decision.audit.trace is candidate.trace
    assert decision.audit.residuals is candidate.residuals
    assert "result" in decision.audit.reason


def test_require_admitted_preserves_block_audit_in_typed_error() -> None:
    candidate = make_candidate(result=None)
    with pytest.raises(StructuralAdmissionError) as raised:
        StructuralAdmissionGate.require_admitted(candidate)

    decision = raised.value.decision
    assert decision.status is StructuralDecisionStatus.BLOCK
    assert decision.transition is None
    assert decision.audit is not None
    assert decision.audit.candidate is candidate
    assert decision.audit.trace is candidate.trace
    assert decision.audit.residuals is candidate.residuals
    assert str(raised.value) == decision.audit.reason


def test_structural_admission_gate_rejects_already_admitted_transition() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    with pytest.raises(ValueError, match="re-admitted"):
        StructuralAdmissionGate.require_admitted(transition)


def test_identity_preserving_requires_declared_invariant() -> None:
    with pytest.raises(ValueError, match="invariant"):
        admit_candidate(
            make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, preserved=())
        )


def test_identity_preserving_requires_declared_change() -> None:
    with pytest.raises(ValueError, match="declared change"):
        admit_candidate(
            make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, changed=())
        )


def test_preserved_and_changed_must_be_disjoint() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                preserved=("component",),
                changed=("component",),
            )
        )


def test_branch_birth_is_distinct_from_identity_preservation() -> None:
    assert (
        make_transition(TransitionKind.BRANCH_BIRTH_CLAIM).kind
        is not TransitionKind.IDENTITY_PRESERVATION_CLAIM
    )


def test_admitted_transition_carries_the_matching_claimed_kind() -> None:
    identity_transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert identity_transition.kind is TransitionKind.IDENTITY_PRESERVATION_CLAIM
    branch_transition = make_transition(TransitionKind.BRANCH_BIRTH_CLAIM)
    assert branch_transition.kind is TransitionKind.BRANCH_BIRTH_CLAIM


def test_candidate_requires_a_declared_kind() -> None:
    with pytest.raises(ValueError, match="declared TransitionKind"):
        make_candidate(kind="INVALID")  # type: ignore[arg-type]


def test_candidate_does_not_carry_its_own_decision() -> None:
    candidate = make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert not hasattr(candidate, "outcome")
    assert not hasattr(candidate, "status")
    assert candidate.kind is TransitionKind.IDENTITY_PRESERVATION_CLAIM


def test_block_is_decision_not_candidate_property() -> None:
    candidate = make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, result=None)
    audit = make_audit(candidate)
    decision = StructuralAdmissionDecision(
        status=StructuralDecisionStatus.BLOCK,
        audit=audit,
    )
    assert decision.status is StructuralDecisionStatus.BLOCK
    assert decision.transition is None
    assert decision.audit is audit
    assert decision.audit.candidate is candidate
    assert candidate.kind is TransitionKind.IDENTITY_PRESERVATION_CLAIM
    assert not hasattr(candidate, "status")


def test_structurally_admissible_transition_does_not_carry_certified_outcome() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert transition.kind is TransitionKind.IDENTITY_PRESERVATION_CLAIM
    assert not hasattr(transition, "outcome")


def test_certified_outcome_cannot_exist_before_certification() -> None:
    outcome_members = set(CertifiedOutcome)
    assert CertifiedOutcome.IDENTITY_PRESERVING_TRANSFORMATION in outcome_members
    assert CertifiedOutcome.CERTIFIED_BRANCH_BIRTH in outcome_members
    assert len(outcome_members) == 2


def test_structural_cannot_be_used_as_evidential() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert isinstance(transition, StructurallyAdmissibleTransition)
    assert len(transition.evidence) > 0
    assert transition.evidence[0].claim_id == transition.claim.claim_id


def test_success_without_evidence_is_rejected() -> None:
    with pytest.raises(ValueError, match="evidence"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                transition_evidence=(),
            )
        )


def test_success_without_result_is_rejected() -> None:
    with pytest.raises(ValueError, match="result"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                result=None,
            )
        )


def test_claim_evidence_binding_without_evidence_is_rejected() -> None:
    with pytest.raises(ValueError, match="evidence"):
        ClaimEvidenceBinding(claim(), ())


def test_claim_evidence_binding_rejects_evidence_for_another_claim_id() -> None:
    with pytest.raises(ValueError, match="binding claim"):
        ClaimEvidenceBinding(claim("claim-1", "same"), (evidence("claim-2"),))


def test_same_statement_does_not_make_same_claim_identity() -> None:
    transition_claim = claim("claim-1", "same statement")
    unrelated_evidence = evidence("claim-2")
    with pytest.raises(ValueError, match="transition evidence"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                transition_claim=transition_claim,
                transition_evidence=(unrelated_evidence,),
            )
        )


def test_transition_evidence_bound_to_transition_claim_is_accepted() -> None:
    transition_claim = claim("claim-1", "transition claim")
    transition = admit_candidate(
        make_candidate(
            TransitionKind.IDENTITY_PRESERVATION_CLAIM,
            transition_claim=transition_claim,
            transition_evidence=(evidence(transition_claim.claim_id),),
        )
    )

    assert transition.evidence[0].claim_id == transition.claim.claim_id


def test_transition_change_must_include_operation_declared_change() -> None:
    with pytest.raises(ValueError, match="declared change"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                operation=Operation("op", "declared"),
                changed=("recorded",),
            )
        )


def test_operation_source_domain_must_match_anchor_domain() -> None:
    with pytest.raises(ValueError, match="source domain"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                anchor=Anchor("a", "DOMAIN_A"),
                operation=Operation(
                    "op",
                    "component",
                    source_domain="DOMAIN_B",
                    target_domain="DOMAIN_C",
                ),
            )
        )


def test_operation_source_domain_matching_anchor_domain_is_accepted() -> None:
    transition = admit_candidate(
        make_candidate(
            TransitionKind.IDENTITY_PRESERVATION_CLAIM,
            anchor=Anchor("a", "DOMAIN_A"),
            operation=Operation(
                "op",
                "component",
                source_domain="DOMAIN_A",
            ),
        )
    )

    assert transition.operation.source_domain == transition.anchor.domain


def test_operation_without_source_domain_is_accepted() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    assert transition.operation.source_domain is None


def test_branch_birth_requires_preserved_information() -> None:
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="preserved information"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
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


def test_branch_birth_requires_explicit_origin_provenance() -> None:
    with pytest.raises(ValueError, match="origin provenance"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=None,
            )
        )


def test_branch_origin_provenance_requires_preserved_components() -> None:
    with pytest.raises(ValueError, match="preserved components"):
        BranchOriginProvenance(
            origin_anchor=Anchor("a", "D"),
            branch_anchor=Anchor("branch", "D"),
            preserved_components=(),
        )


def test_branch_origin_provenance_requires_distinct_branch_anchor() -> None:
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="distinct branch anchor"):
        BranchOriginProvenance(anchor, anchor, ("origin-data",))


def test_branch_origin_provenance_must_match_transition_anchor() -> None:
    with pytest.raises(ValueError, match="transition anchor"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    Anchor("other", "D"), Anchor("branch", "D"), ("origin-data",)
                ),
            )
        )


def test_branch_origin_provenance_branch_anchor_must_be_target_anchor() -> None:
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="target anchor"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    anchor, Anchor("other-branch", "D"), ("origin-data",)
                ),
            )
        )


def test_branch_origin_provenance_components_must_be_declared_preserved() -> None:
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="declared preserved"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    anchor, Anchor("branch", "D"), ("invented-origin-data",)
                ),
            )
        )


def test_branch_origin_provenance_must_account_for_all_declared_preserved() -> None:
    anchor = Anchor("a", "D")
    candidate = make_candidate(
        TransitionKind.BRANCH_BIRTH_CLAIM,
        preserved=("origin-data", "unproven-data"),
        changed=("new",),
        operation=Operation("op", "new"),
        branch_origin_provenance=BranchOriginProvenance(
            anchor, Anchor("branch", "D"), ("origin-data",)
        ),
    )

    decision = StructuralAdmissionGate.assess(candidate)

    assert decision.status is StructuralDecisionStatus.BLOCK
    assert decision.transition is None
    assert decision.audit is not None
    assert decision.audit.candidate is candidate
    assert "exactly match" in decision.audit.reason


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
) -> None:
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
) -> None:
    with pytest.raises(ValueError, match=error):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                preserved=preserved,
                changed=changed,
            )
        )


def test_successful_decision_contains_a_transition() -> None:
    transition = make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM)
    decision = StructuralAdmissionDecision(
        status=StructuralDecisionStatus.ADMITTED,
        transition=transition,
    )
    assert decision.transition is not None
    assert decision.admissible is transition


def test_successful_decision_cannot_carry_a_non_success_audit() -> None:
    with pytest.raises(ValueError, match="non-success audit"):
        StructuralAdmissionDecision(
            status=StructuralDecisionStatus.ADMITTED,
            transition=make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM),
            audit=make_audit(),
        )


def test_identity_preserving_rejects_a_distinct_target_anchor() -> None:
    with pytest.raises(ValueError, match="unchanged anchor"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                target_anchor=Anchor("other", "D"),
            )
        )


def test_identity_preserving_accepts_target_anchor_equal_to_source() -> None:
    anchor = Anchor("a", "D")
    transition = admit_candidate(
        make_candidate(
            TransitionKind.IDENTITY_PRESERVATION_CLAIM,
            anchor=anchor,
            target_anchor=anchor,
        )
    )
    assert transition.target_anchor == transition.anchor


def test_branch_birth_rejects_target_anchor_equal_to_source() -> None:
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="distinct target anchor"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
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


def test_branch_birth_binds_target_anchor_to_provenance_branch() -> None:
    anchor = Anchor("a", "D")
    target = Anchor("branch", "D")
    transition = admit_candidate(
        make_candidate(
            TransitionKind.BRANCH_BIRTH_CLAIM,
            anchor=anchor,
            target_anchor=target,
        )
    )
    provenance = transition.branch_origin_provenance
    assert provenance is not None
    assert provenance.origin_anchor == transition.anchor
    assert provenance.branch_anchor == transition.target_anchor == target
    assert transition.target_anchor != transition.anchor


def test_branch_origin_provenance_origin_must_match_source_anchor() -> None:
    with pytest.raises(ValueError, match="transition anchor"):
        admit_candidate(
            make_candidate(
                TransitionKind.BRANCH_BIRTH_CLAIM,
                preserved=("origin-data",),
                changed=("new",),
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    Anchor("other", "D"), Anchor("branch", "D"), ("origin-data",)
                ),
            )
        )


def test_operation_target_domain_must_match_target_anchor_domain() -> None:
    anchor = Anchor("a", "DOMAIN_A")
    with pytest.raises(ValueError, match="target domain"):
        admit_candidate(
            make_candidate(
                TransitionKind.IDENTITY_PRESERVATION_CLAIM,
                anchor=anchor,
                operation=Operation(
                    "op",
                    "component",
                    source_domain="DOMAIN_A",
                    target_domain="DOMAIN_C",
                ),
            )
        )


def test_operation_target_domain_matching_target_anchor_domain_is_accepted() -> None:
    transition = admit_candidate(
        make_candidate(
            TransitionKind.IDENTITY_PRESERVATION_CLAIM,
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


def test_cross_domain_branch_birth_is_structurally_representable() -> None:
    origin = Anchor("a", "DOMAIN_A")
    target = Anchor("branch", "DOMAIN_B")
    transition = admit_candidate(
        make_candidate(
            TransitionKind.BRANCH_BIRTH_CLAIM,
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


@pytest.mark.parametrize(
    "status",
    [
        StructuralDecisionStatus.BLOCK,
        StructuralDecisionStatus.DEFER,
        StructuralDecisionStatus.UNDEFINED,
    ],
)
def test_non_success_decisions_cannot_contain_a_transition(
    status: StructuralDecisionStatus,
) -> None:
    with pytest.raises(ValueError, match="non-admitted"):
        StructuralAdmissionDecision(
            status=status,
            transition=make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM),
            audit=make_audit(),
        )


@pytest.mark.parametrize(
    "status",
    [
        StructuralDecisionStatus.BLOCK,
        StructuralDecisionStatus.DEFER,
        StructuralDecisionStatus.UNDEFINED,
    ],
)
def test_non_success_decisions_require_an_audit(
    status: StructuralDecisionStatus,
) -> None:
    with pytest.raises(ValueError, match="audit"):
        StructuralAdmissionDecision(status=status)


@pytest.mark.parametrize(
    "status",
    [
        StructuralDecisionStatus.BLOCK,
        StructuralDecisionStatus.DEFER,
        StructuralDecisionStatus.UNDEFINED,
    ],
)
def test_non_success_decisions_preserve_trace_and_residuals(
    status: StructuralDecisionStatus,
) -> None:
    decision = StructuralAdmissionDecision(status=status, audit=make_audit())
    assert decision.audit is not None
    assert decision.audit.trace.events == ("assessed",)
    assert decision.audit.residuals == (Residual("remainder"),)


def test_non_success_decisions_preserve_the_assessed_candidate() -> None:
    candidate = make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, result=None)
    decision = StructuralAdmissionDecision(
        status=StructuralDecisionStatus.BLOCK, audit=make_audit(candidate)
    )
    assert decision.audit is not None
    assert decision.audit.candidate is candidate


def test_non_success_audit_rejects_an_admitted_transition_as_candidate() -> None:
    with pytest.raises(ValueError, match="structurally admissible transition"):
        make_audit(make_transition(TransitionKind.IDENTITY_PRESERVATION_CLAIM))


def test_non_success_decision_audit_accepts_an_optional_reason_code() -> None:
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
) -> None:
    audit = NonSuccessDecisionAudit(
        trace=Trace(("assessed",)),
        residuals=(),
        reason="structural admission refused",
        reason_code=reason_code,
    )
    assert audit.reason_code is reason_code


def test_non_success_decision_audit_reason_code_defaults_to_none() -> None:
    audit = NonSuccessDecisionAudit(
        trace=Trace(("assessed",)),
        residuals=(),
        reason="structural admission refused",
    )
    assert audit.reason_code is None


def test_non_success_decision_audit_rejects_a_non_reason_code_value() -> None:
    with pytest.raises(ValueError, match="DecisionReasonCode"):
        NonSuccessDecisionAudit(
            trace=Trace(("assessed",)),
            residuals=(),
            reason="structural admission refused",
            reason_code="MISSING_EVIDENCE",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("reason", ["", "  "])
def test_non_success_decisions_require_a_non_blank_reason(reason: str) -> None:
    with pytest.raises(ValueError, match="structural reason"):
        NonSuccessDecisionAudit(
            trace=Trace(("assessed",)),
            residuals=(),
            reason=reason,
        )


def test_undefined_decision_is_representable_without_a_candidate() -> None:
    decision = StructuralAdmissionDecision(
        status=StructuralDecisionStatus.UNDEFINED, audit=make_audit()
    )
    assert decision.audit is not None
    assert decision.audit.candidate is None


def test_candidate_cannot_be_audited_with_another_trace() -> None:
    candidate = make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, result=None)
    with pytest.raises(ValueError, match="candidate trace"):
        NonSuccessDecisionAudit(
            trace=Trace(("fabricated",)),
            residuals=candidate.residuals,
            reason="structural admission refused",
            candidate=candidate,
        )


def test_candidate_cannot_be_audited_with_other_residuals() -> None:
    candidate = make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, result=None)
    with pytest.raises(ValueError, match="candidate"):
        NonSuccessDecisionAudit(
            trace=candidate.trace,
            residuals=(Residual("invented"),),
            reason="structural admission refused",
            candidate=candidate,
        )


def test_audit_bound_to_candidate_preserves_the_candidate_history() -> None:
    candidate = make_candidate(TransitionKind.IDENTITY_PRESERVATION_CLAIM, result=None)
    decision = StructuralAdmissionDecision(
        status=StructuralDecisionStatus.DEFER, audit=make_audit(candidate)
    )
    assert decision.audit is not None
    assert decision.audit.trace == candidate.trace
    assert decision.audit.residuals == candidate.residuals
    assert decision.audit.candidate is candidate


@pytest.mark.parametrize(
    "kind",
    [
        TransitionKind.IDENTITY_PRESERVATION_CLAIM,
        TransitionKind.BRANCH_BIRTH_CLAIM,
    ],
)
def test_success_without_explicit_target_anchor_cannot_be_admitted(
    kind: TransitionKind,
) -> None:
    with pytest.raises(ValueError, match="explicit target anchor"):
        admit_candidate(make_candidate(kind=kind, target_anchor=None))


def test_explicit_target_anchor_equal_to_source_is_admitted() -> None:
    anchor = Anchor("a", "D")
    transition = admit_candidate(
        make_candidate(
            TransitionKind.IDENTITY_PRESERVATION_CLAIM,
            anchor=anchor,
            target_anchor=anchor,
        )
    )
    assert transition.target_anchor is anchor


# --- Verified invariant preservation -----------------------------------


def test_invariant_spec_rejects_blank_fields() -> None:
    with pytest.raises(ValueError, match="invariant id"):
        InvariantSpec(invariant_id=" ", component="identity", extractor_id="x")
    with pytest.raises(ValueError, match="component"):
        InvariantSpec(invariant_id="inv-1", component=" ", extractor_id="x")
    with pytest.raises(ValueError, match="extractor id"):
        InvariantSpec(invariant_id="inv-1", component="identity", extractor_id=" ")


def test_invariant_observation_rejects_blank_invariant_id() -> None:
    with pytest.raises(ValueError, match="invariant id"):
        InvariantObservation(invariant_id=" ", before_value=1, after_value=1)


def test_invariant_verification_requires_matching_observation() -> None:
    observation = InvariantObservation(
        invariant_id="inv-1", before_value=1, after_value=1
    )
    with pytest.raises(ValueError, match="own observation"):
        InvariantVerification(
            invariant_id="inv-2",
            preserved=True,
            trace=Trace(("checked",)),
            observation=observation,
        )


def test_registry_rejects_blank_or_duplicate_extractor_ids() -> None:
    registry = InvariantExtractorRegistry()
    with pytest.raises(ValueError, match="blank"):
        registry.register(" ", lambda state: state.value)
    registry.register("identity-extractor", lambda state: state.value)
    with pytest.raises(ValueError, match="already registered"):
        registry.register("identity-extractor", lambda state: state.value)


def test_registry_resolve_raises_for_unregistered_id() -> None:
    registry = InvariantExtractorRegistry()
    with pytest.raises(UnregisteredExtractorError):
        registry.resolve("missing")


def test_invariant_gate_verifies_preserved_value() -> None:
    transition = make_transition()
    registry = InvariantExtractorRegistry()
    registry.register("constant-extractor", lambda state: "same")
    spec = InvariantSpec(
        invariant_id="inv-1", component="identity", extractor_id="constant-extractor"
    )
    verification = InvariantVerificationGate.verify(transition, spec, registry)
    assert verification.preserved is True
    assert verification.observation.before_value == "same"
    assert verification.observation.after_value == "same"
    assert verification.trace.events[:-1] == transition.trace.events
    assert "inv-1" in verification.trace.events[-1]


def test_invariant_gate_detects_non_preservation() -> None:
    transition = make_transition()
    registry = InvariantExtractorRegistry()
    registry.register("value-extractor", lambda state: state.value)
    spec = InvariantSpec(
        invariant_id="inv-1", component="identity", extractor_id="value-extractor"
    )
    verification = InvariantVerificationGate.verify(transition, spec, registry)
    assert verification.preserved is False
    assert verification.observation.before_value == "before"
    assert verification.observation.after_value == "after"


def test_invariant_gate_rejects_component_not_declared_preserved() -> None:
    transition = make_transition(preserved=("identity",))
    registry = InvariantExtractorRegistry()
    registry.register("value-extractor", lambda state: state.value)
    spec = InvariantSpec(
        invariant_id="inv-1", component="other", extractor_id="value-extractor"
    )
    with pytest.raises(ValueError, match="declared preserved components"):
        InvariantVerificationGate.verify(transition, spec, registry)


def test_invariant_gate_requires_registered_extractor() -> None:
    transition = make_transition()
    registry = InvariantExtractorRegistry()
    spec = InvariantSpec(
        invariant_id="inv-1", component="identity", extractor_id="missing"
    )
    with pytest.raises(UnregisteredExtractorError):
        InvariantVerificationGate.verify(transition, spec, registry)


def test_invariant_gate_wraps_extractor_failures() -> None:
    transition = make_transition()
    registry = InvariantExtractorRegistry()

    def failing_extractor(state: State) -> object:
        raise RuntimeError("boom")

    registry.register("failing-extractor", failing_extractor)
    spec = InvariantSpec(
        invariant_id="inv-1", component="identity", extractor_id="failing-extractor"
    )
    with pytest.raises(InvariantExtractionError, match="failing-extractor"):
        InvariantVerificationGate.verify(transition, spec, registry)


def test_invariant_gate_wraps_comparison_failures() -> None:
    transition = make_transition()
    registry = InvariantExtractorRegistry()

    class _RaisingEquality:
        def __eq__(self, other: object) -> bool:
            raise RuntimeError("cannot compare")

    registry.register("uncomparable-extractor", lambda state: _RaisingEquality())
    spec = InvariantSpec(
        invariant_id="inv-1",
        component="identity",
        extractor_id="uncomparable-extractor",
    )
    with pytest.raises(InvariantExtractionError, match="comparing before/after"):
        InvariantVerificationGate.verify(transition, spec, registry)


def test_invariant_spec_cannot_embed_an_extractor_callable() -> None:
    # A spec only carries a string extractor_id; there is no field through
    # which a candidate could smuggle in its own executable "proof".
    field_types = typing.get_type_hints(InvariantSpec)
    assert field_types["extractor_id"] is str
