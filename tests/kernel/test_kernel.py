import pytest

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
    Claim,
    ClaimEvidenceBinding,
    Evidence,
    LicensedTransition,
    LicensingGate,
    Operation,
    OperationResult,
    Outcome,
    Residual,
    State,
    Trace,
    TransitionCandidate,
    TransitionDecision,
)


class _DefaultProvenance:
    pass


_DEFAULT_PROVENANCE = _DefaultProvenance()


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
) -> TransitionCandidate:
    anchor = anchor or Anchor("a", "D")
    transition_claim = transition_claim or claim()
    if transition_evidence is None:
        transition_evidence = (evidence(transition_claim.claim_id),)
    if (
        branch_origin_provenance is _DEFAULT_PROVENANCE
        and outcome is Outcome.CERTIFIED_BRANCH_BIRTH
    ):
        branch_origin_provenance = BranchOriginProvenance(
            origin_anchor=anchor,
            branch_anchor=Anchor("branch", "D"),
            preserved_components=preserved,
        )
    if branch_origin_provenance is _DEFAULT_PROVENANCE:
        branch_origin_provenance = None
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
    )


def license_candidate(candidate: TransitionCandidate) -> LicensedTransition:
    return LicensingGate.license(candidate)


def make_transition(
    outcome: Outcome, preserved: tuple[str, ...] = ("identity",)
) -> LicensedTransition:
    return license_candidate(make_candidate(outcome, preserved=preserved))


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


def test_licensed_transition_cannot_be_constructed_directly():
    with pytest.raises(ValueError, match="LicensingGate"):
        LicensedTransition(
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


def test_licensing_gate_issues_successful_transition():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    assert isinstance(transition, LicensedTransition)


def test_licensing_gate_rejects_already_licensed_transition():
    transition = make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION)
    with pytest.raises(ValueError, match="re-licensed"):
        LicensingGate.license(transition)


def test_identity_preserving_requires_declared_invariant():
    with pytest.raises(ValueError, match="invariant"):
        license_candidate(
            make_candidate(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, preserved=())
        )


def test_identity_preserving_requires_declared_change():
    with pytest.raises(ValueError, match="declared change"):
        license_candidate(
            make_candidate(Outcome.IDENTITY_PRESERVING_TRANSFORMATION, changed=())
        )


def test_preserved_and_changed_must_be_disjoint():
    with pytest.raises(ValueError, match="disjoint"):
        license_candidate(
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


@pytest.mark.parametrize("outcome", [Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED])
def test_non_success_outcomes_are_not_successes(outcome: Outcome):
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
        license_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                transition_evidence=(),
            )
        )


def test_success_without_result_is_rejected():
    with pytest.raises(ValueError, match="result"):
        license_candidate(
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
        license_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                transition_claim=transition_claim,
                transition_evidence=(unrelated_evidence,),
            )
        )


def test_transition_evidence_bound_to_transition_claim_is_accepted():
    transition_claim = claim("claim-1", "transition claim")
    transition = license_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            transition_claim=transition_claim,
            transition_evidence=(evidence(transition_claim.claim_id),),
        )
    )

    assert transition.evidence[0].claim_id == transition.claim.claim_id


def test_transition_change_must_include_operation_declared_change():
    with pytest.raises(ValueError, match="declared change"):
        license_candidate(
            make_candidate(
                Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
                operation=Operation("op", "declared"),
                changed=("recorded",),
            )
        )


def test_operation_source_domain_must_match_anchor_domain():
    with pytest.raises(ValueError, match="source domain"):
        license_candidate(
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
    transition = license_candidate(
        make_candidate(
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            anchor=Anchor("a", "DOMAIN_A"),
            operation=Operation(
                "op",
                "component",
                source_domain="DOMAIN_A",
                target_domain="DOMAIN_C",
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
        license_candidate(
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
        license_candidate(
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
        license_candidate(
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


def test_branch_origin_provenance_branch_domain_must_match_transition_domain():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="transition domain"):
        license_candidate(
            make_candidate(
                Outcome.CERTIFIED_BRANCH_BIRTH,
                preserved=("origin-data",),
                changed=("new",),
                anchor=anchor,
                operation=Operation("op", "new"),
                branch_origin_provenance=BranchOriginProvenance(
                    anchor, Anchor("branch", "OTHER"), ("origin-data",)
                ),
            )
        )


def test_branch_origin_provenance_components_must_be_declared_preserved():
    anchor = Anchor("a", "D")
    with pytest.raises(ValueError, match="declared preserved"):
        license_candidate(
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
        license_candidate(
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
    assert decision.transition is not None


def test_successful_decision_must_match_transition_outcome():
    with pytest.raises(ValueError, match="outcomes must match"):
        TransitionDecision(
            Outcome.CERTIFIED_BRANCH_BIRTH,
            make_transition(Outcome.IDENTITY_PRESERVING_TRANSFORMATION),
        )
