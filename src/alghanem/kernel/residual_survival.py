"""G0.IC.1d: evidence-derived residual survival, and certified closure.

This module closes the second of the two conjuncts AIM-K3 names, and then --
and only then -- assembles all three conjuncts into a closure whose
`is_independent_closure` is genuinely two-valued.

Residual survival, by the same mechanism as G0.IC.1b. `NoBirthWithoutResidual
OrFormalNecessity` asks whether a residual survived measurement or formal
proof. Nothing in this kernel judges that, and nothing here starts to: the
judgement belongs to the residual evaluator, which runs on this request's own
authorized evidence through G0.BA.1b. What was missing was, once again, only
the relation between that evaluator's output string and a closed vocabulary.
`DeclaredResidualSurvivalVocabulary` is that relation, declared as data and
frozen against a content-bound residual definition, exactly as
`DeclaredClosureOutcomeVocabulary` is frozen against a content-bound closure
criterion. The same refusals apply, for the same reasons:

* `CallerDoesNotOwnResidualOutcome`. `ResidualSurvivalGate.assess` accepts no
  status, reason, or survival claim.
* `ExactTokenOrRefusal`. Matching is exact string equality. An unrecognized
  output is refused by residual id, never read as `SURVIVAL_UNDETERMINED`.
* The record must carry the `RESIDUAL_DEFINITION` role and name the request's
  own frozen residual definition.

Certified closure, assembled and never assumed. `CertifiedIndependentClosure`
requires all three conjuncts, each issued by the only authority that may issue
it, and all three bound to one `BirthAssessmentRequest` object:

```
ComparabilityResolved & LicensedWeakerExhausted & ResidualSurvived
```

Its `is_independent_closure` is the conjunction of those three derived
standings. It is not a written field, it is not a caller argument, and every
one of its inputs is refused unless it came from its own gate. This is the
property AIM-K3 asked to become capable of being other than `False`.

What is deliberately left exactly as it was. `IndependentClosureAssessment.is
_independent_closure` (G0.IC.1a) remains `False` unconditionally, and that
module is not edited. The precedent is G0.BA.1b, which layered provenance
above G0.BA.1a rather than weakening it: a stage that declared an unconditional
boundary keeps declaring it, and a later stage that genuinely earns more says
so in its own type. A caller holding only a G0.IC.1a assessment therefore still
cannot read closure out of it.

Claims this module explicitly does **not** make:

* `IndependentClosure != BirthVerdict`. `BirthVerdictGate` is still not wired
  to consume this, and nothing here issues a `BirthVerdict`, `BirthCandidate`,
  `Freeze`, `E0` mapping, or `TraditionalName`. Closure is a precondition the
  verdict authority may one day require; supplying a precondition is not
  supplying the verdict, and G0.BV.1 remains
  `DECLARED_DEFERRED_CONTRACT_ONLY`.
* `DeclaredVocabularyIsNotProvenSemantics`, inherited unchanged: freezing the
  token map before the gate runs prevents tailoring it to an output already
  seen, and proves nothing about why the evaluator emitted that token. Every
  claim assembled here is therefore only as sound as the declared vocabularies
  and the evaluators behind them.
* `CertifiedClosureIsNotProofOfNecessity`. The three conjuncts are the ones
  the constitution names, read from this experiment's own frozen declarations.
  That the experiment declared the right residual, the right criterion, and
  the right poset is not established by anything here
  (`FrozenDeclarationIsNotProvenDeclaration`).
"""

from __future__ import annotations

import threading
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType

from .birth import (
    BirthAssessmentRequest,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    ResidualDefinitionSpec,
    _require_text,
)
from .birth_content_identity import (
    BirthAssessmentContentBinding,
    BirthSemanticsContentIdentity,
)
from .evaluator_input_provenance import ProvenanceBoundEvaluatorExecutionRecord
from .independent_closure import (
    ComparabilityClosureStatus,
    IndependentClosureAssessment,
)
from .weaker_model_exhaustion import WeakerModelExhaustionAssessment

_RESIDUAL_TOKEN = object()


class ResidualSurvivalError(BirthExperimentSpecificationError):
    """A residual survival outcome was read outside its authority boundary."""


