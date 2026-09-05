"""Verified invariant preservation: authorized specs, extractors, and verification.

A ``TransitionCandidate`` may declare a component name in ``preserved``, but
that is only a claim: ``DeclaredInvariant != VerifiedInvariant``. This module
closes that gap for a single named invariant at a time, without letting the
candidate supply its own proof, and without letting the candidate or caller
choose which extractor is authoritative for a given invariant/component.

``InvariantSpec`` names *what* should be checked (an invariant id, the
preserved component it refers to, and a claimed extractor id) but never
carries an executable extractor itself. Extractors are registered
independently in an ``InvariantExtractorRegistry``; resolving an
``extractor_id`` to an actual callable is that registry's authority alone.
This keeps ``Candidate does not own certification authority``: nothing here
lets a candidate hand in ``lambda before, after: True`` and "verify" itself.
But merely being a *registered* extractor id is not enough authority to
check *any* component: ``RegisteredInvariantDefinition`` additionally binds
a specific ``(domain, component, invariant_id)`` to exactly one authorized
``extractor_id``, and ``InvariantVerificationGate.verify`` resolves through
that authorization, not through a bare id lookup. A spec naming a
registered-but-unauthorized extractor id for its component is treated the
same as an unregistered one: epistemically untestable, not a candidate- or
caller-chosen "proof".

Hardening laws close this module's scope for Kernel v0.1:

1. ``VerificationResult must be gate-issued``: ``InvariantVerification`` is
   constructible only through ``InvariantVerificationGate.verify``, enforced
   by a private sentinel token -- not merely documented as the "only way".
2. ``Layer does not own verifier authority``: registration (mutable,
   trusted-setup-owned ``InvariantExtractorRegistry``) is a distinct type
   from resolution (read-only ``SealedInvariantExtractorRegistry``, produced
   by ``InvariantExtractorRegistry.seal()``). ``InvariantVerificationGate``
   only ever accepts the sealed, read-only view; it never registers
   extractors and never manufactures registry/governor authority itself.
3. ``NoVerifiedInvariantWithoutAuthorizedVerifierBinding``: a component can
   only be checked with the specific extractor id that a trusted
   ``RegisteredInvariantDefinition`` authorizes for that exact
   ``(domain, component, invariant_id)`` triple. ``InvariantSpec`` cannot
   freely pick any registered extractor id and have it accepted merely
   because it exists in the sealed registry: ``Candidate/Caller does not
   own verifier selection authority``.
4. ``NoInvariantVerificationWithoutSourceTransitionBinding``: every
   ``InvariantVerification`` carries an ``InvariantVerificationProvenance``
   binding it to the specific transition it was checked against (claim id,
   source anchor, resolved target anchor, and source trace), so a
   verification produced for one transition cannot be silently accepted as
   evidence for another via ``InvariantVerificationGate.require_bound_to``.
5. Exact transition and snapshot identity: structural admission issues an
   opaque ``admission_id`` and sealing issues a ``registry_snapshot_id``;
   verification provenance records both, so matching claim fields alone cannot
   authorize replay.
6. Complete coverage: ``InvariantVerificationBundle`` accepts exactly one
   successful verification for every declared preserved component, while
   ``InvariantVerificationDecision`` preserves blocked/deferred attempts for
   audit.
7. Boolean comparison integrity: ``before_value == after_value`` is not
   assumed to return an actual ``bool`` (for example, some libraries'
   ``__eq__`` return non-bool values). A non-``bool`` comparison result is
   rejected with a typed ``InvariantComparisonError`` rather than silently
   coerced into a verification.
8. ``VerificationArtifactAuthorityMustMatchConstitutionalWording``: both
   ``InvariantVerificationDecision`` and ``InvariantVerificationBundle`` are
   gate-issued only, enforced by private sentinel tokens -- not merely one
   of the two. A caller cannot hand-build
   ``InvariantVerificationDecision(status=VERIFIED, ...)`` or a bare
   ``InvariantVerificationBundle(...)`` without going through
   ``InvariantVerificationGate``, and a ``VERIFIED`` decision enforces the
   same complete-coverage, no-duplicates, transition-bound,
   single-snapshot requirements as the bundle.
9. ``KnownFalsificationDominatesEpistemicDeferral``: aggregating a
   transition's complete preserved set never lets an untestable component
   erase an already-disproved one. Every declared component is assessed
   (not just up to the first failure), and the aggregate follows strict
   precedence -- ``BLOCK`` if any component is disproved, else ``DEFER`` if
   any remaining component is untestable, else ``VERIFIED`` -- independent
   of the order ``specs`` are given in. Disproved (``failed_components``)
   and untestable (``deferred_components``) components are recorded
   separately, never merged into one undifferentiated list.
10. Metadata only, not content identity: ``admission_id`` and
    ``registry_snapshot_id`` are opaque, run-specific identities (fresh
    ``uuid4().hex`` per instance) that guard against accidental replay.
    ``transition_projection_fingerprint`` and ``registry_projection_hash``
    are recorded alongside them as corroborating, deterministic
    *projections* of part of the transition/registry content -- they are
    **not** claimed as canonical content identity or a reproducibility
    guarantee (see their own docstrings for exactly what each omits), and
    must not be used to promote epistemic status. A full canonical content
    identity is deferred to a dedicated reproducibility PR.
11. ``MalformedRequestIsNotDisprovedInvariant``: ``BLOCK`` means at least
    one component was actually verified against an authorized extractor
    and found not preserved. Specs that fail to exactly cover
    ``transition.preserved``, or that duplicate a component, were never
    checked against anything -- ``assess_all_preserved`` raises a typed
    ``InvariantAssessmentSpecificationError`` for these instead of
    returning a ``BLOCK`` decision with fabricated ``failed_components``,
    so a malformed caller request can never masquerade as a disproved
    invariant.

``InvariantVerificationGate.verify`` is the only way to produce an
``InvariantVerification``. It resolves an authorized extractor and extracts
a value from ``before_state`` and ``after_state``, reporting whether they
are equal; a candidate cannot construct this outcome by declaring
``preserved=True``.

Scope: this gate checks declared invariants against one already structurally
admitted transition. It does not, by itself, make invariant verification
mandatory for structural admission, and it is not evidential sufficiency,
authority licensing, or certification -- those remain later, undelivered rungs
of the epistemic ladder in ``docs/CONSTITUTION.md``. Nor
is anything here a cryptographic identity guarantee: the sentinel tokens and
provenance binding raise the bar against accidental misuse and casual
replay, not against a determined, dishonest caller fabricating matching
field values by hand.
"""

