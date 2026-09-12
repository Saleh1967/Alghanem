"""G0.IC.1b: an evidence-derived local closure outcome for one weaker model.

This module closes the *first* of the two questions AIM-K3 names, and only
for a single weaker model at a time. It does not close `IndependentClosure`,
and it does not certify weaker-model exhaustion.

What was already available, and is reused rather than reinvented:

* `ClosureCriterionSpec.supported_statuses` already declares the closed
  three-member vocabulary of `Close(W_i, R)` -- `CLOSE`, `FAIL_TO_CLOSE`,
  `DEFER`. No new outcome vocabulary is invented here.
* `BirthExperimentSpecification.frozen_weaker_models` already *derives* the
  prerequisite cone from the frozen projection poset, so which models must be
  closed is fixed before any evidence exists.
* `ProvenanceBoundEvaluatorExecutionRecord` (G0.BA.1b) already proves
  `EvaluatorExecutedOnEvidence`: its executed input is exactly what a
  registry-owned derivation produced from this request's own authorized
  evidence snapshot.

The single missing step, and the whole of what this module adds: nothing
related an evaluator's `output_content` -- a plain string -- to a member of
that closed vocabulary. `DeclaredClosureOutcomeVocabulary` is that relation,
declared as data rather than computed as a judgement.

Why reading it is not inventing semantics:

* `CallerDoesNotOwnClosureOutcome`. `WeakerModelClosureGate.assess` accepts
  no status, no reason, and no outcome claim. It reads the output string of a
  provenance-bound record and the registry-resolved vocabulary, and nothing
  else.
* `ExactTokenOrRefusal`. The output is matched against the declared tokens by
  exact string equality. There is no trimming, no case folding, no prefix or
  substring match, no nearest match, and no default for an unrecognized
  output. An output outside the declared vocabulary is refused by model id,
  never mapped to `DEFER` as a convenience -- silently reading ignorance as a
  declared outcome is the precise failure this gate exists to prevent.
* `VocabularyIsBoundToFrozenCriterionContent`. A vocabulary is authorized only
  against a `BirthAssessmentContentBinding`, so the criterion it speaks for is
  content-frozen in a sealed semantics registry, not merely named. The gate
  further requires the resolved vocabulary's contract to carry this request's
  own frozen experiment specification.

Claims this module explicitly does **not** make:

* `LocalClosureOutcome != WeakerModelExhaustion`. A certificate speaks for
  exactly one model in the cone. Nothing here aggregates the cone, checks its
  coverage, or derives that the licensed weaker models were exhausted.
  `WeakerModelClosureCertificate.is_weaker_model_exhaustion` is `False`
  unconditionally.
* `WeakerModelClosure != IndependentClosure`. The other conjunct -- a residual
  that survived measurement or formal proof under
  `NoBirthWithoutResidualOrFormalNecessity` -- has no authority here, and the
  comparability conjunct belongs to G0.IC.1a. Accordingly
  `IndependentClosureAssessment.is_independent_closure` is untouched and
  remains `False`, and this module is deliberately not wired to it or to
  `BirthVerdictGate`. This stage issues no `BirthVerdict`, no
  `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`.
* `DeclaredVocabularyIsNotProvenSemantics`. Freezing the token-to-status map
  before the gate runs prevents a map tailored to an output already seen; it
  does not prove the evaluator emitted that token for a sound reason. What is
  read is *which declared outcome this output names*, never *whether that
  outcome is true of the world*.
* `SealedBeforeAssessmentIsNotSealedBeforeEvidence`. Sealing orders the
  vocabulary before every assessment that uses it, exactly as every other
  register -> seal -> gate authority in this kernel does. No authority in this
  repository timestamps a seal against an evidence acquisition run, so the
  vocabulary is proven frozen relative to the gate, not relative to the
  evidence.
* `DeclaredDerivationId != DerivationContentIdentity` is inherited unchanged
  from G0.BA.1b: the record proves its input came from this evidence through
  *the* callable registered under that name, not that the name describes the
  callable truthfully.
"""