class ResidualSurvivalStatus(Enum):
    """The closed vocabulary of `Survives(R)`, never a birth status."""

    RESIDUAL_SURVIVED = "RESIDUAL_SURVIVED"
    RESIDUAL_EXPLAINED_AWAY = "RESIDUAL_EXPLAINED_AWAY"
    SURVIVAL_UNDETERMINED = "SURVIVAL_UNDETERMINED"


_SURVIVAL_REASONS: Mapping[ResidualSurvivalStatus, str] = MappingProxyType(
    {
        ResidualSurvivalStatus.RESIDUAL_SURVIVED: (
            "DeclaredSurvivedTokenRead: the residual evaluator's "
            "evidence-derived output is exactly a token the frozen residual "
            "definition declares as RESIDUAL_SURVIVED. This is one conjunct of "
            "IndependentClosure and no more: it is not exhaustion, not "
            "comparability, and not a birth verdict"
        ),
        ResidualSurvivalStatus.RESIDUAL_EXPLAINED_AWAY: (
            "DeclaredExplainedAwayTokenRead: the residual evaluator's "
            "evidence-derived output is exactly a token the frozen residual "
            "definition declares as RESIDUAL_EXPLAINED_AWAY, so no residual "
            "survives to be closed over in this scope"
        ),
        ResidualSurvivalStatus.SURVIVAL_UNDETERMINED: (
            "DeclaredUndeterminedTokenRead: the residual evaluator's "
            "evidence-derived output is exactly a token the frozen residual "
            "definition declares as SURVIVAL_UNDETERMINED. A declared "
            "undetermined outcome is a read result, never the gate's fallback "
            "for an output it failed to recognize"
        ),
    }
)


@dataclass(frozen=True, slots=True)
class DeclaredResidualSurvivalVocabulary:
    """A frozen map from literal evaluator output tokens to survival outcomes.

    It must cover every member of `ResidualSurvivalStatus` exactly once, so
    that no declared outcome is unreachable and none is silently dropped, and
    it must not bind one token to two outcomes.
    """

    residual_id: str
    domain: str
    tokens: tuple[tuple[str, ResidualSurvivalStatus], ...]

    def __post_init__(self) -> None:
        _require_text(self.residual_id, "residual vocabulary residual id")
        _require_text(self.domain, "residual vocabulary domain")
        if type(self.tokens) is not tuple or not self.tokens:
            raise ResidualSurvivalError(
                "a residual survival vocabulary requires frozen declared tokens"
            )
        seen_tokens: set[str] = set()
        seen_statuses: set[ResidualSurvivalStatus] = set()
        for entry in self.tokens:
            if type(entry) is not tuple or len(entry) != 2:
                raise ResidualSurvivalError(
                    "each declared outcome must be a token and a declared status"
                )
            token, status = entry
            if type(token) is not str or not token or token != token.strip():
                raise ResidualSurvivalError(
                    "a declared outcome token must be exact non-blank text with "
                    "no surrounding whitespace, because matching is exact"
                )
            if not isinstance(status, ResidualSurvivalStatus):
                raise ResidualSurvivalError(
                    "a declared outcome must name a member of the closed "
                    "ResidualSurvivalStatus vocabulary"
                )
            if token in seen_tokens:
                raise ResidualSurvivalError(
                    "a declared outcome token must not name two outcomes"
                )
            if status in seen_statuses:
                raise ResidualSurvivalError(
                    "a declared outcome status must be named by exactly one token"
                )
            seen_tokens.add(token)
            seen_statuses.add(status)
        if seen_statuses != set(ResidualSurvivalStatus):
            raise ResidualSurvivalError(
                "a residual survival vocabulary must cover every member of "
                "ResidualSurvivalStatus, so that no declared outcome is "
                "unreachable by construction"
            )

    @property
    def declared_outcomes(self) -> Mapping[str, ResidualSurvivalStatus]:
        return MappingProxyType(dict(self.tokens))

    @property
    def declared_tokens(self) -> tuple[str, ...]:
        return tuple(token for token, _ in self.tokens)