import hashlib
import threading
from collections.abc import Callable, Mapping
from dataclasses import InitVar, dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING
from uuid import uuid4

from .anchor import Anchor, State
from .trace import Trace

if TYPE_CHECKING:
    from .transition import StructurallyAdmissibleTransition

InvariantExtractor = Callable[[State], object]

_VERIFICATION_TOKEN = object()
_SEAL_TOKEN = object()
_DECISION_TOKEN = object()
_BUNDLE_TOKEN = object()


@dataclass(frozen=True, slots=True)
class InvariantSpec:
    """A claimed invariant to verify: a name, a component, and an extractor id.

    This is ``ClaimedInvariant``, not ``VerifiedInvariant``: declaring a spec
    is not proof that ``component`` was preserved. ``extractor_id`` is a
    lookup key into an ``InvariantExtractorRegistry``, never an executable
    callable, so a spec cannot embed its own ad hoc "proof". Naming a
    registered ``extractor_id`` here is only a *claim* about which extractor
    should be used, not a grant of authority to use it:
    ``InvariantVerificationGate.verify`` independently checks that a
    ``RegisteredInvariantDefinition`` actually authorizes this exact
    ``extractor_id`` for the spec's ``(component, invariant_id)`` (and the
    transition's domain) before resolving it. A spec naming a registered but
    unauthorized extractor id is rejected the same way as one naming an
    unregistered id.
    """

    invariant_id: str
    component: str
    extractor_id: str

    def __post_init__(self) -> None:
        if not self.invariant_id.strip():
            raise ValueError("an invariant spec requires an invariant id")
        if not self.component.strip():
            raise ValueError("an invariant spec requires a component name")
        if not self.extractor_id.strip():
            raise ValueError("an invariant spec requires a registered extractor id")


@dataclass(frozen=True, slots=True)
class RegisteredInvariantDefinition:
    """A trusted, registry-owned authorization binding a verifier to a scope.

    This is the authority a bare ``extractor_id`` lookup was missing:
    registering a callable under an ``extractor_id`` only makes that
    callable resolvable, it does not say which invariant/component/domain
    it is *authorized* to check. A ``RegisteredInvariantDefinition`` closes
    that gap by binding exactly one ``extractor_id`` to a specific
    ``(domain, component, invariant_id)`` scope, plus a ``version`` for
    future evolution of the authorization itself. Only trusted
    registration/governor code (``InvariantExtractorRegistry.authorize``)
    can create this binding; an ``InvariantSpec`` cannot manufacture one, so
    ``Candidate/Caller does not own verifier selection authority``.
    """

    domain: str
    component: str
    invariant_id: str
    extractor_id: str
    version: str = "1"

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("a registered invariant definition requires a domain")
        if not self.component.strip():
            raise ValueError("a registered invariant definition requires a component")
        if not self.invariant_id.strip():
            raise ValueError(
                "a registered invariant definition requires an invariant id"
            )
        if not self.extractor_id.strip():
            raise ValueError(
                "a registered invariant definition requires an extractor id"
            )
        if not self.version.strip():
            raise ValueError("a registered invariant definition requires a version")


@dataclass(frozen=True, slots=True)
class InvariantObservation:
    """The raw before/after values extracted for a claimed invariant."""

    invariant_id: str
    before_value: object
    after_value: object

    def __post_init__(self) -> None:
        if not self.invariant_id.strip():
            raise ValueError("an invariant observation requires an invariant id")


