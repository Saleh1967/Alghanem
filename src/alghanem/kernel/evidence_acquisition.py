"""G0.2a.3 evidence acquisition authority: a pre-evidence causal boundary.

This module closes a narrower, code-provable claim than "evidence was
acquired after the experiment was frozen in the world." It closes:

    FrozenExperimentPrecedesAuthorizedEvidenceIngestion

An `EvidenceAcquisitionAuthorization` can only be issued from a genuine,
already-verified `BirthExperimentSpecificationContentBinding`
(`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`). An
`EvidenceAcquisitionRun` can only be opened by that authorization, and an
`AuthorizedEvidenceSnapshot` can only be produced by that run's own
`ingest` boundary (`NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`).
No caller can construct any of these three objects directly, and no caller
supplies the evidence content identity: it is issued by
`CanonicalEvidenceContentEncoder` from the ingested payload itself.

This does not prove when evidence was first observed or produced outside
this process (`AuthorizedCapture != ProofOfExternalAcquisitionChronology`):
pre-existing evidence could still be ingested through an authorized run.
It also does not claim anything about evidence quality or outcome:
`AuthorizedEvidence != SufficientEvidence`, `AuthorizedEvidence` does not
imply `ResidualSurvival`, and it does not imply `Birth`.

G0.2a.3.1 closes `OccurrenceIssuanceIntegrity`: each issuer keeps its own
registry of the occurrence ids it has issued and rejects a repeat, so
`authorization_id`, `run_id`, and `snapshot_id` are injective within their
issuing scope (an authority's own authorizations, one authorization's own
runs, one run's own snapshots) rather than caller-chosen strings a caller
could repeat across distinct occurrences. Only within that enforced scope
does `EvidenceOccurrenceIdentity != EvidenceContentIdentity` hold without
qualification; two distinct `EvidenceAcquisitionAuthority` instances are
still separate issuance scopes and are not, by themselves, proof that their
respective ids never collide.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .birth import BirthExperimentSpecificationError, EvidenceMode, _require_text
from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    BirthExperimentSpecificationContentIdentity,
)

_EVIDENCE_ACQUISITION_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "evidence-content-manifest-v1"


class EvidenceAcquisitionAuthorityError(BirthExperimentSpecificationError):
    """Evidence acquisition or capture bypassed its authority boundary."""


@dataclass(frozen=True, slots=True)
class EvidenceContentIdentity:
    """A digest reference to encoder-issued canonical evidence content.

    This is `EvidenceContentIdentity`, distinct from the occurrence identity
    (`snapshot_id`, `run_id`, `authorization_id`) of the acquisition that
    produced it: two authorized ingestions of byte-identical content share
    this identity even though they are different occurrences.
    """

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EVIDENCE_ACQUISITION_TOKEN:
            raise EvidenceAcquisitionAuthorityError(
                "evidence content identities must be issued by "
                "CanonicalEvidenceContentEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise EvidenceAcquisitionAuthorityError("invalid evidence content identity")


@dataclass(frozen=True, slots=True)
class CanonicalEvidenceContentManifest:
    """The complete canonical content of one ingested evidence payload."""

    canonical_bytes: bytes
    content_id: EvidenceContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EVIDENCE_ACQUISITION_TOKEN:
            raise EvidenceAcquisitionAuthorityError(
                "canonical evidence manifests must be issued by "
                "CanonicalEvidenceContentEncoder"
            )
        if hashlib.sha256(self.canonical_bytes).hexdigest() != self.content_id.digest:
            raise EvidenceAcquisitionAuthorityError(
                "manifest bytes do not match its content digest"
            )


class CanonicalEvidenceContentEncoder:
    """The sole issuer of canonical evidence content manifests and identities."""

    @classmethod
    def encode(cls, payload: str) -> CanonicalEvidenceContentManifest:
        if type(payload) is not str:
            raise EvidenceAcquisitionAuthorityError(
                "canonical evidence encoding requires a text payload"
            )
        _require_text(payload, "evidence payload")
        canonical_bytes = payload.encode("utf-8", "surrogatepass")
        content_id = EvidenceContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=hashlib.sha256(canonical_bytes).hexdigest(),
            _token=_EVIDENCE_ACQUISITION_TOKEN,
        )
        return CanonicalEvidenceContentManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _token=_EVIDENCE_ACQUISITION_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class AuthorizedEvidenceSnapshot:
    """Issuer-only proof that content was ingested under one frozen run.

    `AuthorizedEvidence != SufficientEvidence`: this does not assert that the
    evidence is correct, sufficient, independent, or that any residual
    survives it. It asserts only that this exact content entered the
    assessment path under an authorization issued from one exact frozen
    experiment.
    """

    snapshot_id: str
    run_id: str
    authorization_id: str
    experiment_content_id: BirthExperimentSpecificationContentIdentity
    domain: str
    evidence_mode: EvidenceMode
    evidence_manifest: CanonicalEvidenceContentManifest
    trace: str
    content_id: EvidenceContentIdentity = field(init=False)
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EVIDENCE_ACQUISITION_TOKEN:
            raise EvidenceAcquisitionAuthorityError(
                "authorized evidence snapshots must be issued by an "
                "EvidenceAcquisitionRun"
            )
        _require_text(self.snapshot_id, "evidence snapshot id")
        _require_text(self.run_id, "evidence acquisition run id")
        _require_text(self.authorization_id, "evidence acquisition authorization id")
        if type(self.experiment_content_id) is not (
            BirthExperimentSpecificationContentIdentity
        ):
            raise EvidenceAcquisitionAuthorityError(
                "authorized evidence snapshot requires a frozen experiment "
                "content identity"
            )
        _require_text(self.domain, "evidence snapshot domain")
        if not isinstance(self.evidence_mode, EvidenceMode):
            raise EvidenceAcquisitionAuthorityError(
                "authorized evidence snapshot requires a declared evidence mode"
            )
        if type(self.evidence_manifest) is not CanonicalEvidenceContentManifest:
            raise EvidenceAcquisitionAuthorityError(
                "authorized evidence snapshot requires a canonical evidence "
                "content manifest"
            )
        _require_text(self.trace, "evidence snapshot trace")
        object.__setattr__(self, "content_id", self.evidence_manifest.content_id)


@dataclass(frozen=True, slots=True)
class EvidenceAcquisitionRun:
    """Issuer-only acquisition run; only it may produce an assessable snapshot."""

    run_id: str
    authorization_id: str
    experiment_content_id: BirthExperimentSpecificationContentIdentity
    domain: str
    evidence_mode: EvidenceMode
    _token: object | None = field(default=None, repr=False, compare=False)
    _issued_snapshot_ids: set[str] = field(
        default_factory=set, repr=False, compare=False, init=False
    )

    def __post_init__(self) -> None:
        if self._token is not _EVIDENCE_ACQUISITION_TOKEN:
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition runs must be issued by an "
                "EvidenceAcquisitionAuthorization"
            )
        _require_text(self.run_id, "evidence acquisition run id")
        _require_text(self.authorization_id, "evidence acquisition authorization id")
        if type(self.experiment_content_id) is not (
            BirthExperimentSpecificationContentIdentity
        ):
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition run requires a frozen experiment content "
                "identity"
            )
        _require_text(self.domain, "evidence acquisition run domain")
        if not isinstance(self.evidence_mode, EvidenceMode):
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition run requires a declared evidence mode"
            )

    def ingest(
        self, *, snapshot_id: str, payload: str, trace: str
    ) -> AuthorizedEvidenceSnapshot:
        """The sole path from a captured payload to an assessable snapshot."""

        _require_text(snapshot_id, "evidence snapshot id")
        if snapshot_id in self._issued_snapshot_ids:
            raise EvidenceAcquisitionAuthorityError(
                "evidence snapshot id already issued by this evidence "
                "acquisition run"
            )
        manifest = CanonicalEvidenceContentEncoder.encode(payload)
        snapshot = AuthorizedEvidenceSnapshot(
            snapshot_id=snapshot_id,
            run_id=self.run_id,
            authorization_id=self.authorization_id,
            experiment_content_id=self.experiment_content_id,
            domain=self.domain,
            evidence_mode=self.evidence_mode,
            evidence_manifest=manifest,
            trace=trace,
            _token=_EVIDENCE_ACQUISITION_TOKEN,
        )
        self._issued_snapshot_ids.add(snapshot_id)
        return snapshot


@dataclass(frozen=True, slots=True)
class EvidenceAcquisitionAuthorization:
    """Issuer-only authorization; conditions are derived, never caller-supplied.

    `experiment_content_id`, `domain`, `evidence_mode`, `evidence_requirements`,
    `revision_id`, and `revision_sequence` are all read from the verified
    `binding` rather than accepted as independent constructor arguments, so an
    authorization cannot assert conditions the frozen experiment never froze.
    """

    authorization_id: str
    binding: BirthExperimentSpecificationContentBinding
    _token: object | None = field(default=None, repr=False, compare=False)
    _issued_run_ids: set[str] = field(
        default_factory=set, repr=False, compare=False, init=False
    )

    def __post_init__(self) -> None:
        if self._token is not _EVIDENCE_ACQUISITION_TOKEN:
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition authorizations must be issued by "
                "EvidenceAcquisitionAuthority"
            )
        _require_text(self.authorization_id, "evidence acquisition authorization id")
        if type(self.binding) is not BirthExperimentSpecificationContentBinding:
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition authorization requires a genuine frozen "
                "experiment binding"
            )

    @property
    def experiment_content_id(self) -> BirthExperimentSpecificationContentIdentity:
        return self.binding.content_id

    @property
    def domain(self) -> str:
        return self.binding.specification.domain

    @property
    def evidence_mode(self) -> EvidenceMode:
        return self.binding.specification.evidence_mode

    @property
    def evidence_requirements(self) -> str:
        return self.binding.specification.evidence_requirements

    @property
    def revision_id(self) -> str:
        return self.binding.specification.revision_id

    @property
    def revision_sequence(self) -> int:
        return self.binding.specification.revision_sequence

    def open_run(self, run_id: str) -> EvidenceAcquisitionRun:
        """The sole path from an authorization to an acquisition run."""

        _require_text(run_id, "evidence acquisition run id")
        if run_id in self._issued_run_ids:
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition run id already issued by this "
                "authorization"
            )
        run = EvidenceAcquisitionRun(
            run_id=run_id,
            authorization_id=self.authorization_id,
            experiment_content_id=self.experiment_content_id,
            domain=self.domain,
            evidence_mode=self.evidence_mode,
            _token=_EVIDENCE_ACQUISITION_TOKEN,
        )
        self._issued_run_ids.add(run_id)
        return run


class EvidenceAcquisitionAuthority:
    """Separate authority boundary issuing evidence acquisition authorizations."""

    def __init__(self) -> None:
        self._issued_authorization_ids: set[str] = set()

    def authorize(
        self,
        *,
        authorization_id: str,
        binding: BirthExperimentSpecificationContentBinding,
    ) -> EvidenceAcquisitionAuthorization:
        """Authorize evidence acquisition only from a genuine frozen binding."""

        if type(binding) is not BirthExperimentSpecificationContentBinding:
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition authority requires a genuine frozen "
                "experiment binding"
            )
        _require_text(authorization_id, "evidence acquisition authorization id")
        if authorization_id in self._issued_authorization_ids:
            raise EvidenceAcquisitionAuthorityError(
                "evidence acquisition authorization id already issued by "
                "this authority"
            )
        authorization = EvidenceAcquisitionAuthorization(
            authorization_id=authorization_id,
            binding=binding,
            _token=_EVIDENCE_ACQUISITION_TOKEN,
        )
        self._issued_authorization_ids.add(authorization_id)
        return authorization


__all__ = [
    "AuthorizedEvidenceSnapshot",
    "CanonicalEvidenceContentEncoder",
    "CanonicalEvidenceContentManifest",
    "EvidenceAcquisitionAuthority",
    "EvidenceAcquisitionAuthorityError",
    "EvidenceAcquisitionAuthorization",
    "EvidenceAcquisitionRun",
    "EvidenceContentIdentity",
]
