"""G0.BC.1a: what a birth certificate must record, and who may not issue one.

The five readings a certification reads are exhaustively enumerated here
(`3 x 3 x 3 x 3 x 3 = 243` combinations), together with the authority boundaries
that decide who may certify and who may execute. Every combination yields no
certificate, and the three structural preventers that make that so are asserted
by name rather than inferred from the absence of one.
"""

import itertools

import pytest

from alghanem.kernel.birth import (
    BirthExperimentSpecificationError,
    BirthVerdictStatus,
    EvidenceMode,
    ResidualSurvivalStatus,
)
from alghanem.kernel.birth_certificate import (
    BIRTH_CERTIFICATE_NAMED_LAWS,
    BirthCertificate,
    BirthCertificateAuthorityError,
    BirthCertificationAssessment,
    BirthPreventer,
    ConstitutionalBirthAuthority,
    ExecutableEntity,
    ExecutiveAdmissionGate,
    PreventerFinding,
    derive_preventer_findings,
)
from alghanem.kernel.birth_verdict import (
    BirthVerdictDecision,
    BirthVerdictGate,
    BirthVerdictScopeRegistry,
)
from alghanem.kernel.independent_closure import ComparabilityClosureStatus
from alghanem.kernel.independent_closure_composition import (
    IndependentClosureCompositionGate,
    IndependentClosureCompositionStatus,
    IndependentClosureDecision,
)
from alghanem.kernel.trace import Trace
from alghanem.kernel.weaker_model_exhaustion import WeakerModelExhaustionStatus
from tests.kernel.test_independent_closure_composition import (
    assessment_request,
    comparability_for,
    exhaustion_for,
    frozen_specification_binding,
    specification,
    survival_for,
)

RESOLVED = ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET
EXHAUSTED = WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
CLOSES = WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL
UNDETERMINED_EXHAUSTION = WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED
SATISFIED = (
    IndependentClosureCompositionStatus.CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION  # noqa: E501
)
REFUTED = IndependentClosureCompositionStatus.CLOSURE_REFUTED_IN_SCOPE

STRUCTURALLY_MISSING = frozenset(
    {
        BirthPreventer.AUTHORITY_MISSING,
        BirthPreventer.IDENTITY_NOT_PROVED,
        BirthPreventer.CANDIDATE_EQUIVALENT_TO_ORIGIN,
    }
)

ALL_READINGS = tuple(
    itertools.product(
        tuple(BirthVerdictStatus),
        tuple(IndependentClosureCompositionStatus),
        tuple(WeakerModelExhaustionStatus),
        tuple(ResidualSurvivalStatus),
        tuple(EvidenceMode),
    )
)


def expected_held(
    verdict_status: BirthVerdictStatus,
    closure_status: IndependentClosureCompositionStatus,
    exhaustion_status: WeakerModelExhaustionStatus,
    survival_status: ResidualSurvivalStatus,
    evidence_mode: EvidenceMode,
) -> frozenset[BirthPreventer]:
    """The enumeration, written independently of the module's own branching."""

    held = set(STRUCTURALLY_MISSING)
    if verdict_status is not BirthVerdictStatus.BIRTH_IN_SCOPE:
        held.add(BirthPreventer.VERDICT_NOT_BIRTH_IN_SCOPE)
    if survival_status is not ResidualSurvivalStatus.SURVIVES:
        held.add(BirthPreventer.NO_UNCLOSED_RESIDUAL)
    if exhaustion_status is not EXHAUSTED:
        held.add(BirthPreventer.LOWER_LAYER_NOT_EXHAUSTED)
    if exhaustion_status is CLOSES:
        held.add(BirthPreventer.WEAKER_RECONSTRUCTION_STILL_SUFFICES)
    if closure_status is REFUTED:
        held.add(BirthPreventer.BLOCKING_RESIDUAL)
    if closure_status is not SATISFIED or evidence_mode is not EvidenceMode.FORMAL:
        held.add(BirthPreventer.EVIDENCE_INSUFFICIENT)
    if evidence_mode is EvidenceMode.MIXED:
        held.add(BirthPreventer.SCOPE_UNDEFINED)
    return frozenset(held)


