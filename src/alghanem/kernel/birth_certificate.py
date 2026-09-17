"""G0.BC.1a: the birth-certificate contract, and the constitutional/executive split.

`BirthVerdictGate` (G0.BV.1a) can issue a scoped verdict.
`IndependentClosureCompositionGate` (G0.IC.1e) can compose three conjunct
readings. Nothing yet says what a *birth* would have to record, nor who may use
what was born. This module supplies that contract and nothing else.

`BirthVerdict != BirthCertificate != Execution`. Three distinct acts:

* a verdict decides that the conditions for existence of this genus were met in
  this scope;
* a certificate preserves that decision together with its identity, scope,
  evidence references, preventers and trace;
* execution uses what was born, and may never create it.

Two authorities, and neither may perform the other's act.
`ConstitutionalBirthAuthority.assess` alone may produce a `BirthCertificate`,
and exposes no method that runs anything. `ExecutiveAdmissionGate.admit` alone
may produce an `ExecutableEntity`, and exposes no method that certifies
anything. `ExecutiveAuthorityCannotIssueBirth` and
`ConstitutionalBirthAuthorityCannotExecuteTheBornEntity` are therefore enforced
by the two classes' surfaces, not only by prose; both surfaces are asserted by
test.

`CallerDoesNotOwnCertification`. `assess` takes exactly two parameters -- a
gate-issued `BirthVerdictDecision` and a gate-issued `IndependentClosureDecision`
-- and no status, reason, preventer finding, or birth claim. It re-derives every
finding itself. `OneRequestOrRefusal`, copied from G0.IC.1c and G0.IC.1e: the
two decisions must speak for the same `BirthAssessmentRequest` by object
identity, and a mismatch raises rather than becoming a negative finding, because
`MalformedRequestIsNotNonExhaustion` applies here unchanged.

`APreventerHasAnIdentityNotABoolean`. A refusal that collapses to `False`
destroys the only thing worth keeping: *why* the birth did not occur. Every
member of `BirthPreventer` is therefore derived on every assessment, held or
cleared, and each finding carries its own reason. `preventers_that_held` and
`preventers_cleared` are separate tuples for the same reason
`InvariantVerificationDecision` separates `failed_components` from
`deferred_components`.

Necessity, and why a candidate does not compel a birth. The existence of a
candidate does not oblige its birth, a use for it does not oblige its birth, and
frequent use of it does not oblige its birth. What obliges it is an unclosed
residual that the lower layer, exhausted, did not close and that no weaker
reconstruction still suffices to explain::

    BirthNecessity = UnclosedResidual
                     and LowerLayerExhausted
                     and not WeakerReconstructionSuffices

Those three conjuncts are not invented here. They are read from the closure
decision this module consumes: `NoBirthWithoutUnclosedResidual` from its
survival certificate, `NoBirthBeforeLowerLayerExhaustion` and
`NoBirthWhenAWeakerReconstructionStillSuffices` from its exhaustion assessment.
Opening a second authority over questions G0.IC.1c and G0.IC.1d already answered
would let two authorities disagree, which is what `ThreeReadingsAreNotAFourth`
forbids.

`NoCertificateIsReachableInThisTree`, declared openly rather than discovered
later. Three preventers hold on every branch, each naming a different missing
authority: no authority issues the `BirthCandidate` a certificate must name
(`AUTHORITY_MISSING`), none proves its identity (`IDENTITY_NOT_PROVED`), and
none proves its difference from the origin it branched from
(`CANDIDATE_EQUIVALENT_TO_ORIGIN`). A fourth, `VERDICT_NOT_BIRTH_IN_SCOPE`,
holds because `BirthVerdictGate`'s codomain is still the single value
`DEFER_IN_SCOPE`. `BirthCertificationAssessment.certificate` is therefore `None`
unconditionally, exactly as `IndependentClosureDecision.is_independent_closure`
is `False` unconditionally. This module activates neither `BIRTH_IN_SCOPE` nor
`NO_BIRTH_IN_SCOPE`, and is wired into no verdict path.

`BirthDoesNotMeanFreeze` and `BirthDoesNotMeanTruth`. A certificate is not a
freeze, not an `E0` mapping, not a `TraditionalName`, and not a claim that the
born entity is true of the world; it records that the conditions for existence
of this genus were met within one frozen experiment's scope. The three denials
are exposed as derived properties so the ceiling is read from the object rather
than from this paragraph.

`NoGenusLadderIsEncodedHere`. Instruction, rule, general rule, universal rule,
law and constitution are *not* encoded as a closed vocabulary: each of those
genera would itself require its own birth certificate and its own
`BirthSpecification` before entering any ontology, and a ladder written now
would be a vocabulary frozen before its text. The certificate's ceiling is
therefore expressed as denials of what it does not confer, never as a rank on a
ladder.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum

from .birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    BirthVerdictStatus,
    EvidenceMode,
    ResidualSurvivalStatus,
    _require_text,
)
from .birth_verdict import AuthorizedBirthVerdictScope, BirthVerdictDecision
from .evidence_acquisition import AuthorizedEvidenceSnapshot
from .independent_closure_composition import (
    IndependentClosureCompositionStatus,
    IndependentClosureDecision,
)
from .trace import Trace
from .weaker_model_exhaustion import WeakerModelExhaustionStatus

_CERTIFICATE_TOKEN = object()
_EXECUTION_TOKEN = object()


class BirthCertificateAuthorityError(BirthExperimentSpecificationError):
    """A certification or admission was requested outside its authority."""


class BirthPreventer(Enum):
    """Named grounds on which a certificate is withheld; never a bare `False`.

    A preventer is an identity preserved in the assessment's own record, so a
    later reader can ask *which* ground stopped the birth rather than only that
    something did.
    """

    VERDICT_NOT_BIRTH_IN_SCOPE = "VERDICT_NOT_BIRTH_IN_SCOPE"
    NO_UNCLOSED_RESIDUAL = "NO_UNCLOSED_RESIDUAL"
    LOWER_LAYER_NOT_EXHAUSTED = "LOWER_LAYER_NOT_EXHAUSTED"
    WEAKER_RECONSTRUCTION_STILL_SUFFICES = "WEAKER_RECONSTRUCTION_STILL_SUFFICES"
    BLOCKING_RESIDUAL = "BLOCKING_RESIDUAL"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    SCOPE_UNDEFINED = "SCOPE_UNDEFINED"
    AUTHORITY_MISSING = "AUTHORITY_MISSING"
    IDENTITY_NOT_PROVED = "IDENTITY_NOT_PROVED"
    CANDIDATE_EQUIVALENT_TO_ORIGIN = "CANDIDATE_EQUIVALENT_TO_ORIGIN"


BIRTH_CERTIFICATE_NAMED_LAWS: dict[str, str] = {
    "BirthVerdictIsNotBirthCertificate": (
        "BirthVerdictIsNotBirthCertificate: a verdict decides that the "
        "conditions for existence of this genus were met in this scope; a "
        "certificate preserves that decision with its identity, scope, "
        "necessity, evidence references, preventers and trace. Holding a "
        "verdict is not holding a certificate, and a decision object is never "
        "read as one"
    ),
    "BirthCertificateIsNotExecution": (
        "BirthCertificateIsNotExecution: a certificate records that something "
        "was born; it does not run it. Using the born entity is a later act "
        "under a different authority, and the certificate confers no capability "
        "of its own"
    ),
    "ExecutiveAuthorityCannotIssueBirth": (
        "ExecutiveAuthorityCannotIssueBirth: the executive side exposes no "
        "method that produces a certificate, so a runtime component cannot "
        "create the genus it needs and then argue for its legitimacy from "
        "having used it successfully. Successful execution is never evidence "
        "of valid birth"
    ),
    "ConstitutionalBirthAuthorityCannotExecuteTheBornEntity": (
        "ConstitutionalBirthAuthorityCannotExecuteTheBornEntity: the "
        "constitutional side exposes no method that runs anything. It may say "
        "that this genus was born in this domain under this certificate, and "
        "nothing further"
    ),
    "NoBirthWithoutUnclosedResidual": (
        "NoBirthWithoutUnclosedResidual: a candidate's existence does not "
        "oblige its birth, a use for it does not oblige its birth, and frequent "
        "use of it does not oblige its birth. What obliges it is a residual "
        "that survived, read from the closure decision's own survival "
        "certificate and never re-derived here"
    ),
    "NoBirthBeforeLowerLayerExhaustion": (
        "NoBirthBeforeLowerLayerExhaustion: a residual counts only after the "
        "licensed weaker models were exhausted, read from the closure "
        "decision's own exhaustion assessment. An unevaluated model is "
        "ignorance, not exhaustion"
    ),
    "NoBirthWhenAWeakerReconstructionStillSuffices": (
        "NoBirthWhenAWeakerReconstructionStillSuffices: if any licensed weaker "
        "model still closes the residual, the richer structure was not needed, "
        "and a birth certified over it would record a preference rather than a "
        "necessity"
    ),
    "BirthDoesNotMeanFreeze": (
        "BirthDoesNotMeanFreeze: a certificate issues no `Freeze`, no `E0` "
        "mapping and no `TraditionalName`. Freezing is a separate later "
        "authority, and it stays separate even after a birth is certified"
    ),
    "BirthDoesNotMeanTruth": (
        "BirthDoesNotMeanTruth: a certificate records that the conditions for "
        "existence of this genus were met inside one frozen experiment's "
        "scope. It does not claim the born entity is true of the world, and "
        "`ScopedBirthIsNotGlobalOntologyClaim` is unaffected by it"
    ),
    "APreventerHasAnIdentityNotABoolean": (
        "APreventerHasAnIdentityNotABoolean: every preventer is derived on "
        "every assessment, held or cleared, and each finding carries its own "
        "reason, so a refusal records which ground stopped the birth rather "
        "than only that something did"
    ),
    "NoGenusLadderIsEncodedHere": (
        "NoGenusLadderIsEncodedHere: instruction, rule, general rule, universal "
        "rule, law and constitution are not encoded as a closed vocabulary. "
        "Each such genus would need its own birth certificate and its own "
        "birth specification before entering any ontology, so the ceiling is "
        "expressed as denials of what a certificate does not confer, never as "
        "a rank on a ladder"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


@dataclass(frozen=True, slots=True)
class PreventerFinding:
    """One preventer, whether it held, and why -- for a single assessment.

    A finding is a reading, not an authority: constructing one grants nothing,
    because only `ConstitutionalBirthAuthority` may place findings in a
    certificate and it re-derives them itself.
    """

    preventer: BirthPreventer
    holds: bool
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.preventer, BirthPreventer):
            raise BirthCertificateAuthorityError(
                "a finding requires a member of BirthPreventer"
            )
        if type(self.holds) is not bool:
            raise BirthCertificateAuthorityError(
                "whether a preventer held is a two-valued fact"
            )
        _require_text(self.reason, "preventer finding reason")


_UNREACHABLE_AUTHORITY_REASONS: dict[BirthPreventer, str] = {
    BirthPreventer.AUTHORITY_MISSING: (
        "no authority in this repository issues the BirthCandidate a "
        "certificate must name; G0.BV.1 keeps it deferred"
    ),
    BirthPreventer.IDENTITY_NOT_PROVED: (
        "no authority in this repository proves the identity of a birth "
        "candidate, so a certificate could not say what it certifies"
    ),
    BirthPreventer.CANDIDATE_EQUIVALENT_TO_ORIGIN: (
        "no authority in this repository proves a candidate differs from the "
        "origin it branched from, so an identical restatement could not be "
        "distinguished from a birth"
    ),
}


def _verdict_finding(status: BirthVerdictStatus) -> PreventerFinding:
    holds = status is not BirthVerdictStatus.BIRTH_IN_SCOPE
    reason = (
        f"the verdict status is {status.name}, and only BIRTH_IN_SCOPE may be "
        "certified"
        if holds
        else "the verdict status is BIRTH_IN_SCOPE"
    )
    return PreventerFinding(
        preventer=BirthPreventer.VERDICT_NOT_BIRTH_IN_SCOPE,
        holds=holds,
        reason=reason,
    )


def _survival_finding(status: ResidualSurvivalStatus) -> PreventerFinding:
    holds = status is not ResidualSurvivalStatus.SURVIVES
    reason = (
        f"the residual survival reading is {status.name}, so no surviving "
        "residual makes this birth necessary"
        if holds
        else "a residual survived every licensed projection"
    )
    return PreventerFinding(
        preventer=BirthPreventer.NO_UNCLOSED_RESIDUAL, holds=holds, reason=reason
    )


def _exhaustion_finding(status: WeakerModelExhaustionStatus) -> PreventerFinding:
    holds = status is not WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
    reason = (
        f"the weaker-model exhaustion reading is {status.name}, so the lower "
        "layer was not exhausted"
        if holds
        else "every licensed weaker model was evaluated and none closed the residual"
    )
    return PreventerFinding(
        preventer=BirthPreventer.LOWER_LAYER_NOT_EXHAUSTED, holds=holds, reason=reason
    )


def _weaker_reconstruction_finding(
    status: WeakerModelExhaustionStatus,
) -> PreventerFinding:
    holds = status is WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL
    reason = (
        "a licensed weaker model still closes the residual, so the richer "
        "structure was not needed"
        if holds
        else "no licensed weaker model was read as closing the residual"
    )
    return PreventerFinding(
        preventer=BirthPreventer.WEAKER_RECONSTRUCTION_STILL_SUFFICES,
        holds=holds,
        reason=reason,
    )


def _blocking_residual_finding(
    status: IndependentClosureCompositionStatus,
) -> PreventerFinding:
    holds = status is IndependentClosureCompositionStatus.CLOSURE_REFUTED_IN_SCOPE
    reason = (
        "the composed closure decision is CLOSURE_REFUTED_IN_SCOPE, which is "
        "declared knowledge against a conjunct of closure"
        if holds
        else (
            f"the composed closure decision is {status.name}, which refutes "
            "no conjunct"
        )
    )
    return PreventerFinding(
        preventer=BirthPreventer.BLOCKING_RESIDUAL, holds=holds, reason=reason
    )


def _evidence_finding(
    *,
    closure_status: IndependentClosureCompositionStatus,
    evidence_mode: EvidenceMode,
) -> PreventerFinding:
    satisfied = (
        closure_status
        is IndependentClosureCompositionStatus.CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION  # noqa: E501
    )
    if not satisfied:
        return PreventerFinding(
            preventer=BirthPreventer.EVIDENCE_INSUFFICIENT,
            holds=True,
            reason=(
                f"the composed closure decision is {closure_status.name}, so its "
                "conjuncts were not all read as satisfied"
            ),
        )
    if evidence_mode is not EvidenceMode.FORMAL:
        return PreventerFinding(
            preventer=BirthPreventer.EVIDENCE_INSUFFICIENT,
            holds=True,
            reason=(
                f"in {evidence_mode.name} mode the constitution requires a measured "
                "residual replicated in a second independent measurement run, and "
                "no authority here knows of a second run "
                "(SurvivalReadIsNotMeasuredReplicatedResidual)"
            ),
        )
    return PreventerFinding(
        preventer=BirthPreventer.EVIDENCE_INSUFFICIENT,
        holds=False,
        reason=(
            "the conjuncts were read as satisfied in FORMAL mode, where no second "
            "measurement run is required"
        ),
    )


def _scope_finding(evidence_mode: EvidenceMode) -> PreventerFinding:
    holds = evidence_mode is EvidenceMode.MIXED
    reason = (
        "MIXED mode is an explicitly typed scoped pair <(D_emp, S_emp), "
        "(D_formal, S_formal)> and no authority here proves those declared "
        "scopes or NoCrossSubstitution between them"
        if holds
        else (
            f"{evidence_mode.name} mode declares a single scope, read from the "
            "frozen experiment and never from a caller"
        )
    )
    return PreventerFinding(
        preventer=BirthPreventer.SCOPE_UNDEFINED, holds=holds, reason=reason
    )


def derive_preventer_findings(
    *,
    verdict_status: BirthVerdictStatus,
    closure_status: IndependentClosureCompositionStatus,
    exhaustion_status: WeakerModelExhaustionStatus,
    survival_status: ResidualSurvivalStatus,
    evidence_mode: EvidenceMode,
) -> tuple[PreventerFinding, ...]:
    """Derive exactly one finding per `BirthPreventer`, in a fixed order.

    A pure function of five declared readings plus this tree's own standing
    authorities. It is exhaustively testable over its inputs, and the gate calls
    it with values it reads itself from two gate-issued decisions; a caller
    calling it directly obtains readings and no certificate.
    """

    if not isinstance(verdict_status, BirthVerdictStatus):
        raise BirthCertificateAuthorityError("a verdict status is required")
    if not isinstance(closure_status, IndependentClosureCompositionStatus):
        raise BirthCertificateAuthorityError("a composed closure status is required")
    if not isinstance(exhaustion_status, WeakerModelExhaustionStatus):
        raise BirthCertificateAuthorityError("an exhaustion status is required")
    if not isinstance(survival_status, ResidualSurvivalStatus):
        raise BirthCertificateAuthorityError("a residual survival status is required")
    if not isinstance(evidence_mode, EvidenceMode):
        raise BirthCertificateAuthorityError("an evidence mode is required")

    findings = (
        _verdict_finding(verdict_status),
        _survival_finding(survival_status),
        _exhaustion_finding(exhaustion_status),
        _weaker_reconstruction_finding(exhaustion_status),
        _blocking_residual_finding(closure_status),
        _evidence_finding(closure_status=closure_status, evidence_mode=evidence_mode),
        _scope_finding(evidence_mode),
    ) + tuple(
        PreventerFinding(preventer=preventer, holds=True, reason=reason)
        for preventer, reason in _UNREACHABLE_AUTHORITY_REASONS.items()
    )
    derived = tuple(finding.preventer for finding in findings)
    if set(derived) != set(BirthPreventer) or len(derived) != len(BirthPreventer):
        raise BirthCertificateAuthorityError(
            "every preventer must be derived exactly once on every assessment"
        )
    return findings


@dataclass(frozen=True, slots=True)
class BirthCertificate:
    """The authority-issued record of one certified scoped birth.

    Not caller-constructible, and not constructible by any executive component:
    only `ConstitutionalBirthAuthority.assess` holds the issuing token, and only
    when every preventer was cleared.

    Everything the certificate preserves is a gate-issued object or derived from
    one -- origin, scope, necessity readings, evidence references and trace --
    rather than caller prose.
    """

    certificate_id: str
    issuing_authority_id: str
    verdict: BirthVerdictDecision
    closure: IndependentClosureDecision
    findings: tuple[PreventerFinding, ...]
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CERTIFICATE_TOKEN:
            raise BirthCertificateAuthorityError(
                "birth certificates must be issued by ConstitutionalBirthAuthority"
            )
        _require_text(self.certificate_id, "birth certificate id")
        _require_text(self.issuing_authority_id, "issuing authority id")
        if type(self.verdict) is not BirthVerdictDecision:
            raise BirthCertificateAuthorityError(
                "a certificate requires a gate-issued birth verdict decision"
            )
        if type(self.closure) is not IndependentClosureDecision:
            raise BirthCertificateAuthorityError(
                "a certificate requires a gate-issued independent closure decision"
            )
        if type(self.trace) is not Trace:
            raise BirthCertificateAuthorityError(
                "a certificate requires a reconstructible trace"
            )
        if type(self.findings) is not tuple or any(
            type(item) is not PreventerFinding for item in self.findings
        ):
            raise BirthCertificateAuthorityError(
                "a certificate requires derived preventer findings"
            )
        covered = tuple(finding.preventer for finding in self.findings)
        if set(covered) != set(BirthPreventer) or len(covered) != len(BirthPreventer):
            raise BirthCertificateAuthorityError(
                "a certificate must record exactly one finding per preventer"
            )
        if any(finding.holds for finding in self.findings):
            raise BirthCertificateAuthorityError(
                "a certificate cannot be issued while any preventer holds"
            )
        if self.verdict.status is not BirthVerdictStatus.BIRTH_IN_SCOPE:
            raise BirthCertificateAuthorityError(
                "a certificate requires a BIRTH_IN_SCOPE verdict"
            )
        if self.verdict.request is not self.closure.request:
            raise BirthCertificateAuthorityError(
                "a certificate requires one request spoken for by both decisions"
            )

    @property
    def request(self) -> BirthAssessmentRequest:
        """The one authorized request both decisions speak for."""

        return self.verdict.request

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def scope(self) -> AuthorizedBirthVerdictScope:
        """The registry-issued scope; the born entity is usable nowhere else."""

        return self.verdict.scope

    @property
    def domain(self) -> str:
        return self.scope.domain

    @property
    def origin_model(self) -> str:
        """The test model the frozen experiment branched from, never caller text."""

        return self.specification.birth_query.test_model

    @property
    def residual_definition_id(self) -> str:
        """The residual whose survival made this birth worth considering."""

        return self.specification.residual_definition_id

    @property
    def evidence_snapshot(self) -> AuthorizedEvidenceSnapshot:
        """The authorized evidence both readings were derived on."""

        return self.request.evidence_snapshot

    @property
    def confers_freeze(self) -> bool:
        """`BirthDoesNotMeanFreeze`; `False` by construction, not by choice."""

        return False

    @property
    def confers_truth(self) -> bool:
        """`BirthDoesNotMeanTruth`; `False` by construction, not by choice."""

        return False

    @property
    def confers_global_ontology_claim(self) -> bool:
        """`ScopedBirthIsNotGlobalOntologyClaim`, unaffected by certification."""

        return False


@dataclass(frozen=True, slots=True)
class BirthCertificationAssessment:
    """The authority-issued record of one certification attempt, granted or not.

    A refusal is still a record: `preventers_that_held` names every ground that
    stopped the birth, with its reason, and `trace` reconstructs what was read.
    """

    assessment_id: str
    issuing_authority_id: str
    verdict: BirthVerdictDecision
    closure: IndependentClosureDecision
    findings: tuple[PreventerFinding, ...]
    certificate: BirthCertificate | None
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CERTIFICATE_TOKEN:
            raise BirthCertificateAuthorityError(
                "certification assessments must be issued by "
                "ConstitutionalBirthAuthority"
            )
        _require_text(self.assessment_id, "certification assessment id")
        _require_text(self.issuing_authority_id, "issuing authority id")
        if type(self.verdict) is not BirthVerdictDecision:
            raise BirthCertificateAuthorityError(
                "an assessment requires a gate-issued birth verdict decision"
            )
        if type(self.closure) is not IndependentClosureDecision:
            raise BirthCertificateAuthorityError(
                "an assessment requires a gate-issued independent closure decision"
            )
        if type(self.trace) is not Trace:
            raise BirthCertificateAuthorityError(
                "an assessment requires a reconstructible trace"
            )
        if type(self.findings) is not tuple or any(
            type(item) is not PreventerFinding for item in self.findings
        ):
            raise BirthCertificateAuthorityError(
                "an assessment requires derived preventer findings"
            )
        covered = tuple(finding.preventer for finding in self.findings)
        if set(covered) != set(BirthPreventer) or len(covered) != len(BirthPreventer):
            raise BirthCertificateAuthorityError(
                "an assessment must record exactly one finding per preventer"
            )
        held = any(finding.holds for finding in self.findings)
        if held and self.certificate is not None:
            raise BirthCertificateAuthorityError(
                "no certificate may accompany a held preventer"
            )
        if not held and type(self.certificate) is not BirthCertificate:
            raise BirthCertificateAuthorityError(
                "an assessment with every preventer cleared must carry its certificate"
            )

    @property
    def preventers_that_held(self) -> tuple[PreventerFinding, ...]:
        """Why the birth did not occur; empty only when a certificate issued."""

        return tuple(finding for finding in self.findings if finding.holds)

    @property
    def preventers_cleared(self) -> tuple[PreventerFinding, ...]:
        """What was checked and found not to stand in the way."""

        return tuple(finding for finding in self.findings if not finding.holds)

    @property
    def is_certified(self) -> bool:
        """Whether a certificate issued; derived from the findings, not written."""

        return self.certificate is not None


class ConstitutionalBirthAuthority:
    """The sole issuer of a `BirthCertificate`; it runs nothing it certifies.

    `ConstitutionalBirthAuthorityCannotExecuteTheBornEntity`: this class exposes
    `assess` and no other public method, so holding the authority that may
    certify a birth never carries the capability to use what was born.
    """

    def __init__(self, *, authority_id: str) -> None:
        _require_text(authority_id, "constitutional birth authority id")
        self._authority_id = authority_id
        self._issued: set[str] = set()
        self._lock = threading.Lock()

    @property
    def authority_id(self) -> str:
        return self._authority_id

    def assess(
        self,
        *,
        assessment_id: str,
        verdict: BirthVerdictDecision,
        closure: IndependentClosureDecision,
    ) -> BirthCertificationAssessment:
        """Derive every preventer for one request, and certify only if all clear."""

        _require_text(assessment_id, "certification assessment id")
        if type(verdict) is not BirthVerdictDecision:
            raise BirthCertificateAuthorityError(
                "certification requires a gate-issued birth verdict decision"
            )
        if type(closure) is not IndependentClosureDecision:
            raise BirthCertificateAuthorityError(
                "certification requires a gate-issued independent closure decision"
            )
        if verdict.request is not closure.request:
            raise BirthCertificateAuthorityError(
                "the verdict and the closure decision must speak for the same "
                "authorized assessment request"
            )

        findings = derive_preventer_findings(
            verdict_status=verdict.status,
            closure_status=closure.status,
            exhaustion_status=closure.exhaustion.status,
            survival_status=closure.survival.status,
            evidence_mode=closure.evidence_mode,
        )
        trace = Trace(
            (
                f"assessment:{assessment_id}",
                f"authority:{self._authority_id}",
                f"domain:{verdict.scope.domain}",
                f"scope:{verdict.scope.scope_id}",
                f"experiment:{verdict.scope.experiment_id}"
                f"@{verdict.scope.revision_id}",
                f"verdict:{verdict.status.name}",
                f"closure:{closure.status.name}",
                f"exhaustion:{closure.exhaustion.status.name}",
                f"survival:{closure.survival.status.name}",
                f"evidence_mode:{closure.evidence_mode.name}",
            )
            + tuple(
                f"preventer:{finding.preventer.value}:"
                f"{'HELD' if finding.holds else 'CLEARED'}:{finding.reason}"
                for finding in findings
            )
        )

        with self._lock:
            if assessment_id in self._issued:
                raise BirthCertificateAuthorityError(
                    "certification assessment id already issued by this authority"
                )
            self._issued.add(assessment_id)

        certificate: BirthCertificate | None = None
        if not any(finding.holds for finding in findings):
            certificate = BirthCertificate(
                certificate_id=f"certificate:{assessment_id}",
                issuing_authority_id=self._authority_id,
                verdict=verdict,
                closure=closure,
                findings=findings,
                trace=trace,
                _token=_CERTIFICATE_TOKEN,
            )
        return BirthCertificationAssessment(
            assessment_id=assessment_id,
            issuing_authority_id=self._authority_id,
            verdict=verdict,
            closure=closure,
            findings=findings,
            certificate=certificate,
            trace=trace,
            _token=_CERTIFICATE_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class ExecutableEntity:
    """A born entity admitted for use within its certificate's own scope.

    Admission carries no authority to certify anything, and the entity may not
    be used outside `certificate.domain`.
    """

    admission_id: str
    certificate: BirthCertificate
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EXECUTION_TOKEN:
            raise BirthCertificateAuthorityError(
                "executable entities must be admitted by ExecutiveAdmissionGate"
            )
        _require_text(self.admission_id, "executive admission id")
        if type(self.certificate) is not BirthCertificate:
            raise BirthCertificateAuthorityError(
                "an executable entity requires an authority-issued birth certificate"
            )

    @property
    def domain(self) -> str:
        """The only domain this entity may be used in; read from its certificate."""

        return self.certificate.domain


class ExecutiveAdmissionGate:
    """The sole issuer of an `ExecutableEntity`; it certifies nothing.

    `ExecutiveAuthorityCannotIssueBirth`: this class exposes `admit` and no
    other public method, and `admit` requires an already-issued certificate. A
    runtime component therefore cannot create the genus it needs and then argue
    for its legitimacy from having used it successfully.
    """

    @staticmethod
    def admit(*, admission_id: str, certificate: BirthCertificate) -> ExecutableEntity:
        """Admit a certified born entity for use inside its certificate's scope."""

        if type(certificate) is not BirthCertificate:
            raise BirthCertificateAuthorityError(
                "execution requires an authority-issued birth certificate"
            )
        return ExecutableEntity(
            admission_id=admission_id,
            certificate=certificate,
            _token=_EXECUTION_TOKEN,
        )


_CONSTITUTIONAL_SURFACE = frozenset({"assess", "authority_id"})
_EXECUTIVE_SURFACE = frozenset({"admit"})


def _public_surface(owner: type) -> frozenset[str]:
    return frozenset(name for name in vars(owner) if not name.startswith("_"))


if _public_surface(ConstitutionalBirthAuthority) != _CONSTITUTIONAL_SURFACE:
    raise RuntimeError(
        "ConstitutionalBirthAuthority must expose no method beyond certification"
    )
if _public_surface(ExecutiveAdmissionGate) != _EXECUTIVE_SURFACE:
    raise RuntimeError("ExecutiveAdmissionGate must expose no method beyond admission")
for _law_name, _law_text in BIRTH_CERTIFICATE_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")
