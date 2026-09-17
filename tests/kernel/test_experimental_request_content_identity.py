"""G0.EX.1d: one canonical content identity for an experimental run request.

Every assertion here is about one boundary: the identity of "what was tried" is
derived from the request's complete canonical content, issued only by the
encoder, and never written by a caller. A field that no rule accounts for
breaks the import rather than dropping silently out of the identity.
"""

from dataclasses import fields

import pytest
from test_experimental import (  # type: ignore[import-not-found]
    candidate,
    case_set,
    request,
    vocabulary,
)

from alghanem.canonical_content import CANONICAL_HASH_ALGORITHM
from alghanem.kernel.experimental import (
    DeclaredCaseSet,
    ExperimentalAuthorityError,
    ExperimentalCandidateDeclaration,
    ExperimentalCaseOutcomeVocabulary,
    ExperimentalOperationRef,
    ExperimentalRunRequest,
)
from alghanem.kernel.experimental_request_content_identity import (
    CANDIDATE_DECLARATION_MANIFEST_COVERAGE,
    CASE_OUTCOME_VOCABULARY_MANIFEST_COVERAGE,
    CASE_SET_MANIFEST_COVERAGE,
    EXPERIMENTAL_REQUEST_IDENTITY_NAMED_LAWS,
    EXPERIMENTAL_REQUEST_MANIFEST_COVERAGE,
    CanonicalExperimentalRunRequestEncoder,
    ExperimentalRunRequestContentIdentity,
    case_set_content_digest,
    request_content_digest,
    require_content_digest,
)


def test_the_identity_is_derived_from_the_complete_request_content() -> None:
    identity = CanonicalExperimentalRunRequestEncoder.encode(request()).content_id

    assert type(identity) is ExperimentalRunRequestContentIdentity
    assert identity.algorithm == CANONICAL_HASH_ALGORITHM
    assert identity.canonicalization_version == (
        "experimental-run-request-manifest-v1"
    )
    assert (
        require_content_digest(identity.digest, "request content digest")
        == identity.digest
    )


def test_a_content_identity_cannot_be_written_by_a_caller() -> None:
    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunRequestContentIdentity(
            algorithm=CANONICAL_HASH_ALGORITHM,
            canonicalization_version="experimental-run-request-manifest-v1",
            digest="0" * 64,
        )


def test_two_content_equal_requests_share_one_identity() -> None:
    assert request_content_digest(request()) == request_content_digest(request())


def test_every_declared_field_changes_the_identity() -> None:
    base = request()
    variants = (
        ExperimentalRunRequest(
            candidate=candidate(candidate_id="other"),
            case_set=base.case_set,
            inputs=base.inputs,
            permitted_operations=base.permitted_operations,
            case_outcome_vocabulary=base.case_outcome_vocabulary,
        ),
        ExperimentalRunRequest(
            candidate=base.candidate,
            case_set=DeclaredCaseSet(case_set_id="other", case_ids=("c1", "c2", "c3")),
            inputs=base.inputs,
            permitted_operations=base.permitted_operations,
            case_outcome_vocabulary=base.case_outcome_vocabulary,
        ),
        ExperimentalRunRequest(
            candidate=base.candidate,
            case_set=base.case_set,
            inputs=tuple(
                (case_id, f"other:{case_id}") for case_id, _ in base.inputs
            ),
            permitted_operations=base.permitted_operations,
            case_outcome_vocabulary=base.case_outcome_vocabulary,
        ),
        ExperimentalRunRequest(
            candidate=base.candidate,
            case_set=base.case_set,
            inputs=base.inputs,
            permitted_operations=(ExperimentalOperationRef("apply"),),
            case_outcome_vocabulary=base.case_outcome_vocabulary,
        ),
        ExperimentalRunRequest(
            candidate=base.candidate,
            case_set=base.case_set,
            inputs=base.inputs,
            permitted_operations=base.permitted_operations,
            case_outcome_vocabulary=ExperimentalCaseOutcomeVocabulary(
                accounted_token="ACCOUNTED:other",
                unaccounted_token="UNACCOUNTED:other",
            ),
        ),
    )

    digests = {request_content_digest(base)}
    for variant in variants:
        digests.add(request_content_digest(variant))

    assert len(digests) == len(variants) + 1


def test_a_flat_encoding_collision_is_not_a_content_identity() -> None:
    def with_conditions(conditions: tuple[str, ...]) -> ExperimentalRunRequest:
        declaration = ExperimentalCandidateDeclaration(
            candidate_id="candidate",
            declared_origin_ref="origin",
            declared_scope="finite-domain",
            declared_conditions=conditions,
            declared_model_ref="model-a",
        )
        return ExperimentalRunRequest(
            candidate=declaration,
            case_set=case_set(("c1",)),
            inputs=(("c1", "input:c1"),),
            permitted_operations=(ExperimentalOperationRef("apply"),),
            case_outcome_vocabulary=vocabulary(),
        )

    assert request_content_digest(
        with_conditions(("a|b",))
    ) != request_content_digest(with_conditions(("a", "b")))
    assert case_set_content_digest(
        DeclaredCaseSet(case_set_id="s", case_ids=("a|b",))
    ) != case_set_content_digest(
        DeclaredCaseSet(case_set_id="s", case_ids=("a", "b"))
    )


def test_a_case_set_identity_reads_content_and_not_object_identity() -> None:
    assert case_set_content_digest(case_set()) == case_set_content_digest(case_set())
    assert case_set_content_digest(case_set()) != case_set_content_digest(
        case_set(("c1", "c2"))
    )


def test_coverage_accounts_for_every_field_of_every_encoded_type() -> None:
    dispositions = (
        (ExperimentalRunRequest, EXPERIMENTAL_REQUEST_MANIFEST_COVERAGE),
        (ExperimentalCandidateDeclaration, CANDIDATE_DECLARATION_MANIFEST_COVERAGE),
        (DeclaredCaseSet, CASE_SET_MANIFEST_COVERAGE),
        (ExperimentalCaseOutcomeVocabulary, CASE_OUTCOME_VOCABULARY_MANIFEST_COVERAGE),
    )

    for encoded_type, covered in dispositions:
        assert {item.name for item in fields(encoded_type)} == set(covered)


def test_only_a_request_can_be_encoded() -> None:
    class LooksLikeARequest:
        candidate = candidate()

    with pytest.raises(ExperimentalAuthorityError):
        CanonicalExperimentalRunRequestEncoder.encode(
            LooksLikeARequest()  # type: ignore[arg-type]
        )


def test_every_named_law_opens_with_its_own_name() -> None:
    assert EXPERIMENTAL_REQUEST_IDENTITY_NAMED_LAWS
    for name, text in EXPERIMENTAL_REQUEST_IDENTITY_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")