def closure_decision(
    exhaustion_status: WeakerModelExhaustionStatus = EXHAUSTED,
    survival_status: ResidualSurvivalStatus = ResidualSurvivalStatus.SURVIVES,
    *,
    experiment_id: str = "experiment",
) -> IndependentClosureDecision:
    """A real gate-issued closure decision, built through the licensed chain."""

    request = assessment_request(
        frozen_specification_binding(
            specification(comparable=True, experiment_id=experiment_id)
        )
    )
    return IndependentClosureCompositionGate.assess(
        comparability=comparability_for(request),
        exhaustion=exhaustion_for(request, exhaustion_status),
        survival=survival_for(request, survival_status),
    )


def verdict_for(closure: IndependentClosureDecision) -> BirthVerdictDecision:
    """The only verdict this tree can issue for the closure's own request."""

    request = closure.request
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="verdict-scope", binding=request.experiment_binding)
    return BirthVerdictGate.assess(
        registry=registry.seal("verdict-snapshot"), request=request
    )


# --- the derivation, enumerated ------------------------------------------------


@pytest.mark.parametrize("readings", ALL_READINGS)
def test_every_reading_derives_one_finding_per_preventer(
    readings: tuple[
        BirthVerdictStatus,
        IndependentClosureCompositionStatus,
        WeakerModelExhaustionStatus,
        ResidualSurvivalStatus,
        EvidenceMode,
    ],
) -> None:
    verdict_status, closure_status, exhaustion, survival, mode = readings
    findings = derive_preventer_findings(
        verdict_status=verdict_status,
        closure_status=closure_status,
        exhaustion_status=exhaustion,
        survival_status=survival,
        evidence_mode=mode,
    )
    covered = tuple(finding.preventer for finding in findings)
    assert len(covered) == len(BirthPreventer)
    assert set(covered) == set(BirthPreventer)
    held = frozenset(finding.preventer for finding in findings if finding.holds)
    assert held == expected_held(
        verdict_status, closure_status, exhaustion, survival, mode
    )


@pytest.mark.parametrize("readings", ALL_READINGS)
def test_no_reading_in_this_tree_clears_every_preventer(
    readings: tuple[
        BirthVerdictStatus,
        IndependentClosureCompositionStatus,
        WeakerModelExhaustionStatus,
        ResidualSurvivalStatus,
        EvidenceMode,
    ],
) -> None:
    """`NoCertificateIsReachableInThisTree`, asserted rather than assumed."""

    verdict_status, closure_status, exhaustion, survival, mode = readings
    findings = derive_preventer_findings(
        verdict_status=verdict_status,
        closure_status=closure_status,
        exhaustion_status=exhaustion,
        survival_status=survival,
        evidence_mode=mode,
    )
    held = {finding.preventer for finding in findings if finding.holds}
    assert STRUCTURALLY_MISSING <= held


def test_the_three_structural_preventers_name_three_missing_authorities() -> None:
    findings = {
        finding.preventer: finding
        for finding in derive_preventer_findings(
            verdict_status=BirthVerdictStatus.BIRTH_IN_SCOPE,
            closure_status=SATISFIED,
            exhaustion_status=EXHAUSTED,
            survival_status=ResidualSurvivalStatus.SURVIVES,
            evidence_mode=EvidenceMode.FORMAL,
        )
    }
    reasons = {findings[preventer].reason for preventer in STRUCTURALLY_MISSING}
    assert len(reasons) == 3
    assert all("no authority in this repository" in reason for reason in reasons)


def test_every_preventer_reason_is_non_blank_on_both_branches() -> None:
    for readings in ALL_READINGS:
        verdict_status, closure_status, exhaustion, survival, mode = readings
        for finding in derive_preventer_findings(
            verdict_status=verdict_status,
            closure_status=closure_status,
            exhaustion_status=exhaustion,
            survival_status=survival,
            evidence_mode=mode,
        ):
            assert finding.reason.strip()


def test_the_derivation_refuses_anything_that_is_not_a_declared_reading() -> None:
    with pytest.raises(BirthCertificateAuthorityError):
        derive_preventer_findings(
            verdict_status="BIRTH_IN_SCOPE",  # type: ignore[arg-type]
            closure_status=SATISFIED,
            exhaustion_status=EXHAUSTED,
            survival_status=ResidualSurvivalStatus.SURVIVES,
            evidence_mode=EvidenceMode.FORMAL,
        )