from __future__ import annotations

import threading
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from .birth import (
    BirthAssessmentRequest,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    ClosureAssessmentStatus,
    ClosureCriterionSpec,
    _require_text,
)
from .birth_content_identity import (
    BirthAssessmentContentBinding,
    BirthSemanticsContentIdentity,
)
from .evaluator_input_provenance import ProvenanceBoundEvaluatorExecutionRecord

_VOCABULARY_TOKEN = object()

_OUTCOME_REASONS: Mapping[ClosureAssessmentStatus, str] = MappingProxyType(
    {
        ClosureAssessmentStatus.CLOSE: (
            "DeclaredCloseTokenRead: the evaluator's evidence-derived output is "
            "exactly a token the frozen closure criterion declares as CLOSE for "
            "this weaker model. This is a local outcome for one model only: it "
            "is not weaker-model exhaustion, not IndependentClosure, and not a "
            "birth verdict"
        ),
        ClosureAssessmentStatus.FAIL_TO_CLOSE: (
            "DeclaredFailToCloseTokenRead: the evaluator's evidence-derived "
            "output is exactly a token the frozen closure criterion declares as "
            "FAIL_TO_CLOSE for this weaker model. One model failing to close the "
            "residual is not the exhaustion of the licensed weaker model set, "
            "which no authority here certifies"
        ),
        ClosureAssessmentStatus.DEFER: (
            "DeclaredDeferTokenRead: the evaluator's evidence-derived output is "
            "exactly a token the frozen closure criterion declares as DEFER for "
            "this weaker model. A declared deferral is a read outcome, never the "
            "gate's own fallback for an output it failed to recognize"
        ),
    }
)


class WeakerModelClosureError(BirthExperimentSpecificationError):
    """A weaker-model closure outcome was read outside its authority boundary."""


@dataclass(frozen=True, slots=True)
class DeclaredClosureOutcomeVocabulary:
    """A frozen map from literal evaluator output tokens to declared outcomes.

    This is data declared by the closure criterion's owner, not a judgement.
    It must cover every member of `ClosureAssessmentStatus` exactly once, so
    that no declared outcome is unreachable and no member is silently dropped,
    and it must not bind one token to two outcomes.
    """

    criterion_id: str
    domain: str
    tokens: tuple[tuple[str, ClosureAssessmentStatus], ...]

    def __post_init__(self) -> None:
        _require_text(self.criterion_id, "closure vocabulary criterion id")
        _require_text(self.domain, "closure vocabulary domain")
        if type(self.tokens) is not tuple or not self.tokens:
            raise WeakerModelClosureError(
                "a closure outcome vocabulary requires frozen declared tokens"
            )
        seen_tokens: set[str] = set()
        seen_statuses: set[ClosureAssessmentStatus] = set()
        for entry in self.tokens:
            if type(entry) is not tuple or len(entry) != 2:
                raise WeakerModelClosureError(
                    "each declared outcome must be a token and a declared status"
                )
            token, status = entry
            if type(token) is not str or not token or token != token.strip():
                raise WeakerModelClosureError(
                    "a declared outcome token must be exact non-blank text with "
                    "no surrounding whitespace, because matching is exact"
                )
            if not isinstance(status, ClosureAssessmentStatus):
                raise WeakerModelClosureError(
                    "a declared outcome must name a member of the closed "
                    "ClosureAssessmentStatus vocabulary"
                )
            if token in seen_tokens:
                raise WeakerModelClosureError(
                    "a declared outcome token must not name two outcomes"
                )
            if status in seen_statuses:
                raise WeakerModelClosureError(
                    "a declared outcome status must be named by exactly one token"
                )
            seen_tokens.add(token)
            seen_statuses.add(status)
        if seen_statuses != set(ClosureAssessmentStatus):
            raise WeakerModelClosureError(
                "a closure outcome vocabulary must cover every member of "
                "ClosureAssessmentStatus, so that no declared outcome is "
                "unreachable by construction"
            )

    @property
    def declared_outcomes(self) -> Mapping[str, ClosureAssessmentStatus]:
        """The frozen token-to-outcome map this vocabulary declares."""

        return MappingProxyType(dict(self.tokens))

    @property
    def declared_tokens(self) -> tuple[str, ...]:
        return tuple(token for token, _ in self.tokens)


