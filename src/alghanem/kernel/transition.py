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


class Outcome(Enum):
    """The complete initial vocabulary of transition outcomes.

    ``IDENTITY_PRESERVING_TRANSFORMATION`` and ``CERTIFIED_BRANCH_BIRTH`` name
    the two claim shapes a successful candidate can take. At Kernel v0.1 they
    are produced only by ``StructuralAdmissionGate``, which certifies
    structural completeness, not that identity was actually preserved or that
    a branch was authoritatively confirmed to have been born. The
    corresponding
    ``TransitionCandidate.kind`` / ``StructurallyAdmissibleTransition.kind``
    (a ``TransitionKind``) is the honestly-named claim; these two ``Outcome``
    members are reserved to describe a future, fully certified
    ``LicensedTransition`` once evidence-sufficiency and authority gates
    exist. Reading a structurally admissible transition's outcome as already
    certified is exactly the confusion this vocabulary must not create.
    """

    IDENTITY_PRESERVING_TRANSFORMATION = auto()
    CERTIFIED_BRANCH_BIRTH = auto()
    BLOCK = auto()
    DEFER = auto()
    UNDEFINED = auto()


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
    evidence-sufficiency gate exists.
    """

    IDENTITY_PRESERVATION_CLAIM = auto()
    BRANCH_BIRTH_CLAIM = auto()


_KIND_FOR_OUTCOME = {
    Outcome.IDENTITY_PRESERVING_TRANSFORMATION: (
        TransitionKind.IDENTITY_PRESERVATION_CLAIM
    ),
    Outcome.CERTIFIED_BRANCH_BIRTH: TransitionKind.BRANCH_BIRTH_CLAIM,
}


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
    outcome: Outcome
    result: OperationResult | None
    branch_origin_provenance: BranchOriginProvenance | None = None
    target_anchor: Anchor | None = None
    kind: TransitionKind | None = None

    @property
    def resolved_target_anchor(self) -> Anchor:
        """The declared target anchor, defaulting to the source anchor.

        A convenience view for incomplete candidates only; it never satisfies
        the explicit-target-anchor requirement for a successful transition.
        """
        return self.target_anchor if self.target_anchor is not None else self.anchor

    def __post_init__(self) -> None:
        _validate_candidate_components(self)
        _validate_kind(self)

    def validate_success(self) -> None:
        """Validate the structural laws required for structural admission."""

        _validate_successful_transition_fields(self)


@dataclass(frozen=True, slots=True)
class StructurallyAdmissibleTransition(TransitionCandidate):
    """A transition that is structurally complete, issued only by the gate.

    Structural admission is not evidential sufficiency and not authority to
    cross domains: it certifies that the transition is well-formed under the
    Kernel v0.1 structural laws (explicit anchors, claim-bound evidence,
    preserved/changed separation, branch provenance, and so on). Whether the
    bound evidence is *sufficient* to support the claim, whether a rank or
    layer has *authority* to make the transition, and whether crossing
    domains is *licensed* are all deferred questions Kernel v0.1 does not
    answer. ``StructurallyAdmissibleTransition`` therefore must not be read
    as ``LicensedTransition``: representability is not licensability.

    ``kind`` is the honestly-named claim (a ``TransitionKind``) this
    transition makes; ``outcome`` names the same claim shape for backward
    compatibility with the wider decision vocabulary, but neither field
    certifies that the claim is true. Certification is a future gate.

    Use ``StructuralAdmissionGate.admit`` on a candidate to create this type.
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
        _validate_candidate_components(self)
        _validate_kind(self)
        self.validate_success()


class StructuralAdmissionGate:
    """Minimal structural admission boundary for successful transitions.

    This gate only certifies structural completeness. It does not certify
    evidential sufficiency, domain-transition authority, or layer authority;
    those remain deferred beyond Kernel v0.1. Already admitted transitions
    are rejected rather than re-admitted.
    """

    @staticmethod
    def admit(candidate: TransitionCandidate) -> StructurallyAdmissibleTransition:
        """Issue a structurally admissible transition after validation."""

        if isinstance(candidate, StructurallyAdmissibleTransition):
            raise ValueError(
                "structurally admissible transitions cannot be re-admitted"
            )
        return StructurallyAdmissibleTransition(
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
            outcome=candidate.outcome,
            result=candidate.result,
            branch_origin_provenance=candidate.branch_origin_provenance,
            target_anchor=candidate.target_anchor,
            kind=candidate.kind,
            _admission_token=_ADMISSION_TOKEN,
        )


