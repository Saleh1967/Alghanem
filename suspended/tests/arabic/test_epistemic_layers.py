"""Tests for the three derived ontological layers of the Arabic pipeline."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields, replace
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    RECORDED_PROBE_REPORT,
    UNICODE_IS_NOT_RECORDED_SOUND_NOTE,
    CrossLayerInferenceRecord,
    EpistemicLayerError,
    EpistemicStanding,
    ImportedInferenceStanding,
    MeasurementProtocolSpec,
    MeasurementRunIdentity,
    ObservationProvenance,
    OntologicalLayer,
    OntologicalLayerClassification,
    OntologicalLayerGate,
    RawSurfaceObservation,
    SurfaceNormalization,
)
from alghanem.arabic import epistemic_layers as layers_module
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def observation(raw: str = "\u0627\u0654") -> RawSurfaceObservation:
    run = MeasurementRunIdentity(
        MeasurementProtocolSpec(
            protocol_id="surface-measurement",
            protocol_version="1",
            source_scope="test-source",
            normalization_policy="NFC",
            occurrence_scheme="caller-issued-sequence",
        ),
        "run-1",
    )
    return RawSurfaceObservation(
        ObservationProvenance("source", "occurrence-1", run),
        raw,
    )


def test_the_three_layers_are_one_closed_vocabulary() -> None:
    assert len(OntologicalLayer) == 3
    assert {layer.value for layer in OntologicalLayer} == {
        "\u0648\u062c\u0648\u062f_\u0641\u064a\u0632\u064a\u0627\u0626\u064a",
        "\u0639\u0642\u062f\u0629_\u0648\u0636\u0639\u064a\u0629",
        "\u062a\u062d\u0644\u064a\u0644_\u0635\u0641\u0627\u062a_"
        "\u0625\u062d\u0635\u0627\u0626\u064a",
    }


def test_a_raw_observation_is_derived_as_the_conventional_knot_layer() -> None:
    classification = OntologicalLayerGate.classify(observation())
    assert classification.layer is OntologicalLayer.CONVENTIONAL_KNOT
    assert classification.standing is EpistemicStanding.CONVENTIONAL_TRANSMITTED
    assert classification.artifact_kind == "RawSurfaceObservation"


def test_a_normalization_audit_is_derived_as_the_conventional_knot_layer() -> None:
    audit = SurfaceNormalization.normalize(observation())
    classification = OntologicalLayerGate.classify(audit)
    assert classification.layer is OntologicalLayer.CONVENTIONAL_KNOT
    assert classification.artifact_kind == "NormalizationAudit"


def test_a_probe_report_is_derived_as_the_statistical_attribute_layer() -> None:
    classification = OntologicalLayerGate.classify(RECORDED_PROBE_REPORT)
    assert classification.layer is OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS
    assert classification.standing is EpistemicStanding.PRESUMPTIVE_ALWAYS


def test_a_discovered_layer_is_also_statistical_not_conventional() -> None:
    discovered = RECORDED_PROBE_REPORT.discovered_layers[0]
    classification = OntologicalLayerGate.classify(discovered)
    assert classification.layer is OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS


def test_an_unknown_artifact_is_refused_by_its_type_name() -> None:
    with pytest.raises(EpistemicLayerError, match="str"):
        OntologicalLayerGate.classify("\u0623\u0644\u0641")  # type: ignore[arg-type]


def test_a_classification_is_not_constructible_outside_the_gate() -> None:
    with pytest.raises(EpistemicLayerError, match="OntologicalLayerGate"):
        OntologicalLayerClassification(
            layer=OntologicalLayer.CONVENTIONAL_KNOT,
            artifact_kind="RawSurfaceObservation",
        )


def test_the_physical_layer_is_declared_and_unconstructible() -> None:
    classification = OntologicalLayerGate.classify(observation())
    with pytest.raises(EpistemicLayerError, match="UnicodeIsNotRecordedSound"):
        replace(classification, layer=OntologicalLayer.PHYSICAL_EXISTENCE)
    assert UNICODE_IS_NOT_RECORDED_SOUND_NOTE.startswith("UnicodeIsNotRecordedSound")
    assert classification.is_measured_by_this_pipeline is True


def test_every_layer_declares_exactly_one_epistemic_standing() -> None:
    standings = {layers_module._STANDING_BY_LAYER[layer] for layer in OntologicalLayer}
    assert len(standings) == len(EpistemicStanding) == 3


def test_a_cross_layer_inference_is_recorded_as_declared_not_verified() -> None:
    record = CrossLayerInferenceRecord(
        inference_id="tajammu-sawti",
        from_layer=OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS,
        to_layer=OntologicalLayer.PHYSICAL_EXISTENCE,
        external_citation="\u0645\u0635\u062f\u0631 \u062e\u0627\u0631\u062c\u064a",
    )
    assert record.standing is ImportedInferenceStanding.DECLARED_NOT_VERIFIED
    assert record.crosses_into_the_physical_layer is True
    assert record.is_produced_by_this_pipeline is False


def test_a_locally_verified_cross_layer_inference_is_refused() -> None:
    with pytest.raises(EpistemicLayerError, match="CrossLayerInferenceIsImported"):
        CrossLayerInferenceRecord(
            inference_id="tajammu-sawti",
            from_layer=OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS,
            to_layer=OntologicalLayer.PHYSICAL_EXISTENCE,
            external_citation="\u0645\u0635\u062f\u0631",
            standing=ImportedInferenceStanding.VERIFIED_LOCALLY,
        )


def test_an_inference_from_a_layer_to_itself_is_refused() -> None:
    with pytest.raises(EpistemicLayerError, match="\u0639\u0628\u0648\u0631"):
        CrossLayerInferenceRecord(
            inference_id="same",
            from_layer=OntologicalLayer.CONVENTIONAL_KNOT,
            to_layer=OntologicalLayer.CONVENTIONAL_KNOT,
            external_citation="\u0645\u0635\u062f\u0631",
        )


def test_an_inference_without_an_external_citation_is_refused() -> None:
    with pytest.raises(EpistemicLayerError, match="\u0627\u0644\u062e\u0627\u0631"):
        CrossLayerInferenceRecord(
            inference_id="no-citation",
            from_layer=OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS,
            to_layer=OntologicalLayer.PHYSICAL_EXISTENCE,
            external_citation="   ",
        )


def test_no_type_here_carries_a_written_layer_label_or_verdict_field() -> None:
    for declaring_type in (OntologicalLayerClassification, CrossLayerInferenceRecord):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("declared_layer", "verdict", "birth", "rank"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "epistemic_layers.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_the_layer_classification() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        text = Path(source.origin).read_text(encoding="utf-8")
        assert "epistemic_layers" not in text, module.name
        assert "OntologicalLayer" not in text, module.name
        assert "CrossLayerInferenceRecord" not in text, module.name


@pytest.mark.parametrize("card", _CARDS)
def test_the_layer_derivation_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    OntologicalLayerGate.classify(RECORDED_PROBE_REPORT)
    OntologicalLayerGate.classify(observation())
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
