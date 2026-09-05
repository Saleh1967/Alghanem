"""Tests for canonical transition content identity.

Covers the central law this module exists to establish:
``OccurrenceIdentity != ContentIdentity`` -- two admissions of the same
declared structural content share a ``TransitionContentIdentity`` even
though each gets its own distinct ``admission_id``.
"""

from __future__ import annotations

import pytest

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
    Claim,
    Evidence,
    Operation,
    OperationResult,
    Residual,
    State,
    StructuralAdmissionGate,
    StructurallyAdmissibleTransition,
    Trace,
    TransitionCandidate,
    TransitionKind,
)
from alghanem.kernel.content_identity import (
    CanonicalizationError,
    CanonicalTransitionEncoder,
    canonicalize,
)


def make_candidate(
    *,
    before_value: object = "before",
    after_value: object = "after",
    result_value: object = "result",
    preserved: tuple[str, ...] = ("identity", "form"),
    changed: tuple[str, ...] = ("component",),
    claim_id: str = "claim-1",
    statement: str = "supported",
    basis: str = "proof",
    trace_events: tuple[str, ...] = ("started", "finished"),
    residual_descriptions: tuple[str, ...] = ("remainder",),
    operation: Operation | None = None,
    anchor: Anchor | None = None,
    target_anchor: Anchor | None = None,
) -> TransitionCandidate:
    source_anchor = anchor or Anchor("a", "D")
    resolved_target_anchor = target_anchor or source_anchor
    resolved_claim = Claim(claim_id, statement)
    return TransitionCandidate(
        anchor=source_anchor,
        target_anchor=resolved_target_anchor,
        before_state=State(before_value),
        operation=operation or Operation("op", "component"),
        after_state=State(after_value),
        claim=resolved_claim,
        evidence=(Evidence(claim_id, basis),),
        preserved=preserved,
        changed=changed,
        trace=Trace(trace_events),
        residuals=tuple(Residual(description) for description in residual_descriptions),
        kind=TransitionKind.IDENTITY_PRESERVATION_CLAIM,
        result=OperationResult(result_value),
    )


def admit(candidate: TransitionCandidate) -> StructurallyAdmissibleTransition:
    return StructuralAdmissionGate.require_admitted(candidate)


def make_branch_candidate(
    anchor: Anchor,
    branch_target: Anchor,
    *,
    preserved: tuple[str, ...] = ("identity", "form"),
) -> TransitionCandidate:
    base = make_candidate(
        anchor=anchor, target_anchor=branch_target, preserved=preserved
    )
    return TransitionCandidate(
        anchor=base.anchor,
        target_anchor=branch_target,
        before_state=base.before_state,
        operation=base.operation,
        after_state=base.after_state,
        claim=base.claim,
        evidence=base.evidence,
        preserved=base.preserved,
        changed=base.changed,
        trace=base.trace,
        residuals=base.residuals,
        kind=TransitionKind.BRANCH_BIRTH_CLAIM,
        branch_origin_provenance=BranchOriginProvenance(
            origin_anchor=anchor,
            branch_anchor=branch_target,
            preserved_components=base.preserved,
        ),
        result=base.result,
    )


def test_same_content_different_occurrence_yields_same_content_id() -> None:
    t1 = admit(make_candidate())
    t2 = admit(make_candidate())

    assert t1.admission_id != t2.admission_id

    manifest1 = CanonicalTransitionEncoder.encode(t1)
    manifest2 = CanonicalTransitionEncoder.encode(t2)

    assert manifest1.content_id == manifest2.content_id
    assert manifest1.content_id.digest == manifest2.content_id.digest


@pytest.mark.parametrize(
    "field, first, second",
    [
        ("before_value", "before-a", "before-b"),
        ("after_value", "after-a", "after-b"),
        ("result_value", "result-a", "result-b"),
        ("claim_id", "claim-1", "claim-2"),
        ("statement", "supported", "different"),
        ("basis", "proof", "different-proof"),
        ("trace_events", ("started", "finished"), ("started", "finished", "more")),
        ("residual_descriptions", ("remainder",), ("other-remainder",)),
    ],
)
def test_changing_a_content_field_changes_content_id(
    field: str, first: object, second: object
) -> None:
    transition_a = admit(make_candidate(**{field: first}))
    transition_b = admit(make_candidate(**{field: second}))

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a != content_id_b


def test_changing_operation_changes_content_id() -> None:
    transition_a = admit(make_candidate(operation=Operation("op", "component")))
    transition_b = admit(
        make_candidate(operation=Operation("other-op", "component"))
    )

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a != content_id_b


def test_changing_anchor_changes_content_id() -> None:
    transition_a = admit(make_candidate(anchor=Anchor("a", "D")))
    transition_b = admit(make_candidate(anchor=Anchor("other", "D")))

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a != content_id_b


def test_changing_target_anchor_changes_content_id() -> None:
    anchor = Anchor("a", "D")
    branch_target_1 = Anchor("branch-1", "D")
    branch_target_2 = Anchor("branch-2", "D")

    transition_a = admit(make_branch_candidate(anchor, branch_target_1))
    transition_b = admit(make_branch_candidate(anchor, branch_target_2))

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a != content_id_b


def test_changing_kind_changes_content_id() -> None:
    anchor = Anchor("a", "D")
    branch_target = Anchor("b", "D")
    identity_candidate = make_candidate(anchor=anchor)
    branch_candidate = make_branch_candidate(anchor, branch_target)

    identity_transition = admit(identity_candidate)
    branch_transition = admit(branch_candidate)

    content_id_identity = CanonicalTransitionEncoder.encode(
        identity_transition
    ).content_id
    content_id_branch = CanonicalTransitionEncoder.encode(branch_transition).content_id

    assert content_id_identity != content_id_branch


