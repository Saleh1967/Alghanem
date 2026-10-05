"""G0.IC.1d: evidence-derived residual survival outcome, for one witness.

G0.IC.1a derived comparability from the frozen poset and G0.IC.1c derived
weaker-model exhaustion from exactly-covered per-model certificates. Both said
the same thing about the conjunct they did not reach: a residual surviving
under `NoBirthWithoutResidualOrFormalNecessity` is certified by no authority in
this repository. This module is that reading, for one witness, and nothing
more.

Nothing new is invented. `ResidualDefinitionSpec` already declares the residual
whose survival is at stake, and its `supported_statuses` declares the closed
three-member vocabulary of a survival reading exactly as
`ClosureCriterionSpec.supported_statuses` declares `Close(W_i, R)`'s.
`ProvenanceBoundEvaluatorExecutionRecord` (G0.BA.1b) already proves
`EvaluatorExecutedOnEvidence`. The single missing step is the same one
G0.IC.1b closed for closure outcomes: nothing related an evaluator's
`output_content` -- a plain string -- to a member of that closed vocabulary.

`DeclaredResidualSurvivalVocabulary` is that relation, declared as data rather
than computed as a judgement: it must cover every `ResidualSurvivalStatus`
member exactly once, must not bind one token to two outcomes, and refuses a
token carrying surrounding whitespace because matching is exact.

The register -> seal -> gate shape is copied from G0.IC.1b, not invented:

* `ResidualSurvivalVocabularyRegistry.register` is the sole issuer of an
  `AuthorizedResidualSurvivalVocabulary` and requires a verified
  `BirthAssessmentContentBinding`, so the residual definition spoken for is
  content-frozen in a sealed semantics registry and not merely named.
* `ResidualSurvivalVocabularyRegistry.seal` alone produces a
  `SealedResidualSurvivalVocabularyRegistry`, which resolves only by the exact
  `(domain, residual_id)` scope.
* `ResidualSurvivalGate.assess` alone produces a
  `ResidualSurvivalCertificate`.

`CallerDoesNotOwnResidualSurvival`: `assess` accepts no status, no reason, and
no survival claim, and takes exactly two parameters. `ExactTokenOrRefusal`: the
output is matched by exact string equality, with no trimming, case folding,
prefix or substring match, nearest match, or default -- an unrecognized output
is refused by residual id and is never read as `DEFER`, because silently
reading ignorance as a declared outcome is precisely the failure this gate
exists to prevent. The gate also refuses a record executed under any role other
than `RESIDUAL_DEFINITION`, and a target that is not the request's own frozen
`residual_definition_id`.

Evidence-mode sensitivity, and the one mode refused by name.
`NoBirthWithoutResidualOrFormalNecessity` declares three modes with different
conditions, and `NoCrossSubstitution(D_emp, D_formal)` forbids either
compensating for the other. The gate reads `evidence_mode` from the request's
own frozen experiment, never from its caller, and the certificate carries it
for audit. `MIXED` is refused by name: that mode is an explicitly typed scoped
pair `<(D_emp, S_emp), (D_formal, S_formal)>`, and no authority here proves the
two declared scopes, nor that neither component compensated for the other. A
named refusal is safer than one certificate that a later reader could take as
having satisfied both modes (`MixedModeNeedsTwoScopedWitnesses`).

Claims this module explicitly does **not** make:

* `ResidualSurvivalOutcome != IndependentClosure`. Survival is one conjunct;
  comparability belongs to G0.IC.1a and exhaustion to G0.IC.1c. Composing the
  three is a separate, later question with no authority here, so
  `is_independent_closure` is `False` unconditionally,
  `IndependentClosureAssessment` is untouched, and this stage is deliberately
  wired to neither it nor `BirthVerdictGate`.
* `DoesNotSurvive != NO_BIRTH_IN_SCOPE`. A residual failing to survive is the
  shape of an argument against birth in this scope. It is not that verdict,
  which only `BirthVerdictGate` may issue.
* `SurvivalReadIsNotMeasuredReplicatedResidual`. In `EMPIRICAL` mode the
  constitution requires a *measured* residual that survives every licensed
  weaker projection *and* replicates in a second independent measurement run.
  Nothing here inspects the provenance genus of the evidence, and nothing here
  knows about a second run.
* `FormalNecessityIsNotProvedHere`. In `FORMAL` mode a declared outcome is
  read; no exhaustive proof over the declared closed domain is verified.
* `DeclaredVocabularyIsNotProvenSemantics`. Freezing the token-to-status map
  before the gate runs prevents a map tailored to an output already seen, and
  proves nothing about why the evaluator emitted that token.
* `SealedBeforeAssessmentIsNotSealedBeforeEvidence`. No authority in this
  repository timestamps a seal against an evidence acquisition run, so the
  vocabulary is proven frozen relative to the gate, not relative to the
  evidence.
* `OneWitnessIsNotResidualCertification`. G0.RC.1 remains deferred exactly as
  written: `ResidualCertificationCandidate` is untouched, and no freeze,
  reconstruction, or comparison authority is created here.

This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0`
mapping, and no `TraditionalName`.
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
    EvidenceMode,
    ResidualDefinitionSpec,
    ResidualSurvivalStatus,
    _require_text,
)
from .birth_content_identity import (
    BirthAssessmentContentBinding,
    BirthSemanticsContentIdentity,
)
from .evaluator_input_provenance import ProvenanceBoundEvaluatorExecutionRecord

_SURVIVAL_TOKEN = object()

_OUTCOME_REASONS: Mapping[ResidualSurvivalStatus, str] = MappingProxyType(
    {
        ResidualSurvivalStatus.SURVIVES: (
            "DeclaredSurvivesTokenRead: the evaluator's evidence-derived output "
            "is exactly a token the frozen residual definition declares as "
            "SURVIVES for this residual. This is one witness for one conjunct: "
            "it is not IndependentClosure, not a certified residual under "
            "G0.RC.1, and not a birth verdict"
        ),
        ResidualSurvivalStatus.DOES_NOT_SURVIVE: (
            "DeclaredDoesNotSurviveTokenRead: the evaluator's evidence-derived "
            "output is exactly a token the frozen residual definition declares "
            "as DOES_NOT_SURVIVE for this residual. A residual that does not "
            "survive is the shape of an argument against birth in this scope; "
            "it is not that verdict, which only BirthVerdictGate may issue"
        ),
        ResidualSurvivalStatus.DEFER: (
            "DeclaredDeferTokenRead: the evaluator's evidence-derived output is "
            "exactly a token the frozen residual definition declares as DEFER "
            "for this residual. A declared deferral is a read outcome, never "
            "the gate's own fallback for an output it failed to recognize"
        ),
    }
)


class ResidualSurvivalError(BirthExperimentSpecificationError):
    """A residual survival outcome was read outside its authority boundary."""


@dataclass(frozen=True, slots=True)
class DeclaredResidualSurvivalVocabulary:
    """A frozen map from literal evaluator output tokens to declared outcomes.

    This is data declared by the residual definition's owner, not a judgement.
    It must cover every member of `ResidualSurvivalStatus` exactly once, so
    that no declared outcome is unreachable and no member is silently dropped,
    and it must not bind one token to two outcomes.
    """

    residual_id: str
    domain: str
    tokens: tuple[tuple[str, ResidualSurvivalStatus], ...]

    def __post_init__(self) -> None:
        _require_text(self.residual_id, "residual survival vocabulary residual id")
        _require_text(self.domain, "residual survival vocabulary domain")
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
        """The frozen token-to-outcome map this vocabulary declares."""

        return MappingProxyType(dict(self.tokens))

    @property
    def declared_tokens(self) -> tuple[str, ...]:
        return tuple(token for token, _ in self.tokens)


@dataclass(frozen=True, slots=True)
class AuthorizedResidualSurvivalVocabulary:
    """Issuer-only authorization of one vocabulary for one frozen residual.

    The residual definition is taken from the verified content binding, never
    from the caller, so an authorization cannot speak for a residual whose
    content was never frozen in a sealed semantics registry. Holding one
    decides nothing: only `ResidualSurvivalGate` may read an evaluator output
    through it.
    """

    vocabulary_id: str
    vocabulary: DeclaredResidualSurvivalVocabulary
    binding: BirthAssessmentContentBinding
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _SURVIVAL_TOKEN:
            raise ResidualSurvivalError(
                "authorized residual survival vocabularies must be issued by "
                "ResidualSurvivalVocabularyRegistry"
            )
        _require_text(self.vocabulary_id, "residual survival vocabulary id")
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
    def residual_definition_content_id(self) -> BirthSemanticsContentIdentity:
        """The sealed-registry identity of the residual's canonical content."""

        return self.binding.residual_definition_content_id


