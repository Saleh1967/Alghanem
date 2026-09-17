"""G0.EX.1c: the one gate through which an experiment may offer evidence.

This module closes exactly one question: how may an observed experimental
result leave the third path? Through one gate, into one canonical shape, and no
further.

`ExperimentalResultIsNotConstitutionalEvidence`. A run record is a laboratory
fact. It becomes *assessable* only when `ExperimentalEvidenceGate.offer`
derives -- never accepts -- that it satisfies every admission condition against
a genuine frozen pre-evidence experiment binding:

1. the record was produced from a bound request, and the binding offered here
   is the very frozen experiment that request was bound to, compared by content
   id: `SameDomainIsNotSameExperiment` and
   `SameExperimentNameIsNotSameFrozenContent`, so a record produced under one
   experiment cannot be offered against another that merely shares its domain
   or its name;
2. the record's own canonical request content digest equals the bound request's,
   so the offered run is the run that was bound;
3. the run's declared scope equals the frozen experiment's own domain, read from
   the binding and never supplied by a caller;
4. a replay observation covering this very record reports identical outputs,
   traces, and statuses, so a result seen once is not offered as a finding;
5. the record carries its own authority-issued trace;
6. the offered payload is the canonical manifest of everything observed, encoded
   by this gate from authority-issued artifacts, so no caller writes the content
   that a later acquisition will hash.

`CallerDoesNotWriteTheOfferedPayload` is enforced by structure rather than by
string concatenation. The manifest is built through
`alghanem.canonical_content` -- the repository's single canonicalization
primitive -- from a structured encoding in which every tuple is a list of its
own members. No separator character stands between two caller strings, so two
different observations cannot encode to one payload, and a coverage sweep at
import refuses any experimental field this manifest does not account for.

A failed or aborted run may be offered. A failure is one of the observed facts
an experiment produces, and discarding it would leave the record of the
experiment better than the experiment was. The offer marks it
(`records_failure`), and `ExperimentalFailureIsNotNoBirth` continues to apply.

What the gate does **not** do is the point of the gate.
`OfferedExperimentalEvidence != AuthorizedEvidence != SufficientEvidence !=
Residual != Birth`. The gate issues no `AuthorizedEvidenceSnapshot` and imports
nothing from `evidence_acquisition`: it produces a payload that must still
travel the full G0.2a.3 chain -- `EvidenceAcquisitionAuthority.authorize` ->
`EvidenceAcquisitionAuthorization.open_run` -> `EvidenceAcquisitionRun.ingest`
-- to become assessable at all. That preserves
`FrozenExperimentPrecedesAuthorizedEvidenceIngestion` unchanged: this module
adds a source of payloads, not a second door into the birth path.

The dependency direction is one-way and deliberate. `experimental` and
`experimental_comparison` import nothing from the birth, verdict, certificate,
or closure modules; this gate and the binding authority import only the
frozen-binding type; and no existing kernel module imports any experimental
type. An experimental reading therefore cannot reach a verdict except by a
caller carrying its payload, openly, through the acquisition authority.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field, fields

from alghanem.canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_bytes,
    canonical_digest,
)

from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
)
from .experimental import (
    ExperimentalAuthorityError,
    ExperimentalFailureRecord,
    ExperimentalRunRecord,
    _require_text,
    sweep_forbidden_fields,
)
from .experimental_comparison import (
    ModelContrastObservation,
    ReplayObservation,
)
from .experimental_request_content_identity import (
    encode_candidate,
    encode_case_set,
    encode_request,
    encode_vocabulary,
)
from .experimental_run_binding import BoundExperimentalRunRequest
from .trace import Trace

_OFFER_TOKEN = object()

EXPERIMENTAL_EVIDENCE_OFFER_VERSION = "experimental-evidence-manifest-v1"

RUN_RECORD_MANIFEST_COVERAGE = (
    "run_id",
    "issuing_authority_id",
    "request",
    "request_content_digest",
    "outcome_status",
    "output_content",
    "failure",
    "observed_unexplained_cases",
    "operations_used",
    "trace",
)
FAILURE_RECORD_MANIFEST_COVERAGE = ("failure_kind", "case_id", "message", "trace")
REPLAY_OBSERVATION_MANIFEST_COVERAGE = (
    "observation_id",
    "issuing_authority_id",
    "records",
    "outputs_identical",
    "traces_identical",
    "statuses_identical",
    "trace",
)
CONTRAST_OBSERVATION_MANIFEST_COVERAGE = (
    "observation_id",
    "issuing_authority_id",
    "record_a",
    "record_b",
    "status",
    "cases_unexplained_by_a",
    "cases_unexplained_by_b",
    "cases_closed_only_by_a",
    "cases_closed_only_by_b",
    "trace",
)
MANIFEST_TOKEN_EXCLUSIONS = ("_token",)

EXPERIMENTAL_EVIDENCE_NAMED_LAWS: dict[str, str] = {
    "ExperimentalResultIsNotConstitutionalEvidence": (
        "ExperimentalResultIsNotConstitutionalEvidence: an observed result "
        "leaves the experimental path only through this gate, and even then "
        "only as a payload that the G0.2a.3 acquisition chain must still "
        "ingest. The gate confers assessability, never sufficiency"
    ),
    "OfferedExperimentalEvidenceIsNotAuthorizedEvidence": (
        "OfferedExperimentalEvidenceIsNotAuthorizedEvidence: this gate issues "
        "no authorized evidence snapshot and imports no acquisition type. "
        "`Offer != AuthorizedEvidence != SufficientEvidence != Residual != "
        "Birth`"
    ),
    "AnOfferIsScopedToOneFrozenExperiment": (
        "AnOfferIsScopedToOneFrozenExperiment: an offer requires the bound "
        "request the record was produced from, and the offered binding must be "
        "the very frozen experiment that request was bound to, compared by "
        "content id. Equal domains and equal experiment ids are not equal "
        "experiments, and the run's declared scope must still equal the frozen "
        "experiment's own domain"
    ),
    "NoOfferWithoutAgreeingReplay": (
        "NoOfferWithoutAgreeingReplay: an offer requires a replay observation "
        "covering this very record whose outputs and traces agreed. A result "
        "seen exactly once is not offered as a finding, and agreement in this "
        "process is still not reproducibility"
    ),
    "AFailedRunIsStillOffered": (
        "AFailedRunIsStillOffered: a failed or aborted run may be offered and "
        "is marked as such. Dropping failures would make the record of the "
        "experiment better than the experiment, and a failure is still not a "
        "NO_BIRTH_IN_SCOPE verdict"
    ),
    "CallerDoesNotWriteTheOfferedPayload": (
        "CallerDoesNotWriteTheOfferedPayload: the payload is the canonical "
        "manifest of the record, its bound request, its replay and its "
        "contrast, encoded structurally through the repository's single "
        "canonicalization primitive. No separator stands between two caller "
        "strings, so two different observations cannot encode to one payload"
    ),
    "NothingObservedIsOmittedFromTheManifest": (
        "NothingObservedIsOmittedFromTheManifest: the manifest carries the "
        "request content identity, the candidate declaration, the case set, "
        "every case input, the permitted operations, the outcome vocabulary, "
        "the outputs or the failure, the trace, the replay reading, the "
        "contrast reading if any, and the frozen experiment's content id. A "
        "coverage sweep at import refuses any field it does not account for"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


@dataclass(frozen=True, slots=True)
class CanonicalExperimentalEvidenceManifest:
    """The complete canonical content of one offered experimental observation."""

    canonical_bytes: bytes
    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _OFFER_TOKEN:
            raise ExperimentalAuthorityError(
                "canonical experimental evidence manifests must be issued by "
                "CanonicalExperimentalEvidenceEncoder"
            )
        if canonical_digest(self.canonical_bytes) != self.digest:
            raise ExperimentalAuthorityError(
                "manifest bytes do not match its content digest"
            )

    @property
    def payload(self) -> str:
        """The canonical bytes as the text the acquisition chain will ingest."""

        return self.canonical_bytes.decode("utf-8", "surrogatepass")


@dataclass(frozen=True, slots=True)
class ExperimentalEvidenceOffer:
    """Gate-issued offer of one observed experimental result, and nothing more.

    Constructible only by `ExperimentalEvidenceGate.offer`. Holding one grants
    no assessment, no snapshot, and no birth: it is a canonical manifest plus
    the reasons the gate accepted it.
    """

    offer_id: str
    record: ExperimentalRunRecord
    replay: ReplayObservation
    contrast: ModelContrastObservation | None
    bound_request: BoundExperimentalRunRequest
    binding: BirthExperimentSpecificationContentBinding
    manifest: CanonicalExperimentalEvidenceManifest
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _OFFER_TOKEN:
            raise ExperimentalAuthorityError(
                "experimental evidence offers must be issued by "
                "ExperimentalEvidenceGate"
            )
        _require_text(self.offer_id, "experimental evidence offer id")
        if type(self.manifest) is not CanonicalExperimentalEvidenceManifest:
            raise ExperimentalAuthorityError(
                "an experimental evidence offer requires a canonical manifest"
            )
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError(
                "an experimental evidence offer requires a trace"
            )

    @property
    def payload(self) -> str:
        """The canonical payload the acquisition chain must still ingest."""

        return self.manifest.payload

    @property
    def manifest_digest(self) -> str:
        """The digest of exactly what is offered; derived, never given."""

        return self.manifest.digest

    @property
    def domain(self) -> str:
        """The frozen experiment's own domain; read from the binding."""

        return self.binding.specification.domain

    @property
    def records_failure(self) -> bool:
        """Whether the offered run failed or aborted; marked, never dropped."""

        return self.record.records_failure

    @property
    def confers_authorized_evidence(self) -> bool:
        """`Offer != AuthorizedEvidence`; structurally false."""

        return False

    @property
    def confers_sufficiency(self) -> bool:
        """`Offer != SufficientEvidence`; structurally false."""

        return False

    @property
    def confers_residual_certification(self) -> bool:
        """`Offer != Residual`; structurally false."""

        return False

    @property
    def confers_birth(self) -> bool:
        """`Offer != Birth`; structurally false."""

        return False


