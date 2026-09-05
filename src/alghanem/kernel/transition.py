"""Transition candidates, structurally admissible transitions, and
explicit decisions."""

from dataclasses import InitVar, dataclass
from enum import Enum, auto

from .anchor import Anchor, State
from .evidence import Claim, Evidence
from .operation import Operation, OperationResult
from .residual import Residual
from .trace import Trace

_ADMISSION_TOKEN = object()


class TransitionKind(Enum):
    """What a transition candidate claims to be, prior to certification.

    A claimed kind is not a certified outcome. ``StructuralAdmissionGate``
    validates that a candidate of this kind is well-formed under Kernel
    v0.1's structural laws (for example, that an identity-preservation claim
    declares an unchanged target anchor); it does not verify that the claim
    is true. In particular, anchor equality (``target_anchor == anchor``) is
    a structural check, not proof that identity was preserved in substance:
    ``AnchorEquality != ProvenIdentityPreservation``. Likewise, declaring a
    name in ``preserved`` or ``changed`` is not proof that the named
    component was actually extracted from ``before_state``/``after_state``:
    ``DeclaredInvariant != VerifiedInvariant``. Both remain deferred until an
    evidence-sufficiency gate exists. See ``docs/CONSTITUTION.md`` for the
    full epistemic ladder this vocabulary sits on.
    """

    IDENTITY_PRESERVATION_CLAIM = auto()
    BRANCH_BIRTH_CLAIM = auto()


class CertifiedOutcome(Enum):
    """The vocabulary of fully certified transition outcomes.

    ``IDENTITY_PRESERVING_TRANSFORMATION`` and ``CERTIFIED_BRANCH_BIRTH`` are
    strictly reserved for the final certification stage (a future
    ``CertifiedTransition`` / ``CertifiedLicensedTransition``). They cannot be
    carried by uncertified ``TransitionCandidate`` proposals or by intermediate
    ``StructurallyAdmissibleTransition``s, which only certify structural
    well-formedness.
    """

    IDENTITY_PRESERVING_TRANSFORMATION = auto()
    CERTIFIED_BRANCH_BIRTH = auto()


class StructuralDecisionStatus(Enum):
    """The status of a structural admission assessment.

    ``ADMITTED`` indicates the transition candidate satisfies all structural
    laws and was issued as a ``StructurallyAdmissibleTransition``. ``BLOCK``,
    ``DEFER``, and ``UNDEFINED`` are non-admission decision statuses; they are
    external judgments rendered on or without a candidate, never intrinsic
    properties of a candidate itself.
    """

    ADMITTED = auto()
    BLOCK = auto()
    DEFER = auto()
    UNDEFINED = auto()


@dataclass(frozen=True, slots=True)
class BranchOriginProvenance:
    """Structural origin provenance for preserved branch components."""

    origin_anchor: Anchor
    branch_anchor: Anchor
    preserved_components: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.preserved_components:
            raise ValueError("branch origin provenance requires preserved components")
        _validate_components(
            "branch origin provenance preserved components",
            self.preserved_components,
        )
        if self.branch_anchor == self.origin_anchor:
            raise ValueError(
                "branch origin provenance requires a distinct branch anchor"
            )