@dataclass(frozen=True, slots=True)
class AuthorizedResidualSurvivalVocabulary:
    """Issuer-only authorization of one vocabulary for one frozen residual."""

    vocabulary_id: str
    vocabulary: DeclaredResidualSurvivalVocabulary
    binding: BirthAssessmentContentBinding
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _RESIDUAL_TOKEN:
            raise ResidualSurvivalError(
                "authorized residual survival vocabularies must be issued by "
                "ResidualSurvivalVocabularyRegistry"
            )
        _require_text(self.vocabulary_id, "residual vocabulary id")
        if type(self.vocabulary) is not DeclaredResidualSurvivalVocabulary:
            raise ResidualSurvivalError(
                "an authorization requires a declared residual survival vocabulary"
            )
        if type(self.binding) is not BirthAssessmentContentBinding:
            raise ResidualSurvivalError(
                "an authorization requires a verified birth assessment content "
                "binding, so that the residual it speaks for is content-frozen"
            )
        if self.vocabulary.residual_id != self.residual_definition.residual_id:
            raise ResidualSurvivalError(
                "a residual survival vocabulary must name the bound contract's "
                "own frozen residual definition"
            )
        if self.vocabulary.domain != self.specification.domain:
            raise ResidualSurvivalError(
                "a residual survival vocabulary domain must match the bound "
                "contract's own frozen experiment domain"
            )

    @property
    def contract_specification(self) -> BirthExperimentSpecification:
        return self.binding.contract.specification

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.contract_specification

    @property
    def residual_definition(self) -> ResidualDefinitionSpec:
        return self.binding.contract.residual_definition

    @property
    def residual_id(self) -> str:
        return self.residual_definition.residual_id

    @property
    def domain(self) -> str:
        return self.specification.domain

    @property
    def residual_content_id(self) -> BirthSemanticsContentIdentity:
        return self.binding.residual_definition_content_id