def _encode_failure(failure: ExperimentalFailureRecord) -> dict[str, object]:
    return {
        "case_id": failure.case_id,
        "failure_kind": failure.failure_kind.name,
        "message": failure.message,
        "trace": list(failure.trace.events),
    }


def _encode_record(record: ExperimentalRunRecord) -> dict[str, object]:
    failure = record.failure
    return {
        "candidate": encode_candidate(record.candidate),
        "case_outcome_vocabulary": encode_vocabulary(
            record.request.case_outcome_vocabulary
        ),
        "case_set": encode_case_set(record.case_set),
        "failure": None if failure is None else _encode_failure(failure),
        "inputs": [[case_id, content] for case_id, content in record.request.inputs],
        "issuing_authority_id": record.issuing_authority_id,
        "observed_unexplained_cases": list(record.observed_unexplained_cases),
        "operations_used": list(record.operations_used),
        "outcome_status": record.outcome_status.name,
        "output_content": record.output_content,
        "permitted_operations": [
            operation.identifier for operation in record.request.permitted_operations
        ],
        "request": encode_request(record.request),
        "request_content_digest": record.request_content_digest,
        "run_id": record.run_id,
        "trace": list(record.trace.events),
    }


def _encode_replay(replay: ReplayObservation) -> dict[str, object]:
    return {
        "issuing_authority_id": replay.issuing_authority_id,
        "observation_id": replay.observation_id,
        "outputs_identical": replay.outputs_identical,
        "run_ids": list(replay.run_ids),
        "statuses_identical": replay.statuses_identical,
        "trace": list(replay.trace.events),
        "traces_identical": replay.traces_identical,
    }