@dataclass(frozen=True, slots=True)
class InvariantVerificationProvenance:
    """Binds an ``InvariantVerification`` to the specific transition it checked.

    Copying ``trace.events`` into the verification's own trace does not, by
    itself, prove that the verification actually ran against a particular
    transition: it is just data that could be copied onto an unrelated
    verification. This provenance record additionally captures identifying
    fields of the source ``StructurallyAdmissibleTransition`` -- its claim
    id, source anchor, resolved target anchor, and its own trace -- together
    with the invariant/extractor ids that were checked. Combined with
    ``InvariantVerificationGate.require_bound_to``, this prevents a
    verification produced for transition T1 from being silently accepted as
    evidence for a different transition T2, even when both declare the same
    ``invariant_id``: ``Verification(T1) does not imply Verification(T2)``.

    This is a structural binding, not a cryptographic identity claim.

    ``source_admission_id``/``registry_snapshot_id`` are opaque, run-specific
    identities (each a fresh ``uuid4().hex``) that guard against accidental
    replay across instances. ``source_transition_projection_fingerprint``/
    ``registry_projection_hash`` are recorded alongside them as
    corroborating, deterministic *projections* of part of the
    transition/registry content: ``OccurrenceIdentity != ContentIdentity``.
    They are **not** canonical content identity (see their own docstrings
    for exactly what each omits) and must not be used to promote epistemic
    status; a full canonical content identity is deferred to a dedicated
    reproducibility PR.
    """

    source_claim_id: str
    source_anchor: Anchor
    source_target_anchor: Anchor
    source_trace: Trace
    invariant_id: str
    extractor_id: str
    source_admission_id: str | None = None
    registry_snapshot_id: str | None = None
    source_transition_projection_fingerprint: str | None = None
    registry_projection_hash: str | None = None

    def __post_init__(self) -> None:
        if not self.source_claim_id.strip():
            raise ValueError(
                "invariant verification provenance requires a source claim id"
            )
        if not self.invariant_id.strip():
            raise ValueError(
                "invariant verification provenance requires an invariant id"
            )
        if not self.extractor_id.strip():
            raise ValueError(
                "invariant verification provenance requires an extractor id"
            )
        if (
            self.source_admission_id is not None
            and not self.source_admission_id.strip()
        ):
            raise ValueError(
                "invariant verification provenance requires an admission id"
            )
        if (
            self.registry_snapshot_id is not None
            and not self.registry_snapshot_id.strip()
        ):
            raise ValueError(
                "invariant verification provenance requires a registry snapshot id"
            )
        if (
            self.source_transition_projection_fingerprint is not None
            and not self.source_transition_projection_fingerprint.strip()
        ):
            raise ValueError(
                "invariant verification provenance requires a transition "
                "projection fingerprint"
            )
        if (
            self.registry_projection_hash is not None
            and not self.registry_projection_hash.strip()
        ):
            raise ValueError(
                "invariant verification provenance requires a registry projection hash"
            )


@dataclass(frozen=True, slots=True)
class InvariantVerification:
    """The independently produced result of checking I(before) == I(after).

    Never constructed from a candidate's own declaration: a candidate saying
    ``preserved=True`` is a claim, not a verification.
    ``ClaimedInvariant != VerifiedInvariant``. Construction is enforced, not
    merely documented, to be gate-issued: passing anything other than
    ``InvariantVerificationGate``'s private token raises.
    """

    invariant_id: str
    preserved: bool
    trace: Trace
    observation: InvariantObservation
    provenance: InvariantVerificationProvenance
    component: str = ""
    # The leading underscore here does not mean "conventionally private but
    # freely usable by keyword"; it means "gate-only". No caller outside
    # ``InvariantVerificationGate.verify`` holds a reference to
    # ``_VERIFICATION_TOKEN``, so passing this keyword directly is only ever
    # legitimate from that gate (or from white-box tests that deliberately
    # import the token to exercise otherwise-unreachable invariants). This
    # mirrors the existing ``_admission_token`` convention on
    # ``StructurallyAdmissibleTransition`` in ``transition.py``.
    _verification_token: InitVar[object | None] = None

    def __post_init__(self, _verification_token: object | None) -> None:
        if _verification_token is not _VERIFICATION_TOKEN:
            raise ValueError(
                "invariant verifications must be issued by "
                "InvariantVerificationGate.verify"
            )
        if not self.invariant_id.strip():
            raise ValueError("an invariant verification requires an invariant id")
        # `type(...) is not bool` (not `isinstance`) is deliberate: it rejects
        # bool subclasses too, so a truthy/falsy-but-not-actually-bool value
        # cannot masquerade as a genuine preservation decision.
        if type(self.preserved) is not bool:
            raise ValueError("an invariant verification's preserved must be a bool")
        if self.invariant_id != self.observation.invariant_id:
            raise ValueError(
                "invariant verification must reference its own observation"
            )
        if self.invariant_id != self.provenance.invariant_id:
            raise ValueError("invariant verification must reference its own provenance")
        if self.component and not self.component.strip():
            raise ValueError("an invariant verification component cannot be blank")


class UnregisteredExtractorError(KeyError):
    """Raised when an ``InvariantSpec`` names an unregistered extractor id."""


class UnauthorizedExtractorError(ValueError):
    """Raised when a spec's extractor id is registered but not authorized.

    A registered ``extractor_id`` is merely resolvable; it is not
    automatically authoritative for every ``(component, invariant_id,
    domain)`` a spec might name it for. This is raised when no
    ``RegisteredInvariantDefinition`` authorizes the spec's exact
    ``extractor_id`` for its ``(domain, component, invariant_id)`` scope --
    for example, an extractor authorized only for a different component, or
    a caller naming a different, unauthorized extractor id for an otherwise
    authorized component/invariant. This is treated as epistemically
    untestable (no authorized verifier is bound), not as a disproved
    invariant: ``Candidate/Caller does not own verifier selection
    authority``.
    """


class InvariantExtractionError(Exception):
    """Raised when a registered extractor fails while extracting a value.

    Wraps the underlying exception so callers see which extractor and which
    side of the transition (``before_state`` or ``after_state``) failed,
    rather than an opaque exception surfacing from inside the gate.
    """


class InvariantComparisonError(TypeError):
    """Raised when ``before_value == after_value`` does not yield an actual bool.

    ``==`` is not guaranteed to return ``bool`` for every Python object (for
    example, element-wise comparisons on array-like objects). Silently
    treating a non-``bool`` result as truthy/falsy would let ambiguous
    comparator semantics masquerade as a verified preservation decision, so
    it is rejected instead of coerced.
    """


class InvariantProvenanceMismatchError(ValueError):
    """Raised when an ``InvariantVerification`` is checked against the wrong transition.

    Signals that the verification's recorded ``InvariantVerificationProvenance``
    does not match the transition it is being checked against -- for example,
    a verification produced for one transition being replayed as if it were
    evidence for a different one.
    """


