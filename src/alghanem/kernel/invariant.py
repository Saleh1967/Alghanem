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

``InvariantVerificationGate.verify`` is the only way to produce an
``InvariantVerification``. It extracts a value from ``before_state`` and
``after_state`` via the registered extractor and reports whether they are
equal; a candidate cannot construct this outcome by declaring
``preserved=True``.

Scope: this gate checks one declared invariant against one already
structurally admitted transition. It does not, by itself, make invariant
verification mandatory for structural admission, and it is not evidential
sufficiency, authority licensing, or certification -- those remain later,
undelivered rungs of the epistemic ladder in ``docs/CONSTITUTION.md``.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .anchor import State
from .trace import Trace

if TYPE_CHECKING:
    from .transition import StructurallyAdmissibleTransition

InvariantExtractor = Callable[[State], object]


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
class InvariantVerification:
    """The independently produced result of checking I(before) == I(after).

    Never constructed from a candidate's own declaration: a candidate saying
    ``preserved=True`` is a claim, not a verification.
    ``ClaimedInvariant != VerifiedInvariant``.
    """

    invariant_id: str
    preserved: bool
    trace: Trace
    observation: InvariantObservation

    def __post_init__(self) -> None:
        if not self.invariant_id.strip():
            raise ValueError("an invariant verification requires an invariant id")
        if self.invariant_id != self.observation.invariant_id:
            raise ValueError(
                "invariant verification must reference its own observation"
            )


class UnregisteredExtractorError(KeyError):
    """Raised when an ``InvariantSpec`` names an unregistered extractor id."""


class InvariantExtractionError(Exception):
    """Raised when a registered extractor fails while extracting a value.

    Wraps the underlying exception so callers see which extractor and which
    side of the transition (``before_state`` or ``after_state``) failed,
    rather than an opaque exception surfacing from inside the gate.
    """


class InvariantExtractorRegistry:
    """Registration authority for invariant extractors.

    Extractors are registered here, never carried by a ``TransitionCandidate``
    or an ``InvariantSpec``. A spec only names an ``extractor_id``; resolving
    that id to an actual callable is this registry's authority alone.

    Not thread-safe: concurrent ``register`` calls on the same instance are
    not synchronized. Registration is expected at module import/setup time,
    not under concurrent access; callers sharing a registry across threads
    must provide their own synchronization.
    """

    def __init__(self) -> None:
        self._extractors: dict[str, InvariantExtractor] = {}

    def register(self, extractor_id: str, extractor: InvariantExtractor) -> None:
        """Register an extractor under ``extractor_id``.

        Raises if ``extractor_id`` is blank or already registered: an
        extractor id is a stable, single-owner registration, not a mutable
        slot a later caller can silently overwrite.
        """

        if not extractor_id.strip():
            raise ValueError("an extractor id cannot be blank")
        if extractor_id in self._extractors:
            raise ValueError(f"extractor id already registered: {extractor_id!r}")
        self._extractors[extractor_id] = extractor

    def resolve(self, extractor_id: str) -> InvariantExtractor:
        """Resolve a registered extractor, or raise if none is registered."""

        try:
            return self._extractors[extractor_id]
        except KeyError as error:
            raise UnregisteredExtractorError(
                f"no extractor registered for id: {extractor_id!r}"
            ) from error


class InvariantVerificationGate:
    """Independently verifies a claimed invariant against an admitted transition.

    This gate -- not the candidate -- owns extraction and comparison. It
    requires a ``StructurallyAdmissibleTransition`` (so verification only ever
    runs on something that already passed structural admission) and an
    ``InvariantExtractorRegistry`` (so the extractor is never supplied by the
    candidate itself). Extractors must return values comparable with ``==``;
    equality is used directly to decide ``preserved``, so an extractor
    returning identity-compared or otherwise non-meaningfully-comparable
    objects (for example, plain objects without a custom ``__eq__``) will not
    produce a trustworthy verification.

    This only verifies invariants named in ``transition.preserved``: a
    candidate's ``changed`` components are, by definition, not claimed as
    preserved, so there is intentionally no path here to "verify" one of
    them stayed the same.
    """

    @staticmethod
    def verify(
        transition: "StructurallyAdmissibleTransition",
        spec: InvariantSpec,
        registry: InvariantExtractorRegistry,
    ) -> InvariantVerification:
        """Verify ``spec`` against ``transition`` using a registered extractor."""

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
        try:
            preserved = before_value == after_value
        except Exception as error:
            raise InvariantExtractionError(
                f"comparing before/after values failed for invariant "
                f"{spec.invariant_id!r}: {error}"
            ) from error
        observation = InvariantObservation(
            invariant_id=spec.invariant_id,
            before_value=before_value,
            after_value=after_value,
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
        )


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