@dataclass(frozen=True, slots=True)
class AuthorizedClosureOutcomeVocabulary:
    """Issuer-only authorization of one vocabulary for one frozen criterion.

    The criterion is taken from the verified content binding, never from the
    caller, so an authorization cannot speak for a criterion whose content was
    never frozen in a sealed semantics registry. Holding one decides nothing:
    only `WeakerModelClosureGate` may read an evaluator output through it.
    """

    vocabulary_id: str
    vocabulary: DeclaredClosureOutcomeVocabulary
    binding: BirthAssessmentContentBinding
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _VOCABULARY_TOKEN:
            raise WeakerModelClosureError(
                "authorized closure outcome vocabularies must be issued by "
                "ClosureOutcomeVocabularyRegistry"
            )
        _require_text(self.vocabulary_id, "closure vocabulary id")
        if type(self.vocabulary) is not DeclaredClosureOutcomeVocabulary:
            raise WeakerModelClosureError(
                "an authorization requires a declared closure outcome vocabulary"
            )
        if type(self.binding) is not BirthAssessmentContentBinding:
            raise WeakerModelClosureError(
                "an authorization requires a verified birth assessment content "
                "binding, so that the criterion it speaks for is content-frozen"
            )
        if self.vocabulary.criterion_id != self.closure_criterion.criterion_id:
            raise WeakerModelClosureError(
                "a closure outcome vocabulary must name the bound contract's own "
                "frozen closure criterion"
            )
        if self.vocabulary.domain != self.specification.domain:
            raise WeakerModelClosureError(
                "a closure outcome vocabulary domain must match the bound "
                "contract's own frozen experiment domain"
            )

    @property
    def contract_specification(self) -> BirthExperimentSpecification:
        return self.binding.contract.specification

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.contract_specification

    @property
    def closure_criterion(self) -> ClosureCriterionSpec:
        return self.binding.contract.closure_criterion

    @property
    def criterion_id(self) -> str:
        return self.closure_criterion.criterion_id

    @property
    def domain(self) -> str:
        return self.specification.domain

    @property
    def criterion_content_id(self) -> BirthSemanticsContentIdentity:
        """The sealed-registry identity of the criterion's canonical content."""

        return self.binding.closure_criterion_content_id