class InvariantAssessmentSpecificationError(ValueError):
    """Raised when specs cannot form a complete, unambiguous assessment request.

    Missing, extra, or duplicate components describe an invalid request, not an
    observed invariant failure. The error is deliberately separate from
    ``InvariantVerificationError``, which always carries an epistemic decision.
    """


# Errors that mean "this invariant could not be observed/checked", not
# "this invariant was checked and disproved". ``InvariantVerificationGate.
# assess_all_preserved`` maps exactly these to ``DEFER``; every other
# exception is a programming/internal error and is left to propagate rather
# than being coerced into a BLOCK or DEFER epistemic judgment.
_UNTESTABLE_EVIDENCE_ERRORS = (
    UnregisteredExtractorError,
    UnauthorizedExtractorError,
    InvariantExtractionError,
    InvariantComparisonError,
)


class InvariantVerificationDecisionStatus(Enum):
    VERIFIED = auto()
    BLOCK = auto()
    DEFER = auto()


@dataclass(frozen=True, slots=True)
class InvariantVerificationDecision:
    """Auditable result of checking the complete preserved-invariant set.

    Gate-issued only, mirroring ``InvariantVerification`` and
    ``StructurallyAdmissibleTransition``: passing anything other than
    ``InvariantVerificationGate``'s private decision token raises. Without
    this, an ordinary caller could hand-build
    ``InvariantVerificationDecision(status=VERIFIED, ...)`` without ever
    running ``InvariantVerificationGate.verify``, letting a later layer that
    trusts ``decision.status == VERIFIED`` be fooled by a self-declared
    result -- the same failure mode this module closes for individual
    ``InvariantVerification``s. A ``VERIFIED`` decision additionally can only
    be constructed with complete, duplicate-free, transition-bound coverage
    (the same requirements ``InvariantVerificationBundle`` enforces), so
    ``BundleAuthority`` and ``DecisionIntegrity`` no longer diverge.

    ``status`` distinguishes three genuinely different epistemic situations:
    ``BLOCK`` means at least one declared component was checked and
    found *not* preserved (``I(before) != I(after)``) -- a disproved claim.
    ``DEFER`` means no component was disproved, but at least one could not
    be checked at all (an unregistered or unauthorized extractor, a failing
    extractor, or an ambiguous, non-``bool`` comparison) -- an
    epistemically untestable claim, not a disproved one. ``BLOCK`` always
    takes precedence over ``DEFER`` for the overall conjunctive claim
    (``I_1 and I_2 and ... and I_n``): a disproved component is never
    erased by an untestable one elsewhere (``False and Unknown == False``),
    so ``failed_components`` (disproved) and ``deferred_components``
    (untestable) are recorded as separate fields, and the aggregate status
    never depends on the order ``specs`` were given in. Internal/programming
    errors (anything not raised as one of the recognized untestable-evidence
    errors) are not caught into either status; they propagate as ordinary
    exceptions, since a bug in the checking code itself is neither a
    verified fact about the invariant nor an epistemic non-answer about it.
    Likewise, malformed assessment specifications are rejected before
    assessment with ``InvariantAssessmentSpecificationError`` rather than
    being represented by any status.
    """

    status: InvariantVerificationDecisionStatus
    transition: "StructurallyAdmissibleTransition"
    verifications: tuple[InvariantVerification, ...] = ()
    failed_components: tuple[str, ...] = ()
    deferred_components: tuple[str, ...] = ()
    trace: Trace | None = None
    residuals: tuple[object, ...] = ()
    reason: str = ""
    _decision_token: InitVar[object | None] = None

    def __post_init__(self, _decision_token: object | None) -> None:
        if _decision_token is not _DECISION_TOKEN:
            raise ValueError(
                "invariant verification decisions must be issued by "
                "InvariantVerificationGate"
            )
        if not self.reason.strip():
            raise ValueError("invariant verification decisions require a reason")
        if self.status is InvariantVerificationDecisionStatus.VERIFIED:
            if self.failed_components:
                raise ValueError("verified decisions cannot have failed components")
            if self.deferred_components:
                raise ValueError("verified decisions cannot have deferred components")
            components = tuple(v.component for v in self.verifications)
            if len(set(components)) != len(components):
                raise ValueError(
                    "verified decisions cannot contain duplicate components"
                )
            if set(components) != set(self.transition.preserved):
                raise ValueError(
                    "verified decisions require complete invariant coverage"
                )
            for verification in self.verifications:
                InvariantVerificationGate.require_bound_to(
                    verification, self.transition
                )
                if not verification.preserved:
                    raise ValueError(
                        "verified decisions require every invariant to be preserved"
                    )
            snapshot_ids = {
                verification.provenance.registry_snapshot_id
                for verification in self.verifications
            }
            if len(snapshot_ids) != 1 or None in snapshot_ids:
                raise ValueError("verified decisions require one registry snapshot")


class InvariantVerificationError(ValueError):
    """Typed error carrying a complete invariant verification decision."""

    def __init__(self, decision: InvariantVerificationDecision) -> None:
        self.decision = decision
        super().__init__(decision.reason)


