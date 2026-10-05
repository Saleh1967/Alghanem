"""G0.EX.1b: contrasting two declared models, and replaying one, as observation.

This module closes exactly one question: what may be read from two experimental
runs rather than one? Two readings, and nothing else:

* a *contrast* between two declared models over one frozen case set, identical
  by canonical content digest --
  which cases each model did not account for, and whether one's unaccounted set
  is strictly contained in the other's;
* a *replay* of one declared candidate -- whether repeated runs produced
  identical outputs and identical traces.

`BetterExperimentalFitIsNotNecessity`. A model that accounts for cases another
left unaccounted has closed more of one declared case set. It has not shown that
a new genus is necessary, that the weaker model is insufficient in general, or
that anything should be born. The whole Instruction-only versus Rule-plus-
Instructions question is expressible here, but only as a contrast between two
opaque `declared_model_ref` strings: the kernel names no genus, so no result of
this module can say which genus won.

The direction that matters most is the negative one. If the model with fewer
declared parts accounts for every case, the contrast reports
`NO_DIFFERENCE_OBSERVED` or that the weaker model closes the strict superset,
and there is nothing for a richer candidate to be necessary *for*. That is the
reading this module exists to make cheap.

`ObservedDeterminismInThisProcess != Reproducibility`. A replay compares runs
performed in one process, in one interpreter, at one moment. Identical outputs
show that these runs agreed; they do not show that the candidate is
deterministic, portable, or reproducible elsewhere. `ReplayIsNotReplication`:
the independent second measurement run that
`SyntheticInterventionMayGenerateHypothesisOnly` requires is a measurement
question, not this one.

`OneContentIdentityLawForSameness`. Both authorities decide what counts as "the
same thing" by canonical content digest: a replay is repeated runs of one
request content identity, and a contrast is two distinct request content
identities read against one case set content identity. Python object identity
decides nothing here, so two separately constructed but content-equal freezes
are one freeze for both authorities rather than one for each.

`ThreeReadingsAreNotAFourth`, copied from G0.IC.1e: nothing is re-derived here.
Both authorities read only what `ExperimentalAuthority` already recorded, and
neither opens an implementation, a case input, or a frozen experiment.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum

from .experimental import (
    DeclaredCaseSet,
    ExperimentalAuthorityError,
    ExperimentalCandidateDeclaration,
    ExperimentalOutcomeStatus,
    ExperimentalRunRecord,
    _require_text,
    sweep_forbidden_fields,
)
from .experimental_request_content_identity import case_set_content_digest
from .trace import Trace

_CONTRAST_TOKEN = object()

EXPERIMENTAL_COMPARISON_NAMED_LAWS: dict[str, str] = {
    "BetterExperimentalFitIsNotNecessity": (
        "BetterExperimentalFitIsNotNecessity: one declared model accounting "
        "for cases another left unaccounted is an observation about two models "
        "on one declared case set. It is not a necessity proof, not a residual "
        "certification, and not a reason to birth anything"
    ),
    "OneCaseSetOrRefusal": (
        "OneCaseSetOrRefusal: two runs may be contrasted only if they were read "
        "against the same frozen case set, decided by canonical content digest. "
        "Runs over different case sets are refused, never reconciled, because a "
        "difference between two case sets would be read as a difference between "
        "two models"
    ),
    "OneContentIdentityLawForSameness": (
        "OneContentIdentityLawForSameness: both authorities decide sameness by "
        "canonical content digest and by no other rule. A replay is repeated "
        "runs of one request content identity, a contrast is two distinct "
        "request content identities over one case set content identity, and "
        "Python object identity decides neither"
    ),
    "ObservedDeterminismInThisProcessIsNotReproducibility": (
        "ObservedDeterminismInThisProcessIsNotReproducibility: a replay "
        "observes that runs of one request content identity, in this process, "
        "agreed. It does not establish determinism, portability, replication "
        "in an independent measurement run, or reproducibility of any kind"
    ),
    "AContrastReadsRecordsAndDerivesNothingElse": (
        "AContrastReadsRecordsAndDerivesNothingElse: both authorities read only "
        "authority-issued run records. Neither opens an implementation, a case "
        "input, or a frozen experiment, so no second authority can contradict "
        "the first over a question already answered"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


class ModelContrastStatus(Enum):
    """How two models' unaccounted case sets stand to each other. Observation only."""

    NO_DIFFERENCE_OBSERVED = "NO_DIFFERENCE_OBSERVED"
    A_CLOSES_STRICT_SUPERSET = "A_CLOSES_STRICT_SUPERSET"
    B_CLOSES_STRICT_SUPERSET = "B_CLOSES_STRICT_SUPERSET"
    INCOMPARABLE_DIFFERENCE = "INCOMPARABLE_DIFFERENCE"