def _encode_contrast(contrast: ModelContrastObservation) -> dict[str, object]:
    return {
        "cases_closed_only_by_a": list(contrast.cases_closed_only_by_a),
        "cases_closed_only_by_b": list(contrast.cases_closed_only_by_b),
        "cases_unexplained_by_a": list(contrast.cases_unexplained_by_a),
        "cases_unexplained_by_b": list(contrast.cases_unexplained_by_b),
        "issuing_authority_id": contrast.issuing_authority_id,
        "model_ref_a": contrast.model_ref_a,
        "model_ref_b": contrast.model_ref_b,
        "observation_id": contrast.observation_id,
        "record_a_run_id": contrast.record_a.run_id,
        "record_b_run_id": contrast.record_b.run_id,
        "status": contrast.status.name,
        "trace": list(contrast.trace.events),
    }


class CanonicalExperimentalEvidenceEncoder:
    """The sole issuer of canonical experimental evidence manifests."""

    @classmethod
    def encode(
        cls,
        *,
        record: ExperimentalRunRecord,
        replay: ReplayObservation,
        bound_request: BoundExperimentalRunRequest,
        contrast: ModelContrastObservation | None = None,
    ) -> CanonicalExperimentalEvidenceManifest:
        """Canonically encode one observation; the caller supplies no content."""

        if type(record) is not ExperimentalRunRecord:
            raise ExperimentalAuthorityError(
                "canonical offer encoding requires an authority-issued run record"
            )
        if type(replay) is not ReplayObservation:
            raise ExperimentalAuthorityError(
                "canonical offer encoding requires an authority-issued replay"
            )
        if type(bound_request) is not BoundExperimentalRunRequest:
            raise ExperimentalAuthorityError(
                "canonical offer encoding requires an authority-issued bound request"
            )
        if contrast is not None and type(contrast) is not ModelContrastObservation:
            raise ExperimentalAuthorityError(
                "canonical offer encoding requires an authority-issued contrast"
            )
        _assert_schema_coverage()
        specification = bound_request.binding.specification
        experiment_content_id = bound_request.experiment_content_id
        encoded: dict[str, object] = {
            "binding": {
                "binding_id": bound_request.binding_id,
                "domain": bound_request.domain,
                "experiment_content_algorithm": experiment_content_id.algorithm,
                "experiment_content_digest": experiment_content_id.digest,
                "experiment_content_version": (
                    experiment_content_id.canonicalization_version
                ),
                "experiment_id": specification.experiment_id,
                "issuing_authority_id": bound_request.issuing_authority_id,
                "request_content_digest": bound_request.request_content_digest,
                "revision_id": specification.revision_id,
                "revision_sequence": specification.revision_sequence,
                "trace": list(bound_request.trace.events),
            },
            "contrast": None if contrast is None else _encode_contrast(contrast),
            "record": _encode_record(record),
            "replay": _encode_replay(replay),
            "version": EXPERIMENTAL_EVIDENCE_OFFER_VERSION,
        }
        content_bytes = canonical_bytes(encoded)
        return CanonicalExperimentalEvidenceManifest(
            canonical_bytes=content_bytes,
            algorithm=CANONICAL_HASH_ALGORITHM,
            canonicalization_version=EXPERIMENTAL_EVIDENCE_OFFER_VERSION,
            digest=canonical_digest(content_bytes),
            _token=_OFFER_TOKEN,
        )


