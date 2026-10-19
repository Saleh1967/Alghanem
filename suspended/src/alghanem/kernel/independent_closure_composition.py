"""G0.IC.1e: composition of the three derived `IndependentClosure` conjuncts.

G0.IC.1a, G0.IC.1c and G0.IC.1d each derive exactly one conjunct of
`IndependentClosure`, and each says the same thing in the same words: composing
them is a separate question with no authority in this repository. This module is
that composition, and nothing more.

Nothing new is read. The gate opens no evidence, executes no evaluator, and
inspects no frozen poset: every input is already a gate-issued reading, and this
stage only relates the three readings to each other. `ThreeReadingsAreNotAFourth`
-- a composition that re-derived any conjunct would be a second authority over a
question already answered, and the two answers could disagree.

`CallerDoesNotOwnComposition`: `assess` takes exactly three parameters -- the
comparability assessment, the exhaustion assessment and the survival certificate
-- and no status, no reason, and no closure claim.

`OneRequestOrRefusal`. The three readings must speak for the *same*
`BirthAssessmentRequest`, compared by object identity, exactly as G0.IC.1c
requires of its certificates. Readings of different requests are refused, never
composed: a comparability result for one frozen experiment and a survival
reading for another would compose into a closure claim no single experiment ever
supported.

The enumeration performed before this module was written. Comparability is
two-valued and exhaustion and survival are three-valued, so there are exactly
`2 x 3 x 3 = 18` combinations. Every one of them was named before any code here
existed, and each conjunct is classified independently into exactly one of three
roles:

* *satisfied* -- `COMPETITION_RESOLVED_IN_POSET`,
  `LICENSED_WEAKER_MODELS_EXHAUSTED`, `SURVIVES`.
* *refuting* -- `WEAKER_MODEL_CLOSES_RESIDUAL`, `DOES_NOT_SURVIVE`. These are
  declared knowledge *against* the conjunct, read from evidence-derived
  executions.
* *undetermined* -- `EXHAUSTION_UNDETERMINED`, `DEFER`, and
  `COMPETITION_UNRESOLVED_IN_POSET`.

`UnresolvedComparabilityIsIgnoranceNotRefutation` is why comparability has no
refuting branch at all: G0.IC.1a already resolves `AbsentRelation !=
DeclaredIncomparability` conservatively, so its unresolved branch means the
frozen poset did not settle the relation -- not that a competing explanation was
established. Reading it as a refutation would manufacture knowledge out of
silence, which is the mirror image of the fabricated closure this chain exists
to forbid.

Aggregation follows the precedence already enforced twice in this kernel
(`BLOCK > DEFER > VERIFIED` in `InvariantVerificationGate`, and
`WEAKER_MODEL_CLOSES_RESIDUAL > EXHAUSTION_UNDETERMINED >
LICENSED_WEAKER_MODELS_EXHAUSTED` in `WeakerModelExhaustionGate`):

```
CLOSURE_REFUTED_IN_SCOPE
  > CLOSURE_UNDETERMINED_IN_SCOPE
  > CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION
```

A single refuting conjunct outranks every deferral (`False and Unknown ==
False`), and the two are tracked in separate `refuting_conjuncts` and
`undetermined_conjuncts` fields, because a conjunct disproved and a conjunct
unknown are different epistemic states that a single field would erase. Of the
18 combinations, 10 are refuted, 7 are undetermined, and exactly 1 -- resolved
comparability, exhausted licensed weaker models, and a surviving residual --
reaches the third status.

`SatisfiedConjunctsIsNotIndependentClosure`, and why that one reachable
combination still yields `False`. The three conjuncts hold *as read*, and
reading is all that happened. Three named barriers, already declared by the
stages that produced these very inputs, stand between that and closure:

* `OneWitnessIsNotResidualCertification` -- G0.IC.1d certifies one witness, and
  G0.RC.1 (`ResidualCertificationCandidate`) remains deferred, so no certified
  residual exists to be closed over.
* `SurvivalReadIsNotMeasuredReplicatedResidual` -- in `EMPIRICAL` mode the
  constitution requires a measured residual replicated in a second independent
  measurement run, and no authority here knows about a second run.
* `CoverageIsNotCorrectness` and `FrozenConeIsDeclaredNotProven` -- G0.IC.1c
  proves the licensed cone was covered exactly once, not that its declared
  outcomes are true of the world.

`IndependentClosureDecision.is_independent_closure` is therefore `False` on
every branch, including the satisfied one. The status name says exactly what was
reached and what it is pending on, rather than overstating it; AIM-K3 remains an
open barrier, now narrowed by name rather than declared met.

`CompositionIsNotAVerdict`. This stage is deliberately not wired to
`BirthVerdictGate`, and the assessments it consumes are untouched: their own
`is_independent_closure` properties remain `False` constants. It issues no
`BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no
`TraditionalName`. `ClosureRefutedInScope != NO_BIRTH_IN_SCOPE`: a refuted
conjunct is the shape of an argument against birth in this scope, not that
verdict.
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
    EvidenceMode,
    ResidualSurvivalStatus,
    _require_text,
)
from .independent_closure import (
    ComparabilityClosureStatus,
    IndependentClosureAssessment,
)
from .residual_survival import ResidualSurvivalCertificate
from .weaker_model_exhaustion import (
    WeakerModelExhaustionAssessment,
    WeakerModelExhaustionStatus,
)

_COMPOSITION_TOKEN = object()


class IndependentClosureCompositionError(BirthExperimentSpecificationError):
    """A closure composition was requested outside its authority boundary."""


class IndependentClosureConjunct(Enum):
    """The three conjuncts this composition relates, and no others."""

    COMPARABILITY = "COMPARABILITY"
    WEAKER_MODEL_EXHAUSTION = "WEAKER_MODEL_EXHAUSTION"
    RESIDUAL_SURVIVAL = "RESIDUAL_SURVIVAL"


class IndependentClosureCompositionStatus(Enum):
    """The gate's own three-valued composition outcome, never a birth status."""

    CLOSURE_REFUTED_IN_SCOPE = "CLOSURE_REFUTED_IN_SCOPE"
    CLOSURE_UNDETERMINED_IN_SCOPE = "CLOSURE_UNDETERMINED_IN_SCOPE"
    CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION = (
        "CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION"
    )


