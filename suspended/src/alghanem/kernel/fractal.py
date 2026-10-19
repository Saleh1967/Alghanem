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
has actually been born or frozen: `ConstructibleContract != IssuedByAuthority`,
equivalently `WellFormedFrozenFactorRef != AuthorityIssuedFrozenFactorRef`. No
code in this module (or elsewhere) may treat successful construction, or a
passing `isinstance` check, as proof that a genuine freeze occurred. A
future freeze/reopen authority -- analogous to
`EvidenceAcquisitionAuthority`'s sole-issuer pattern -- is a separate,
later milestone; only that authority may make an issued `FrozenFactorRef`
trustworthy.

This module deliberately does not define a `Layer` enum
(`NoTraditionalLayerEnum`): a domain is a `DiscoveryJurisdiction`, identified
by its own frozen experiment scope, never by a preset linguistic category.

Two structural integrity properties are enforced even at this
pre-authority, skeleton stage:

- `ExactFrozenReferencePreservation`: `FractalSnapshot` checks relation and
  bridge membership against the *exact* `FrozenFactorRef` value recorded in
  the snapshot (every declared field), never against a bare `factor_id`. A
  reference that shares a `factor_id` but differs in content id, domain,
  birth experiment, birth revision, or freeze certificate names a different,
  unrecognized occurrence and is rejected, not silently accepted.
- `ReopenComposesG0DoesNotForkG0`: `ReopenExperimentSpecification` embeds an
  ordinary, complete `BirthExperimentSpecification` rather than redeclaring
  its own question/residual/closure fields, so reopen semantics can never
  drift from G0 semantics. `DerivedRelationRef`-based provenance similarly
  binds a derived relation's `derivation_content_id`, not merely its
  `relation_id`, into `FractalProvenancePath` (`SameRelationId !=
  SameDerivationSemantics`).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .birth import (
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    _require_text,
    _require_text_tuple,
)


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
    endpoints exist and are frozen (`NoBridgeBeforeEndpointFreeze`). Its birth
    experiment must also differ from either endpoint's: parentage is proof
    lineage, never an ontological bridge.
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
        if any(
            endpoint.birth_experiment_id == self.birth_experiment_id
            for endpoint in self.endpoint_refs
        ):
            raise FractalContractError(
                "a bridge must be born in an experiment independent of its endpoints"
            )


FrozenOntologyRef = FrozenFactorRef | BornBridgeRef


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
    """A pre-evidence contract opening a new G0 question around frozen parents.

    `Reopen(F) != Rebirth(F)`: this contract never reconstructs, copies, or
    revalidates a parent's content; it only attaches a normal, complete
    `BirthExperimentSpecification` to a set of already-frozen parents.
    `E_{n+1} = Reopen(F_1, ..., F_k; Q_{n+1})`, never
    `BuildNewVersion(F_1, ..., F_k)`. Every declared parent is preserved
    verbatim (`PreservedParentIdentities`); nothing here can mutate an
    upstream frozen factor (`NoUpstreamIdentityMutation`).

    Reopen deliberately does **not** redeclare its own question, residual
    definition, or closure criterion: doing so would let reopen semantics
    drift from G0 semantics over time (`G0SemanticsDriftBetweenBirthAndReopen`).
    Instead, `experiment` embeds a complete, ordinary
    `BirthExperimentSpecification` unmodified, so a reopened experiment
    keeps G0's own revision identity, `EvidenceMode`, `ProjectionPoset`,
    `BirthQuery`, residual/closure identities, and derived prerequisite
    cone -- `ReopenComposesG0DoesNotForkG0`: reopen uses G0, it does not fork
    G0's experiment protocol into a second, parallel one.
    """

    reopen_id: str
    parents: tuple[FrozenOntologyRef, ...]
    experiment: BirthExperimentSpecification
    allowed_observables: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.reopen_id, "reopen id")
        _require_text_tuple(self.allowed_observables, "reopen allowed observables")
        if not isinstance(self.experiment, BirthExperimentSpecification):
            raise FractalContractError(
                "a reopen experiment must embed a frozen G0 "
                "BirthExperimentSpecification, not a parallel specification"
            )
        if len(self.parents) < 1:
            raise FractalContractError(
                "a reopen experiment requires at least one frozen parent reference"
            )
        if any(
            not isinstance(parent, FrozenFactorRef | BornBridgeRef)
            for parent in self.parents
        ):
            raise FractalContractError(
                "reopen parents must be frozen ontology references"
            )
        if len(set(self.parents)) != len(self.parents):
            raise FractalContractError(
                "reopen parents must not repeat the same exact frozen reference"
            )