@dataclass(frozen=True, slots=True)
class TransitionCandidate:
    """A transition-shaped candidate that has not crossed the admission boundary.

    A candidate declares what it claims to be via ``kind`` (a ``TransitionKind``),
    together with its anchors, state representations, operation, claim, evidence,
    and trace history. It does not carry an outcome or decision status: candidates
    do not judge or certify themselves.

    ``anchor`` is the source anchor; ``target_anchor`` is the explicitly
    declared anchor the transition targets. A candidate may omit
    ``target_anchor`` before admission, but a successful transition must
    declare it explicitly; ``resolved_target_anchor`` never substitutes for
    the explicitness requirement.
    """

    anchor: Anchor
    before_state: State
    operation: Operation
    after_state: State
    claim: Claim
    evidence: tuple[Evidence, ...]
    preserved: tuple[str, ...]
    changed: tuple[str, ...]
    trace: Trace
    residuals: tuple[Residual, ...]
    kind: TransitionKind
    result: OperationResult | None = None
    branch_origin_provenance: BranchOriginProvenance | None = None
    target_anchor: Anchor | None = None

    @property
    def resolved_target_anchor(self) -> Anchor:
        """The declared target anchor, defaulting to the source anchor.

        A convenience view for incomplete candidates only; it never satisfies
        the explicit-target-anchor requirement for a successful transition.
        """
        return self.target_anchor if self.target_anchor is not None else self.anchor

    def __post_init__(self) -> None:
        if not isinstance(self.kind, TransitionKind):
            raise ValueError("a candidate requires a declared TransitionKind")
        _validate_candidate_components(self)

    def validate_success(self) -> None:
        """Validate the structural laws required for structural admission."""

        _validate_successful_transition_fields(self)


@dataclass(frozen=True, slots=True)
class StructurallyAdmissibleTransition(TransitionCandidate):
    """A transition that is structurally complete, issued only by the gate.

    Structural admission is not evidential sufficiency, not authority to
    cross domains, and not final certification: it certifies that the transition
    is well-formed under the Kernel v0.1 structural laws (explicit anchors,
    claim-bound evidence, preserved/changed separation, branch provenance, and
    so on).

    ``kind`` is the honestly-named claim (a ``TransitionKind``) this
    transition makes. It does not carry a ``CertifiedOutcome``; certification
    is a future gate at the end of the epistemic ladder.

    Use ``StructuralAdmissionGate.assess`` or ``require_admitted`` on a
    candidate to create this type.
    Dataclass replacement paths that rerun ``__init__`` are not admission
    paths.
    """

    _admission_token: InitVar[object | None] = None

    def __post_init__(self, _admission_token: object | None) -> None:
        if _admission_token is not _ADMISSION_TOKEN:
            raise ValueError(
                "structurally admissible transitions must be issued by "
                "StructuralAdmissionGate"
            )
        # Re-validated here, not inherited from TransitionCandidate: this
        # dataclass's own __post_init__ fully overrides the parent's, and
        # any dataclasses.replace() on an existing instance re-runs __init__
        # (and therefore this method), so the checks must be re-asserted
        # rather than assumed to still hold.
        if not isinstance(self.kind, TransitionKind):
            raise ValueError("a candidate requires a declared TransitionKind")
        _validate_candidate_components(self)
        self.validate_success()


class StructuralAdmissionGate:
    """Structural admission boundary that records every candidate assessment.

    This gate only certifies structural completeness. It does not certify
    evidential sufficiency, domain-transition authority, or layer authority;
    those remain deferred beyond Kernel v0.1. Already admitted transitions
    are rejected as API misuse rather than re-admitted.
    """

    @staticmethod
    def assess(candidate: TransitionCandidate) -> "StructuralAdmissionDecision":
        """Assess a candidate, recording structural failure as a BLOCK decision."""

        if not isinstance(candidate, TransitionCandidate):
            raise TypeError("structural admission requires a TransitionCandidate")
        if isinstance(candidate, StructurallyAdmissibleTransition):
            raise ValueError(
                "structurally admissible transitions cannot be re-admitted"
            )
        try:
            transition = StructurallyAdmissibleTransition(
                anchor=candidate.anchor,
                before_state=candidate.before_state,
                operation=candidate.operation,
                after_state=candidate.after_state,
                claim=candidate.claim,
                evidence=candidate.evidence,
                preserved=candidate.preserved,
                changed=candidate.changed,
                trace=candidate.trace,
                residuals=candidate.residuals,
                kind=candidate.kind,
                result=candidate.result,
                branch_origin_provenance=candidate.branch_origin_provenance,
                target_anchor=candidate.target_anchor,
                _admission_token=_ADMISSION_TOKEN,
            )
        except ValueError as error:
            return StructuralAdmissionDecision(
                status=StructuralDecisionStatus.BLOCK,
                audit=NonSuccessDecisionAudit(
                    trace=candidate.trace,
                    residuals=candidate.residuals,
                    reason=str(error),
                    candidate=candidate,
                ),
            )
        return StructuralAdmissionDecision(
            status=StructuralDecisionStatus.ADMITTED,
            transition=transition,
        )

    @staticmethod
    def require_admitted(
        candidate: TransitionCandidate,
    ) -> StructurallyAdmissibleTransition:
        """Return an admitted transition or raise for structural refusal."""

        decision = StructuralAdmissionGate.assess(candidate)
        if decision.transition is None:
            assert decision.audit is not None
            raise ValueError(decision.audit.reason)
        return decision.transition