@dataclass(frozen=True, slots=True)
class ModelContrastObservation:
    """Authority-issued contrast of two runs over one identical frozen case set.

    Every set-valued field is derived from the two records; none is accepted
    from a caller. Constructible only by `ExperimentalContrastAuthority.observe`.
    """

    observation_id: str
    issuing_authority_id: str
    record_a: ExperimentalRunRecord
    record_b: ExperimentalRunRecord
    status: ModelContrastStatus
    cases_unexplained_by_a: tuple[str, ...]
    cases_unexplained_by_b: tuple[str, ...]
    cases_closed_only_by_a: tuple[str, ...]
    cases_closed_only_by_b: tuple[str, ...]
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CONTRAST_TOKEN:
            raise ExperimentalAuthorityError(
                "model contrast observations must be issued by "
                "ExperimentalContrastAuthority"
            )
        _require_text(self.observation_id, "model contrast observation id")
        _require_text(self.issuing_authority_id, "experimental contrast authority id")
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError("a contrast observation requires a trace")

    @property
    def case_set(self) -> DeclaredCaseSet:
        return self.record_a.case_set

    @property
    def model_ref_a(self) -> str:
        return self.record_a.declared_model_ref

    @property
    def model_ref_b(self) -> str:
        return self.record_b.declared_model_ref

    @property
    def confers_necessity(self) -> bool:
        """`BetterExperimentalFitIsNotNecessity`; structurally false."""

        return False

    @property
    def confers_birth(self) -> bool:
        """A contrast births nothing; structurally false."""

        return False

    @property
    def confers_residual_certification(self) -> bool:
        """An unaccounted case is observed, never certified; structurally false."""

        return False


@dataclass(frozen=True, slots=True)
class ReplayObservation:
    """Authority-issued reading of repeated runs of one declared candidate.

    `outputs_identical` and `traces_identical` are derived comparisons over the
    records themselves, and say nothing beyond what happened in this process.
    """

    observation_id: str
    issuing_authority_id: str
    records: tuple[ExperimentalRunRecord, ...]
    outputs_identical: bool
    traces_identical: bool
    statuses_identical: bool
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CONTRAST_TOKEN:
            raise ExperimentalAuthorityError(
                "replay observations must be issued by ExperimentalReplayAuthority"
            )
        _require_text(self.observation_id, "replay observation id")
        _require_text(self.issuing_authority_id, "experimental replay authority id")
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError("a replay observation requires a trace")

    @property
    def candidate(self) -> ExperimentalCandidateDeclaration:
        return self.records[0].candidate

    @property
    def run_ids(self) -> tuple[str, ...]:
        return tuple(record.run_id for record in self.records)

    @property
    def proves_reproducibility(self) -> bool:
        """`ObservedDeterminismInThisProcess != Reproducibility`; structurally false."""

        return False

    @property
    def proves_independent_replication(self) -> bool:
        """`ReplayIsNotReplication`; structurally false."""

        return False


def _require_issued_record(record: object, role: str) -> ExperimentalRunRecord:
    if type(record) is not ExperimentalRunRecord:
        raise ExperimentalAuthorityError(
            f"{role} must be an authority-issued experimental run record"
        )
    return record


class ExperimentalContrastAuthority:
    """The sole issuer of a `ModelContrastObservation`; it runs nothing."""

    def __init__(self, *, authority_id: str) -> None:
        _require_text(authority_id, "experimental contrast authority id")
        self._authority_id = authority_id
        self._issued_observation_ids: set[str] = set()
        self._lock = threading.Lock()

    @property
    def authority_id(self) -> str:
        return self._authority_id

    def observe(
        self,
        *,
        observation_id: str,
        record_a: ExperimentalRunRecord,
        record_b: ExperimentalRunRecord,
    ) -> ModelContrastObservation:
        """Contrast two completed runs of two distinct models over one case set."""

        _require_text(observation_id, "model contrast observation id")
        first = _require_issued_record(record_a, "the first contrasted record")
        second = _require_issued_record(record_b, "the second contrasted record")
        if first is second:
            raise ExperimentalAuthorityError(
                "a record contrasted with itself observes no difference at all"
            )
        if case_set_content_digest(first.case_set) != case_set_content_digest(
            second.case_set
        ):
            raise ExperimentalAuthorityError(
                "contrasted runs must be read against the same frozen case set"
            )
        if first.request_content_digest == second.request_content_digest:
            raise ExperimentalAuthorityError(
                "two runs of one request content identity are a replay, not a "
                "contrast"
            )
        if first.declared_model_ref == second.declared_model_ref:
            raise ExperimentalAuthorityError(
                "contrasted runs must declare two distinct models"
            )
        for record in (first, second):
            if record.outcome_status is not ExperimentalOutcomeStatus.COMPLETED:
                raise ExperimentalAuthorityError(
                    "a run that did not complete has no per-case reading to contrast"
                )

        unexplained_a = tuple(first.observed_unexplained_cases)
        unexplained_b = tuple(second.observed_unexplained_cases)
        set_a = set(unexplained_a)
        set_b = set(unexplained_b)
        closed_only_by_b = tuple(
            case_id for case_id in unexplained_a if case_id not in set_b
        )
        closed_only_by_a = tuple(
            case_id for case_id in unexplained_b if case_id not in set_a
        )
        if set_a == set_b:
            status = ModelContrastStatus.NO_DIFFERENCE_OBSERVED
        elif set_b < set_a:
            status = ModelContrastStatus.B_CLOSES_STRICT_SUPERSET
        elif set_a < set_b:
            status = ModelContrastStatus.A_CLOSES_STRICT_SUPERSET
        else:
            status = ModelContrastStatus.INCOMPARABLE_DIFFERENCE

        trace = Trace(
            (
                f"observation:{observation_id}",
                f"authority:{self._authority_id}",
                f"case_set:{first.case_set.case_set_id}",
                f"model_a:{first.declared_model_ref}@{first.run_id}",
                f"model_b:{second.declared_model_ref}@{second.run_id}",
                f"unexplained_by_a:{','.join(unexplained_a) or '-'}",
                f"unexplained_by_b:{','.join(unexplained_b) or '-'}",
                f"status:{status.name}",
                "reading:BetterExperimentalFitIsNotNecessity",
            )
        )

        with self._lock:
            if observation_id in self._issued_observation_ids:
                raise ExperimentalAuthorityError(
                    "model contrast observation id already issued by this authority"
                )
            self._issued_observation_ids.add(observation_id)

        return ModelContrastObservation(
            observation_id=observation_id,
            issuing_authority_id=self._authority_id,
            record_a=first,
            record_b=second,
            status=status,
            cases_unexplained_by_a=unexplained_a,
            cases_unexplained_by_b=unexplained_b,
            cases_closed_only_by_a=closed_only_by_a,
            cases_closed_only_by_b=closed_only_by_b,
            trace=trace,
            _token=_CONTRAST_TOKEN,
        )