class ResidualSurvivalVocabularyRegistry:
    """Authority that issues and seals outcome vocabularies; it reads nothing."""

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
        """Authorize exactly one outcome vocabulary for one frozen residual."""

        authorized = AuthorizedResidualSurvivalVocabulary(
            vocabulary_id=vocabulary_id,
            vocabulary=vocabulary,
            binding=binding,
            _token=_SURVIVAL_TOKEN,
        )
        key = (authorized.domain, authorized.residual_id)
        with self._lock:
            if vocabulary_id in self._issued_ids:
                raise ResidualSurvivalError(
                    "residual survival vocabulary id already issued by this registry"
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
        """Freeze the authorized outcome vocabularies."""

        _require_text(snapshot_id, "residual survival registry snapshot id")
        with self._lock:
            vocabularies = tuple(self._vocabularies.values())
        return SealedResidualSurvivalVocabularyRegistry(
            snapshot_id=snapshot_id,
            vocabularies=vocabularies,
            _token=_SURVIVAL_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedResidualSurvivalVocabularyRegistry:
    """Frozen vocabulary snapshot; it authorizes vocabularies but reads none."""

    snapshot_id: str
    vocabularies: tuple[AuthorizedResidualSurvivalVocabulary, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _SURVIVAL_TOKEN:
            raise ResidualSurvivalError(
                "sealed residual survival vocabulary registries must be issued "
                "by ResidualSurvivalVocabularyRegistry"
            )
        _require_text(self.snapshot_id, "residual survival registry snapshot id")
        if type(self.vocabularies) is not tuple or any(
            type(item) is not AuthorizedResidualSurvivalVocabulary
            for item in self.vocabularies
        ):
            raise ResidualSurvivalError(
                "sealed residual survival vocabulary registries require frozen "
                "authorized vocabularies"
            )
        seen: set[tuple[str, str]] = set()
        for authorized in self.vocabularies:
            key = (authorized.domain, authorized.residual_id)
            if key in seen:
                raise ResidualSurvivalError(
                    "sealed residual survival vocabulary registry must not "
                    "contain duplicate vocabularies"
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
    """The gate-issued survival outcome for exactly one residual witness.

    `status` is never caller-supplied: it is the outcome the frozen vocabulary
    declares for the exact token this record's evidence-derived execution
    produced. It speaks for one witness and for nothing else -- see
    `is_independent_closure`.
    """

    authorization: AuthorizedResidualSurvivalVocabulary
    record: ProvenanceBoundEvaluatorExecutionRecord
    residual_id: str
    matched_token: str
    status: ResidualSurvivalStatus
    reason: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _SURVIVAL_TOKEN:
            raise ResidualSurvivalError(
                "residual survival certificates must be issued by "
                "ResidualSurvivalGate"
            )
        if type(self.authorization) is not AuthorizedResidualSurvivalVocabulary:
            raise ResidualSurvivalError(
                "a survival certificate requires an authorized outcome vocabulary"
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
        """The authorized request whose evidence produced the read output."""

        return self.record.execution_record.request

    @property
    def specification(self) -> BirthExperimentSpecification:
        return self.request.specification

    @property
    def evidence_mode(self) -> EvidenceMode:
        """The mode declared by the frozen experiment, never by a caller."""

        return self.specification.evidence_mode

    @property
    def residual_definition(self) -> ResidualDefinitionSpec:
        """The frozen residual definition this reading speaks for."""

        return self.authorization.residual_definition

    @property
    def is_independent_closure(self) -> bool:
        """Always `False`: a survival reading is one conjunct, not closure.

        Closure additionally requires an exhausted licensed weaker model set
        (G0.IC.1c) and resolved comparability (G0.IC.1a), and composing the
        three conjuncts is a separate question with no authority here.
        """

        return False


class ResidualSurvivalGate:
    """The sole authority that may issue a `ResidualSurvivalCertificate`.

    The gate accepts no status, reason, or survival claim from its caller. It
    resolves the request's own frozen residual definition against a sealed
    vocabulary registry and matches the record's evidence-derived output
    against that vocabulary by exact string equality.
    """

    @staticmethod
    def assess(
        *,
        registry: SealedResidualSurvivalVocabularyRegistry,
        record: ProvenanceBoundEvaluatorExecutionRecord,
    ) -> ResidualSurvivalCertificate:
        """Read one residual's declared survival outcome from its record."""

        if type(registry) is not SealedResidualSurvivalVocabularyRegistry:
            raise ResidualSurvivalError(
                "survival outcome reading requires a sealed vocabulary registry"
            )
        if type(record) is not ProvenanceBoundEvaluatorExecutionRecord:
            raise ResidualSurvivalError(
                "survival outcome reading requires a provenance-bound execution "
                "record; an unbound record proves no evidence provenance"
            )
        if record.role is not BirthEvaluatorRole.RESIDUAL_DEFINITION:
            raise ResidualSurvivalError(
                "survival outcome reading requires a record executed under the "
                "RESIDUAL_DEFINITION role; no other role's output is a survival "
                "reading of the residual"
            )

        request = record.execution_record.request
        specification = request.specification
        if record.definition.domain != specification.domain:
            raise ResidualSurvivalError(
                "the executing evaluator's authorized domain does not match the "
                "request's own frozen experiment domain"
            )
        if specification.evidence_mode is EvidenceMode.MIXED:
            raise ResidualSurvivalError(
                "MixedModeNeedsTwoScopedWitnesses: a MIXED experiment declares "
                "an explicitly scoped pair of empirical and formal demands, and "
                "no authority here proves those scopes or that neither "
                "compensated for the other; one certificate is refused rather "
                "than read as satisfying both modes"
            )

        residual_id = record.target_id
        if residual_id != specification.residual_definition_id:
            raise ResidualSurvivalError(
                "the executed target is not this experiment's own frozen "
                "residual definition"
            )

        authorization = registry.resolve(
            domain=specification.domain,
            residual_id=specification.residual_definition_id,
        )
        if authorization.contract_specification != specification:
            raise ResidualSurvivalError(
                "the resolved outcome vocabulary is bound to a contract whose "
                "frozen experiment specification is not this request's own"
            )

        token = record.output_content
        declared = authorization.vocabulary.declared_outcomes
        if token not in declared:
            raise ResidualSurvivalError(
                "the executed output is not a token the frozen residual "
                "definition declares; an unrecognized output is refused, never "
                "read as a deferral or any other declared outcome"
            )
        status = declared[token]

        return ResidualSurvivalCertificate(
            authorization=authorization,
            record=record,
            residual_id=residual_id,
            matched_token=token,
            status=status,
            reason=_OUTCOME_REASONS[status],
            _token=_SURVIVAL_TOKEN,
        )
