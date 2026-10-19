"""Structural separation of synthetic from measured evidence provenance.

`docs/CONSTITUTION.md` already declares two laws about this boundary, but only
as prose: `CounterfactualResultIsNotObservation` and
`SyntheticInterventionMayGenerateHypothesisOnly`. Both are marked
`DECLARED_DEFERRED`, and a declared law is not an enforced one — nothing in
this package previously prevented an intervention result from being carried
alongside measured observations into whatever consumes them next. This module
closes exactly that gap for the two artifact kinds that already exist here,
and nothing wider:

    DeclaredProvenanceLabel != DerivedProvenanceGenus

The genus of a piece of evidence is never accepted from its holder. It is
derived by a gate from the artifact's own type: a `NormalizationAudit` that a
manifest binds to a measurement run is `MEASURED`, and a
`SurfaceInterventionAuditRow` is `SYNTHETIC`. There is no field on any type
here in which a caller may write a genus, so mislabeling is not refused after
the fact — it is unsayable.

`EvidenceProvenanceGenus` is deliberately two-valued with no `MIXED`. Evidence
of both provenances is a set of both, each classified on its own, never one
artifact wearing a blended label.

What this module deliberately does **not** contain, and why:

* No rank, no promotion, no freeze. A hypothesis becomes birth-eligible only
  after an independently measured contrast survives every licensed weaker
  projection *and* replicates in a second independent measurement run. Neither
  the weaker-projection assessment nor any freeze authority exists in this
  package, so `HypothesisResidual.is_birth_eligible` is structurally `False`
  and no method here can change it. Counting sources is not that test, and a
  rank ladder that ascends on a count would be exactly the caller-owned freeze
  authority the constitution refuses.
* No `FactorCandidate`. `SyntheticInterventionMayGenerateHypothesisOnly` says
  a synthetically discovered residual licenses a hypothesis and nothing more,
  so the only thing constructible from synthetic evidence here is a
  `HypothesisResidual`, which is checked at import to carry no candidate,
  verdict, birth, or rank field.

Authority-wise this module is inert: `EvidenceProvenanceClassification !=
BirthVerdict`, `HypothesisResidual != FactorCandidate`, and
`MeasuredContrastSet != CertifiedResidual`. There is no type in `kernel/`, no
`Freeze`, no `E0`, and no kernel gate reads any of it, which a test asserts by
scanning every `kernel/` module.

Naming note, recorded rather than silently avoided: this genus is *not*
`EvidenceGenus`. `alghanem.arabic.probe_preregistration.EvidenceGenus` already
names an unrelated distinction (`DISTRIBUTIONAL` vs `MORPHO_FUNCTIONAL`, the
kind of linguistic evidence). One name over two dimensions is the drift that
`alghanem.canonical_content` exists to make impossible; provenance therefore
carries its own name.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Final

from .intervention import SurfaceInterventionAuditRow
from .measurement import MeasurementRunIdentity
from .normalization import NormalizationAudit, ObservationLedgerManifest

_GATE_TOKEN = object()

_HYPOTHESIS_FORBIDDEN_FIELD_MARKERS: Final = (
    "candidate",
    "verdict",
    "birth",
    "rank",
    "frozen",
    "certified",
    "promotion",
)

COUNTERFACTUAL_IS_NOT_OBSERVATION_NOTE: Final = (
    "an intervention result is not an observation: its genus is derived from "
    "its own type and can never be admitted where measured evidence is required"
)

SYNTHETIC_LICENSES_HYPOTHESIS_ONLY_NOTE: Final = (
    "a synthetically discovered difference licenses a hypothesis and nothing "
    "more; it is not a factor candidate and cannot be promoted here"
)

BIRTH_ELIGIBILITY_DEFERRAL_NOTE: Final = (
    "birth eligibility needs a measured contrast surviving every licensed "
    "weaker projection and replicating in a second independent measurement "
    "run; no authority in this package assesses weaker projections, so no "
    "count of measured sources may stand in for that assessment"
)

PROVENANCE_AUTHORITY_NOTE: Final = (
    "classification only: this module issues no verdict, no freeze, and no "
    "promotion, and no kernel gate reads anything in it"
)


class EvidenceProvenanceError(ValueError):
    """A rejected provenance input; never coerced to the nearest genus."""


class EvidenceProvenanceGenus(Enum):
    """The closed provenance genus; two values, and deliberately no `MIXED`."""

    MEASURED = "measured"
    SYNTHETIC = "synthetic"


if len(EvidenceProvenanceGenus) != 2:  # pragma: no cover - guard
    raise RuntimeError("evidence provenance genus is deliberately two-valued")


@dataclass(frozen=True, slots=True)
class EvidenceProvenanceClassification:
    """A gate-derived genus for one artifact; not caller-constructible."""

    genus: EvidenceProvenanceGenus
    run_identity: MeasurementRunIdentity | None
    source_id: str
    occurrence_id: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _GATE_TOKEN:
            raise EvidenceProvenanceError(
                "a provenance classification is issued only by "
                "EvidenceProvenanceGate"
            )
        if not isinstance(self.genus, EvidenceProvenanceGenus):
            raise EvidenceProvenanceError("genus must come from the closed vocabulary")
        if self.genus is EvidenceProvenanceGenus.MEASURED and self.run_identity is None:
            raise EvidenceProvenanceError(
                "measured evidence must carry the measurement run it came from"
            )
        if (
            self.genus is EvidenceProvenanceGenus.SYNTHETIC
            and self.run_identity is not None
        ):
            raise EvidenceProvenanceError(
                "synthetic evidence carries no measurement run identity: the run "
                "it was derived from measured its source, never its result"
            )


class EvidenceProvenanceGate:
    """The sole issuer of a provenance genus, derived from artifact type."""

    @staticmethod
    def classify_measured(
        manifest: ObservationLedgerManifest, audit: NormalizationAudit
    ) -> EvidenceProvenanceClassification:
        """Classify one audit that the given manifest actually binds."""

        if not isinstance(manifest, ObservationLedgerManifest):
            raise EvidenceProvenanceError(
                "measured classification needs an observation ledger manifest"
            )
        if not isinstance(audit, NormalizationAudit):
            raise EvidenceProvenanceError(
                "measured classification needs a normalization audit"
            )
        if audit not in manifest.ledger.audits:
            raise EvidenceProvenanceError(
                "an audit outside the manifested ledger is not measured evidence "
                "of that run; membership is checked, not declared"
            )
        provenance = audit.trace.observation.provenance
        return EvidenceProvenanceClassification(
            genus=EvidenceProvenanceGenus.MEASURED,
            run_identity=provenance.run_identity,
            source_id=provenance.source_id,
            occurrence_id=provenance.occurrence_id,
            _token=_GATE_TOKEN,
        )

    @staticmethod
    def classify_synthetic(
        row: SurfaceInterventionAuditRow,
    ) -> EvidenceProvenanceClassification:
        """Classify one intervention result; its genus is never negotiable."""

        if not isinstance(row, SurfaceInterventionAuditRow):
            raise EvidenceProvenanceError(
                "synthetic classification needs a surface intervention audit row"
            )
        return EvidenceProvenanceClassification(
            genus=EvidenceProvenanceGenus.SYNTHETIC,
            run_identity=None,
            source_id=row.source_id,
            occurrence_id=row.occurrence_id,
            _token=_GATE_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class MeasuredContrastSet:
    """Measured classifications only; a synthetic one cannot enter."""

    classifications: tuple[EvidenceProvenanceClassification, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.classifications, tuple) or not self.classifications:
            raise EvidenceProvenanceError(
                "a measured contrast set declares at least one classification"
            )
        for classification in self.classifications:
            if type(classification) is not EvidenceProvenanceClassification:
                raise EvidenceProvenanceError(
                    "a contrast set holds gate-issued classifications only"
                )
            if classification.genus is not EvidenceProvenanceGenus.MEASURED:
                raise EvidenceProvenanceError(COUNTERFACTUAL_IS_NOT_OBSERVATION_NOTE)

    @property
    def distinct_measurement_runs(self) -> tuple[MeasurementRunIdentity, ...]:
        """The distinct runs present, in first-seen order; a count, not a proof."""

        seen: list[MeasurementRunIdentity] = []
        for classification in self.classifications:
            run_identity = classification.run_identity
            assert run_identity is not None
            if run_identity not in seen:
                seen.append(run_identity)
        return tuple(seen)


@dataclass(frozen=True, slots=True)
class HypothesisResidual:
    """All a synthetic difference licenses: a recorded hypothesis, no more."""

    hypothesis_id: str
    statement: str
    synthetic_evidence: tuple[EvidenceProvenanceClassification, ...]

    def __post_init__(self) -> None:
        for value, name in (
            (self.hypothesis_id, "hypothesis id"),
            (self.statement, "hypothesis statement"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise EvidenceProvenanceError(f"{name} must be non-blank text")
        if (
            not isinstance(self.synthetic_evidence, tuple)
            or not self.synthetic_evidence
        ):
            raise EvidenceProvenanceError(
                "a hypothesis residual declares the synthetic evidence it came from"
            )
        for classification in self.synthetic_evidence:
            if type(classification) is not EvidenceProvenanceClassification:
                raise EvidenceProvenanceError(
                    "a hypothesis residual holds gate-issued classifications only"
                )
            if classification.genus is not EvidenceProvenanceGenus.SYNTHETIC:
                raise EvidenceProvenanceError(
                    "measured evidence does not belong in a hypothesis residual: "
                    "a hypothesis records what only an intervention suggested"
                )

    @property
    def is_birth_eligible(self) -> bool:
        """`False` structurally at this stage; no method here can raise it."""

        return False


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


_assert_no_fields_matching(
    HypothesisResidual,
    _HYPOTHESIS_FORBIDDEN_FIELD_MARKERS,
    "a hypothesis residual may not carry a candidate, verdict, birth, or rank field",
)


__all__ = [
    "BIRTH_ELIGIBILITY_DEFERRAL_NOTE",
    "COUNTERFACTUAL_IS_NOT_OBSERVATION_NOTE",
    "EvidenceProvenanceClassification",
    "EvidenceProvenanceError",
    "EvidenceProvenanceGate",
    "EvidenceProvenanceGenus",
    "HypothesisResidual",
    "MeasuredContrastSet",
    "PROVENANCE_AUTHORITY_NOTE",
    "SYNTHETIC_LICENSES_HYPOTHESIS_ONLY_NOTE",
]
