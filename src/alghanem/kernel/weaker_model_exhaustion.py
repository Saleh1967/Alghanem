"""G0.IC.1c: exhaustion of the licensed weaker model set, derived by coverage.

G0.IC.1b reads one weaker model's declared `Close(W_i, R)` outcome from an
evidence-derived execution. It says so explicitly:
`WeakerModelClosureCertificate.is_weaker_model_exhaustion` is `False`
unconditionally, because one model is not the set. This module is that set,
and nothing more.

`NoBirthBeforeLicensedWeakerExhaustion` speaks about *all* licensed weaker
models. The cone those models form is already derived, not written:
`BirthExperimentSpecification.frozen_weaker_models` reads it off the frozen
projection poset before any evidence exists. So the question "were they
exhausted?" has a decidable shape -- exact coverage of a frozen finite set --
and this gate answers only that shape.

Coverage before judgement, copied from an existing authority. The precedent is
`InvariantVerificationGate.assess_all_preserved`, which refuses specs that do
not exactly cover `transition.preserved` or that name a component twice,
because a malformed request is neither a falsified nor an untestable claim.
The same rule holds here:

* A certificate set missing a model in the cone is refused, never read as
  exhaustion-so-far. `MissingModelIsNotFailureToClose` -- an unevaluated model
  is ignorance, and silently treating ignorance as a failure to close is
  exactly how a fabricated exhaustion would be manufactured.
* A certificate set naming a model twice is refused, because two outcomes for
  one model would let a caller choose which one counts by ordering.
* A certificate naming a model outside the cone is refused, because a model
  the frozen poset never licensed cannot contribute to exhausting the licensed
  set.

Aggregation, and the precedence that governs it. Every certificate is read
independently; the gate never stops at the first one. The status is then the
conjunctive claim's precedence, mirroring `BLOCK > DEFER > VERIFIED`:

```
WEAKER_MODEL_CLOSES_RESIDUAL > EXHAUSTION_UNDETERMINED > LICENSED_WEAKER_MODELS_EXHAUSTED
```

A single `CLOSE` outranks every deferral: knowing that some weaker model *does*
close the residual is knowledge, and an unrelated `DEFER` elsewhere must not
erase it (`False and Unknown == False`). `LICENSED_WEAKER_MODELS_EXHAUSTED` is
therefore reachable only when *every* model in the frozen cone was certified
`FAIL_TO_CLOSE`, and the result does not depend on the order the certificates
were given in.

`WeakerModelClosesResidual != NoBirthVerdict`. The `CLOSE` branch is evidence
that a weaker model suffices, which is the shape of an argument against birth
in this scope. It is not that verdict: `BirthVerdictGate` is the only authority
that may issue one, this module is deliberately not wired to it, and nothing
here issues a `BirthVerdict`, `BirthCandidate`, `Freeze`, `E0` mapping, or
`TraditionalName`.

Claims this module explicitly does **not** make:

* `WeakerModelExhaustion != IndependentClosure`. Exhaustion is one conjunct.
  The others are a residual that survived measurement or formal proof, and
  resolved comparability (G0.IC.1a). `is_independent_closure` is `False`
  unconditionally here too, and `IndependentClosureAssessment` is untouched.
* `CoverageIsNotCorrectness`. The gate proves that every licensed weaker model
  was evaluated on this request's own authorized evidence and reported a
  declared outcome. It does not prove those outcomes are true of the world, nor
  that the frozen poset licensed the right models in the first place
  (`FrozenConeIsDeclaredNotProven`).
* `SameRequestIsNotSameEvidenceRun`. Certificates are required to share one
  `BirthAssessmentRequest` object, so they speak about one frozen experiment
  and one authorized evidence snapshot. Nothing here proves the evaluators ran
  in any particular order, concurrently, or at all in the same process.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType

from .birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    ClosureAssessmentStatus,
    _require_text,
)
from .weaker_model_closure import WeakerModelClosureCertificate

_EXHAUSTION_TOKEN = object()


class WeakerModelExhaustionError(BirthExperimentSpecificationError):
    """An exhaustion assessment was requested outside its authority boundary."""


class WeakerModelExhaustionStatus(Enum):
    """The gate's own three-valued exhaustion outcome, never a birth status."""

    LICENSED_WEAKER_MODELS_EXHAUSTED = "LICENSED_WEAKER_MODELS_EXHAUSTED"
    WEAKER_MODEL_CLOSES_RESIDUAL = "WEAKER_MODEL_CLOSES_RESIDUAL"
    EXHAUSTION_UNDETERMINED = "EXHAUSTION_UNDETERMINED"


