"""G0.EX.1c: the one gate through which an experiment may offer evidence.

This module closes exactly one question: how may an observed experimental
result leave the third path? Through one gate, into one shape, and no further.

`ExperimentalResultIsNotConstitutionalEvidence`. A run record is a laboratory
fact. It becomes *assessable* only when `ExperimentalEvidenceGate.offer`
derives -- never accepts -- that it satisfies four admission conditions against
a genuine frozen pre-evidence experiment binding:

1. the run's declared scope equals the frozen experiment's own domain, so an
   experiment run for one question cannot be offered to another;
2. a replay observation covering this very record reports identical outputs and
   identical traces, so a result seen once is not offered as a finding;
3. the record carries its own authority-issued trace;
4. the offered payload is encoded canonically from the record itself, so no
   caller writes the content that will later be hashed.

A failed or aborted run may be offered. A failure is one of the observed facts
an experiment produces, and discarding it would leave the record of the
experiment better than the experiment was. The offer marks it
(`records_failure`), and `ExperimentalFailureIsNotNoBirth` continues to apply.

What the gate does **not** do is the point of the gate.
`OfferedExperimentalEvidence != AuthorizedEvidence != SufficientEvidence !=
Residual != Birth`. The gate issues no `AuthorizedEvidenceSnapshot` and imports
nothing from `evidence_acquisition`: it produces a payload string that must
still travel the full G0.2a.3 chain -- `EvidenceAcquisitionAuthority.authorize`
-> `EvidenceAcquisitionAuthorization.open_run` ->
`EvidenceAcquisitionRun.ingest` -- to become assessable at all. That preserves
`FrozenExperimentPrecedesAuthorizedEvidenceIngestion` unchanged: this module
adds a source of payloads, not a second door into the birth path.

The dependency direction is one-way and deliberate. `experimental` and
`experimental_comparison` import nothing from the birth, verdict, certificate,
or closure modules; this gate imports only the frozen-binding type; and no
existing kernel module imports any experimental type. An experimental reading
therefore cannot reach a verdict except by a caller carrying its payload,
openly, through the acquisition authority.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field

from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
)
from .experimental import (
    ExperimentalAuthorityError,
    ExperimentalRunRecord,
    _require_text,
    sweep_forbidden_fields,
)
from .experimental_comparison import (
    ModelContrastObservation,
    ReplayObservation,
)
from .trace import Trace

_OFFER_TOKEN = object()

EXPERIMENTAL_EVIDENCE_OFFER_VERSION = "experimental-evidence-offer-v1"

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
        "AnOfferIsScopedToOneFrozenExperiment: the run's declared scope must "
        "equal the frozen experiment's own domain, read from the binding and "
        "never supplied by the caller, so a result obtained for one question "
        "cannot be offered to another"
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
        "CallerDoesNotWriteTheOfferedPayload: the payload is encoded "
        "canonically from the record itself, so the content a later acquisition "
        "hashes is derived from what was observed rather than written by whoever "
        "wants it assessed"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


@dataclass(frozen=True, slots=True)
class ExperimentalEvidenceOffer:
    """Gate-issued offer of one observed experimental result, and nothing more.

    Constructible only by `ExperimentalEvidenceGate.offer`. Holding one grants
    no assessment, no snapshot, and no birth: it is a payload plus the reasons
    the gate accepted it.
    """

    offer_id: str
    record: ExperimentalRunRecord
    replay: ReplayObservation
    contrast: ModelContrastObservation | None
    binding: BirthExperimentSpecificationContentBinding
    payload: str
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _OFFER_TOKEN:
            raise ExperimentalAuthorityError(
                "experimental evidence offers must be issued by "
                "ExperimentalEvidenceGate"
            )
        _require_text(self.offer_id, "experimental evidence offer id")
        _require_text(self.payload, "experimental evidence payload")
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError(
                "an experimental evidence offer requires a trace"
            )

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


def encode_offer_payload(record: ExperimentalRunRecord) -> str:
    """Canonically encode one run record; the caller supplies no content."""

    if type(record) is not ExperimentalRunRecord:
        raise ExperimentalAuthorityError(
            "canonical offer encoding requires an authority-issued run record"
        )
    candidate = record.candidate
    lines = [
        f"version={EXPERIMENTAL_EVIDENCE_OFFER_VERSION}",
        f"run_id={record.run_id}",
        f"authority_id={record.issuing_authority_id}",
        f"candidate_id={candidate.candidate_id}",
        f"declared_origin_ref={candidate.declared_origin_ref}",
        f"declared_model_ref={candidate.declared_model_ref}",
        f"declared_scope={candidate.declared_scope}",
        f"declared_conditions={'|'.join(candidate.declared_conditions)}",
        f"case_set_id={record.case_set.case_set_id}",
        f"case_ids={'|'.join(record.case_set.case_ids)}",
        f"outcome_status={record.outcome_status.name}",
        f"observed_unexplained_cases={'|'.join(record.observed_unexplained_cases)}",
        f"operations_used={'|'.join(record.operations_used)}",
        f"output_content={record.output_content or ''}",
    ]
    failure = record.failure
    if failure is not None:
        lines.extend(
            (
                f"failure_kind={failure.failure_kind.name}",
                f"failure_case_id={failure.case_id}",
                f"failure_message={failure.message}",
            )
        )
    lines.extend(f"trace={event}" for event in record.trace.events)
    return "\n".join(lines)


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
        if type(binding) is not BirthExperimentSpecificationContentBinding:
            raise ExperimentalAuthorityError(
                "an offer requires a genuine frozen experiment content binding"
            )
        if contrast is not None and type(contrast) is not ModelContrastObservation:
            raise ExperimentalAuthorityError(
                "an offered contrast must be an authority-issued contrast observation"
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

        payload = encode_offer_payload(record)
        trace = Trace(
            (
                f"offer:{offer_id}",
                f"gate:{self._gate_id}",
                f"run:{record.run_id}",
                f"candidate:{record.candidate.candidate_id}",
                f"domain:{domain}",
                f"experiment:{binding.specification.experiment_id}"
                f"@{binding.specification.revision_id}",
                f"outcome:{record.outcome_status.name}",
                f"records_failure:{record.failure is not None}",
                f"replay:{replay.observation_id}",
                f"contrast:{contrast.observation_id if contrast else '-'}",
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
            binding=binding,
            payload=payload,
            trace=trace,
            _token=_OFFER_TOKEN,
        )


_GATE_SURFACE = frozenset({"gate_id", "offer"})


def _public_surface(owner: type) -> frozenset[str]:
    return frozenset(name for name in vars(owner) if not name.startswith("_"))


sweep_forbidden_fields(ExperimentalEvidenceOffer)

if _public_surface(ExperimentalEvidenceGate) != _GATE_SURFACE:
    raise RuntimeError(
        "ExperimentalEvidenceGate must expose no method beyond offering evidence"
    )
for _law_name, _law_text in EXPERIMENTAL_EVIDENCE_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "EXPERIMENTAL_EVIDENCE_NAMED_LAWS",
    "EXPERIMENTAL_EVIDENCE_OFFER_VERSION",
    "ExperimentalEvidenceGate",
    "ExperimentalEvidenceOffer",
    "encode_offer_payload",
]