@dataclass(frozen=True, slots=True)
class InvariantVerificationBundle:
    """The complete, one-to-one verification coverage for an admitted transition.

    Gate-issued only, matching the constitutional wording that both
    ``InvariantVerificationDecision`` and ``InvariantVerificationBundle``
    are gate-issued: passing anything other than
    ``InvariantVerificationGate``'s private bundle token raises. A bare
    ``InvariantVerificationBundle(transition, verifications)`` call is no
    longer legitimate outside ``InvariantVerificationGate.require_all_preserved``,
    even though its content-validation (complete coverage, no duplicates,
    transition-bound, single snapshot) is unchanged.
    """

    transition: "StructurallyAdmissibleTransition"
    verifications: tuple[InvariantVerification, ...]
    _bundle_token: InitVar[object | None] = None

    def __post_init__(self, _bundle_token: object | None) -> None:
        if _bundle_token is not _BUNDLE_TOKEN:
            raise ValueError(
                "invariant verification bundles must be issued by "
                "InvariantVerificationGate.require_all_preserved"
            )
        components = tuple(v.component for v in self.verifications)
        if len(set(components)) != len(components):
            raise ValueError("invariant verification bundle cannot contain duplicates")
        if set(components) != set(self.transition.preserved):
            raise ValueError(
                "invariant verification bundle must exactly cover preserved components"
            )
        for verification in self.verifications:
            InvariantVerificationGate.require_bound_to(verification, self.transition)
            if not verification.preserved:
                raise ValueError(
                    "invariant verification bundle requires every invariant "
                    "to be preserved"
                )
        snapshot_ids = {
            verification.provenance.registry_snapshot_id
            for verification in self.verifications
        }
        if len(snapshot_ids) != 1 or None in snapshot_ids:
            raise ValueError(
                "invariant verification bundle requires one registry snapshot"
            )


class SealedInvariantExtractorRegistry:
    """Read-only, resolution-only view over a sealed set of registered extractors.

    Produced only by ``InvariantExtractorRegistry.seal()``, this is the sole
    registry type ``InvariantVerificationGate.verify`` accepts. It exposes no
    ``register``/``authorize`` methods: registration and authorization
    authority (the mutable ``InvariantExtractorRegistry``, owned by trusted
    setup/governor code) are a distinct type from resolution authority (this
    sealed, read-only view, injected into the gate). A caller who still
    holds the mutable registry cannot register or authorize a fresh
    extractor and have it recognized by a previously-issued sealed view,
    and the gate itself never has the ability to register or authorize
    anything -- it only resolves through ``resolve_authorized``.
    """

    __slots__ = (
        "_extractors",
        "_definitions",
        "_registry_snapshot_id",
        "_registry_projection_hash",
    )

    def __init__(
        self,
        extractors: Mapping[str, InvariantExtractor],
        definitions: Mapping[tuple[str, str, str], RegisteredInvariantDefinition],
        _seal_token: object,
    ) -> None:
        # As with ``InvariantVerification``'s ``_verification_token``, the
        # leading underscore marks this as "seal-only", not "conventionally
        # private but freely usable by keyword". Only
        # ``InvariantExtractorRegistry.seal()`` holds ``_SEAL_TOKEN``, so
        # passing this keyword directly is only ever legitimate from that
        # method.
        if _seal_token is not _SEAL_TOKEN:
            raise ValueError(
                "sealed invariant extractor registries must be issued by "
                "InvariantExtractorRegistry.seal()"
            )
        # ``extractors``/``definitions`` are copied into fresh, private
        # containers here. This constructor call happens synchronously
        # inside ``InvariantExtractorRegistry.seal()``'s ``with self._lock:``
        # block (Python evaluates and fully executes the constructed
        # expression, including this copy, before the ``with`` statement's
        # lock release runs as part of returning), so the copy is made
        # while the registration lock is still held -- no concurrent
        # ``register()``/``authorize()`` call can interleave with it.
        self._extractors: dict[str, InvariantExtractor] = dict(extractors)
        self._definitions: dict[tuple[str, str, str], RegisteredInvariantDefinition] = (
            dict(definitions)
        )
        self._registry_snapshot_id = uuid4().hex
        self._registry_projection_hash = hashlib.sha256(
            "|".join(sorted(self._extractors)).encode("utf-8")
        ).hexdigest()

    @property
    def registry_snapshot_id(self) -> str:
        """Opaque identity of this sealed registry snapshot."""

        return self._registry_snapshot_id

    @property
    def registry_projection_hash(self) -> str:
        """Deterministic digest of a *partial projection* of this snapshot.

        ``registry_snapshot_id`` is an opaque ``uuid4().hex`` minted fresh by
        every ``seal()`` call, so it cannot by itself confirm that two
        snapshots (perhaps sealed on different days) actually registered the
        same extractor ids: ``OccurrenceIdentity != ContentIdentity`` applies
        to registries too. This hash is deliberately **not** claimed as
        canonical content identity for the registry:

        * It only covers registered extractor *ids* (sorted, joined), not
          the authorized ``(domain, component, invariant_id) ->
          RegisteredInvariantDefinition`` bindings, and not the extractor
          callables' own behavior. Two registries could register the same
          ids with differently-behaving callables, or with entirely
          different authorizations, and still hash identically.
        * It is corroborating evidence of reproducible *id* registration
          only, not a proof that the underlying callables or
          authorizations are identical. A canonical
          ``RegistryManifestHash`` covering typed extractor registrations
          (implementation identity/version/digest, authorized scope) is
          deferred to a dedicated reproducibility PR.
        """

        return self._registry_projection_hash

    def resolve(self, extractor_id: str) -> InvariantExtractor:
        """Resolve a registered extractor, or raise if none is registered.

        This performs *resolution* only -- it does not check whether
        ``extractor_id`` is *authorized* for any particular component or
        invariant. ``InvariantVerificationGate.verify`` uses
        ``resolve_authorized`` instead, precisely so a spec cannot pick an
        arbitrary registered id and have it accepted merely because it
        resolves.
        """

        try:
            return self._extractors[extractor_id]
        except KeyError as error:
            raise UnregisteredExtractorError(
                f"no extractor registered for id: {extractor_id!r}"
            ) from error

    def resolve_authorized(
        self, *, domain: str, component: str, invariant_id: str, extractor_id: str
    ) -> InvariantExtractor:
        """Resolve an extractor only if authorized for this exact scope.

        First raises ``UnregisteredExtractorError`` (via ``resolve``) if
        ``extractor_id`` is not registered at all -- an unresolvable id is
        never a scope-authorization question. Then raises
        ``UnauthorizedExtractorError`` unless a
        ``RegisteredInvariantDefinition`` exists for
        ``(domain, component, invariant_id)`` *and* that definition's own
        ``extractor_id`` matches the one requested here. This is the
        authority check a caller cannot bypass by simply registering (or
        knowing the id of) some other extractor: a spec naming a
        registered-but-unauthorized-for-this-scope id fails just as surely
        as one naming a wholly unregistered id, just with a distinct,
        typed reason.
        """

        extractor = self.resolve(extractor_id)
        definition = self._definitions.get((domain, component, invariant_id))
        if definition is None or definition.extractor_id != extractor_id:
            raise UnauthorizedExtractorError(
                f"extractor {extractor_id!r} is not authorized for "
                f"domain={domain!r}, component={component!r}, "
                f"invariant_id={invariant_id!r}"
            )
        return extractor