_EXHAUSTION_REASONS: Mapping[WeakerModelExhaustionStatus, str] = MappingProxyType(
    {
        WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED: (
            "EveryLicensedWeakerModelFailedToClose: every model in the frozen "
            "prerequisite cone was certified FAIL_TO_CLOSE on this request's own "
            "authorized evidence, and the cone was covered exactly. This closes "
            "one conjunct of IndependentClosure and no other: no residual "
            "survival is certified here, comparability belongs to G0.IC.1a, and "
            "no birth verdict follows"
        ),
        WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL: (
            "LicensedWeakerModelClosesTheResidual: at least one model in the "
            "frozen cone was certified CLOSE, so the licensed weaker set is not "
            "exhausted. A weaker model sufficing is the shape of an argument "
            "against birth in this scope; it is not that verdict, which only "
            "BirthVerdictGate may issue"
        ),
        WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED: (
            "DeclaredDeferralLeavesExhaustionUndetermined: no model was "
            "certified CLOSE, but at least one was certified DEFER, so whether "
            "the licensed weaker set is exhausted is not determined by these "
            "certificates. A deferral is never counted as a failure to close"
        ),
    }
)

_PRECEDENCE: tuple[tuple[ClosureAssessmentStatus, WeakerModelExhaustionStatus], ...] = (
    (
        ClosureAssessmentStatus.CLOSE,
        WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL,
    ),
    (
        ClosureAssessmentStatus.DEFER,
        WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED,
    ),
)