def test_a_preventer_is_an_identity_with_a_reason_not_a_bare_boolean() -> None:
    with pytest.raises(BirthExperimentSpecificationError):
        PreventerFinding(
            preventer=BirthPreventer.SCOPE_UNDEFINED, holds=True, reason="  "
        )
    with pytest.raises(BirthCertificateAuthorityError):
        PreventerFinding(
            preventer="SCOPE_UNDEFINED",  # type: ignore[arg-type]
            holds=True,
            reason="a reason",
        )


# --- the authority boundary ----------------------------------------------------


def test_a_certificate_is_not_caller_constructible() -> None:
    closure = closure_decision()
    verdict = verdict_for(closure)
    findings = derive_preventer_findings(
        verdict_status=BirthVerdictStatus.BIRTH_IN_SCOPE,
        closure_status=SATISFIED,
        exhaustion_status=EXHAUSTED,
        survival_status=ResidualSurvivalStatus.SURVIVES,
        evidence_mode=EvidenceMode.FORMAL,
    )
    with pytest.raises(BirthCertificateAuthorityError):
        BirthCertificate(
            certificate_id="forged",
            issuing_authority_id="forged",
            verdict=verdict,
            closure=closure,
            findings=findings,
            trace=Trace(("forged",)),
        )


def test_an_assessment_is_not_caller_constructible() -> None:
    closure = closure_decision()
    with pytest.raises(BirthCertificateAuthorityError):
        BirthCertificationAssessment(
            assessment_id="forged",
            issuing_authority_id="forged",
            verdict=verdict_for(closure),
            closure=closure,
            findings=(),
            certificate=None,
            trace=Trace(("forged",)),
        )


def test_an_executable_entity_is_not_caller_constructible() -> None:
    with pytest.raises(BirthCertificateAuthorityError):
        ExecutableEntity(
            admission_id="forged",
            certificate=None,  # type: ignore[arg-type]
        )


def test_the_deferred_verdict_this_tree_issues_produces_no_certificate() -> None:
    closure = closure_decision()
    verdict = verdict_for(closure)
    assert verdict.status is BirthVerdictStatus.DEFER_IN_SCOPE
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict, closure=closure
    )
    assert assessment.certificate is None
    assert assessment.is_certified is False
    held = {finding.preventer for finding in assessment.preventers_that_held}
    assert BirthPreventer.VERDICT_NOT_BIRTH_IN_SCOPE in held


def test_no_verdict_status_other_than_birth_in_scope_may_be_certified() -> None:
    """`DEFER_IN_SCOPE` and `NO_BIRTH_IN_SCOPE` are both refused by derivation."""

    for status in (
        BirthVerdictStatus.DEFER_IN_SCOPE,
        BirthVerdictStatus.NO_BIRTH_IN_SCOPE,
    ):
        findings = {
            finding.preventer: finding
            for finding in derive_preventer_findings(
                verdict_status=status,
                closure_status=SATISFIED,
                exhaustion_status=EXHAUSTED,
                survival_status=ResidualSurvivalStatus.SURVIVES,
                evidence_mode=EvidenceMode.FORMAL,
            )
        }
        finding = findings[BirthPreventer.VERDICT_NOT_BIRTH_IN_SCOPE]
        assert finding.holds is True
        assert status.name in finding.reason


def test_a_surviving_residual_without_exhaustion_produces_no_certificate() -> None:
    closure = closure_decision(
        UNDETERMINED_EXHAUSTION, ResidualSurvivalStatus.SURVIVES
    )
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    held = {finding.preventer for finding in assessment.preventers_that_held}
    assert BirthPreventer.LOWER_LAYER_NOT_EXHAUSTED in held
    assert BirthPreventer.NO_UNCLOSED_RESIDUAL not in held
    assert assessment.certificate is None


def test_a_weaker_model_that_still_closes_the_residual_blocks_birth() -> None:
    closure = closure_decision(CLOSES, ResidualSurvivalStatus.SURVIVES)
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    held = {finding.preventer for finding in assessment.preventers_that_held}
    assert BirthPreventer.WEAKER_RECONSTRUCTION_STILL_SUFFICES in held
    assert BirthPreventer.BLOCKING_RESIDUAL in held