class ExperimentalEvidenceGate:
    """The sole issuer of an `ExperimentalEvidenceOffer`; it ingests nothing.

    This class exposes `offer` and its own id, and no method that authorizes
    acquisition, produces a snapshot, certifies a birth, or admits an entity.
    """

    def __init__(self, *, gate_id: str) -> None:
        _require_text(gate_id, "experimental evidence gate id")
        self._gate_id = gate_id
        self._issued_offer_ids: set[str] = set()
        self._lock = threading.Lock()

    @property
    def gate_id(self) -> str:
        return self._gate_id

    def offer(
        self,
        *,
        offer_id: str,
        record: ExperimentalRunRecord,
        replay: ReplayObservation,
        bound_request: BoundExperimentalRunRequest,
        binding: BirthExperimentSpecificationContentBinding,
        contrast: ModelContrastObservation | None = None,
    ) -> ExperimentalEvidenceOffer:
        """Derive every admission condition, and offer only if all of them hold."""

        _require_text(offer_id, "experimental evidence offer id")
        if type(record) is not ExperimentalRunRecord:
            raise ExperimentalAuthorityError(
                "an offer requires an authority-issued experimental run record"
            )
        if type(replay) is not ReplayObservation:
            raise ExperimentalAuthorityError(
                "an offer requires an authority-issued replay observation"
            )
        if type(bound_request) is not BoundExperimentalRunRequest:
            raise ExperimentalAuthorityError(
                "an offer requires the authority-issued bound request the record "
                "was produced from"
            )
        if type(binding) is not BirthExperimentSpecificationContentBinding:
            raise ExperimentalAuthorityError(
                "an offer requires a genuine frozen experiment content binding"
            )
        if contrast is not None and type(contrast) is not ModelContrastObservation:
            raise ExperimentalAuthorityError(
                "an offered contrast must be an authority-issued contrast observation"
            )
        if bound_request.experiment_content_id != binding.content_id:
            raise ExperimentalAuthorityError(
                "the run was bound to a different frozen experiment than the one "
                "it is offered to: SameDomainIsNotSameExperiment"
            )
        if record.request_content_digest != bound_request.request_content_digest:
            raise ExperimentalAuthorityError(
                "the offered record was not produced from this bound request"
            )
        if not any(replayed is record for replayed in replay.records):
            raise ExperimentalAuthorityError(
                "the replay observation must cover this very run record"
            )
        if not (replay.outputs_identical and replay.traces_identical):
            raise ExperimentalAuthorityError(
                "an offer requires a replay whose outputs and traces agreed"
            )
        if not replay.statuses_identical:
            raise ExperimentalAuthorityError(
                "an offer requires a replay whose runs ended the same way"
            )
        if contrast is not None and not any(
            contrasted is record
            for contrasted in (contrast.record_a, contrast.record_b)
        ):
            raise ExperimentalAuthorityError(
                "an offered contrast must contrast this very run record"
            )
        domain = binding.specification.domain
        if record.request.declared_scope != domain:
            raise ExperimentalAuthorityError(
                "the run's declared scope must equal the frozen experiment's domain"
            )

        manifest = CanonicalExperimentalEvidenceEncoder.encode(
            record=record,
            replay=replay,
            bound_request=bound_request,
            contrast=contrast,
        )
        trace = Trace(
            (
                f"offer:{offer_id}",
                f"gate:{self._gate_id}",
                f"run:{record.run_id}",
                f"candidate:{record.candidate.candidate_id}",
                f"domain:{domain}",
                f"experiment:{binding.specification.experiment_id}"
                f"@{binding.specification.revision_id}",
                f"experiment_content:{binding.content_id.digest}",
                f"request_content:{record.request_content_digest}",
                f"binding:{bound_request.binding_id}",
                f"outcome:{record.outcome_status.name}",
                f"records_failure:{record.failure is not None}",
                f"replay:{replay.observation_id}",
                f"contrast:{contrast.observation_id if contrast else '-'}",
                f"manifest:{manifest.digest}",
                "reading:ExperimentalResultIsNotConstitutionalEvidence",
                "reading:OfferedExperimentalEvidenceIsNotAuthorizedEvidence",
            )
        )

        with self._lock:
            if offer_id in self._issued_offer_ids:
                raise ExperimentalAuthorityError(
                    "experimental evidence offer id already issued by this gate"
                )
            self._issued_offer_ids.add(offer_id)

        return ExperimentalEvidenceOffer(
            offer_id=offer_id,
            record=record,
            replay=replay,
            contrast=contrast,
            bound_request=bound_request,
            binding=binding,
            manifest=manifest,
            trace=trace,
            _token=_OFFER_TOKEN,
        )