def test_branch_origin_provenance_instance_identity_does_not_affect_content_id() -> (
    None
):
    """Locks in the module's stated redundancy assumption for branch birth.

    ``CanonicalTransitionManifest`` deliberately excludes
    ``branch_origin_provenance``. This is only safe because
    ``_validate_branch_birth`` already forces its ``origin_anchor``,
    ``branch_anchor``, and ``preserved_components`` to exactly equal the
    candidate's own ``anchor``, ``target_anchor``, and ``preserved`` --
    fields the manifest already covers directly. Two structurally
    equivalent branch-birth candidates built with distinct
    ``BranchOriginProvenance`` *instances* (same field values, different
    object identity) must therefore still produce the same content id.
    """

    anchor = Anchor("a", "D")
    branch_target = Anchor("b", "D")

    branch_candidate_1 = make_branch_candidate(anchor, branch_target)
    branch_candidate_2 = make_branch_candidate(anchor, branch_target)
    assert (
        branch_candidate_1.branch_origin_provenance
        is not branch_candidate_2.branch_origin_provenance
    )
    assert (
        branch_candidate_1.branch_origin_provenance
        == branch_candidate_2.branch_origin_provenance
    )

    transition_1 = admit(branch_candidate_1)
    transition_2 = admit(branch_candidate_2)

    assert (
        CanonicalTransitionEncoder.encode(transition_1).content_id
        == CanonicalTransitionEncoder.encode(transition_2).content_id
    )


def test_admission_id_alone_does_not_affect_content_id() -> None:
    candidate = make_candidate()
    transition_1 = admit(candidate)
    transition_2 = admit(candidate)

    assert transition_1.admission_id != transition_2.admission_id
    assert (
        CanonicalTransitionEncoder.encode(transition_1).content_id
        == CanonicalTransitionEncoder.encode(transition_2).content_id
    )


def test_projection_fingerprint_is_not_the_source_of_truth() -> None:
    transition_a = admit(make_candidate(before_value="before-a"))
    transition_b = admit(make_candidate(before_value="before-b"))

    # Two admitted transitions with a differing structural field must not
    # accidentally share a projection fingerprint, and the manifest must be
    # built from the transition's own fields, not derived from the old
    # partial fingerprint.
    assert (
        transition_a.transition_projection_fingerprint
        != transition_b.transition_projection_fingerprint
    )
    assert (
        CanonicalTransitionEncoder.encode(transition_a).content_id
        != CanonicalTransitionEncoder.encode(transition_b).content_id
    )


def test_mutating_payload_after_snapshot_does_not_change_manifest() -> None:
    mutable_before = {"x": [1, 2]}
    transition = admit(make_candidate(before_value=mutable_before))

    manifest = CanonicalTransitionEncoder.encode(transition)
    content_id_before_mutation = manifest.content_id

    mutable_before["x"].append(3)

    assert manifest.content_id == content_id_before_mutation
    assert (
        CanonicalTransitionEncoder.encode(transition).content_id
        != content_id_before_mutation
    )


class _WeirdWithStableRepr:
    """A payload whose ``repr()`` looks stable but is not canonicalizable.

    Used to assert ``StableRepr != CanonicalIdentity``: canonicalization
    must refuse this, never fall back to ``repr()``.
    """

    def __repr__(self) -> str:
        return "stable-looking-value"


def test_unsupported_payload_raises_canonicalization_error() -> None:
    transition = admit(make_candidate(before_value=_WeirdWithStableRepr()))

    with pytest.raises(CanonicalizationError):
        CanonicalTransitionEncoder.encode(transition)


def test_canonicalize_rejects_repr_fallback_directly() -> None:
    with pytest.raises(CanonicalizationError):
        canonicalize(_WeirdWithStableRepr())


@pytest.mark.parametrize("bad_float", [float("nan"), float("inf"), float("-inf")])
def test_canonicalize_rejects_non_finite_floats(bad_float: float) -> None:
    with pytest.raises(CanonicalizationError):
        canonicalize(bad_float)


def test_canonicalize_accepts_finite_float() -> None:
    assert canonicalize(1.5) == ("float", repr(1.5))


def test_canonicalize_rejects_non_string_mapping_keys() -> None:
    with pytest.raises(CanonicalizationError):
        canonicalize({1: "value"})


def test_dict_key_ordering_does_not_change_digest() -> None:
    transition_a = admit(make_candidate(before_value={"a": 1, "b": 2}))
    transition_b = admit(make_candidate(before_value={"b": 2, "a": 1}))

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a == content_id_b


def test_sequence_order_changes_digest() -> None:
    transition_a = admit(make_candidate(before_value=[1, 2]))
    transition_b = admit(make_candidate(before_value=[2, 1]))

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a != content_id_b


def test_preserved_and_changed_are_canonicalized_as_sorted_unique_sets() -> None:
    transition_a = admit(make_candidate(preserved=("identity", "form")))
    transition_b = admit(make_candidate(preserved=("form", "identity")))

    content_id_a = CanonicalTransitionEncoder.encode(transition_a).content_id
    content_id_b = CanonicalTransitionEncoder.encode(transition_b).content_id

    assert content_id_a == content_id_b


def test_transition_content_identity_requires_non_blank_fields() -> None:
    from alghanem.kernel.content_identity import TransitionContentIdentity

    with pytest.raises(ValueError):
        TransitionContentIdentity(
            algorithm="", canonicalization_version="v1", digest="abc"
        )
    with pytest.raises(ValueError):
        TransitionContentIdentity(
            algorithm="sha256", canonicalization_version="", digest="abc"
        )
    with pytest.raises(ValueError):
        TransitionContentIdentity(
            algorithm="sha256", canonicalization_version="v1", digest=""
        )