def test_exhaustion_without_a_surviving_residual_produces_no_certificate() -> None:
    closure = closure_decision(EXHAUSTED, ResidualSurvivalStatus.DEFER)
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    held = {finding.preventer for finding in assessment.preventers_that_held}
    assert BirthPreventer.NO_UNCLOSED_RESIDUAL in held
    assert BirthPreventer.LOWER_LAYER_NOT_EXHAUSTED not in held


def test_identity_and_difference_remain_unproved_even_when_readings_are_best() -> None:
    """Exhaustion and survival together still leave identity and difference open."""

    closure = closure_decision(EXHAUSTED, ResidualSurvivalStatus.SURVIVES)
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    held = {finding.preventer for finding in assessment.preventers_that_held}
    assert BirthPreventer.IDENTITY_NOT_PROVED in held
    assert BirthPreventer.CANDIDATE_EQUIVALENT_TO_ORIGIN in held
    assert assessment.certificate is None


def test_two_decisions_for_different_requests_are_refused_not_scored() -> None:
    closure = closure_decision(experiment_id="experiment")
    other = closure_decision(experiment_id="other-experiment")
    with pytest.raises(BirthCertificateAuthorityError):
        ConstitutionalBirthAuthority(authority_id="authority").assess(
            assessment_id="assessment", verdict=verdict_for(other), closure=closure
        )


def test_the_authority_takes_no_status_reason_or_birth_claim() -> None:
    closure = closure_decision()
    with pytest.raises(TypeError):
        ConstitutionalBirthAuthority(authority_id="authority").assess(  # type: ignore[call-arg]
            assessment_id="assessment",
            verdict=verdict_for(closure),
            closure=closure,
            status=BirthVerdictStatus.BIRTH_IN_SCOPE,
        )


def test_an_assessment_id_is_issued_once_per_authority() -> None:
    closure = closure_decision()
    authority = ConstitutionalBirthAuthority(authority_id="authority")
    authority.assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    with pytest.raises(BirthCertificateAuthorityError):
        authority.assess(
            assessment_id="assessment", verdict=verdict_for(closure), closure=closure
        )


def test_the_authority_refuses_inputs_that_are_not_gate_issued() -> None:
    closure = closure_decision()
    authority = ConstitutionalBirthAuthority(authority_id="authority")
    with pytest.raises(BirthCertificateAuthorityError):
        authority.assess(
            assessment_id="a", verdict=None, closure=closure  # type: ignore[arg-type]
        )
    with pytest.raises(BirthCertificateAuthorityError):
        authority.assess(
            assessment_id="b",
            verdict=verdict_for(closure),
            closure=None,  # type: ignore[arg-type]
        )


# --- the constitutional / executive split --------------------------------------


def test_the_constitutional_authority_exposes_no_way_to_execute() -> None:
    surface = {
        name for name in vars(ConstitutionalBirthAuthority) if not name.startswith("_")
    }
    assert surface == {"assess", "authority_id"}


def test_the_executive_gate_exposes_no_way_to_certify() -> None:
    surface = {
        name for name in vars(ExecutiveAdmissionGate) if not name.startswith("_")
    }
    assert surface == {"admit"}


def test_execution_requires_an_authority_issued_certificate() -> None:
    closure = closure_decision()
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    assert assessment.certificate is None
    with pytest.raises(BirthCertificateAuthorityError):
        ExecutiveAdmissionGate.admit(
            admission_id="admission",
            certificate=assessment.certificate,  # type: ignore[arg-type]
        )


def test_a_verdict_decision_is_never_accepted_in_place_of_a_certificate() -> None:
    closure = closure_decision()
    with pytest.raises(BirthCertificateAuthorityError):
        ExecutiveAdmissionGate.admit(
            admission_id="admission",
            certificate=verdict_for(closure),  # type: ignore[arg-type]
        )


# --- what a certificate would and would not confer -----------------------------


def test_a_certificate_would_confer_neither_freeze_nor_truth() -> None:
    for name in ("confers_freeze", "confers_truth", "confers_global_ontology_claim"):
        assert getattr(BirthCertificate, name).fget(object()) is False


