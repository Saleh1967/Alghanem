"""Constitutional tests for canonical transition-content snapshots."""

from __future__ import annotations

from dataclasses import fields
from enum import IntEnum

import pytest

from alghanem.kernel import (
    Anchor,
    BranchOriginProvenance,
    CanonicalTransitionEncoder,
    Claim,
    Evidence,
    Operation,
    OperationResult,
    Residual,
    State,
    StructuralAdmissionGate,
    Trace,
    TransitionCandidate,
    TransitionContentIdentity,
    TransitionKind,
)
from alghanem.kernel.content_identity import (
    MANIFEST_COVERAGE,
    OCCURRENCE_ONLY_EXCLUSIONS,
)
from alghanem.kernel.transition import StructurallyAdmissibleTransition


def admitted(
    *,
    before_value: object = "before",
    after_value: object = "after",
    kind: TransitionKind = TransitionKind.IDENTITY_PRESERVATION_CLAIM,
) -> StructurallyAdmissibleTransition:
    source = Anchor("source", "domain")
    target = (
        Anchor("branch", "domain")
        if kind is TransitionKind.BRANCH_BIRTH_CLAIM
        else source
    )
    provenance = (
        BranchOriginProvenance(source, target, ("identity",))
        if kind is TransitionKind.BRANCH_BIRTH_CLAIM
        else None
    )
    candidate = TransitionCandidate(
        anchor=source,
        before_state=State(before_value),
        operation=Operation("transform", "component"),
        after_state=State(after_value),
        claim=Claim("claim", "statement"),
        evidence=(Evidence("claim", "basis"),),
        preserved=("identity",),
        changed=("component",),
        trace=Trace(("started", "finished")),
        residuals=(Residual("none"),),
        kind=kind,
        result=OperationResult(after_value),
        branch_origin_provenance=provenance,
        target_anchor=target,
    )
    return StructuralAdmissionGate.require_admitted(candidate)


def test_encoder_is_the_sole_content_identity_issuer() -> None:
    with pytest.raises(ValueError, match="issued by CanonicalTransitionEncoder"):
        TransitionContentIdentity("sha256", "transition-manifest-v1", "0" * 64)


def test_manifest_is_a_stable_snapshot_of_mutable_payloads() -> None:
    payload = {"items": [1, 2]}
    transition = admitted(before_value=payload)
    manifest = CanonicalTransitionEncoder.encode(transition)

    payload["items"].append(3)
    later_manifest = CanonicalTransitionEncoder.encode(transition)

    assert manifest.content_id != later_manifest.content_id
    assert manifest.canonical_bytes != later_manifest.canonical_bytes


def test_branch_provenance_is_part_of_canonical_content() -> None:
    identity = CanonicalTransitionEncoder.encode(admitted())
    branch = CanonicalTransitionEncoder.encode(
        admitted(kind=TransitionKind.BRANCH_BIRTH_CLAIM)
    )

    assert identity.content_id != branch.content_id


def test_list_and_tuple_are_not_canonically_equivalent() -> None:
    list_manifest = CanonicalTransitionEncoder.encode(admitted(before_value=[1, 2]))
    tuple_manifest = CanonicalTransitionEncoder.encode(admitted(before_value=(1, 2)))

    assert list_manifest.canonical_bytes != tuple_manifest.canonical_bytes


class CustomInt(int):
    pass


class Number(IntEnum):
    ONE = 1


@pytest.mark.parametrize("value", [CustomInt(1), Number.ONE, bytearray(b"x")])
def test_subclasses_and_unlicensed_value_types_are_rejected(value: object) -> None:
    with pytest.raises(TypeError, match="unsupported canonical value type"):
        CanonicalTransitionEncoder.encode(admitted(before_value=value))


def test_unicode_is_preserved_as_raw_codepoints() -> None:
    composed = CanonicalTransitionEncoder.encode(admitted(before_value="\u00e9"))
    decomposed = CanonicalTransitionEncoder.encode(admitted(before_value="e\u0301"))

    assert composed.canonical_bytes != decomposed.canonical_bytes


def test_float_encoding_distinguishes_binary64_signed_zero() -> None:
    positive_zero = CanonicalTransitionEncoder.encode(admitted(before_value=0.0))
    negative_zero = CanonicalTransitionEncoder.encode(admitted(before_value=-0.0))

    assert positive_zero.canonical_bytes != negative_zero.canonical_bytes


def test_every_admitted_transition_field_has_explicit_manifest_disposition() -> None:
    admitted_fields = {field.name for field in fields(StructurallyAdmissibleTransition)}

    assert admitted_fields == set(MANIFEST_COVERAGE) | set(OCCURRENCE_ONLY_EXCLUSIONS)