class ExperimentalReplayAuthority:
    """The sole issuer of a `ReplayObservation`; it runs nothing."""

    def __init__(self, *, authority_id: str) -> None:
        _require_text(authority_id, "experimental replay authority id")
        self._authority_id = authority_id
        self._issued_observation_ids: set[str] = set()
        self._lock = threading.Lock()

    @property
    def authority_id(self) -> str:
        return self._authority_id

    def observe(
        self,
        *,
        observation_id: str,
        records: tuple[ExperimentalRunRecord, ...],
    ) -> ReplayObservation:
        """Read whether repeated runs of one declared candidate agreed."""

        _require_text(observation_id, "replay observation id")
        if type(records) is not tuple or len(records) < 2:
            raise ExperimentalAuthorityError(
                "a replay requires at least two experimental run records"
            )
        for record in records:
            _require_issued_record(record, "each replayed record")
        first = records[0]
        for record in records[1:]:
            if record.request_content_digest != first.request_content_digest:
                raise ExperimentalAuthorityError(
                    "replayed runs must share one experimental run request "
                    "content identity"
                )
        run_ids = tuple(record.run_id for record in records)
        if len(set(run_ids)) != len(run_ids):
            raise ExperimentalAuthorityError(
                "one record read twice is not a replay: run ids must be distinct"
            )

        outputs_identical = all(
            record.output_content == first.output_content for record in records
        )
        traces_identical = all(
            _comparable_trace(record) == _comparable_trace(first) for record in records
        )
        statuses_identical = all(
            record.outcome_status is first.outcome_status for record in records
        )
        trace = Trace(
            (
                f"observation:{observation_id}",
                f"authority:{self._authority_id}",
                f"candidate:{first.candidate.candidate_id}",
                f"runs:{','.join(run_ids)}",
                f"outputs_identical:{outputs_identical}",
                f"traces_identical:{traces_identical}",
                f"statuses_identical:{statuses_identical}",
                "reading:ObservedDeterminismInThisProcessIsNotReproducibility",
            )
        )

        with self._lock:
            if observation_id in self._issued_observation_ids:
                raise ExperimentalAuthorityError(
                    "replay observation id already issued by this authority"
                )
            self._issued_observation_ids.add(observation_id)

        return ReplayObservation(
            observation_id=observation_id,
            issuing_authority_id=self._authority_id,
            records=records,
            outputs_identical=outputs_identical,
            traces_identical=traces_identical,
            statuses_identical=statuses_identical,
            trace=trace,
            _token=_CONTRAST_TOKEN,
        )


def _comparable_trace(record: ExperimentalRunRecord) -> tuple[str, ...]:
    """A run's trace with its own run id removed; run ids necessarily differ."""

    return tuple(
        event for event in record.trace.events if event != f"run:{record.run_id}"
    )


sweep_forbidden_fields(ModelContrastObservation, ReplayObservation)

for _law_name, _law_text in EXPERIMENTAL_COMPARISON_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "EXPERIMENTAL_COMPARISON_NAMED_LAWS",
    "ExperimentalContrastAuthority",
    "ExperimentalReplayAuthority",
    "ModelContrastObservation",
    "ModelContrastStatus",
    "ReplayObservation",
]