@dataclass(frozen=True, slots=True)
class WeakerModelExhaustionAssessment:
    """The gate-issued exhaustion record for one frozen prerequisite cone.

    `status` is never caller-supplied: it is derived from the certificates'
    own declared outcomes under a fixed precedence, after the cone was proven
    covered exactly once.
    """

    request: BirthAssessmentRequest
    certificates: tuple[WeakerModelClosureCertificate, ...]
    status: WeakerModelExhaustionStatus
    reason: str
    closing_models: tuple[str, ...]
    deferred_models: tuple[str, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EXHAUSTION_TOKEN:
            raise WeakerModelExhaustionError(
                "exhaustion assessments must be issued by WeakerModelExhaustionGate"
            )
        if type(self.request) is not BirthAssessmentRequest:
            raise WeakerModelExhaustionError(
                "an exhaustion assessment requires an authorized assessment request"
            )
        if type(self.certificates) is not tuple or any(
            type(item) is not WeakerModelClosureCertificate
            for item in self.certificates
        ):
            raise WeakerModelExhaustionError(
                "an exhaustion assessment requires gate-issued closure certificates"
            )
        if not isinstance(self.status, WeakerModelExhaustionStatus):
            raise WeakerModelExhaustionError(
                "an exhaustion assessment requires a derived exhaustion status"
            )
        _require_text(self.reason, "exhaustion assessment reason")
        for models, field_name in (
            (self.closing_models, "closing models"),
            (self.deferred_models, "deferred models"),
        ):
            if type(models) is not tuple or any(
                type(item) is not str for item in models
            ):
                raise WeakerModelExhaustionError(f"{field_name} must be frozen text")
        if self.status is WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL:
            if not self.closing_models:
                raise WeakerModelExhaustionError(
                    "a closing status requires the models that closed the residual"
                )
        elif self.closing_models:
            raise WeakerModelExhaustionError(
                "only a closing status may name models that closed the residual"
            )
        if self.status is WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED and (
            not self.deferred_models
        ):
            raise WeakerModelExhaustionError(
                "an undetermined status requires the models that deferred"
            )
        if (
            self.status is WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
            and self.deferred_models
        ):
            raise WeakerModelExhaustionError(
                "an exhausted status cannot name a deferred model"
            )

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def frozen_weaker_models(self) -> tuple[str, ...]:
        """The derived cone this assessment proved covered exactly once."""

        return self.specification.frozen_weaker_models

    @property
    def certified_models(self) -> tuple[str, ...]:
        return tuple(certificate.model_id for certificate in self.certificates)

    @property
    def outcome_counts(self) -> Mapping[ClosureAssessmentStatus, int]:
        """Derived counts over every declared outcome, including zeros."""

        counts = dict.fromkeys(ClosureAssessmentStatus, 0)
        for certificate in self.certificates:
            counts[certificate.status] += 1
        return MappingProxyType(counts)

    @property
    def is_weaker_model_exhaustion(self) -> bool:
        """Whether every licensed weaker model was certified `FAIL_TO_CLOSE`.

        Unlike the per-model certificate's property of the same name, this one
        is derived and genuinely two-valued: the cone was proven covered
        exactly once, and every member reported a declared outcome.
        """

        return (
            self.status is WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
        )

    @property
    def is_independent_closure(self) -> bool:
        """Always `False`: exhaustion is one conjunct of closure, not closure.

        A surviving residual under `NoBirthWithoutResidualOrFormalNecessity`
        and resolved comparability under
        `NoRicherStructureBeforeLowerOpenResidualClosure` are separate
        conjuncts, neither certified here.
        """

        return False


class WeakerModelExhaustionGate:
    """The sole authority that may issue a `WeakerModelExhaustionAssessment`.

    The gate accepts no status, reason, or exhaustion claim. It proves that the
    given certificates cover the request's own frozen prerequisite cone exactly
    once, and then derives the status from their declared outcomes.
    """

    @staticmethod
    def assess(
        *,
        request: BirthAssessmentRequest,
        certificates: tuple[WeakerModelClosureCertificate, ...],
    ) -> WeakerModelExhaustionAssessment:
        """Derive one exhaustion outcome for a frozen prerequisite cone."""

        if type(request) is not BirthAssessmentRequest:
            raise WeakerModelExhaustionError(
                "exhaustion assessment requires an authorized assessment request"
            )
        if type(certificates) is not tuple or any(
            type(item) is not WeakerModelClosureCertificate for item in certificates
        ):
            raise WeakerModelExhaustionError(
                "exhaustion assessment requires gate-issued closure certificates"
            )

        for certificate in certificates:
            if certificate.request is not request:
                raise WeakerModelExhaustionError(
                    "every closure certificate must speak for this exact "
                    "authorized assessment request"
                )

        cone = request.specification.frozen_weaker_models
        certified = tuple(certificate.model_id for certificate in certificates)
        if len(set(certified)) != len(certified):
            raise WeakerModelExhaustionError(
                "closure certificates cannot name one weaker model twice; two "
                "outcomes for one model would let ordering choose the result"
            )
        if set(certified) != set(cone):
            raise WeakerModelExhaustionError(
                "closure certificates must exactly cover the frozen prerequisite "
                "cone; an unevaluated model is ignorance, never a failure to close"
            )

        closing = tuple(
            sorted(
                certificate.model_id
                for certificate in certificates
                if certificate.status is ClosureAssessmentStatus.CLOSE
            )
        )
        deferred = tuple(
            sorted(
                certificate.model_id
                for certificate in certificates
                if certificate.status is ClosureAssessmentStatus.DEFER
            )
        )

        status = WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
        outcomes = {certificate.status for certificate in certificates}
        for outcome, ranked in _PRECEDENCE:
            if outcome in outcomes:
                status = ranked
                break

        return WeakerModelExhaustionAssessment(
            request=request,
            certificates=certificates,
            status=status,
            reason=_EXHAUSTION_REASONS[status],
            closing_models=closing,
            deferred_models=deferred,
            _token=_EXHAUSTION_TOKEN,
        )