_COMPOSITION_REASONS: Mapping[IndependentClosureCompositionStatus, str] = (
    MappingProxyType(
        {
            IndependentClosureCompositionStatus.CLOSURE_REFUTED_IN_SCOPE: (
                "DeclaredOutcomeRefutesAConjunct: at least one conjunct of "
                "IndependentClosure was read as declaredly not holding -- a "
                "licensed weaker model that closes the residual, or a residual "
                "that does not survive. A refuting conjunct outranks every "
                "deferral, because knowledge that a conjunct fails is not erased "
                "by ignorance elsewhere. This is the shape of an argument against "
                "birth in this scope; it is not NO_BIRTH_IN_SCOPE, which only "
                "BirthVerdictGate may issue"
            ),
            IndependentClosureCompositionStatus.CLOSURE_UNDETERMINED_IN_SCOPE: (
                "ComposedReadingsLeaveAConjunctUndetermined: no conjunct was "
                "refuted, but at least one was left undetermined -- an unresolved "
                "comparability in the frozen poset, a deferred exhaustion, or a "
                "deferred survival reading. An undetermined conjunct is ignorance, "
                "counted neither as satisfied nor as refuted"
            ),
            IndependentClosureCompositionStatus.CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION: (  # noqa: E501
                "ThreeConjunctsReadSatisfiedPendingResidualCertification: "
                "comparability is resolved in the frozen poset, every licensed "
                "weaker model was certified FAIL_TO_CLOSE, and the residual was "
                "read as SURVIVES. This is what the three readings say, and no "
                "more: OneWitnessIsNotResidualCertification (G0.RC.1 is deferred), "
                "SurvivalReadIsNotMeasuredReplicatedResidual, and "
                "CoverageIsNotCorrectness each remain open by name, so "
                "is_independent_closure is False on this branch too"
            ),
        }
    )
)

_REFUTING_EXHAUSTION: frozenset[WeakerModelExhaustionStatus] = frozenset(
    {WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL}
)
_UNDETERMINED_EXHAUSTION: frozenset[WeakerModelExhaustionStatus] = frozenset(
    {WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED}
)
_REFUTING_SURVIVAL: frozenset[ResidualSurvivalStatus] = frozenset(
    {ResidualSurvivalStatus.DOES_NOT_SURVIVE}
)
_UNDETERMINED_SURVIVAL: frozenset[ResidualSurvivalStatus] = frozenset(
    {ResidualSurvivalStatus.DEFER}
)
_UNDETERMINED_COMPARABILITY: frozenset[ComparabilityClosureStatus] = frozenset(
    {ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET}
)