class ClosureOutcomeVocabularyRegistry:
    """Authority that issues and seals outcome vocabularies; it reads nothing."""

    def __init__(self) -> None:
        self._vocabularies: dict[
            tuple[str, str], AuthorizedClosureOutcomeVocabulary
        ] = {}
        self._issued_ids: set[str] = set()
        self._lock = threading.Lock()

    def register(
        self,
        *,
        vocabulary_id: str,
        vocabulary: DeclaredClosureOutcomeVocabulary,
        binding: BirthAssessmentContentBinding,
    ) -> AuthorizedClosureOutcomeVocabulary:
        """Authorize exactly one outcome vocabulary for one frozen criterion."""

        authorized = AuthorizedClosureOutcomeVocabulary(
            vocabulary_id=vocabulary_id,
            vocabulary=vocabulary,
            binding=binding,
            _token=_VOCABULARY_TOKEN,
        )
        key = (authorized.domain, authorized.criterion_id)
        with self._lock:
            if vocabulary_id in self._issued_ids:
                raise WeakerModelClosureError(
                    "closure vocabulary id already issued by this registry"
                )
            if key in self._vocabularies:
                raise WeakerModelClosureError(
                    "a closure outcome vocabulary is already authorized for this "
                    "exact domain and closure criterion"
                )
            self._vocabularies[key] = authorized
            self._issued_ids.add(vocabulary_id)
        return authorized

    def seal(self, snapshot_id: str) -> SealedClosureOutcomeVocabularyRegistry:
        """Freeze the authorized outcome vocabularies."""

        _require_text(snapshot_id, "closure vocabulary registry snapshot id")
        with self._lock:
            vocabularies = tuple(self._vocabularies.values())
        return SealedClosureOutcomeVocabularyRegistry(
            snapshot_id=snapshot_id,
            vocabularies=vocabularies,
            _token=_VOCABULARY_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedClosureOutcomeVocabularyRegistry:
    """Frozen vocabulary snapshot; it authorizes vocabularies but reads none."""

    snapshot_id: str
    vocabularies: tuple[AuthorizedClosureOutcomeVocabulary, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _VOCABULARY_TOKEN:
            raise WeakerModelClosureError(
                "sealed closure vocabulary registries must be issued by "
                "ClosureOutcomeVocabularyRegistry"
            )
        _require_text(self.snapshot_id, "closure vocabulary registry snapshot id")
        if type(self.vocabularies) is not tuple or any(
            type(item) is not AuthorizedClosureOutcomeVocabulary
            for item in self.vocabularies
        ):
            raise WeakerModelClosureError(
                "sealed closure vocabulary registries require frozen "
                "authorized vocabularies"
            )
        seen: set[tuple[str, str]] = set()
        for authorized in self.vocabularies:
            key = (authorized.domain, authorized.criterion_id)
            if key in seen:
                raise WeakerModelClosureError(
                    "sealed closure vocabulary registry must not contain "
                    "duplicate vocabularies"
                )
            seen.add(key)

    def resolve(
        self, *, domain: str, criterion_id: str
    ) -> AuthorizedClosureOutcomeVocabulary:
        """Return the exact authorized vocabulary for this domain and criterion."""

        for authorized in self.vocabularies:
            if authorized.domain == domain and authorized.criterion_id == criterion_id:
                return authorized
        raise WeakerModelClosureError(
            "no closure outcome vocabulary is authorized for this exact domain "
            "and closure criterion"
        )


@dataclass(frozen=True, slots=True)
class WeakerModelClosureCertificate:
    """The gate-issued local closure outcome for exactly one weaker model.

    `status` is never caller-supplied: it is the outcome the frozen vocabulary
    declares for the exact token this record's evidence-derived execution
    produced. It speaks for one model in the cone and for nothing else -- see
    `is_weaker_model_exhaustion` and `is_independent_closure`.
    """

    authorization: AuthorizedClosureOutcomeVocabulary
    record: ProvenanceBoundEvaluatorExecutionRecord
    model_id: str
    matched_token: str
    status: ClosureAssessmentStatus
    reason: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _VOCABULARY_TOKEN:
            raise WeakerModelClosureError(
                "closure certificates must be issued by WeakerModelClosureGate"
            )
        if type(self.authorization) is not AuthorizedClosureOutcomeVocabulary:
            raise WeakerModelClosureError(
                "a closure certificate requires an authorized outcome vocabulary"
            )
        if type(self.record) is not ProvenanceBoundEvaluatorExecutionRecord:
            raise WeakerModelClosureError(
                "a closure certificate requires a provenance-bound execution "
                "record, so that the read output came from authorized evidence"
            )
        _require_text(self.model_id, "closure certificate model id")
        _require_text(self.matched_token, "closure certificate matched token")
        _require_text(self.reason, "closure certificate reason")
        if not isinstance(self.status, ClosureAssessmentStatus):
            raise WeakerModelClosureError(
                "a closure certificate requires a derived closure status"
            )
        declared = self.authorization.vocabulary.declared_outcomes
        if declared.get(self.matched_token) is not self.status:
            raise WeakerModelClosureError(
                "certificate status must be the outcome the frozen vocabulary "
                "declares for the matched token"
            )
        if self.matched_token != self.record.output_content:
            raise WeakerModelClosureError(
                "the matched token must be the record's own executed output"
            )
        if self.model_id != self.record.target_id:
            raise WeakerModelClosureError(
                "the certified model must be the record's own evaluator target"
            )

    @property
    def request(self) -> BirthAssessmentRequest:
        """The authorized request whose evidence produced the read output."""

        return self.record.execution_record.request

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def frozen_weaker_models(self) -> tuple[str, ...]:
        """The derived prerequisite cone this certificate covers one member of."""

        return self.specification.frozen_weaker_models

    @property
    def is_weaker_model_exhaustion(self) -> bool:
        """Always `False`: one model's outcome is not the cone's exhaustion.

        `NoBirthBeforeLicensedWeakerExhaustion` speaks about the whole licensed
        weaker model set. Nothing here aggregates certificates, checks that the
        cone is covered, or refuses a missing model, so no caller may read one
        certificate -- or any collection of them gathered by hand -- as
        exhaustion.
        """

        return False

    @property
    def is_independent_closure(self) -> bool:
        """Always `False`: a local outcome is not `IndependentClosure`.

        Closure additionally requires a residual that survived measurement or
        formal proof, an exhausted licensed weaker model set, and resolved
        comparability. This certificate supplies none of the three.
        """

        return False


class WeakerModelClosureGate:
    """The sole authority that may issue a `WeakerModelClosureCertificate`.

    The gate accepts no status, reason, or outcome claim from its caller. It
    resolves the request's own frozen closure criterion against a sealed
    vocabulary registry and matches the record's evidence-derived output
    against that vocabulary by exact string equality.
    """

    @staticmethod
    def assess(
        *,
        registry: SealedClosureOutcomeVocabularyRegistry,
        record: ProvenanceBoundEvaluatorExecutionRecord,
    ) -> WeakerModelClosureCertificate:
        """Read one weaker model's declared closure outcome from its record."""

        if type(registry) is not SealedClosureOutcomeVocabularyRegistry:
            raise WeakerModelClosureError(
                "closure outcome reading requires a sealed vocabulary registry"
            )
        if type(record) is not ProvenanceBoundEvaluatorExecutionRecord:
            raise WeakerModelClosureError(
                "closure outcome reading requires a provenance-bound execution "
                "record; an unbound record proves no evidence provenance"
            )
        if record.role is not BirthEvaluatorRole.WEAKER_MODEL:
            raise WeakerModelClosureError(
                "closure outcome reading requires a record executed under the "
                "WEAKER_MODEL role; no other role's output is a Close(W_i, R)"
            )

        request = record.execution_record.request
        specification = request.specification
        if record.definition.domain != specification.domain:
            raise WeakerModelClosureError(
                "the executing evaluator's authorized domain does not match the "
                "request's own frozen experiment domain"
            )

        model_id = record.target_id
        if model_id not in specification.frozen_weaker_models:
            raise WeakerModelClosureError(
                "the executed target is not a member of the derived frozen "
                "prerequisite cone of this experiment"
            )

        authorization = registry.resolve(
            domain=specification.domain,
            criterion_id=specification.closure_criterion_id,
        )
        if authorization.contract_specification != specification:
            raise WeakerModelClosureError(
                "the resolved outcome vocabulary is bound to a contract whose "
                "frozen experiment specification is not this request's own"
            )

        token = record.output_content
        declared = authorization.vocabulary.declared_outcomes
        if token not in declared:
            raise WeakerModelClosureError(
                "the executed output is not a token the frozen closure criterion "
                "declares; an unrecognized output is refused, never read as a "
                "deferral or any other declared outcome"
            )
        status = declared[token]

        return WeakerModelClosureCertificate(
            authorization=authorization,
            record=record,
            model_id=model_id,
            matched_token=token,
            status=status,
            reason=_OUTCOME_REASONS[status],
            _token=_VOCABULARY_TOKEN,
        )