def _validate_components(label: str, components: tuple[str, ...]) -> None:
    if any(not component.strip() for component in components):
        raise ValueError(f"{label} cannot be blank")
    if len(set(components)) != len(components):
        raise ValueError(f"{label} must be unique")


def _validate_candidate_components(candidate: TransitionCandidate) -> None:
    _validate_components("preserved components", candidate.preserved)
    _validate_components("changed components", candidate.changed)


def _validate_successful_transition_fields(candidate: TransitionCandidate) -> None:
    if candidate.result is None:
        raise ValueError("successful transitions require a result")
    if (
        candidate.operation.source_domain is not None
        and candidate.operation.source_domain != candidate.anchor.domain
    ):
        raise ValueError(
            "operation source domain must match the transition anchor domain"
        )
    if candidate.target_anchor is None:
        raise ValueError("successful transitions require an explicit target anchor")
    target_anchor = candidate.target_anchor
    if (
        candidate.operation.target_domain is not None
        and candidate.operation.target_domain != target_anchor.domain
    ):
        raise ValueError("operation target domain must match the target anchor domain")
    if not candidate.evidence:
        raise ValueError("successful transitions require evidence")
    if any(
        evidence.claim_id != candidate.claim.claim_id for evidence in candidate.evidence
    ):
        raise ValueError("transition evidence must be bound to its claim")
    if candidate.kind is TransitionKind.IDENTITY_PRESERVATION_CLAIM:
        if not candidate.preserved:
            raise ValueError("identity-preserving transformations require an invariant")
        if not candidate.changed:
            raise ValueError(
                "identity-preserving transformations require a declared change"
            )
        if target_anchor != candidate.anchor:
            raise ValueError(
                "identity-preserving transformations require an unchanged anchor"
            )
    elif candidate.kind is TransitionKind.BRANCH_BIRTH_CLAIM:
        _validate_branch_birth(candidate)
    else:
        raise ValueError("unrecognized transition kind")

    if not candidate.changed:
        raise ValueError("successful transitions require a declared change")
    if candidate.operation.declared_change not in candidate.changed:
        raise ValueError(
            "transition changes must include the operation's declared change"
        )
    if not set(candidate.preserved).isdisjoint(candidate.changed):
        raise ValueError("preserved and changed components must be disjoint")


def _validate_branch_birth(candidate: TransitionCandidate) -> None:
    if not candidate.preserved:
        raise ValueError("branch-birth claims require preserved information")
    if candidate.branch_origin_provenance is None:
        raise ValueError("branch-birth claims require explicit origin provenance")
    if candidate.branch_origin_provenance.origin_anchor != candidate.anchor:
        raise ValueError("branch origin provenance must match the transition anchor")
    if candidate.target_anchor is None:
        raise ValueError("branch-birth claims require an explicit target anchor")
    target_anchor = candidate.target_anchor
    if target_anchor == candidate.anchor:
        raise ValueError("branch-birth claims require a distinct target anchor")
    if candidate.branch_origin_provenance.branch_anchor != target_anchor:
        raise ValueError(
            "branch origin provenance branch anchor must be the target anchor"
        )
    provenance_components = set(candidate.branch_origin_provenance.preserved_components)
    if not provenance_components.issubset(set(candidate.preserved)):
        raise ValueError(
            "branch origin provenance components must be declared preserved"
        )


