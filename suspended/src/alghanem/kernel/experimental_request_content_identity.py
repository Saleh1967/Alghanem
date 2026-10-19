"""G0.EX.1d: canonical, pre-run identity for one experimental run request.

This module closes exactly one question: what does it mean for two experimental
run requests to be *the same request*? The answer is content, and only content:
one canonical byte encoding of every declared field, and one digest of those
bytes.

`OneContentIdentityLawForSameness`. Before this module the experimental path
answered that question twice, differently -- a contrast compared case sets by
Python object identity while a replay compared requests by dataclass equality --
so two requests could be the same for one authority and different for the other.
Sameness is now decided in exactly one place, by exactly one rule, for every
experimental authority that needs it.

The encoding is complete rather than summarised. Every field of the request,
including each case's input content in its declared order, contributes to the
digest, because a digest that omits what was fed to an implementation cannot
answer "what was actually tried?". `alghanem.canonical_content` is the single
canonicalization primitive of this repository and is reused unchanged here:
`Canonicalization != Authority`, so importing it transfers a byte encoding and
no permission whatsoever.

A coverage sweep runs at import over every experimental dataclass this module
encodes. A field added later that no coverage constant accounts for fails the
import rather than silently dropping out of the identity of the thing it was
added to.

This module issues an identity and nothing else. It confers no birth, no
validity, no evidence, and no permission to run: `SameRequest != GoodRequest`,
and binding a request to a frozen experiment is a separate authority's act.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields

from alghanem.canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_bytes,
    canonical_digest,
    is_canonical_digest,
)

from .experimental import (
    DeclaredCaseSet,
    ExperimentalAuthorityError,
    ExperimentalCandidateDeclaration,
    ExperimentalCaseOutcomeVocabulary,
    ExperimentalRunRequest,
    _require_text,
)

_REQUEST_CONTENT_TOKEN = object()
_ALGORITHM = CANONICAL_HASH_ALGORITHM
_CANONICALIZATION_VERSION = "experimental-run-request-manifest-v1"

EXPERIMENTAL_REQUEST_MANIFEST_COVERAGE = (
    "candidate",
    "case_set",
    "inputs",
    "permitted_operations",
    "case_outcome_vocabulary",
)
CANDIDATE_DECLARATION_MANIFEST_COVERAGE = (
    "candidate_id",
    "declared_origin_ref",
    "declared_scope",
    "declared_conditions",
    "declared_model_ref",
)
CASE_SET_MANIFEST_COVERAGE = ("case_set_id", "case_ids")
CASE_OUTCOME_VOCABULARY_MANIFEST_COVERAGE = ("accounted_token", "unaccounted_token")

EXPERIMENTAL_REQUEST_IDENTITY_NAMED_LAWS: dict[str, str] = {
    "OneContentIdentityLawForSameness": (
        "OneContentIdentityLawForSameness: two experimental artifacts are the "
        "same artifact when their canonical content digests are equal, and by "
        "no other rule. Object identity and ad-hoc structural comparison are "
        "not second answers to the same question"
    ),
    "AnIdentityIsNotAPermission": (
        "AnIdentityIsNotAPermission: this module encodes and digests, and "
        "decides nothing. A request having an identity does not make it bound "
        "to a frozen experiment, runnable, offerable, or evidence of anything"
    ),
    "NothingEncodedIsSummarised": (
        "NothingEncodedIsSummarised: every declared field of a request, "
        "including each case's own input content in declared order, is encoded "
        "structurally. A digest that dropped what was fed to an implementation "
        "could not answer what was actually tried"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


@dataclass(frozen=True, slots=True)
class ExperimentalRunRequestContentIdentity:
    """A digest reference to an encoder-issued canonical request manifest."""

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _REQUEST_CONTENT_TOKEN:
            raise ExperimentalAuthorityError(
                "experimental request content identities must be issued by "
                "CanonicalExperimentalRunRequestEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or not is_canonical_digest(self.digest)
        ):
            raise ExperimentalAuthorityError(
                "invalid experimental run request content identity"
            )

    @property
    def confers_binding(self) -> bool:
        """`AnIdentityIsNotAPermission`; structurally false."""

        return False


@dataclass(frozen=True, slots=True)
class CanonicalExperimentalRunRequestManifest:
    """The complete canonical content of one experimental run request."""

    canonical_bytes: bytes
    content_id: ExperimentalRunRequestContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _REQUEST_CONTENT_TOKEN:
            raise ExperimentalAuthorityError(
                "canonical experimental request manifests must be issued by "
                "CanonicalExperimentalRunRequestEncoder"
            )
        if canonical_digest(self.canonical_bytes) != self.content_id.digest:
            raise ExperimentalAuthorityError(
                "manifest bytes do not match its content digest"
            )


def encode_candidate(
    candidate: ExperimentalCandidateDeclaration,
) -> dict[str, object]:
    """The canonical encoding of one candidate declaration; structural, not joined."""

    if type(candidate) is not ExperimentalCandidateDeclaration:
        raise ExperimentalAuthorityError(
            "canonical encoding requires an experimental candidate declaration"
        )
    return {
        "candidate_id": candidate.candidate_id,
        "declared_conditions": list(candidate.declared_conditions),
        "declared_model_ref": candidate.declared_model_ref,
        "declared_origin_ref": candidate.declared_origin_ref,
        "declared_scope": candidate.declared_scope,
    }


def encode_case_set(case_set: DeclaredCaseSet) -> dict[str, object]:
    """The canonical encoding of one frozen case set."""

    if type(case_set) is not DeclaredCaseSet:
        raise ExperimentalAuthorityError(
            "canonical encoding requires a declared case set"
        )
    return {
        "case_ids": list(case_set.case_ids),
        "case_set_id": case_set.case_set_id,
    }


def encode_vocabulary(
    vocabulary: ExperimentalCaseOutcomeVocabulary,
) -> dict[str, object]:
    """The canonical encoding of one frozen per-case outcome vocabulary."""

    if type(vocabulary) is not ExperimentalCaseOutcomeVocabulary:
        raise ExperimentalAuthorityError(
            "canonical encoding requires a case outcome vocabulary"
        )
    return {
        "accounted_token": vocabulary.accounted_token,
        "unaccounted_token": vocabulary.unaccounted_token,
    }


def encode_request(request: ExperimentalRunRequest) -> dict[str, object]:
    """The canonical encoding of one run request, every field included."""

    if type(request) is not ExperimentalRunRequest:
        raise ExperimentalAuthorityError(
            "canonical encoding requires an experimental run request"
        )
    _assert_schema_coverage()
    return {
        "candidate": encode_candidate(request.candidate),
        "case_outcome_vocabulary": encode_vocabulary(request.case_outcome_vocabulary),
        "case_set": encode_case_set(request.case_set),
        "inputs": [[case_id, content] for case_id, content in request.inputs],
        "permitted_operations": [
            operation.identifier for operation in request.permitted_operations
        ],
        "version": _CANONICALIZATION_VERSION,
    }


class CanonicalExperimentalRunRequestEncoder:
    """The sole issuer of complete, canonical experimental request manifests."""

    @classmethod
    def encode(
        cls, request: ExperimentalRunRequest
    ) -> CanonicalExperimentalRunRequestManifest:
        encoded = encode_request(request)
        content_bytes = canonical_bytes(encoded)
        content_id = ExperimentalRunRequestContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=canonical_digest(content_bytes),
            _token=_REQUEST_CONTENT_TOKEN,
        )
        return CanonicalExperimentalRunRequestManifest(
            canonical_bytes=content_bytes,
            content_id=content_id,
            _token=_REQUEST_CONTENT_TOKEN,
        )


def case_set_content_digest(case_set: DeclaredCaseSet) -> str:
    """The one rule by which two frozen case sets are the same case set."""

    return canonical_digest(
        canonical_bytes(
            {
                "case_set": encode_case_set(case_set),
                "version": _CANONICALIZATION_VERSION,
            }
        )
    )


def request_content_digest(request: ExperimentalRunRequest) -> str:
    """The one rule by which two run requests are the same request."""

    return CanonicalExperimentalRunRequestEncoder.encode(request).content_id.digest


def require_content_digest(value: object, field_name: str) -> str:
    """Refuse anything that does not have the exact shape of a content digest."""

    _require_text(value, field_name)
    if not is_canonical_digest(value):
        raise ExperimentalAuthorityError(f"{field_name} must be a canonical digest")
    assert isinstance(value, str)
    return value


def _assert_schema_coverage() -> None:
    schema_dispositions = (
        (ExperimentalRunRequest, EXPERIMENTAL_REQUEST_MANIFEST_COVERAGE),
        (ExperimentalCandidateDeclaration, CANDIDATE_DECLARATION_MANIFEST_COVERAGE),
        (DeclaredCaseSet, CASE_SET_MANIFEST_COVERAGE),
        (
            ExperimentalCaseOutcomeVocabulary,
            CASE_OUTCOME_VOCABULARY_MANIFEST_COVERAGE,
        ),
    )
    for declared_type, covered in schema_dispositions:
        field_names = {item.name for item in fields(declared_type)}
        if field_names != set(covered):
            raise RuntimeError(
                "canonical experimental request manifest coverage must "
                f"explicitly account for every {declared_type.__name__} field"
            )


_assert_schema_coverage()
for _law_name, _law_text in EXPERIMENTAL_REQUEST_IDENTITY_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "CANDIDATE_DECLARATION_MANIFEST_COVERAGE",
    "CASE_OUTCOME_VOCABULARY_MANIFEST_COVERAGE",
    "CASE_SET_MANIFEST_COVERAGE",
    "CanonicalExperimentalRunRequestEncoder",
    "CanonicalExperimentalRunRequestManifest",
    "EXPERIMENTAL_REQUEST_IDENTITY_NAMED_LAWS",
    "EXPERIMENTAL_REQUEST_MANIFEST_COVERAGE",
    "ExperimentalRunRequestContentIdentity",
    "case_set_content_digest",
    "encode_candidate",
    "encode_case_set",
    "encode_request",
    "encode_vocabulary",
    "request_content_digest",
    "require_content_digest",
]
