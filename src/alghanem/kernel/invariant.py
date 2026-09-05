"""Verified invariant preservation: specs, extractors, and verification.

A ``TransitionCandidate`` may declare a component name in ``preserved``, but
that is only a claim: ``DeclaredInvariant != VerifiedInvariant``. This module
closes that gap for a single named invariant at a time, without letting the
candidate supply its own proof.

``InvariantSpec`` names *what* should be checked (an invariant id, the
preserved component it refers to, and a registered extractor id) but never
carries an executable extractor itself. Extractors are registered
independently in an ``InvariantExtractorRegistry``; resolving an
``extractor_id`` to an actual callable is that registry's authority alone.
This keeps ``Candidate does not own certification authority``: nothing here
lets a candidate hand in ``lambda before, after: True`` and "verify" itself.

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
3. ``NoInvariantVerificationWithoutSourceTransitionBinding``: every
   ``InvariantVerification`` carries an ``InvariantVerificationProvenance``
   binding it to the specific transition it was checked against (claim id,
   source anchor, resolved target anchor, and source trace), so a
   verification produced for one transition cannot be silently accepted as
   evidence for another via ``InvariantVerificationGate.require_bound_to``.
4. Exact transition and snapshot identity: structural admission issues an
   opaque ``admission_id`` and sealing issues a ``registry_snapshot_id``;
   verification provenance records both, so matching claim fields alone cannot
   authorize replay.
5. Complete coverage: ``InvariantVerificationBundle`` accepts exactly one
   successful verification for every declared preserved component, while
   ``InvariantVerificationDecision`` preserves blocked attempts for audit.
6. Boolean comparison integrity: ``before_value == after_value`` is not
   assumed to return an actual ``bool`` (for example, some libraries'
   ``__eq__`` return non-bool values). A non-``bool`` comparison result is
   rejected with a typed ``InvariantComparisonError`` rather than silently
   coerced into a verification.

``InvariantVerificationGate.verify`` is the only way to produce an
``InvariantVerification``. It extracts a value from ``before_state`` and
``after_state`` via the registered extractor and reports whether they are
equal; a candidate cannot construct this outcome by declaring
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


@dataclass(frozen=True, slots=True)
class InvariantSpec:
    """A claimed invariant to verify: a name, a component, and an extractor id.

    This is ``ClaimedInvariant``, not ``VerifiedInvariant``: declaring a spec
    is not proof that ``component`` was preserved. ``extractor_id`` is a
    lookup key into an ``InvariantExtractorRegistry``, never an executable
    callable, so a spec cannot embed its own ad hoc "proof".
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
    """

    source_claim_id: str
    source_anchor: Anchor
    source_target_anchor: Anchor
    source_trace: Trace
    invariant_id: str
    extractor_id: str
    source_admission_id: str | None = None
    registry_snapshot_id: str | None = None

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


class InvariantVerificationDecisionStatus(Enum):
    VERIFIED = auto()
    BLOCK = auto()
    DEFER = auto()


@dataclass(frozen=True, slots=True)
class InvariantVerificationDecision:
    """Auditable result of checking the complete preserved-invariant set."""

    status: InvariantVerificationDecisionStatus
    transition: "StructurallyAdmissibleTransition"
    verifications: tuple[InvariantVerification, ...] = ()
    failed_components: tuple[str, ...] = ()
    trace: Trace | None = None
    residuals: tuple[object, ...] = ()
    reason: str = ""

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise ValueError("invariant verification decisions require a reason")
        if self.status is InvariantVerificationDecisionStatus.VERIFIED:
            if self.failed_components:
                raise ValueError("verified decisions cannot have failed components")
            if set(v.component for v in self.verifications) != set(
                self.transition.preserved
            ):
                raise ValueError(
                    "verified decisions require complete invariant coverage"
                )


class InvariantVerificationError(ValueError):
    """Typed error carrying a complete invariant verification decision."""

    def __init__(self, decision: InvariantVerificationDecision) -> None:
        self.decision = decision
        super().__init__(decision.reason)


@dataclass(frozen=True, slots=True)
class InvariantVerificationBundle:
    """The complete, one-to-one verification coverage for an admitted transition."""

    transition: "StructurallyAdmissibleTransition"
    verifications: tuple[InvariantVerification, ...]

    def __post_init__(self) -> None:
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
    ``register`` method: registration authority (the mutable
    ``InvariantExtractorRegistry``, owned by trusted setup/governor code) and
    resolution authority (this sealed, read-only view, injected into the
    gate) are different types. A caller who still holds the mutable registry
    cannot register a fresh extractor and have it recognized by a
    previously-issued sealed view, and the gate itself never has the ability
    to register anything -- it only resolves.
    """

    __slots__ = ("_extractors", "_registry_snapshot_id")

    def __init__(
        self, extractors: Mapping[str, InvariantExtractor], _seal_token: object
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
        # ``extractors`` is copied into a fresh, private dict here. This
        # constructor call happens synchronously inside
        # ``InvariantExtractorRegistry.seal()``'s ``with self._lock:`` block
        # (Python evaluates and fully executes the constructed expression,
        # including this copy, before the ``with`` statement's lock release
        # runs as part of returning), so the copy is made while the
        # registration lock is still held -- no concurrent ``register()``
        # call can interleave with it.
        self._extractors: dict[str, InvariantExtractor] = dict(extractors)
        self._registry_snapshot_id = uuid4().hex

    @property
    def registry_snapshot_id(self) -> str:
        """Opaque identity of this sealed registry snapshot."""

        return self._registry_snapshot_id

    def resolve(self, extractor_id: str) -> InvariantExtractor:
        """Resolve a registered extractor, or raise if none is registered."""

        try:
            return self._extractors[extractor_id]
        except KeyError as error:
            raise UnregisteredExtractorError(
                f"no extractor registered for id: {extractor_id!r}"
            ) from error


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

    ``register`` and ``seal`` are synchronized with an internal lock, so
    concurrent registration calls on the same instance do not corrupt its
    internal state. This only protects the registry's own bookkeeping; it
    does not make the overall registration *sequence* deterministic across
    threads, so registration is still expected at module import/setup time,
    not under concurrent, racing access.
    """

    def __init__(self) -> None:
        self._extractors: dict[str, InvariantExtractor] = {}
        self._lock = threading.Lock()

    def register(self, extractor_id: str, extractor: InvariantExtractor) -> None:
        """Register an extractor under ``extractor_id``.

        Raises if ``extractor_id`` is blank or already registered: an
        extractor id is a stable, single-owner registration, not a mutable
        slot a later caller can silently overwrite.
        """

        if not extractor_id.strip():
            raise ValueError("an extractor id cannot be blank")
        with self._lock:
            if extractor_id in self._extractors:
                raise ValueError(f"extractor id already registered: {extractor_id!r}")
            self._extractors[extractor_id] = extractor

    def seal(self) -> SealedInvariantExtractorRegistry:
        """Freeze current registrations into a read-only, resolution-only view.

        Sealing is the boundary between registration authority (this mutable
        registry) and resolution authority (the sealed view actually
        injected into ``InvariantVerificationGate``). Registering more
        extractors on this instance after sealing does not retroactively
        affect already-issued sealed views: each ``seal()`` call snapshots
        the registrations made so far. The snapshot copy itself happens
        inside ``SealedInvariantExtractorRegistry.__init__``, which this
        method calls while still holding ``self._lock`` (the lock is only
        released once the constructor -- and its internal copy -- has
        already returned), so a concurrent ``register()`` cannot interleave
        with the copy.
        """

        with self._lock:
            return SealedInvariantExtractorRegistry(self._extractors, _SEAL_TOKEN)


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
        """Verify ``spec`` against ``transition`` using a registered extractor."""

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
        extractor = registry.resolve(spec.extractor_id)
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
        """Assess complete invariant coverage without discarding failed history."""

        if {spec.component for spec in specs} != set(transition.preserved):
            return InvariantVerificationDecision(
                status=InvariantVerificationDecisionStatus.BLOCK,
                transition=transition,
                failed_components=tuple(transition.preserved),
                trace=transition.trace,
                residuals=transition.residuals,
                reason="invariant specs must exactly cover preserved components",
            )
        verifications: list[InvariantVerification] = []
        if len({spec.component for spec in specs}) != len(specs):
            return InvariantVerificationDecision(
                status=InvariantVerificationDecisionStatus.BLOCK,
                transition=transition,
                failed_components=tuple(transition.preserved),
                trace=transition.trace,
                residuals=transition.residuals,
                reason="invariant specs cannot duplicate preserved components",
            )
        current_component = ""
        try:
            for spec in specs:
                current_component = spec.component
                verifications.append(
                    InvariantVerificationGate.verify(transition, spec, registry)
                )
        except Exception as error:
            failed = tuple(
                component
                for component in transition.preserved
                if component
                not in {verification.component for verification in verifications}
            )
            if current_component and current_component not in failed:
                failed += (current_component,)
            return InvariantVerificationDecision(
                status=InvariantVerificationDecisionStatus.BLOCK,
                transition=transition,
                verifications=tuple(verifications),
                failed_components=failed,
                trace=Trace(
                    transition.trace.events
                    + (f"invariant verification blocked: {error}",)
                ),
                residuals=transition.residuals,
                reason=str(error),
            )
        if any(not verification.preserved for verification in verifications):
            failed = tuple(
                verification.component
                for verification in verifications
                if not verification.preserved
            )
            return InvariantVerificationDecision(
                status=InvariantVerificationDecisionStatus.BLOCK,
                transition=transition,
                verifications=tuple(verifications),
                failed_components=failed,
                trace=verifications[-1].trace if verifications else transition.trace,
                residuals=transition.residuals,
                reason="one or more preserved invariants were not verified",
            )
        return InvariantVerificationDecision(
            status=InvariantVerificationDecisionStatus.VERIFIED,
            transition=transition,
            verifications=tuple(verifications),
            trace=verifications[-1].trace,
            residuals=transition.residuals,
            reason="all declared preserved invariants were verified",
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
        return InvariantVerificationBundle(transition, decision.verifications)

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
            or (
                registry is not None
                and provenance.registry_snapshot_id != registry.registry_snapshot_id
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