_GATE_SURFACE = frozenset({"gate_id", "offer"})


def _public_surface(owner: type) -> frozenset[str]:
    return frozenset(name for name in vars(owner) if not name.startswith("_"))


def _assert_schema_coverage() -> None:
    schema_dispositions = (
        (ExperimentalRunRecord, RUN_RECORD_MANIFEST_COVERAGE),
        (ExperimentalFailureRecord, FAILURE_RECORD_MANIFEST_COVERAGE),
        (ReplayObservation, REPLAY_OBSERVATION_MANIFEST_COVERAGE),
        (ModelContrastObservation, CONTRAST_OBSERVATION_MANIFEST_COVERAGE),
    )
    for observed_type, covered in schema_dispositions:
        field_names = {item.name for item in fields(observed_type)}
        if field_names != set(covered) | set(MANIFEST_TOKEN_EXCLUSIONS):
            raise RuntimeError(
                "canonical experimental evidence manifest coverage must "
                f"explicitly account for every {observed_type.__name__} field"
            )


sweep_forbidden_fields(CanonicalExperimentalEvidenceManifest, ExperimentalEvidenceOffer)
_assert_schema_coverage()

if _public_surface(ExperimentalEvidenceGate) != _GATE_SURFACE:
    raise RuntimeError(
        "ExperimentalEvidenceGate must expose no method beyond offering evidence"
    )
for _law_name, _law_text in EXPERIMENTAL_EVIDENCE_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "CONTRAST_OBSERVATION_MANIFEST_COVERAGE",
    "EXPERIMENTAL_EVIDENCE_NAMED_LAWS",
    "EXPERIMENTAL_EVIDENCE_OFFER_VERSION",
    "FAILURE_RECORD_MANIFEST_COVERAGE",
    "MANIFEST_TOKEN_EXCLUSIONS",
    "REPLAY_OBSERVATION_MANIFEST_COVERAGE",
    "RUN_RECORD_MANIFEST_COVERAGE",
    "CanonicalExperimentalEvidenceEncoder",
    "CanonicalExperimentalEvidenceManifest",
    "ExperimentalEvidenceGate",
    "ExperimentalEvidenceOffer",
]
