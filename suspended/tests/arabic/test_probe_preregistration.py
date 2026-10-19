"""اختبارات تجميد مواصفة التحقيق القادم وتسجيل سؤال الطور الثاني."""

from __future__ import annotations

import pkgutil
from dataclasses import fields, replace

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.distributional_probe_report import (
    RECORDED_PROBE_REPORT,
    RECORDED_PROBE_SPECIFICATION,
    RECORDED_REFUTED_CLAIM,
    DiscoveredLayerKind,
    LayerNature,
    ProbeFeature,
    ProbeOutcome,
    SelectionCriterion,
)
from alghanem.arabic.probe_preregistration import (
    PHASE2_OPEN_QUESTION,
    CanonicalFollowupProbeSpecificationEncoder,
    EvidenceGenus,
    FollowupProbeSpecificationContentBinding,
    FrozenFollowupProbeSpecification,
    Phase2Hypothesis,
    Phase2OpenQuestion,
    PreEvidenceProbeSpecificationRegistry,
    ProbePreregistrationError,
    ProbeResultAttachment,
    StoppingRule,
)

FROZEN_FEATURES = (
    ProbeFeature.LENGTH,
    ProbeFeature.FINAL_RATIO,
    ProbeFeature.SUCCESSOR_DIVERSITY,
)


def _specification(**overrides: object) -> FrozenFollowupProbeSpecification:
    base = dict(
        experiment_id="phase2-probe",
        revision_id="rev-1",
        revision_sequence=0,
        evidence_genus=EvidenceGenus.DISTRIBUTIONAL,
        features=FROZEN_FEATURES,
        minimum_support=5,
        smallest_scanned_k=2,
        largest_scanned_k=11,
        selection_criterion=SelectionCriterion.SILHOUETTE,
        stopping_rule=StoppingRule.EXHAUSTIVE_DECLARED_K_SCAN,
        evaluation_criterion_id="criterion-1",
        evaluation_criterion="تطابق العناقيد مع تقسيم اسم/فعل/حرف",
    )
    base.update(overrides)
    return FrozenFollowupProbeSpecification(**base)  # type: ignore[arg-type]


def _binding(
    specification: FrozenFollowupProbeSpecification | None = None,
) -> FollowupProbeSpecificationContentBinding:
    specification = specification or _specification()
    registry = PreEvidenceProbeSpecificationRegistry()
    return FollowupProbeSpecificationContentBinding(
        specification=specification,
        frozen_manifest=registry.freeze(specification),
    )


def _attachment(**overrides: object) -> ProbeResultAttachment:
    base = dict(
        binding=_binding(),
        used_features=FROZEN_FEATURES,
        used_selection_criterion=SelectionCriterion.SILHOUETTE,
        used_stopping_rule=StoppingRule.EXHAUSTIVE_DECLARED_K_SCAN,
        selected_k=2,
    )
    base.update(overrides)
    return ProbeResultAttachment(**base)  # type: ignore[arg-type]


def test_a_frozen_specification_carries_no_result_field() -> None:
    declared = {item.name for item in fields(FrozenFollowupProbeSpecification)}
    forbidden = ("result", "outcome", "cluster", "partition", "layer", "selected")
    assert not [
        name for name in declared if any(marker in name for marker in forbidden)
    ]


def test_a_well_formed_specification_freezes_and_binds() -> None:
    binding = _binding()
    assert binding.content_id.digest == binding.frozen_manifest.content_id.digest
    assert binding.specification.scanned_k_values[0] == 2


def test_refreezing_identical_content_returns_the_same_frozen_manifest() -> None:
    registry = PreEvidenceProbeSpecificationRegistry()
    specification = _specification()
    first = registry.freeze(specification)
    assert registry.freeze(_specification()) is first


def test_content_changed_after_freezing_under_one_identity_is_refused() -> None:
    registry = PreEvidenceProbeSpecificationRegistry()
    registry.freeze(_specification())
    with pytest.raises(ProbePreregistrationError):
        registry.freeze(_specification(minimum_support=7))


def test_a_binding_to_another_specifications_freeze_is_refused() -> None:
    registry = PreEvidenceProbeSpecificationRegistry()
    frozen = registry.freeze(_specification())
    with pytest.raises(ProbePreregistrationError):
        FollowupProbeSpecificationContentBinding(
            specification=_specification(
                experiment_id="phase2-probe-other", revision_id="rev-2"
            ),
            frozen_manifest=frozen,
        )


def test_a_digest_mismatch_between_bytes_and_identity_is_refused() -> None:
    manifest = CanonicalFollowupProbeSpecificationEncoder.encode(_specification())
    with pytest.raises(ProbePreregistrationError):
        replace(manifest, content_bytes=manifest.content_bytes + b" ")


def test_a_content_identity_cannot_be_constructed_outside_the_encoder() -> None:
    manifest = CanonicalFollowupProbeSpecificationEncoder.encode(_specification())
    with pytest.raises(ProbePreregistrationError):
        replace(manifest.content_id, _token=None)


def test_a_result_without_a_binding_cannot_be_built() -> None:
    with pytest.raises(ProbePreregistrationError):
        _attachment(binding=_specification())


def test_a_feature_outside_the_frozen_set_is_refused() -> None:
    with pytest.raises(ProbePreregistrationError):
        _attachment(
            used_features=FROZEN_FEATURES
            + (ProbeFeature.SILENT_SKELETON_HOST_DIVERSITY,)
        )