def _validate_components(label: str, components: tuple[str, ...]) -> None:
    if any(not component.strip() for component in components):
        raise ValueError(f"{label} cannot be blank")
    if len(set(components)) != len(components):
        raise ValueError(f"{label} must be unique")


def _validate_candidate_components(candidate: TransitionCandidate) -> None:
    _validate_components("preserved components", candidate.preserved)
    _validate_components("changed components", candidate.changed)


def _validate_kind(candidate: TransitionCandidate) -> None:
    """Validate that a candidate's declared kind matches its outcome.

    ``kind`` and ``outcome`` are kept as two independent fields on purpose,
    not one derived from the other: ``outcome`` is the decision-level
    vocabulary slot (shared with ``TransitionDecision`` and the future,
    fully certified ``LicensedTransition``), while ``kind`` is the narrower,
    honestly-named claim a candidate itself makes. They coincide 1:1 today
    only because Kernel v0.1 has exactly two success-shaped outcomes; a
    future kind vocabulary is not required to stay in lockstep with the
    outcome vocabulary (for example, distinct kinds might later map to the
    same certified outcome). This function is the explicit seam that keeps
    the two fields consistent for as long as they do overlap, rather than
    collapsing them into a single field that a later split would have to
    re-separate.
    """

    expected_kind = _KIND_FOR_OUTCOME.get(candidate.outcome)
    if expected_kind is None:
        if candidate.kind is not None:
            raise ValueError(
                "non-transition outcomes cannot declare a claimed transition kind"
            )
        return
    if candidate.kind is None:
        raise ValueError("a successful outcome requires a declared transition kind")
    if candidate.kind is not expected_kind:
        raise ValueError("declared transition kind must match the candidate's outcome")


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
    if candidate.outcome in {Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED}:
        raise ValueError(
            "non-transition outcomes cannot be StructurallyAdmissibleTransition"
        )
    if not candidate.evidence:
        raise ValueError("successful transitions require evidence")
    if any(
        evidence.claim_id != candidate.claim.claim_id for evidence in candidate.evidence
    ):
        raise ValueError("transition evidence must be bound to its claim")
    if candidate.outcome is Outcome.IDENTITY_PRESERVING_TRANSFORMATION:
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
    if not candidate.changed:
        raise ValueError("successful transitions require a declared change")
    if candidate.operation.declared_change not in candidate.changed:
        raise ValueError(
            "transition changes must include the operation's declared change"
        )
    if not set(candidate.preserved).isdisjoint(candidate.changed):
        raise ValueError("preserved and changed components must be disjoint")
    if candidate.outcome is Outcome.CERTIFIED_BRANCH_BIRTH:
        _validate_branch_birth(candidate)


def _validate_branch_birth(candidate: TransitionCandidate) -> None:
    if not candidate.preserved:
        raise ValueError("certified branch births require preserved information")
    if candidate.branch_origin_provenance is None:
        raise ValueError("certified branch births require explicit origin provenance")
    if candidate.branch_origin_provenance.origin_anchor != candidate.anchor:
        raise ValueError("branch origin provenance must match the transition anchor")
    if candidate.target_anchor is None:
        raise ValueError("certified branch births require an explicit target anchor")
    target_anchor = candidate.target_anchor
    if target_anchor == candidate.anchor:
        raise ValueError("certified branch births require a distinct target anchor")
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
class TransitionDecision:
    """The assessment of an attempted transition, successful or not."""

    outcome: Outcome
    admissible: StructurallyAdmissibleTransition | None = None
    audit: NonSuccessDecisionAudit | None = None

    def __post_init__(self) -> None:
        successful = {
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            Outcome.CERTIFIED_BRANCH_BIRTH,
        }
        if self.outcome in successful:
            if self.admissible is None:
                raise ValueError(
                    "successful decisions require a structurally admissible transition"
                )
            if self.audit is not None:
                raise ValueError(
                    "successful decisions cannot carry a non-success audit"
                )
        else:
            if self.admissible is not None:
                raise ValueError(
                    "non-transition decisions cannot contain a structurally "
                    "admissible transition"
                )
            if self.audit is None:
                raise ValueError("non-transition decisions require an audit record")
        if self.admissible is not None and self.outcome is not self.admissible.outcome:
            raise ValueError(
                "decision and structurally admissible transition outcomes must match"
            )