class ResidualSurvivalVocabularyRegistry:
    """Authority that issues and seals survival vocabularies; it reads nothing."""

    def __init__(self) -> None:
        self._vocabularies: dict[
            tuple[str, str], AuthorizedResidualSurvivalVocabulary
        ] = {}
        self._issued_ids: set[str] = set()
        self._lock = threading.Lock()

    def register(
        self,
        *,
        vocabulary_id: str,
        vocabulary: DeclaredResidualSurvivalVocabulary,
        binding: BirthAssessmentContentBinding,
    ) -> AuthorizedResidualSurvivalVocabulary:
        """Authorize exactly one survival vocabulary for one frozen residual."""

        authorized = AuthorizedResidualSurvivalVocabulary(
            vocabulary_id=vocabulary_id,
            vocabulary=vocabulary,
            binding=binding,
            _token=_RESIDUAL_TOKEN,
        )
        key = (authorized.domain, authorized.residual_id)
        with self._lock:
            if vocabulary_id in self._issued_ids:
                raise ResidualSurvivalError(
                    "residual vocabulary id already issued by this registry"
                )
            if key in self._vocabularies:
                raise ResidualSurvivalError(
                    "a residual survival vocabulary is already authorized for "
                    "this exact domain and residual definition"
                )
            self._vocabularies[key] = authorized
            self._issued_ids.add(vocabulary_id)
        return authorized

    def seal(self, snapshot_id: str) -> SealedResidualSurvivalVocabularyRegistry:
        """Freeze the authorized survival vocabularies."""

        _require_text(snapshot_id, "residual vocabulary registry snapshot id")
        with self._lock:
            vocabularies = tuple(self._vocabularies.values())
        return SealedResidualSurvivalVocabularyRegistry(
            snapshot_id=snapshot_id,
            vocabularies=vocabularies,
            _token=_RESIDUAL_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedResidualSurvivalVocabularyRegistry:
    """Frozen vocabulary snapshot; it authorizes vocabularies but reads none."""

    snapshot_id: str
    vocabularies: tuple[AuthorizedResidualSurvivalVocabulary, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _RESIDUAL_TOKEN:
            raise ResidualSurvivalError(
                "sealed residual vocabulary registries must be issued by "
                "ResidualSurvivalVocabularyRegistry"
            )
        _require_text(self.snapshot_id, "residual vocabulary registry snapshot id")
        if type(self.vocabularies) is not tuple or any(
            type(item) is not AuthorizedResidualSurvivalVocabulary
            for item in self.vocabularies
        ):
            raise ResidualSurvivalError(
                "sealed residual vocabulary registries require frozen "
                "authorized vocabularies"
            )
        seen: set[tuple[str, str]] = set()
        for authorized in self.vocabularies:
            key = (authorized.domain, authorized.residual_id)
            if key in seen:
                raise ResidualSurvivalError(
                    "sealed residual vocabulary registry must not contain "
                    "duplicate vocabularies"
                )
            seen.add(key)

    def resolve(
        self, *, domain: str, residual_id: str
    ) -> AuthorizedResidualSurvivalVocabulary:
        """Return the exact authorized vocabulary for this domain and residual."""

        for authorized in self.vocabularies:
            if authorized.domain == domain and authorized.residual_id == residual_id:
                return authorized
        raise ResidualSurvivalError(
            "no residual survival vocabulary is authorized for this exact "
            "domain and residual definition"
        )


@dataclass(frozen=True, slots=True)
class ResidualSurvivalCertificate:
    """The gate-issued survival outcome for one frozen residual definition."""

    authorization: AuthorizedResidualSurvivalVocabulary
    record: ProvenanceBoundEvaluatorExecutionRecord
    residual_id: str
    matched_token: str
    status: ResidualSurvivalStatus
    reason: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _RESIDUAL_TOKEN:
            raise ResidualSurvivalError(
                "survival certificates must be issued by ResidualSurvivalGate"
            )
        if type(self.authorization) is not AuthorizedResidualSurvivalVocabulary:
            raise ResidualSurvivalError(
                "a survival certificate requires an authorized survival vocabulary"
            )
        if type(self.record) is not ProvenanceBoundEvaluatorExecutionRecord:
            raise ResidualSurvivalError(
                "a survival certificate requires a provenance-bound execution "
                "record, so that the read output came from authorized evidence"
            )
        _require_text(self.residual_id, "survival certificate residual id")
        _require_text(self.matched_token, "survival certificate matched token")
        _require_text(self.reason, "survival certificate reason")
        if not isinstance(self.status, ResidualSurvivalStatus):
            raise ResidualSurvivalError(
                "a survival certificate requires a derived survival status"
            )
        declared = self.authorization.vocabulary.declared_outcomes
        if declared.get(self.matched_token) is not self.status:
            raise ResidualSurvivalError(
                "certificate status must be the outcome the frozen vocabulary "
                "declares for the matched token"
            )
        if self.matched_token != self.record.output_content:
            raise ResidualSurvivalError(
                "the matched token must be the record's own executed output"
            )
        if self.residual_id != self.record.target_id:
            raise ResidualSurvivalError(
                "the certified residual must be the record's own evaluator target"
            )

    @property
    def request(self) -> BirthAssessmentRequest:
        return self.record.execution_record.request

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def residual_survived(self) -> bool:
        """Whether the frozen residual was certified to have survived."""

        return self.status is ResidualSurvivalStatus.RESIDUAL_SURVIVED

    @property
    def is_independent_closure(self) -> bool:
        """Always `False`: survival is one conjunct of closure, not closure."""

        return False


class ResidualSurvivalGate:
    """The sole authority that may issue a `ResidualSurvivalCertificate`."""

    @staticmethod
    def assess(
        *,
        registry: SealedResidualSurvivalVocabularyRegistry,
        record: ProvenanceBoundEvaluatorExecutionRecord,
    ) -> ResidualSurvivalCertificate:
        """Read the frozen residual's declared survival outcome from its record."""

        if type(registry) is not SealedResidualSurvivalVocabularyRegistry:
            raise ResidualSurvivalError(
                "survival reading requires a sealed vocabulary registry"
            )
        if type(record) is not ProvenanceBoundEvaluatorExecutionRecord:
            raise ResidualSurvivalError(
                "survival reading requires a provenance-bound execution record; "
                "an unbound record proves no evidence provenance"
            )
        if record.role is not BirthEvaluatorRole.RESIDUAL_DEFINITION:
            raise ResidualSurvivalError(
                "survival reading requires a record executed under the "
                "RESIDUAL_DEFINITION role; no other role's output is a Survives(R)"
            )

        request = record.execution_record.request
        specification = request.specification
        if record.definition.domain != specification.domain:
            raise ResidualSurvivalError(
                "the executing evaluator's authorized domain does not match the "
                "request's own frozen experiment domain"
            )
        if record.target_id != specification.residual_definition_id:
            raise ResidualSurvivalError(
                "the executed target is not this request's own frozen residual "
                "definition"
            )

        authorization = registry.resolve(
            domain=specification.domain,
            residual_id=specification.residual_definition_id,
        )
        if authorization.contract_specification != specification:
            raise ResidualSurvivalError(
                "the resolved survival vocabulary is bound to a contract whose "
                "frozen experiment specification is not this request's own"
            )

        token = record.output_content
        declared = authorization.vocabulary.declared_outcomes
        if token not in declared:
            raise ResidualSurvivalError(
                "the executed output is not a token the frozen residual "
                "definition declares; an unrecognized output is refused, never "
                "read as undetermined or any other declared outcome"
            )
        status = declared[token]

        return ResidualSurvivalCertificate(
            authorization=authorization,
            record=record,
            residual_id=record.target_id,
            matched_token=token,
            status=status,
            reason=_SURVIVAL_REASONS[status],
            _token=_RESIDUAL_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class CertifiedIndependentClosure:
    """All three conjuncts of `IndependentClosure`, each from its own authority.

    `is_independent_closure` here is derived from the three standings, not
    written. It is the first place in this kernel where that property is
    capable of being other than `False`, and it is capable of it only because
    every conjunct arrives as a gate-issued certificate bound to one authorized
    request.
    """

    comparability: IndependentClosureAssessment
    exhaustion: WeakerModelExhaustionAssessment
    survival: ResidualSurvivalCertificate
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _RESIDUAL_TOKEN:
            raise ResidualSurvivalError(
                "certified closures must be issued by CertifiedIndependentClosureGate"
            )
        if type(self.comparability) is not IndependentClosureAssessment:
            raise ResidualSurvivalError(
                "a certified closure requires a gate-issued comparability " "assessment"
            )
        if type(self.exhaustion) is not WeakerModelExhaustionAssessment:
            raise ResidualSurvivalError(
                "a certified closure requires a gate-issued exhaustion assessment"
            )
        if type(self.survival) is not ResidualSurvivalCertificate:
            raise ResidualSurvivalError(
                "a certified closure requires a gate-issued survival certificate"
            )
        request = self.comparability.request
        if self.exhaustion.request is not request or self.survival.request is not (
            request
        ):
            raise ResidualSurvivalError(
                "every conjunct must speak for this exact authorized assessment "
                "request; conjuncts from different requests are not one closure"
            )

    @property
    def request(self) -> BirthAssessmentRequest:
        return self.comparability.request

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def comparability_resolved(self) -> bool:
        return (
            self.comparability.status
            is ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET
        )

    @property
    def weaker_models_exhausted(self) -> bool:
        return self.exhaustion.is_weaker_model_exhaustion

    @property
    def residual_survived(self) -> bool:
        return self.survival.residual_survived

    @property
    def is_independent_closure(self) -> bool:
        """The conjunction of the three certified conjuncts.

        This is not `NoBirthWithoutResidualOrFormalNecessity` satisfied by
        assertion: each conjunct was issued by the only authority permitted to
        issue it, from an evaluation of this request's own authorized evidence
        or its own frozen poset. It remains a precondition and not a verdict:
        `BirthVerdictGate` is not wired to consume this, and G0.BV.1 is still
        `DECLARED_DEFERRED_CONTRACT_ONLY`.
        """

        return (
            self.comparability_resolved
            and self.weaker_models_exhausted
            and self.residual_survived
        )

    @property
    def unmet_conjuncts(self) -> tuple[str, ...]:
        """The named conjuncts that were not certified, in a fixed order."""

        unmet: list[str] = []
        if not self.comparability_resolved:
            unmet.append("NoRicherStructureBeforeLowerOpenResidualClosure")
        if not self.weaker_models_exhausted:
            unmet.append("NoBirthBeforeLicensedWeakerExhaustion")
        if not self.residual_survived:
            unmet.append("NoBirthWithoutResidualOrFormalNecessity")
        return tuple(unmet)

    @property
    def is_birth_verdict(self) -> bool:
        """Always `False`: a satisfied precondition is not a verdict."""

        return False


class CertifiedIndependentClosureGate:
    """The sole authority that may issue a `CertifiedIndependentClosure`.

    It accepts no closure claim. It requires all three conjuncts as gate-issued
    records bound to one authorized request, and derives nothing else.
    """

    @staticmethod
    def assess(
        *,
        comparability: IndependentClosureAssessment,
        exhaustion: WeakerModelExhaustionAssessment,
        survival: ResidualSurvivalCertificate,
    ) -> CertifiedIndependentClosure:
        """Assemble the three certified conjuncts of `IndependentClosure`."""

        return CertifiedIndependentClosure(
            comparability=comparability,
            exhaustion=exhaustion,
            survival=survival,
            _token=_RESIDUAL_TOKEN,
        )