class InvariantExtractorRegistry:
    """Mutable registration authority for invariant extractors.

    Extractors are registered here, never carried by a ``TransitionCandidate``
    or an ``InvariantSpec``. A spec only names an ``extractor_id``; resolving
    that id to an actual callable requires going through
    ``InvariantVerificationGate``, which itself only accepts a
    ``SealedInvariantExtractorRegistry`` produced by ``seal()`` -- never this
    mutable registry directly. This registry is meant to be owned and
    populated once by trusted setup/governor code, not by an arbitrary
    candidate or linguistic layer immediately before verification.

    Registering an extractor id only makes it *resolvable*; it does not, by
    itself, authorize that extractor for any particular invariant or
    component. Authorization is a distinct step: ``authorize`` binds a
    ``RegisteredInvariantDefinition`` (domain, component, invariant_id ->
    exactly one extractor_id) that must reference an already-registered
    extractor id. ``InvariantVerificationGate.verify`` only resolves through
    that authorized binding (``resolve_authorized``), so a candidate/caller
    naming a registered-but-unauthorized extractor id for a given
    component is rejected the same way as naming an unregistered one.

    ``register``, ``authorize``, and ``seal`` are synchronized with an
    internal lock, so concurrent calls on the same instance do not corrupt
    its internal state. This only protects the registry's own bookkeeping;
    it does not make the overall registration *sequence* deterministic
    across threads, so registration is still expected at module
    import/setup time, not under concurrent, racing access.
    """

    def __init__(self) -> None:
        self._extractors: dict[str, InvariantExtractor] = {}
        self._definitions: dict[
            tuple[str, str, str], RegisteredInvariantDefinition
        ] = {}
        self._lock = threading.Lock()

    def register(self, extractor_id: str, extractor: InvariantExtractor) -> None:
        """Register an extractor under ``extractor_id``.

        Raises if ``extractor_id`` is blank or already registered: an
        extractor id is a stable, single-owner registration, not a mutable
        slot a later caller can silently overwrite. Registering an id does
        not authorize it for anything; use ``authorize`` separately to bind
        it to a specific ``(domain, component, invariant_id)`` scope.
        """

        if not extractor_id.strip():
            raise ValueError("an extractor id cannot be blank")
        with self._lock:
            if extractor_id in self._extractors:
                raise ValueError(f"extractor id already registered: {extractor_id!r}")
            self._extractors[extractor_id] = extractor

    def authorize(self, definition: RegisteredInvariantDefinition) -> None:
        """Authorize ``definition``'s extractor for its declared scope.

        Raises if ``definition.extractor_id`` is not already registered (an
        authorization cannot reference a nonexistent implementation), or if
        its ``(domain, component, invariant_id)`` scope is already
        authorized (a scope is a stable, single-owner authorization, not a
        mutable slot a later caller can silently overwrite).
        """

        with self._lock:
            if definition.extractor_id not in self._extractors:
                raise ValueError(
                    "cannot authorize an unregistered extractor id: "
                    f"{definition.extractor_id!r}"
                )
            key = (definition.domain, definition.component, definition.invariant_id)
            if key in self._definitions:
                raise ValueError(
                    "invariant definition already authorized for "
                    f"domain={definition.domain!r}, "
                    f"component={definition.component!r}, "
                    f"invariant_id={definition.invariant_id!r}"
                )
            self._definitions[key] = definition

    def seal(self) -> SealedInvariantExtractorRegistry:
        """Freeze current registrations into a read-only, resolution-only view.

        Sealing is the boundary between registration/authorization authority
        (this mutable registry) and resolution authority (the sealed view
        actually injected into ``InvariantVerificationGate``). Registering
        or authorizing more on this instance after sealing does not
        retroactively affect already-issued sealed views: each ``seal()``
        call snapshots the registrations and authorizations made so far.
        The snapshot copy itself happens inside
        ``SealedInvariantExtractorRegistry.__init__``, which this method
        calls while still holding ``self._lock`` (the lock is only released
        once the constructor -- and its internal copy -- has already
        returned), so a concurrent ``register()``/``authorize()`` cannot
        interleave with the copy.
        """

        with self._lock:
            return SealedInvariantExtractorRegistry(
                self._extractors, self._definitions, _SEAL_TOKEN
            )


