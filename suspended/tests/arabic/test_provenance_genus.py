"""Tests for the synthetic/measured evidence provenance separation."""

from __future__ import annotations

import pkgutil

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    EvidenceProvenanceClassification,
    EvidenceProvenanceError,
    EvidenceProvenanceGate,
    EvidenceProvenanceGenus,
    HypothesisResidual,
    MeasuredContrastSet,
    MeasurementProtocolSpec,
    MeasurementRunIdentity,
    ObservationProvenance,
    RawSurfaceObservation,
    SurfaceAtomIntervention,
    SurfaceAtomInterventionAudit,
    SurfaceInterventionAuditRow,
    SurfaceNormalization,
)
from alghanem.arabic.encoding.normalization import ObservationLedgerManifest


def measurement_run(run_id: str = "run-1") -> MeasurementRunIdentity:
    return MeasurementRunIdentity(
        MeasurementProtocolSpec(
            protocol_id="surface-measurement",
            protocol_version="1",
            source_scope="test-source",
            normalization_policy="NFC",
            occurrence_scheme="caller-issued-sequence",
        ),
        run_id,
    )


def observation(
    source_id: str,
    occurrence_id: str,
    surface: str,
    run_identity: MeasurementRunIdentity | None = None,
) -> RawSurfaceObservation:
    return RawSurfaceObservation(
        ObservationProvenance(
            source_id,
            occurrence_id,
            run_identity or measurement_run(),
        ),
        surface,
    )


def manifest(
    run_identity: MeasurementRunIdentity | None = None,
) -> ObservationLedgerManifest:
    resolved = run_identity or measurement_run()
    return SurfaceNormalization.ledger_manifest(
        resolved,
        [
            observation("source", "one", "\u0628\u064e", resolved),
            observation("source", "two", "\u0627\u0654", resolved),
        ],
    )


def synthetic_row(
    ledger_manifest: ObservationLedgerManifest,
) -> SurfaceInterventionAuditRow:
    table = SurfaceAtomInterventionAudit.audit(
        ledger_manifest,
        (
            SurfaceAtomIntervention(
                source_id="source",
                occurrence_id="one",
                intervention_type="delete",
                coordinates=(0,),
            ),
        ),
    )
    return table.rows[0]


def test_genus_is_two_valued_with_no_mixed_value() -> None:
    assert {genus.name for genus in EvidenceProvenanceGenus} == {
        "MEASURED",
        "SYNTHETIC",
    }


def test_gate_derives_measured_genus_from_a_manifested_audit() -> None:
    ledger_manifest = manifest()
    audit = ledger_manifest.ledger.audits[0]

    classification = EvidenceProvenanceGate.classify_measured(ledger_manifest, audit)

    assert classification.genus is EvidenceProvenanceGenus.MEASURED
    assert classification.run_identity == ledger_manifest.run_identity
    assert (classification.source_id, classification.occurrence_id) == (
        "source",
        "one",
    )


def test_gate_derives_synthetic_genus_and_records_no_measurement_run() -> None:
    ledger_manifest = manifest()

    classification = EvidenceProvenanceGate.classify_synthetic(
        synthetic_row(ledger_manifest)
    )

    assert classification.genus is EvidenceProvenanceGenus.SYNTHETIC
    assert classification.run_identity is None


def test_gate_refuses_an_audit_outside_the_manifested_ledger() -> None:
    other_audit = SurfaceNormalization.normalize(
        observation("other-source", "one", "\u0628\u064e")
    )

    with pytest.raises(EvidenceProvenanceError, match="outside the manifested ledger"):
        EvidenceProvenanceGate.classify_measured(manifest(), other_audit)


def test_a_classification_is_not_caller_constructible() -> None:
    with pytest.raises(EvidenceProvenanceError, match="issued only by"):
        EvidenceProvenanceClassification(
            genus=EvidenceProvenanceGenus.MEASURED,
            run_identity=measurement_run(),
            source_id="source",
            occurrence_id="one",
        )


def test_synthetic_evidence_cannot_enter_a_measured_contrast_set() -> None:
    ledger_manifest = manifest()
    synthetic = EvidenceProvenanceGate.classify_synthetic(
        synthetic_row(ledger_manifest)
    )
    measured = EvidenceProvenanceGate.classify_measured(
        ledger_manifest, ledger_manifest.ledger.audits[0]
    )

    with pytest.raises(EvidenceProvenanceError, match="not an observation"):
        MeasuredContrastSet((measured, synthetic))


def test_measured_contrast_set_reports_distinct_runs_without_promoting() -> None:
    first = manifest(measurement_run("run-1"))
    second = manifest(measurement_run("run-2"))
    contrast = MeasuredContrastSet(
        (
            EvidenceProvenanceGate.classify_measured(first, first.ledger.audits[0]),
            EvidenceProvenanceGate.classify_measured(second, second.ledger.audits[0]),
        )
    )

    assert contrast.distinct_measurement_runs == (
        first.run_identity,
        second.run_identity,
    )
    assert not hasattr(contrast, "rank")
    assert not hasattr(contrast, "is_birth_eligible")


def test_measured_evidence_cannot_enter_a_hypothesis_residual() -> None:
    ledger_manifest = manifest()
    measured = EvidenceProvenanceGate.classify_measured(
        ledger_manifest, ledger_manifest.ledger.audits[0]
    )

    with pytest.raises(EvidenceProvenanceError, match="hypothesis records"):
        HypothesisResidual(
            hypothesis_id="order-sensitivity",
            statement="codepoint sequences are order sensitive",
            synthetic_evidence=(measured,),
        )


def test_a_hypothesis_residual_is_never_birth_eligible_here() -> None:
    ledger_manifest = manifest()
    synthetic = EvidenceProvenanceGate.classify_synthetic(
        synthetic_row(ledger_manifest)
    )

    hypothesis = HypothesisResidual(
        hypothesis_id="order-sensitivity",
        statement="codepoint sequences are order sensitive",
        synthetic_evidence=(synthetic,),
    )

    assert hypothesis.is_birth_eligible is False


def test_no_kernel_module_reads_the_provenance_genus() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "provenance_genus" not in text, module.name
        assert "HypothesisResidual" not in text, module.name