@dataclass(frozen=True, slots=True)
class DerivedRelationRef:
    """A content-bound reference to an already-recorded `DerivedRelationSpec`.

    `SameRelationId != SameDerivationSemantics`: a bare `relation_id` string
    cannot distinguish two different derivations that happen to reuse the
    same id, exactly as `EvidenceOccurrenceIdentity != EvidenceContentIdentity`
    already separates label from content elsewhere in this kernel. Provenance
    that names a derived relation must therefore bind both the `relation_id`
    and the `derivation_content_id` it observed, so a later drift in the
    relation's own recorded content is detectable rather than silently
    trusted by id alone.
    """

    relation_id: str
    derivation_content_id: str

    def __post_init__(self) -> None:
        _require_text(self.relation_id, "derived relation ref id")
        _require_text(self.derivation_content_id, "derived relation ref content id")


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
    derived_relation_refs: tuple[DerivedRelationRef, ...]
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
        if any(
            not isinstance(ref, DerivedRelationRef)
            for ref in self.derived_relation_refs
        ):
            raise FractalContractError(
                "derived relation provenance must be content-bound derived "
                "relation references, not bare relation id strings"
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
class ProofLineageEdge:
    """A reopen/provenance edge, never an ontological relation.

    This records that a separately frozen child was discovered by reopening a
    frozen parent. It belongs exclusively to the provenance graph: neither
    endpoint is thereby a bridge endpoint and the edge cannot be used as a
    `BornBridgeRef` or `DerivedRelationSpec`.
    """

    parent_ref: FrozenOntologyRef
    child_ref: FrozenFactorRef
    reopen_specification: ReopenExperimentSpecification

    def __post_init__(self) -> None:
        if not isinstance(self.parent_ref, FrozenFactorRef | BornBridgeRef):
            raise FractalContractError(
                "proof lineage parents must be frozen ontology references"
            )
        if not isinstance(self.child_ref, FrozenFactorRef):
            raise FractalContractError(
                "proof lineage children must be frozen factor references"
            )
        if self.parent_ref == self.child_ref:
            raise FractalContractError(
                "proof lineage must connect distinct frozen factors"
            )
        if not isinstance(self.reopen_specification, ReopenExperimentSpecification):
            raise FractalContractError(
                "proof lineage must bind a reopen experiment specification"
            )
        experiment = self.reopen_specification.experiment
        if self.child_ref.birth_experiment_id != experiment.experiment_id:
            raise FractalContractError(
                "proof lineage child must be born by its recorded reopen experiment"
            )
        if self.parent_ref not in self.reopen_specification.parents:
            raise FractalContractError(
                "proof lineage parent must be declared by its reopen specification"
            )


def _ensure_acyclic(
    adjacency: dict[FrozenOntologyRef, set[FrozenOntologyRef]],
) -> None:
    """Reject cycles using explicit enter/exit markers instead of recursion."""
    visiting: set[FrozenOntologyRef] = set()
    visited: set[FrozenOntologyRef] = set()
    for node in adjacency:
        if node in visited:
            continue
        stack: list[tuple[FrozenOntologyRef, bool]] = [(node, False)]
        while stack:
            current, exiting = stack.pop()
            if exiting:
                visiting.remove(current)
                visited.add(current)
                continue
            if current in visited:
                continue
            if current in visiting:
                raise FractalContractError("proof lineage graph must be acyclic")
            visiting.add(current)
            stack.append((current, True))
            stack.extend(
                (child, False) for child in adjacency[current] if child not in visited
            )


@dataclass(frozen=True, slots=True)
class FractalSnapshot:
    """An audit-only snapshot of a discovery jurisdiction's fractal graph.

    `FractalGraph = ProvenanceGraph + BornOntologyGraph +
    DerivedRelationGraph`: the three are never conflated. Proof-lineage edges
    record reopen history only; frozen factors and born bridges form ontology;
    reconstructible relations form the derived graph. This snapshot contains no
    `ArabicRuleTable` or other compiled artifact; a rule table is a strictly
    later, derived projection (`RuleTableIsDerivedArtifact`).

    Membership of a relation's or bridge's referenced factor is checked
    against the *exact* frozen reference recorded in this snapshot -- every
    declared field, not merely `factor_id` -- so a reference that shares a
    `factor_id` but differs in `factor_content_id`, `domain`,
    `birth_experiment_id`, `birth_revision_id`, or `freeze_certificate_id` is
    rejected as an unrecognized, distinct occurrence
    (`ExactFrozenReferencePreservation`); `factor_id` equality alone is never
    sufficient.
    """

    frozen_factors: tuple[FrozenFactorRef, ...]
    derived_relations: tuple[DerivedRelationSpec, ...]
    born_bridges: tuple[BornBridgeRef, ...]
    proof_lineage_edges: tuple[ProofLineageEdge, ...] = ()
    _factor_ids: frozenset[str] = field(init=False, repr=False, compare=False)
    _frozen_refs: frozenset[FrozenFactorRef] = field(
        init=False, repr=False, compare=False
    )

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
        if any(
            not isinstance(edge, ProofLineageEdge) for edge in self.proof_lineage_edges
        ):
            raise FractalContractError(
                "fractal snapshot provenance must be proof lineage edges"
            )
        factor_ids = tuple(factor.factor_id for factor in self.frozen_factors)
        if len(set(factor_ids)) != len(factor_ids):
            raise FractalContractError(
                "fractal snapshot must not repeat the same frozen factor"
            )
        object.__setattr__(self, "_factor_ids", frozenset(factor_ids))
        object.__setattr__(self, "_frozen_refs", frozenset(self.frozen_factors))
        for relation in self.derived_relations:
            if any(
                source not in self._frozen_refs
                for source in relation.source_factor_refs
            ):
                raise FractalContractError(
                    "derived relation sources must be exact frozen references "
                    "already present in this snapshot, not merely matching factor ids"
                )
        for bridge in self.born_bridges:
            if any(
                endpoint not in self._frozen_refs for endpoint in bridge.endpoint_refs
            ):
                raise FractalContractError(
                    "bridge endpoints must be exact frozen references already "
                    "present in this snapshot, not merely matching factor ids"
                )
        reopen_specs: dict[str, ReopenExperimentSpecification] = {}
        born_bridge_refs = set(self.born_bridges)
        adjacency: dict[FrozenOntologyRef, set[FrozenOntologyRef]] = {
            factor: set() for factor in self.frozen_factors
        }
        adjacency.update({bridge: set() for bridge in self.born_bridges})
        for edge in self.proof_lineage_edges:
            if (
                edge.parent_ref not in self._frozen_refs
                and edge.parent_ref not in born_bridge_refs
            ) or edge.child_ref not in self._frozen_refs:
                raise FractalContractError(
                    "proof lineage endpoints must be exact frozen ontology "
                    "references already present in this snapshot"
                )
            if any(
                parent not in self._frozen_refs and parent not in born_bridge_refs
                for parent in edge.reopen_specification.parents
            ):
                raise FractalContractError(
                    "reopen specification parents must be exact frozen ontology "
                    "references already present in this snapshot"
                )
            reopen_id = edge.reopen_specification.reopen_id
            existing_specification = reopen_specs.setdefault(
                reopen_id, edge.reopen_specification
            )
            if existing_specification != edge.reopen_specification:
                raise FractalContractError(
                    "a reopen id must bind one exact experiment specification"
                )
            adjacency[edge.parent_ref].add(edge.child_ref)
        _ensure_acyclic(adjacency)