def test_a_subset_of_the_frozen_features_is_admitted() -> None:
    assert _attachment(used_features=(ProbeFeature.LENGTH,)).used_features == (
        ProbeFeature.LENGTH,
    )


def test_a_stopping_rule_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(ProbePreregistrationError):
        _attachment(used_stopping_rule="مسح_شامل_لمدى_k_المُعلَن")


def test_a_selection_criterion_that_is_not_the_frozen_one_is_refused() -> None:
    with pytest.raises(ProbePreregistrationError):
        _attachment(used_selection_criterion=StoppingRule.EXHAUSTIVE_DECLARED_K_SCAN)


def test_a_selected_k_outside_the_frozen_range_is_refused() -> None:
    with pytest.raises(ProbePreregistrationError):
        _attachment(selected_k=12)


def test_the_morpho_functional_genus_is_declared_but_not_yet_constructible() -> None:
    assert EvidenceGenus.MORPHO_FUNCTIONAL in set(EvidenceGenus)
    with pytest.raises(ProbePreregistrationError):
        _specification(evidence_genus=EvidenceGenus.MORPHO_FUNCTIONAL)


def test_the_evidence_genus_vocabulary_declares_no_mixed_value() -> None:
    assert {genus.name for genus in EvidenceGenus} == {
        "DISTRIBUTIONAL",
        "MORPHO_FUNCTIONAL",
    }


def test_the_open_question_has_no_answer_or_verdict_field() -> None:
    declared = {item.name for item in fields(Phase2OpenQuestion)}
    forbidden = ("answer", "verdict", "conclusion", "resolution", "decision")
    assert not [
        name for name in declared if any(marker in name for marker in forbidden)
    ]
    assert not [
        name
        for name in dir(PHASE2_OPEN_QUESTION)
        if not name.startswith("_") and any(marker in name for marker in forbidden)
    ]


def test_the_open_question_keeps_all_three_hypotheses() -> None:
    assert set(PHASE2_OPEN_QUESTION.hypotheses) == set(Phase2Hypothesis)
    assert PHASE2_OPEN_QUESTION.remains_open
    assert PHASE2_OPEN_QUESTION.why_open.strip()


def test_dropping_one_hypothesis_makes_a_false_dichotomy_and_is_refused() -> None:
    with pytest.raises(ProbePreregistrationError):
        Phase2OpenQuestion(
            question_id="q",
            hypotheses=(
                Phase2Hypothesis.CURRENT_FEATURES_INSUFFICIENT,
                Phase2Hypothesis.DIVISION_IS_NOT_SURFACE_DISTRIBUTIONAL,
            ),
            why_open="سبب",
        )


def test_repeating_a_hypothesis_is_refused() -> None:
    with pytest.raises(ProbePreregistrationError):
        Phase2OpenQuestion(
            question_id="q",
            hypotheses=(
                Phase2Hypothesis.CURRENT_FEATURES_INSUFFICIENT,
                Phase2Hypothesis.CURRENT_FEATURES_INSUFFICIENT,
                Phase2Hypothesis.DIVISION_IS_NOT_SURFACE_DISTRIBUTIONAL,
                Phase2Hypothesis.NEEDS_LOWER_BORN_VARIABLES,
            ),
            why_open="سبب",
        )


def test_the_recorded_negative_result_is_unchanged_field_for_field() -> None:
    assert RECORDED_PROBE_SPECIFICATION.features == (
        ProbeFeature.LENGTH,
        ProbeFeature.FINAL_RATIO,
        ProbeFeature.SUCCESSOR_DIVERSITY,
        ProbeFeature.PREDECESSOR_DIVERSITY,
        ProbeFeature.SILENT_SKELETON_HOST_DIVERSITY,
    )
    assert RECORDED_PROBE_SPECIFICATION.minimum_support == 5
    assert RECORDED_PROBE_SPECIFICATION.surface_form_count == 2193
    assert RECORDED_PROBE_SPECIFICATION.smallest_scanned_k == 2
    assert RECORDED_PROBE_SPECIFICATION.largest_scanned_k == 11
    assert (
        RECORDED_PROBE_SPECIFICATION.selection_criterion
        is SelectionCriterion.SILHOUETTE
    )
    assert RECORDED_PROBE_REPORT.selected_k == 2
    assert RECORDED_PROBE_REPORT.outcome is ProbeOutcome.DISCOVERED_OTHER_LAYER
    assert RECORDED_PROBE_REPORT.is_negative_result
    assert RECORDED_PROBE_REPORT.refuted_claim == RECORDED_REFUTED_CLAIM
    assert tuple(
        (partition.k, partition.cluster_sizes)
        for partition in RECORDED_PROBE_REPORT.partitions
    ) == ((2, (2159, 34)), (3, (1878, 289, 26)))
    assert RECORDED_PROBE_REPORT.layers_by_kind == (
        (DiscoveredLayerKind.OVER_CONNECTIVITY, 2),
        (DiscoveredLayerKind.OVER_CONNECTIVITY, 3),
        (DiscoveredLayerKind.QURANIC_CADENCE, 3),
    )
    assert LayerNature.GRAMMATICAL not in {
        layer.nature for layer in RECORDED_PROBE_REPORT.discovered_layers
    }


def test_no_kernel_module_reads_the_probe_or_its_preregistration() -> None:
    forbidden = ("distributional_probe_report", "probe_preregistration")
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert not [marker for marker in forbidden if marker in text], module.name