class DecisionReasonCode(Enum):
    """A machine-auditable classification of a non-success decision.

    ``reason`` remains the human-readable explanation; ``reason_code`` is an
    optional, coarse-grained classification meant to make BLOCK and DEFER
    decisions queryable at scale. It does not replace ``reason`` and does not
    itself carry additional structural authority. Some members (for example
    ``AUTHORITY_NOT_AVAILABLE`` and ``PROOF_INSUFFICIENT``) name deferred
    concepts — authority and evidential sufficiency — that Kernel v0.1's
    structural admission gate does not adjudicate; they are reserved for
    decisions made by future authority/evidence gates layered on top of this
    kernel, not something ``StructuralAdmissionGate`` itself determines.
    """

    MISSING_EVIDENCE = auto()
    DOMAIN_MISMATCH = auto()
    TARGET_ANCHOR_MISMATCH = auto()
    INVARIANT_VIOLATION = auto()
    PROVENANCE_VIOLATION = auto()
    RESIDUAL_UNRESOLVED = auto()
    AUTHORITY_NOT_AVAILABLE = auto()
    PROOF_INSUFFICIENT = auto()


@dataclass(frozen=True, slots=True)
class NonSuccessDecisionAudit:
    """Reviewable record of a decision that did not admit a transition.

    A non-success decision is not an erased history: it preserves the trace,
    the residuals, and a structural reason so the decision can be reviewed.
    When an assessed candidate exists, the audit trace and residuals are bound
    to that candidate's own history, so no history is fabricated or attached
    without provenance. Without a candidate, the audit owns its trace and
    residuals directly. Residuals are preserved, not interpreted.

    ``reason_code``, when present, is an optional machine-auditable
    classification; the kernel does not verify that it is semantically
    consistent with the free-text ``reason``, so callers issuing an audit are
    responsible for keeping the two aligned.
    """

    trace: Trace
    residuals: tuple[Residual, ...]
    reason: str
    candidate: TransitionCandidate | None = None
    reason_code: DecisionReasonCode | None = None

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise ValueError("non-success decisions require a structural reason")
        if self.reason_code is not None and not isinstance(
            self.reason_code, DecisionReasonCode
        ):
            raise ValueError("reason_code must be a DecisionReasonCode member")
        if self.candidate is not None and isinstance(
            self.candidate, StructurallyAdmissibleTransition
        ):
            raise ValueError(
                "non-success decision audits cannot reference a structurally "
                "admissible transition"
            )
        if self.candidate is not None and self.trace != self.candidate.trace:
            raise ValueError(
                "non-success decision audit trace must match the candidate trace"
            )
        if self.candidate is not None and self.residuals != self.candidate.residuals:
            raise ValueError(
                "non-success decision audit residuals must match the candidate"
            )


@dataclass(frozen=True, slots=True)
class StructuralAdmissionDecision:
    """The assessment of an attempted transition admission, successful or not."""

    status: StructuralDecisionStatus
    transition: StructurallyAdmissibleTransition | None = None
    audit: NonSuccessDecisionAudit | None = None

    @property
    def admissible(self) -> StructurallyAdmissibleTransition | None:
        """Compatibility property for accessing the admitted transition."""
        return self.transition

    def __post_init__(self) -> None:
        if not isinstance(self.status, StructuralDecisionStatus):
            raise ValueError("status must be a StructuralDecisionStatus member")
        if self.status is StructuralDecisionStatus.ADMITTED:
            if self.transition is None:
                raise ValueError(
                    "admitted decisions require a structurally admissible transition"
                )
            if self.audit is not None:
                raise ValueError("admitted decisions cannot carry a non-success audit")
        else:
            if self.transition is not None:
                raise ValueError(
                    "non-admitted decisions cannot contain a structurally "
                    "admissible transition"
                )
            if self.audit is None:
                raise ValueError("non-admitted decisions require an audit record")