_CONJUNCT_ORDER: tuple[IndependentClosureConjunct, ...] = (
    IndependentClosureConjunct.COMPARABILITY,
    IndependentClosureConjunct.WEAKER_MODEL_EXHAUSTION,
    IndependentClosureConjunct.RESIDUAL_SURVIVAL,
)


@dataclass(frozen=True, slots=True)
class IndependentClosureDecision:
    """The gate-issued composition of three conjunct readings for one request.

    `status` is never caller-supplied: it is derived from the three readings'
    own derived statuses under a fixed precedence, after they were proven to
    speak for one and the same authorized assessment request.
    """

    comparability: IndependentClosureAssessment
    exhaustion: WeakerModelExhaustionAssessment
    survival: ResidualSurvivalCertificate
    status: IndependentClosureCompositionStatus
    reason: str
    refuting_conjuncts: tuple[IndependentClosureConjunct, ...]
    undetermined_conjuncts: tuple[IndependentClosureConjunct, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _COMPOSITION_TOKEN:
            raise IndependentClosureCompositionError(
                "closure decisions must be issued by "
                "IndependentClosureCompositionGate"
            )
        if type(self.comparability) is not IndependentClosureAssessment:
            raise IndependentClosureCompositionError(
                "a closure decision requires a gate-issued comparability assessment"
            )
        if type(self.exhaustion) is not WeakerModelExhaustionAssessment:
            raise IndependentClosureCompositionError(
                "a closure decision requires a gate-issued exhaustion assessment"
            )
        if type(self.survival) is not ResidualSurvivalCertificate:
            raise IndependentClosureCompositionError(
                "a closure decision requires a gate-issued survival certificate"
            )
        if not isinstance(self.status, IndependentClosureCompositionStatus):
            raise IndependentClosureCompositionError(
                "a closure decision requires a derived composition status"
            )
        _require_text(self.reason, "closure decision reason")
        for conjuncts, field_name in (
            (self.refuting_conjuncts, "refuting conjuncts"),
            (self.undetermined_conjuncts, "undetermined conjuncts"),
        ):
            if type(conjuncts) is not tuple or any(
                not isinstance(item, IndependentClosureConjunct) for item in conjuncts
            ):
                raise IndependentClosureCompositionError(
                    f"{field_name} must be frozen members of "
                    "IndependentClosureConjunct"
                )
            if len(set(conjuncts)) != len(conjuncts):
                raise IndependentClosureCompositionError(
                    f"{field_name} must not name one conjunct twice"
                )
        if set(self.refuting_conjuncts) & set(self.undetermined_conjuncts):
            raise IndependentClosureCompositionError(
                "a conjunct cannot be both refuted and undetermined"
            )
        if self.status is IndependentClosureCompositionStatus.CLOSURE_REFUTED_IN_SCOPE:
            if not self.refuting_conjuncts:
                raise IndependentClosureCompositionError(
                    "a refuted status requires the conjuncts that were refuted"
                )
        elif self.refuting_conjuncts:
            raise IndependentClosureCompositionError(
                "only a refuted status may name refuted conjuncts"
            )
        if (
            self.status
            is IndependentClosureCompositionStatus.CLOSURE_UNDETERMINED_IN_SCOPE
            and not self.undetermined_conjuncts
        ):
            raise IndependentClosureCompositionError(
                "an undetermined status requires the conjuncts left undetermined"
            )
        if (
            self.status
            is IndependentClosureCompositionStatus.CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION  # noqa: E501
            and (self.undetermined_conjuncts or self.refuting_conjuncts)
        ):
            raise IndependentClosureCompositionError(
                "a satisfied status cannot name a refuted or undetermined conjunct"
            )

    @property
    def request(self) -> BirthAssessmentRequest:
        """The one authorized request all three readings speak for."""

        return self.comparability.request

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def evidence_mode(self) -> EvidenceMode:
        """The mode declared by the frozen experiment, never by a caller."""

        return self.specification.evidence_mode

    @property
    def conjunct_statuses(
        self,
    ) -> Mapping[IndependentClosureConjunct, str]:
        """Each conjunct's own derived status name, for audit."""

        return MappingProxyType(
            {
                IndependentClosureConjunct.COMPARABILITY: (
                    self.comparability.status.name
                ),
                IndependentClosureConjunct.WEAKER_MODEL_EXHAUSTION: (
                    self.exhaustion.status.name
                ),
                IndependentClosureConjunct.RESIDUAL_SURVIVAL: self.survival.status.name,
            }
        )

    @property
    def satisfied_conjuncts(self) -> tuple[IndependentClosureConjunct, ...]:
        """The conjuncts read as holding, in a fixed order, never caller order."""

        excluded = set(self.refuting_conjuncts) | set(self.undetermined_conjuncts)
        return tuple(
            conjunct for conjunct in _CONJUNCT_ORDER if conjunct not in excluded
        )

    @property
    def is_independent_closure(self) -> bool:
        """Always `False`: three satisfied readings are not a certified closure.

        Even on the satisfied branch, `OneWitnessIsNotResidualCertification`,
        `SurvivalReadIsNotMeasuredReplicatedResidual` and
        `CoverageIsNotCorrectness` remain open by name, and G0.RC.1 is
        deferred. The status records exactly what the three readings reached
        and what it is pending on; this property claims nothing beyond it.
        """

        return False


class IndependentClosureCompositionGate:
    """The sole authority that may issue an `IndependentClosureDecision`.

    The gate accepts no status, reason, or closure claim from its caller, and
    re-derives no conjunct. It proves the three gate-issued readings speak for
    one and the same authorized assessment request, then composes their own
    derived statuses under a fixed precedence.
    """

    @staticmethod
    def assess(
        *,
        comparability: IndependentClosureAssessment,
        exhaustion: WeakerModelExhaustionAssessment,
        survival: ResidualSurvivalCertificate,
    ) -> IndependentClosureDecision:
        """Compose the three derived conjunct readings for one frozen request."""

        if type(comparability) is not IndependentClosureAssessment:
            raise IndependentClosureCompositionError(
                "closure composition requires a gate-issued comparability " "assessment"
            )
        if type(exhaustion) is not WeakerModelExhaustionAssessment:
            raise IndependentClosureCompositionError(
                "closure composition requires a gate-issued exhaustion assessment"
            )
        if type(survival) is not ResidualSurvivalCertificate:
            raise IndependentClosureCompositionError(
                "closure composition requires a gate-issued survival certificate"
            )

        request = comparability.request
        if exhaustion.request is not request or survival.request is not request:
            raise IndependentClosureCompositionError(
                "every conjunct reading must speak for this exact authorized "
                "assessment request; readings of different requests compose into "
                "a closure claim no single frozen experiment supported"
            )
        if survival.record.execution_record.request.evidence_snapshot is not (
            request.evidence_snapshot
        ):
            raise IndependentClosureCompositionError(
                "the survival reading must be derived from this request's own "
                "authorized evidence snapshot"
            )

        refuting: list[IndependentClosureConjunct] = []
        undetermined: list[IndependentClosureConjunct] = []
        if comparability.status in _UNDETERMINED_COMPARABILITY:
            undetermined.append(IndependentClosureConjunct.COMPARABILITY)
        if exhaustion.status in _REFUTING_EXHAUSTION:
            refuting.append(IndependentClosureConjunct.WEAKER_MODEL_EXHAUSTION)
        elif exhaustion.status in _UNDETERMINED_EXHAUSTION:
            undetermined.append(IndependentClosureConjunct.WEAKER_MODEL_EXHAUSTION)
        if survival.status in _REFUTING_SURVIVAL:
            refuting.append(IndependentClosureConjunct.RESIDUAL_SURVIVAL)
        elif survival.status in _UNDETERMINED_SURVIVAL:
            undetermined.append(IndependentClosureConjunct.RESIDUAL_SURVIVAL)

        if refuting:
            status = IndependentClosureCompositionStatus.CLOSURE_REFUTED_IN_SCOPE
        elif undetermined:
            status = IndependentClosureCompositionStatus.CLOSURE_UNDETERMINED_IN_SCOPE
        else:
            status = (
                IndependentClosureCompositionStatus.CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION  # noqa: E501
            )

        ordered = {conjunct: index for index, conjunct in enumerate(_CONJUNCT_ORDER)}
        return IndependentClosureDecision(
            comparability=comparability,
            exhaustion=exhaustion,
            survival=survival,
            status=status,
            reason=_COMPOSITION_REASONS[status],
            refuting_conjuncts=tuple(sorted(refuting, key=ordered.__getitem__)),
            undetermined_conjuncts=tuple(sorted(undetermined, key=ordered.__getitem__)),
            _token=_COMPOSITION_TOKEN,
        )