def test_the_certificate_records_the_gate_issued_objects_not_prose() -> None:
    annotations = BirthCertificate.__annotations__
    assert annotations["verdict"] == "BirthVerdictDecision"
    assert annotations["closure"] == "IndependentClosureDecision"
    assert annotations["findings"] == "tuple[PreventerFinding, ...]"
    assert annotations["trace"] == "Trace"


def test_the_trace_reconstructs_the_scope_and_every_preventer() -> None:
    closure = closure_decision()
    verdict = verdict_for(closure)
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict, closure=closure
    )
    events = assessment.trace.events
    assert f"domain:{verdict.scope.domain}" in events
    assert f"verdict:{verdict.status.name}" in events
    assert f"closure:{closure.status.name}" in events
    for finding in assessment.findings:
        marker = f"preventer:{finding.preventer.value}:"
        matched = [event for event in events if event.startswith(marker)]
        assert len(matched) == 1
        assert ("HELD" if finding.holds else "CLEARED") in matched[0]
        assert finding.reason in matched[0]


def test_held_and_cleared_findings_partition_the_vocabulary() -> None:
    closure = closure_decision()
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )
    held = {finding.preventer for finding in assessment.preventers_that_held}
    cleared = {finding.preventer for finding in assessment.preventers_cleared}
    assert held | cleared == set(BirthPreventer)
    assert not held & cleared


# --- the named limits ----------------------------------------------------------


def test_every_named_law_opens_with_its_own_name() -> None:
    for name, text in BIRTH_CERTIFICATE_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")


def test_the_nine_requested_laws_are_all_deposited() -> None:
    for name in (
        "BirthVerdictIsNotBirthCertificate",
        "BirthCertificateIsNotExecution",
        "ExecutiveAuthorityCannotIssueBirth",
        "ConstitutionalBirthAuthorityCannotExecuteTheBornEntity",
        "NoBirthWithoutUnclosedResidual",
        "NoBirthBeforeLowerLayerExhaustion",
        "NoBirthWhenAWeakerReconstructionStillSuffices",
        "BirthDoesNotMeanFreeze",
        "BirthDoesNotMeanTruth",
    ):
        assert name in BIRTH_CERTIFICATE_NAMED_LAWS


def test_no_genus_ladder_was_encoded() -> None:
    """Instruction -> rule -> ... -> constitution is not a closed vocabulary here."""

    from pathlib import Path

    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "kernel"
        / "birth_certificate.py"
    ).read_text(encoding="utf-8")
    for forbidden in (
        "class GenusRank",
        "class BirthGenus",
        "UNIVERSAL_RULE =",
        "GENERAL_RULE =",
        "rank_ceiling",
    ):
        assert forbidden not in source
    assert "NoGenusLadderIsEncodedHere" in BIRTH_CERTIFICATE_NAMED_LAWS


def test_this_module_activates_no_new_verdict_branch() -> None:
    """`BirthVerdictGate` still defers; nothing here widened its codomain."""

    closure = closure_decision()
    assert verdict_for(closure).status is BirthVerdictStatus.DEFER_IN_SCOPE
    assert verdict_for(closure).is_birth is False


def test_the_constitution_records_this_stage_without_flipping_a_deferred_row() -> None:
    from pathlib import Path

    constitution = (
        Path(__file__).resolve().parents[2] / "docs" / "CONSTITUTION.md"
    ).read_text(encoding="utf-8")
    assert "G0.BC.1a birth-certificate contract" in constitution
    assert (
        "| G0.BV.1 authority-issued birth verdict | "
        "DECLARED_DEFERRED_CONTRACT_ONLY |" in constitution
    )


def test_the_ledger_reads_the_new_row_under_its_own_declared_status() -> None:
    """The extracted status vocabulary follows the document, never precedes it."""

    from pathlib import Path

    from alghanem.program.constitution_ledger import (
        DeclaredLawStatus,
        read_constitution_ledger,
    )

    ledger = read_constitution_ledger(
        (Path(__file__).resolve().parents[2] / "docs" / "CONSTITUTION.md").read_text(
            encoding="utf-8"
        )
    )
    status = DeclaredLawStatus.ENFORCED_AT_CERTIFICATION_GATE
    rows = ledger.laws.rows_with_status(status)
    assert len(rows) == 1
    assert rows[0].law.startswith("G0.BC.1a")
    assert ledger.laws.status_counts[status] == 1
