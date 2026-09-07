"""G0.F fractal reopen contracts: declared law only, no issuing authority yet.

Birth (G0.1/G0.2a) closes one experiment's evidence and factorization
question. This module closes the *next* question a factorization-first
kernel must answer: once a factor, derived relation, or bridge has been
frozen, how does a *later, higher* experiment refer to it without copying it,
mutating it, or silently re-deriving its identity?

The governing law is the recurrence declared in `docs/CONSTITUTION.md`'s
G0.F section:

    Birth -> Freeze -> Reopen -> Residual -> MinimalFactorization
    -> Freeze -> Reopen -> ...

`Reopen(F) != Rebirth(F)`: reopening a frozen factor in a later experiment
never reconstructs, revalidates, or reissues its identity
(`Id_after(F) == Id_before(F)`). A higher experiment holds only a reference
to a frozen factor (`HigherLayerOwnsReference != HigherLayerOwnsIdentity`);
it can never modify, rename, reinterpret, merge, or re-rank the referenced
factor -- it can only open a new relation *around* it.

None of the dataclasses in this module are issued by any authority yet,
because no `BirthGate`, `Freeze`, or `E0` runtime exists yet (see G0 and
G0.F in `docs/CONSTITUTION.md`). They are contract *skeletons*: their
constructors validate only internal well-formedness (non-blank fields,
non-empty parent tuples, and so on), exactly as `BirthExperimentSpecification`
and its G0.2a siblings do before any executable assessment runtime exists.
A caller can therefore construct a syntactically valid `FrozenFactorRef` by
hand today; that is deliberate and mirrors G0.1's `BirthExperimentSpecification`
before `PreEvidenceSpecificationRegistry` existed. It does not mean a factor
has actually been born or frozen: `ConstructibleContract != IssuedByAuthority`.
A future freeze/reopen authority -- analogous to
`EvidenceAcquisitionAuthority`'s sole-issuer pattern -- is a separate,
later milestone.

This module deliberately does not define a `Layer` enum
(`NoTraditionalLayerEnum`): a domain is a `DiscoveryJurisdiction`, identified
by its own frozen experiment scope, never by a preset linguistic category.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .birth import BirthExperimentSpecificationError, _require_text, _require_text_tuple


class FractalContractError(BirthExperimentSpecificationError):
    """A malformed fractal reopen contract cannot enter a future runtime."""


@dataclass(frozen=True, slots=True)
class FrozenFactorRef:
    """An opaque reference to an already-frozen factor, not a copy of it.

    `HigherLayerOwnsReference != HigherLayerOwnsIdentity`: holding this
    reference grants no authority to modify, rename, reinterpret, merge, or
    re-rank the referenced factor. It carries only enough to identify which
    frozen factor, from which birth experiment and revision, under which
    freeze certificate, is being reopened -- never the factor's own content.
    """

    factor_id: str
    factor_content_id: str
    freeze_certificate_id: str
    domain: str
    birth_experiment_id: str
    birth_revision_id: str

    def __post_init__(self) -> None:
        _require_text(self.factor_id, "factor id")
        _require_text(self.factor_content_id, "factor content id")
        _require_text(self.freeze_certificate_id, "freeze certificate id")
        _require_text(self.domain, "factor domain")
        _require_text(self.birth_experiment_id, "birth experiment id")
        _require_text(self.birth_revision_id, "birth revision id")


@dataclass(frozen=True, slots=True)
class BornBridgeRef:
    """An opaque reference to an already-frozen, independently born bridge.

    Distinct from `FrozenFactorRef`: a bridge's endpoints are themselves
    `FrozenFactorRef`s, so a bridge cannot be referenced before both of its
    endpoints exist and are frozen (`NoBridgeBeforeEndpointFreeze`).
    """

    bridge_id: str
    bridge_content_id: str
    freeze_certificate_id: str
    domain: str
    endpoint_refs: tuple[FrozenFactorRef, ...]
    birth_experiment_id: str
    birth_revision_id: str

    def __post_init__(self) -> None:
        _require_text(self.bridge_id, "bridge id")
        _require_text(self.bridge_content_id, "bridge content id")
        _require_text(self.freeze_certificate_id, "freeze certificate id")
        _require_text(self.domain, "bridge domain")
        _require_text(self.birth_experiment_id, "birth experiment id")
        _require_text(self.birth_revision_id, "birth revision id")
        if len(self.endpoint_refs) < 2:
            raise FractalContractError(
                "a bridge requires at least two frozen endpoint references"
            )
        if any(
            not isinstance(endpoint, FrozenFactorRef) for endpoint in self.endpoint_refs
        ):
            raise FractalContractError(
                "bridge endpoints must be frozen factor references"
            )
        if len({endpoint.factor_id for endpoint in self.endpoint_refs}) != len(
            self.endpoint_refs
        ):
            raise FractalContractError(
                "bridge endpoint references must not repeat the same factor"
            )


@dataclass(frozen=True, slots=True)
class DerivedRelationSpec:
    """A relation reconstructible from already-frozen factors: `DERIVED_NO_BIRTH`.

    `DerivedRelationDoesNotBirth`: this type exists precisely so the system
    can distinguish "this relation exists" from "this relation is primitive
    ontology." A `DerivedRelationSpec` never receives a freeze certificate or
    a `FrozenFactorRef`/`BornBridgeRef`-style identity of its own; it is
    recorded for audit, not promoted to an ontology object.
    """

    relation_id: str
    source_factor_refs: tuple[FrozenFactorRef, ...]
    derivation_spec_id: str
    derivation_content_id: str
    trace_id: str

    def __post_init__(self) -> None:
        _require_text(self.relation_id, "derived relation id")
        _require_text(self.derivation_spec_id, "derivation spec id")
        _require_text(self.derivation_content_id, "derivation content id")
        _require_text(self.trace_id, "derived relation trace id")
        if len(self.source_factor_refs) < 1:
            raise FractalContractError(
                "a derived relation requires at least one source factor reference"
            )
        if any(
            not isinstance(source, FrozenFactorRef)
            for source in self.source_factor_refs
        ):
            raise FractalContractError(
                "derived relation sources must be frozen factor references"
            )
        if len({source.factor_id for source in self.source_factor_refs}) != len(
            self.source_factor_refs
        ):
            raise FractalContractError(
                "derived relation sources must not repeat the same factor"
            )


@dataclass(frozen=True, slots=True)
class ReopenExperimentSpecification:
    """A pre-evidence contract opening a new question around frozen parents.

    `Reopen(F) != Rebirth(F)`: this contract never reconstructs, copies, or
    revalidates a parent's content; it only declares a new question about
    the parents as they already stand. `E_{n+1} = Reopen(F_1, ..., F_k;
    Q_{n+1})`, never `BuildNewVersion(F_1, ..., F_k)`. Every declared parent
    is preserved verbatim (`PreservedParentIdentities`); nothing here can
    mutate an upstream frozen factor (`NoUpstreamIdentityMutation`).
    """

    reopen_id: str
    parents: tuple[FrozenFactorRef, ...]
    new_question: str
    allowed_observables: tuple[str, ...]
    residual_definition_id: str
    residual_definition: str
    closure_criterion_id: str
    closure_criterion: str

    def __post_init__(self) -> None:
        _require_text(self.reopen_id, "reopen id")
        _require_text(self.new_question, "reopen new question")
        _require_text_tuple(self.allowed_observables, "reopen allowed observables")
        _require_text(self.residual_definition_id, "reopen residual definition id")
        _require_text(self.residual_definition, "reopen residual definition")
        _require_text(self.closure_criterion_id, "reopen closure criterion id")
        _require_text(self.closure_criterion, "reopen closure criterion")
        if len(self.parents) < 1:
            raise FractalContractError(
                "a reopen experiment requires at least one frozen parent reference"
            )
        if any(not isinstance(parent, FrozenFactorRef) for parent in self.parents):
            raise FractalContractError(
                "reopen parents must be frozen factor references"
            )
        if len({parent.factor_id for parent in self.parents}) != len(self.parents):
            raise FractalContractError(
                "reopen parents must not repeat the same frozen factor"
            )


@dataclass(frozen=True, slots=True)
class FractalProvenancePath:
    """A record of which prior factors, bridges, and experiments produced one result.

    `Parentage != Identity`: this path lets a later factor answer "which
    earlier factors was I reopened from," without any of those ancestors
    becoming part of this factor's own declared identity. Two factors with
    identical content but different provenance paths remain distinct
    occurrences in exactly the sense `EvidenceOccurrenceIdentity !=
    EvidenceContentIdentity` already separates elsewhere in this kernel.
    """

    factor_id: str
    reopened_factor_refs: tuple[FrozenFactorRef, ...]
    reopened_bridge_refs: tuple[BornBridgeRef, ...]
    derived_relation_ids: tuple[str, ...]
    reopen_experiment_id: str
    reopen_revision_id: str
    residual_id: str
    factorization_component_index: int | None = None

    def __post_init__(self) -> None:
        _require_text(self.factor_id, "provenance factor id")
        _require_text(self.reopen_experiment_id, "provenance reopen experiment id")
        _require_text(self.reopen_revision_id, "provenance reopen revision id")
        _require_text(self.residual_id, "provenance residual id")
        if any(
            not isinstance(ref, FrozenFactorRef) for ref in self.reopened_factor_refs
        ):
            raise FractalContractError(
                "reopened factor provenance must be frozen factor references"
            )
        if any(not isinstance(ref, BornBridgeRef) for ref in self.reopened_bridge_refs):
            raise FractalContractError(
                "reopened bridge provenance must be born bridge references"
            )
        _require_text_tuple(
            self.derived_relation_ids,
            "provenance derived relation ids",
            allow_empty=True,
        )
        if not self.reopened_factor_refs and not self.reopened_bridge_refs:
            raise FractalContractError(
                "a provenance path requires at least one reopened ancestor"
            )
        if self.factorization_component_index is not None and (
            not isinstance(self.factorization_component_index, int)
            or isinstance(self.factorization_component_index, bool)
            or self.factorization_component_index < 0
        ):
            raise FractalContractError(
                "factorization component index must be a non-negative integer"
            )


@dataclass(frozen=True, slots=True)
class FractalSnapshot:
    """An audit-only snapshot of a discovery jurisdiction's fractal graph.

    `FractalGraph = FrozenFactors + DerivedRelations + BornBridges`: the
    three are never conflated. This snapshot contains no `ArabicRuleTable`
    or other compiled artifact; a rule table is a strictly later, derived
    projection of a frozen snapshot like this one (`RuleTableIsDerivedArtifact`).
    """

    frozen_factors: tuple[FrozenFactorRef, ...]
    derived_relations: tuple[DerivedRelationSpec, ...]
    born_bridges: tuple[BornBridgeRef, ...]
    _factor_ids: frozenset[str] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if any(
            not isinstance(factor, FrozenFactorRef) for factor in self.frozen_factors
        ):
            raise FractalContractError(
                "fractal snapshot factors must be frozen factor references"
            )
        if any(
            not isinstance(relation, DerivedRelationSpec)
            for relation in self.derived_relations
        ):
            raise FractalContractError(
                "fractal snapshot derived relations must be derived relation specs"
            )
        if any(not isinstance(bridge, BornBridgeRef) for bridge in self.born_bridges):
            raise FractalContractError(
                "fractal snapshot bridges must be born bridge references"
            )
        factor_ids = tuple(factor.factor_id for factor in self.frozen_factors)
        if len(set(factor_ids)) != len(factor_ids):
            raise FractalContractError(
                "fractal snapshot must not repeat the same frozen factor"
            )
        object.__setattr__(self, "_factor_ids", frozenset(factor_ids))
        for relation in self.derived_relations:
            if any(
                source.factor_id not in self._factor_ids
                for source in relation.source_factor_refs
            ):
                raise FractalContractError(
                    "derived relation sources must be part of this snapshot"
                )
        for bridge in self.born_bridges:
            if any(
                endpoint.factor_id not in self._factor_ids
                for endpoint in bridge.endpoint_refs
            ):
                raise FractalContractError(
                    "bridge endpoints must be part of this snapshot"
                )