class InvariantVerificationGate:
    """Independently verifies a claimed invariant against an admitted transition.

    This gate -- not the candidate -- owns extraction and comparison. It
    requires a ``StructurallyAdmissibleTransition`` (so verification only ever
    runs on something that already passed structural admission) and a
    ``SealedInvariantExtractorRegistry`` (so the extractor is never supplied
    by the candidate itself, and the gate never has registration authority --
    it cannot create or seal a registry on its own). Extractors must return
    values comparable with ``==``; the comparison result is required to be an
    actual ``bool`` (see ``InvariantComparisonError``), so ambiguous or
    non-boolean comparator semantics cannot masquerade as a verification.

    This only verifies invariants named in ``transition.preserved``: a
    candidate's ``changed`` components are, by definition, not claimed as
    preserved, so there is intentionally no path here to "verify" one of
    them stayed the same.

    Every issued ``InvariantVerification`` carries an
    ``InvariantVerificationProvenance`` binding it to the transition it was
    checked against; use ``require_bound_to`` to check that binding before
    treating a verification as evidence for a specific transition.
    """

    @staticmethod
    def verify(
        transition: "StructurallyAdmissibleTransition",
        spec: InvariantSpec,
        registry: SealedInvariantExtractorRegistry,
    ) -> InvariantVerification:
        """Verify ``spec`` against ``transition`` using an authorized extractor."""

        if not isinstance(registry, SealedInvariantExtractorRegistry):
            raise TypeError(
                "invariant verification requires a SealedInvariantExtractorRegistry; "
                "call InvariantExtractorRegistry.seal() first"
            )
        if spec.component not in transition.preserved:
            raise ValueError(
                "invariant spec component must be among the transition's "
                "declared preserved components"
            )
        # ``spec.extractor_id`` is only a claim, not a grant of authority: it
        # is resolved through ``resolve_authorized``, which raises
        # ``UnauthorizedExtractorError`` unless a trusted
        # ``RegisteredInvariantDefinition`` binds exactly this extractor id
        # to this ``(domain, component, invariant_id)`` scope. The candidate
        # does not own verifier-selection authority.
        extractor = registry.resolve_authorized(
            domain=transition.anchor.domain,
            component=spec.component,
            invariant_id=spec.invariant_id,
            extractor_id=spec.extractor_id,
        )
        before_value = _extract(
            extractor, transition.before_state, "before_state", spec
        )
        after_value = _extract(extractor, transition.after_state, "after_state", spec)
        preserved = _compare(before_value, after_value, spec)
        observation = InvariantObservation(
            invariant_id=spec.invariant_id,
            before_value=before_value,
            after_value=after_value,
        )
        provenance = InvariantVerificationProvenance(
            source_claim_id=transition.claim.claim_id,
            source_anchor=transition.anchor,
            source_target_anchor=transition.resolved_target_anchor,
            source_trace=transition.trace,
            invariant_id=spec.invariant_id,
            extractor_id=spec.extractor_id,
            source_admission_id=transition.admission_id,
            registry_snapshot_id=registry.registry_snapshot_id,
            source_transition_projection_fingerprint=(
                transition.transition_projection_fingerprint
            ),
            registry_projection_hash=registry.registry_projection_hash,
        )
        trace = Trace(
            transition.trace.events
            + (f"invariant {spec.invariant_id} verified: preserved={preserved}",)
        )
        return InvariantVerification(
            invariant_id=spec.invariant_id,
            preserved=preserved,
            trace=trace,
            observation=observation,
            provenance=provenance,
            component=spec.component,
            _verification_token=_VERIFICATION_TOKEN,
        )

    @staticmethod
    def assess_all_preserved(
        transition: "StructurallyAdmissibleTransition",
        specs: tuple[InvariantSpec, ...],
        registry: SealedInvariantExtractorRegistry,
    ) -> InvariantVerificationDecision:
        """Assess complete invariant coverage without discarding failed history.

        The specification must first contain exactly one spec for each declared
        preserved component. Missing, extra, or duplicate components raise
        ``InvariantAssessmentSpecificationError``: a malformed request is
        neither a falsified nor an untestable invariant claim.

        Once the request is well-formed, every spec is evaluated independently
        -- evaluation never stops at
        the first untestable spec -- so a component checked later in
        ``specs`` and found disproved is never hidden behind an earlier
        component's ``DEFER``. Each spec resolves to exactly one of three
        outcomes: verified-preserved, verified-not-preserved (disproved), or
        untestable (an unregistered/unauthorized extractor
        (``UnregisteredExtractorError``, ``UnauthorizedExtractorError``), a
        failing extractor (``InvariantExtractionError``), or an ambiguous,
        non-``bool`` comparison (``InvariantComparisonError``)). These are
        tracked as two separate, order-independent (sorted) component sets:
        ``failed_components`` (disproved) and ``deferred_components``
        (untestable). The overall status is then the conjunctive claim's
        precedence -- ``BLOCK`` if any component is disproved, else
        ``DEFER`` if any component is untestable, else ``VERIFIED`` -- so a
        known falsification is never erased by an unrelated deferral
        (``False and Unknown == False``), and the aggregate judgment does
        not depend on the order ``specs`` were given in. Any other
        exception (an internal/programming error, not one of the
        recognized untestable-evidence errors) is not caught here; it
        propagates to the caller unchanged, since a bug in the checking
        code itself is neither a verified nor a deferred judgment about the
        invariant.

        ``specs`` that do not exactly cover ``transition.preserved``, or
        that name the same component more than once, are a malformed
        request, not an epistemic judgment: no component in such a request
        was ever actually checked against an extractor, so this raises
        ``InvariantAssessmentSpecificationError`` instead of returning a
        ``BLOCK`` decision. Equating a malformed request with a disproved
        invariant would let ``MalformedVerificationRequest`` masquerade as
        ``DisprovedInvariant``.
        """

        components = tuple(spec.component for spec in specs)
        if len(set(components)) != len(components):
            raise InvariantAssessmentSpecificationError(
                "invariant specs cannot duplicate preserved components"
            )
        if set(components) != set(transition.preserved):
            raise InvariantAssessmentSpecificationError(
                "invariant specs must exactly cover preserved components"
        if {spec.component for spec in specs} != set(transition.preserved):
            raise InvariantAssessmentSpecificationError(
                "invariant specs must exactly cover preserved components"
            )
        if len({spec.component for spec in specs}) != len(specs):
            raise InvariantAssessmentSpecificationError(
                "invariant specs cannot duplicate preserved components"
            )
        verifications: list[InvariantVerification] = []
        blocked: list[str] = []
        deferred: list[str] = []
        events: list[str] = []
        for spec in specs:
            try:
                verification = InvariantVerificationGate.verify(
                    transition, spec, registry
                )
            except _UNTESTABLE_EVIDENCE_ERRORS as error:
                deferred.append(spec.component)
                events.append(
                    f"invariant {spec.invariant_id} deferred "
                    f"(component={spec.component}): {error}"
                )
                continue
            verifications.append(verification)
            events.append(verification.trace.events[-1])
            if not verification.preserved:
                blocked.append(spec.component)
        if blocked:
            status = InvariantVerificationDecisionStatus.BLOCK
            reason = "one or more preserved invariants were not verified"
        elif deferred:
            status = InvariantVerificationDecisionStatus.DEFER
            reason = "one or more preserved invariants could not be checked"
        else:
            status = InvariantVerificationDecisionStatus.VERIFIED
            reason = "all declared preserved invariants were verified"
        return InvariantVerificationDecision(
            status=status,
            transition=transition,
            verifications=tuple(verifications),
            failed_components=tuple(sorted(blocked)),
            deferred_components=tuple(sorted(deferred)),
            trace=Trace(transition.trace.events + tuple(events)),
            residuals=transition.residuals,
            reason=reason,
            _decision_token=_DECISION_TOKEN,
        )

    @staticmethod
    def require_all_preserved(
        transition: "StructurallyAdmissibleTransition",
        specs: tuple[InvariantSpec, ...],
        registry: SealedInvariantExtractorRegistry,
    ) -> InvariantVerificationBundle:
        """Return a complete bundle or raise while preserving its decision."""

        decision = InvariantVerificationGate.assess_all_preserved(
            transition, specs, registry
        )
        if decision.status is not InvariantVerificationDecisionStatus.VERIFIED:
            raise InvariantVerificationError(decision)
        return InvariantVerificationBundle(
            transition, decision.verifications, _bundle_token=_BUNDLE_TOKEN
        )

    @staticmethod
    def require_bound_to(
        verification: InvariantVerification,
        transition: "StructurallyAdmissibleTransition",
        registry: SealedInvariantExtractorRegistry | None = None,
    ) -> InvariantVerification:
        """Return ``verification`` only if it is bound to ``transition``.

        Raises ``InvariantProvenanceMismatchError`` if any identifying field
        of ``transition`` (claim id, source anchor, resolved target anchor,
        or trace) does not match the verification's recorded provenance --
        for example, when a verification produced for one transition is
        replayed against an unrelated one.
        """

        provenance = verification.provenance
        if (
            provenance.source_claim_id != transition.claim.claim_id
            or provenance.source_anchor != transition.anchor
            or provenance.source_target_anchor != transition.resolved_target_anchor
            or provenance.source_trace != transition.trace
            or provenance.source_admission_id != transition.admission_id
            or provenance.source_transition_projection_fingerprint
            != transition.transition_projection_fingerprint
            or (
                registry is not None
                and (
                    provenance.registry_snapshot_id != registry.registry_snapshot_id
                    or provenance.registry_projection_hash
                    != registry.registry_projection_hash
                )
            )
        ):
            raise InvariantProvenanceMismatchError(
                "invariant verification is not bound to the given transition"
            )
        return verification


def _extract(
    extractor: InvariantExtractor, state: State, label: str, spec: InvariantSpec
) -> object:
    """Run ``extractor`` on ``state``, wrapping any failure with context."""

    try:
        return extractor(state)
    except Exception as error:
        raise InvariantExtractionError(
            f"extractor {spec.extractor_id!r} failed on {label} "
            f"for invariant {spec.invariant_id!r}: {error}"
        ) from error


def _compare(before_value: object, after_value: object, spec: InvariantSpec) -> bool:
    """Compare extracted values, requiring an actual ``bool`` result."""

    try:
        comparison = before_value == after_value
    except Exception as error:
        raise InvariantComparisonError(
            f"comparing before/after values failed for invariant "
            f"{spec.invariant_id!r}: {error}"
        ) from error
    if type(comparison) is not bool:
        # `type(...) is not bool` (not `isinstance`) deliberately excludes
        # bool subclasses too, so ambiguous or non-boolean comparator
        # semantics (for example, some libraries' element-wise `__eq__`)
        # cannot masquerade as a genuine preservation decision.
        raise InvariantComparisonError(
            f"comparator for invariant {spec.invariant_id!r} did not return a "
            f"bool (got {type(comparison).__name__})"
        )
    return comparison
